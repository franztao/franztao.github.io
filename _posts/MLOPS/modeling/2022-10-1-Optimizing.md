---

layout:     post
title:      优化超参数
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Optimizing Hyperparameters

---

优化超参数子集以实现目标。

## Intuition

优化是在实验中微调超参数以优化特定目标的过程。它可能是一个涉及计算的过程，具体取决于参数的数量、搜索空间和模型架构。超参数不仅包括模型的参数，还包括来自预处理、分割等的参数（选择）。当查看所有可以调整的不同参数时，它很快就变成了一个非常大的搜索空间。然而，仅仅因为某些东西是超参数并不意味着需要调整它。

- `lower=True`修复一些超参数（例如在预处理期间）并将它们从调整子集中删除是绝对可以的。请务必注意您正在修复哪些参数以及您这样做的理由。
- 您最初可以只调整一小部分但有影响力的超参数子集，您认为这些子集会产生最佳结果。

希望优化超参数，以便能够了解它们中的每一个如何影响目标。通过在合理的搜索空间中进行多次试验，可以确定不同参数的接近理想值。这也是确定较小参数是否产生与较大参数（效率）相似的性能的好机会。

超参数调整有很多选项（[Optuna](https://github.com/optuna/optuna)、[Ray tune](https://github.com/ray-project/ray/tree/master/python/ray/tune)、[Hyperopt](https://github.com/hyperopt/hyperopt)等）。将使用 Optuna 是因为它的简单性、流行性和效率，尽管它们都同样如此。这实际上归结为熟悉程度以及库是否具有易于测试和可用的特定实现。

## 应用

执行超参数优化时需要考虑许多因素，幸运的是 Optuna 允许轻松[实现](https://optuna.readthedocs.io/en/stable/reference/)它们。将进行一项小型研究，其中将调整一组参数（当将代码移动到 Python 脚本时，将对参数空间进行更彻底的[研究）。](https://optuna.readthedocs.io/en/stable/reference/study.html)以下是研究的过程：

1. 定义目标（指标）并确定优化[方向](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)。
2. `[OPTIONAL]`选择一个[采样器](https://optuna.readthedocs.io/en/stable/reference/samplers.html)来确定后续试验的参数。（默认是基于树的采样器）。
3. `[OPTIONAL]`选择一个[修枝剪](https://optuna.readthedocs.io/en/stable/reference/pruners.html)提早结束没有希望的试验。
4. 定义要在每个[试验](https://optuna.readthedocs.io/en/stable/reference/trial.html)中调整的参数以及要采样的值的[分布](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna-trial-trial)。

```
pip install optuna==2.10.0 numpyencoder==0.3.0 -q
```

将使用与以前相同的训练函数，因为已经添加了在`trial`参数不是时修剪特定运行的功能`None`。

```
# Pruning (inside train() function)
trial.report(val_loss, epoch)
if trial.should_prune():
    raise optuna.TrialPruned()

```



## 客观的

需要定义一个目标函数，该函数将使用试验和一组参数并生成要优化的指标（`f1`在例子中）。

```
def objective(args, trial):
    """Objective function for optimization trials."""
    # Parameters to tune
    args.analyzer = trial.suggest_categorical("analyzer", ["word", "char", "char_wb"])
    args.ngram_max_range = trial.suggest_int("ngram_max_range", 3, 10)
    args.learning_rate = trial.suggest_loguniform("learning_rate", 1e-2, 1e0)
    args.power_t = trial.suggest_uniform("power_t", 0.1, 0.5)

    # Train & evaluate
    artifacts = train(args=args, df=df, trial=trial)

    # Set additional attributes
    performance = artifacts["performance"]
    print(json.dumps(performance, indent=2))
    trial.set_user_attr("precision", performance["precision"])
    trial.set_user_attr("recall", performance["recall"])
    trial.set_user_attr("f1", performance["f1"])

    return performance["f1"]

```



## 学习

已准备好使用[MLFlowCallback](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.integration.MLflowCallback.html)开始研究，这样就可以跟踪所有不同的试验。

```
from numpyencoder import NumpyEncoder
from optuna.integration.mlflow import MLflowCallback

```

```
NUM_TRIALS = 20  # small sample for now

```

```
# Optimize
pruner = optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5)
study = optuna.create_study(study_name="optimization", direction="maximize", pruner=pruner)
mlflow_callback = MLflowCallback(
    tracking_uri=mlflow.get_tracking_uri(), metric_name="f1")
study.optimize(lambda trial: objective(args, trial),
            n_trials=NUM_TRIALS,
            callbacks=[mlflow_callback])

```

A new study created in memory with name: optimization
Epoch: 00 | train_loss: 1.34116, val_loss: 1.35091
...
Epoch: 90 | train_loss: 0.32167, val_loss: 0.57661
Stopping early!
Trial 0 finished with value: 0.7703281822265505 and parameters: {'analyzer': 'char', 'ngram_max_range': 10, 'learning_rate': 0.025679294001785473, 'power_t': 0.15046698128066294}. Best is trial 0 with value: 0.7703281822265505.
...
Trial 10 pruned.
...
Epoch: 80 | train_loss: 0.16680, val_loss: 0.43964
Epoch: 90 | train_loss: 0.16134, val_loss: 0.43686
Trial 19 finished with value: 0.8470890576153735 and parameters: {'analyzer': 'char_wb', 'ngram_max_range': 4, 'learning_rate': 0.08452049154544644, 'power_t': 0.39657115651885855}. Best is trial 3 with value: 0.8470890576153735.



```
# Run MLFlow server and localtunnel
get_ipython().system_raw("mlflow server -h 0.0.0.0 -p 8000 --backend-store-uri $PWD/experiments/ &")
!npx localtunnel --port 8000

```

```
# Run MLFlow server and localtunnel
get_ipython().system_raw("mlflow server -h 0.0.0.0 -p 8000 --backend-store-uri $PWD/experiments/ &")
!npx localtunnel --port 8000

```



1\. 点击 Experiments 下左侧的“优化”**实验**。2\. 通过单击每个运行左侧的切换框或单击标题中的切换框来选择该实验中的所有运行来选择要比较的运行。3\. 单击**比较**按钮。

![比较试验](https://madewithml.com/static/images/mlops/hyperparameter_optimization/compare.png)

1. 在对比页面中，可以通过各种镜头（轮廓、平行坐标等）查看结果

![等高线图](https://madewithml.com/static/images/mlops/hyperparameter_optimization/contour.png)

![平行坐标](https://madewithml.com/static/images/mlops/hyperparameter_optimization/parallel_coordinates.png)

```
# All trials
trials_df = study.trials_dataframe()
trials_df = trials_df.sort_values(["user_attrs_f1"], ascending=False)  # sort by metric
trials_df.head()

```

```
# Best trial
print (f"Best value (f1): {study.best_trial.value}")
print (f"Best hyperparameters: {json.dumps(study.best_trial.params, indent=2)}")

```

Best value (f1): 0.8535985582060417
Best hyperparameters: {
  "analyzer": "char_wb",
  "ngram_max_range": 4,
  "learning_rate": 0.08981103667371809,
  "power_t": 0.2583427488720579
}

```
# Save best parameter values
args = {**args.__dict__, **study.best_trial.params}
print (json.dumps(args, indent=2, cls=NumpyEncoder))

```

{
  "lower": true,
  "stem": false,
  "analyzer": "char_wb",
  "ngram_max_range": 4,
  "alpha": 0.0001,
  "learning_rate": 0.08833689034118489,
  "power_t": 0.1181958972675695
}





...现在终于准备好从使用 Jupyter 笔记本转向 Python 脚本了。将重新审视迄今为止所做的一切，但这次使用适当的软件工程原则，例如面向对象编程 (OOP)、样式、测试等。

___

本文主体源自以下链接：

```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
---
layout:     post
title:      命令行界面 (CLI) 应用程序
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Application
    - Commands
    - Arguments

---

使用命令行界面 (CLI) 应用程序来组织应用程序的进程。

## Intuition

当模型要提供服务时，需要考虑将应用程序的功能公开给自己、团队成员以及最终最终使用用户。实现这一点的接口会有所不同。回想一下[Organization lesson](https://franztao.github.io/2022/10/10/Organization/)，通过终端和 Python 解释器执行[main operations](https://franztao.github.io/2022/10/10/Organization/#operations)

```
from tagifai import main
main.elt_data()
```

`main.py`或者替代方法是在文件中显式调用的操作：

```
# tagifai/main.py
if __name__ == "__main__":
    elt_data()
```

这变得非常低效，不得不一次次深入研究代码并执行一个函数。一种解决方案是构建一个允许在操作级别进行交互的命令行界面 (CLI) 应用程序。它的设计应该使可以查看所有可能的操作（及其所需的参数）并从 shell 执行它们。

## 应用

将使用[Typer](https://typer.tiangolo.com/)创建 CLI ：

```
# Add to requirements.txt
typer==0.4.1
```

就像初始化应用程序然后将适当的装饰器添加到希望在 CLI 命令中使用的每个函数操作一样简单`main.py`：

```
# tagifai/main.py
import typer
app = typer.Typer()
```

```
@app.command()
def elt_data():
    ...
```

将对要通过 CLI 访问的所有其他功能重复相同的操作：`elt_data()`、`train_model()`、`optimize()`、`predict_tag()`。将使其所有参数都是可选的，以便可以在 bash 命令中明确定义它们。例如，将成为.`def train_model(args_fp: str, ...):``def train_model(args_fp: str = "config/args.json", ...):`

> 查看`tagifai/main.py`函数头

```
@app.command()
def elt_data():
    ...


@app.command()
def train_model(
    args_fp: str = "config/args.json",
    experiment_name: str = "baselines",
    run_name: str = "sgd",
    test_run: bool = False,
) -> None:
    ...


@app.command()
def optimize(
    args_fp: str = "config/args.json",
    study_name: str = "optimization",
    num_trials: int = 20
) -> None:
    ...

@app.command()
def predict_tag(text: str = "", run_id: str = None) -> None:
    ...
```

## 命令

要使用 CLI 应用程序，可以首先查看可用的命令，这要归功于添加到想要向 CLI 公开的某些功能中的装饰器：

```
python tagifai/main.py --help
```

> Typer 还附带一个名为[typer-cli](https://typer.tiangolo.com/typer-cli/)的实用工具，但与其他库存在一些依赖冲突，因此不会使用它。

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help       Show this message and exit.

Commands:
  elt-data     Extract, load and transform data.
  label-data   Label data using constraints.
  optimize     Optimize hyperparameters.
  predict-tag  Predict tag for text.
  train-model  Train a model given arguments.
```

## Arguments

使用 Typer，函数的输入参数会自动呈现为命令行选项。例如，`predict_tags`函数`text`使用一个可选`run_id`的作为输入，它们自动成为`predict-tags`CLI 命令的参数。

```
@app.command()
def predict_tag(text: str = "", run_id: str = None) -> None:
    """Predict tag for text.

    Args:
        text (str): input text to predict label for.
        run_id (str, optional): run id to load artifacts for prediction. Defaults to None.
    """
    if not run_id:
        run_id = open(Path(config.CONFIG_DIR, "run_id.txt")).read()
    artifacts = load_artifacts(run_id=run_id)
    prediction = predict.predict(texts=[text], artifacts=artifacts)
    logger.info(json.dumps(prediction, indent=2))
    return prediction
```

但是也可以就这个特定的命令寻求帮助，而无需进入代码：

```
python tagifai/main.py predict-tag --help
```

```
Usage: main.py predict-tag [OPTIONS]

  Predict tag for text.

  Args:
    text (str): input text to predict label for.
    run_id (str, optional): run id to load artifacts for prediction. Defaults to None.

Options:
  --text TEXT
  --run-id TEXT
  --help         Show this message and exit.
```

## 用法

最后，可以使用所有参数执行特定命令：

```
python tagifai/main.py predict-tag --text="Transfer learning with transformers for text classification."
```

```
[
    {
        "input_text": "Transfer learning with transformers for text classification.",
        "predicted_tag": "natural-language-processing"
    }
]
```

___

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)

转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

本文主体源自以下链接：

```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
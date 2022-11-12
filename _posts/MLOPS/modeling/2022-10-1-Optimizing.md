
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

## 直觉

优化是在我们的实验中微调超参数以优化特定目标的过程。它可能是一个涉及计算的过程，具体取决于参数的数量、搜索空间和模型架构。超参数不仅包括模型的参数，还包括来自预处理、分割等的参数（选择）。当我们查看所有可以调整的不同参数时，它很快就变成了一个非常大的搜索空间。然而，仅仅因为某些东西是超参数并不意味着我们需要调整它。

-   `lower=True`修复一些超参数（例如在预处理期间）并将它们从调整子集中删除是绝对可以的。请务必注意您正在修复哪些参数以及您这样做的理由。
-   您最初可以只调整一小部分但有影响力的超参数子集，您认为这些子集会产生最佳结果。

我们希望优化我们的超参数，以便我们能够了解它们中的每一个如何影响我们的目标。通过在合理的搜索空间中进行多次试验，我们可以确定不同参数的接近理想值。这也是确定较小参数是否产生与较大参数（效率）相似的性能的好机会。

超参数调整有很多选项（[Optuna](https://github.com/optuna/optuna)、[Ray tune](https://github.com/ray-project/ray/tree/master/python/ray/tune)、[Hyperopt](https://github.com/hyperopt/hyperopt)等）。我们将使用 Optuna 是因为它的简单性、流行性和效率，尽管它们都同样如此。这实际上归结为熟悉程度以及库是否具有易于测试和可用的特定实现。

## 应用

执行超参数优化时需要考虑许多因素，幸运的是 Optuna 允许我们轻松[实现](https://optuna.readthedocs.io/en/stable/reference/)它们。我们将进行一项小型研究，其中我们将调整一组参数（当我们将代码移动到 Python 脚本时，我们将对参数空间进行更彻底的[研究）。](https://optuna.readthedocs.io/en/stable/reference/study.html)以下是研究的过程：

1.  定义目标（指标）并确定优化[方向](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)。
2.  `[OPTIONAL]`选择一个[采样器](https://optuna.readthedocs.io/en/stable/reference/samplers.html)来确定后续试验的参数。（默认是基于树的采样器）。
3.  `[OPTIONAL]`选择一个[修枝剪](https://optuna.readthedocs.io/en/stable/reference/pruners.html)提早结束没有希望的试验。
4.  定义要在每个[试验](https://optuna.readthedocs.io/en/stable/reference/trial.html)中调整的参数以及要采样的值的[分布](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna-trial-trial)。

```
pip install optuna==2.10.0 numpyencoder==0.3.0 -q

```

我们将使用与以前相同的训练函数，因为我们已经添加了在`trial`参数不是时修剪特定运行的功能`None`。

<table><tbody><tr><td></td><td><div><pre id="__code_3"><span></span><code><span># Pruning (inside train() function)</span>
<span>trial</span><span>.</span><span>report</span><span>(</span><span>val_loss</span><span>,</span> <span>epoch</span><span>)</span>
<span>if</span> <span>trial</span><span>.</span><span>should_prune</span><span>():</span>
    <span>raise</span> <span>optuna</span><span>.</span><span>TrialPruned</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

## 客观的

我们需要定义一个目标函数，该函数将使用试验和一组参数并生成要优化的指标（`f1`在我们的例子中）。

<table><tbody><tr><td><div><pre><span></span><span><span><span>1 </span></span></span>
<span><span><span>2 </span></span></span>
<span><span><span>3 </span></span></span>
<span><span><span>4 </span></span></span>
<span><span><span>5 </span></span></span>
<span><span><span>6 </span></span></span>
<span><span><span>7 </span></span></span>
<span><span><span>8 </span></span></span>
<span><span><span>9 </span></span></span>
<span><span><span>10 </span></span></span>
<span><span><span>11 </span></span></span>
<span><span><span>12 </span></span></span>
<span><span><span>13 </span></span></span>
<span><span><span>14 </span></span></span>
<span><span><span>15 </span></span></span>
<span><span><span>16 </span></span></span>
<span><span><span>17 </span></span></span>
<span><span><span>18 </span></span></span>
<span><span><span>19</span></span></span></pre></div></td><td><div><pre id="__code_4"><span></span><code tabindex="0"><span>def</span> <span>objective</span><span>(</span><span>args</span><span>,</span> <span>trial</span><span>):</span>
    <span>"""Objective function for optimization trials."""</span>
    <span># Parameters to tune</span>
    <span>args</span><span>.</span><span>analyzer</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_categorical</span><span>(</span><span>"analyzer"</span><span>,</span> <span>[</span><span>"word"</span><span>,</span> <span>"char"</span><span>,</span> <span>"char_wb"</span><span>])</span>
    <span>args</span><span>.</span><span>ngram_max_range</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_int</span><span>(</span><span>"ngram_max_range"</span><span>,</span> <span>3</span><span>,</span> <span>10</span><span>)</span>
    <span>args</span><span>.</span><span>learning_rate</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_loguniform</span><span>(</span><span>"learning_rate"</span><span>,</span> <span>1e-2</span><span>,</span> <span>1e0</span><span>)</span>
    <span>args</span><span>.</span><span>power_t</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_uniform</span><span>(</span><span>"power_t"</span><span>,</span> <span>0.1</span><span>,</span> <span>0.5</span><span>)</span><span></span>
<span></span>
    <span># Train &amp; evaluate</span>
    <span>artifacts</span> <span>=</span> <span>train</span><span>(</span><span>args</span><span>=</span><span>args</span><span>,</span> <span>df</span><span>=</span><span>df</span><span>,</span> <span>trial</span><span>=</span><span>trial</span><span>)</span><span></span>
<span></span>
    <span># Set additional attributes</span>
    <span>performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>]</span>
    <span>print</span><span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"precision"</span><span>,</span> <span>performance</span><span>[</span><span>"precision"</span><span>])</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"recall"</span><span>,</span> <span>performance</span><span>[</span><span>"recall"</span><span>])</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"f1"</span><span>,</span> <span>performance</span><span>[</span><span>"f1"</span><span>])</span><span></span>
<span></span>
    <span>return</span> <span>performance</span><span>[</span><span>"f1"</span><span>]</span>
</code></pre></div></td></tr></tbody></table>

## 学习

我们已准备好使用[MLFlowCallback](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.integration.MLflowCallback.html)开始我们的研究，这样我们就可以跟踪所有不同的试验。

<table><tbody><tr><td></td><td><div><pre id="__code_5"><span></span><code><span>from</span> <span>numpyencoder</span> <span>import</span> <span>NumpyEncoder</span>
<span>from</span> <span>optuna.integration.mlflow</span> <span>import</span> <span>MLflowCallback</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_6"><span></span><code><span>NUM_TRIALS</span> <span>=</span> <span>20</span>  <span># small sample for now</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_7"><span></span><code tabindex="0"><span># Optimize</span>
<span>pruner</span> <span>=</span> <span>optuna</span><span>.</span><span>pruners</span><span>.</span><span>MedianPruner</span><span>(</span><span>n_startup_trials</span><span>=</span><span>5</span><span>,</span> <span>n_warmup_steps</span><span>=</span><span>5</span><span>)</span>
<span>study</span> <span>=</span> <span>optuna</span><span>.</span><span>create_study</span><span>(</span><span>study_name</span><span>=</span><span>"optimization"</span><span>,</span> <span>direction</span><span>=</span><span>"maximize"</span><span>,</span> <span>pruner</span><span>=</span><span>pruner</span><span>)</span>
<span>mlflow_callback</span> <span>=</span> <span>MLflowCallback</span><span>(</span>
    <span>tracking_uri</span><span>=</span><span>mlflow</span><span>.</span><span>get_tracking_uri</span><span>(),</span> <span>metric_name</span><span>=</span><span>"f1"</span><span>)</span>
<span>study</span><span>.</span><span>optimize</span><span>(</span><span>lambda</span> <span>trial</span><span>:</span> <span>objective</span><span>(</span><span>args</span><span>,</span> <span>trial</span><span>),</span>
            <span>n_trials</span><span>=</span><span>NUM_TRIALS</span><span>,</span>
            <span>callbacks</span><span>=</span><span>[</span><span>mlflow_callback</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
在内存中创建的一项新研究，名称为：优化
时代：00 | train_loss：1.34116，val_loss：1.35091
...
时代：90 | train_loss：0.32167，val_loss：0.57661
早停！
试验 0 以值完成：0.7703281822265505 和参数：{'analyzer': 'char', 'ngram_max_range': 10, 'learning_rate': 0.025679294001785473, 'power_t': 0.15046698128066294}。最好是试验 0，其值为：0.7703281822265505。

...

修剪试验 10。

...

时代：80 | train_loss：0.16680，val_loss：0.43964
时代：90 | train_loss：0.16134，val_loss：0.43686
试验 19 完成值：0.8470890576153735 和参数：{'analyzer': 'char_wb', 'ngram_max_range': 4, 'learning_rate': 0.08452049154544644, 'power_t': 0.39657115651885855}。最好的是试验 3，其值为：0.8470890576153735。

```

<table><tbody><tr><td></td><td><div><pre id="__code_8"><span></span><code tabindex="0"><span># Run MLFlow server and localtunnel</span>
<span>get_ipython</span><span>()</span><span>.</span><span>system_raw</span><span>(</span><span>"mlflow server -h 0.0.0.0 -p 8000 --backend-store-uri $PWD/experiments/ &amp;"</span><span>)</span>
<span>!</span><span>npx</span> <span>localtunnel</span> <span>--</span><span>port</span> <span>8000</span>
</code></pre></div></td></tr></tbody></table>

1\. 点击 Experiments 下左侧的“优化”**实验**。2\. 通过单击每个运行左侧的切换框或单击标题中的切换框来选择该实验中的所有运行来选择要比较的运行。3\. 单击**比较**按钮。

![比较试验](https://madewithml.com/static/images/mlops/hyperparameter_optimization/compare.png)

1.  在对比页面中，我们可以通过各种镜头（轮廓、平行坐标等）查看结果

![等高线图](https://madewithml.com/static/images/mlops/hyperparameter_optimization/contour.png)

![平行坐标](https://madewithml.com/static/images/mlops/hyperparameter_optimization/parallel_coordinates.png)

<table><tbody><tr><td></td><td><div><pre id="__code_9"><span></span><code tabindex="0"><span># All trials</span>
<span>trials_df</span> <span>=</span> <span>study</span><span>.</span><span>trials_dataframe</span><span>()</span>
<span>trials_df</span> <span>=</span> <span>trials_df</span><span>.</span><span>sort_values</span><span>([</span><span>"user_attrs_f1"</span><span>],</span> <span>ascending</span><span>=</span><span>False</span><span>)</span>  <span># sort by metric</span>
<span>trials_df</span><span>.</span><span>head</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

|  | 数字 | 价值 | 日期时间开始 | 日期时间完成 | 期间 | params\_analyzer | params\_learning\_rate | params\_ngram\_max\_range | params\_power\_t | user\_attrs\_f1 | user\_attrs\_precision | user\_attrs\_recall | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 0.847089 | 2022-05-18 18:16:58.108105 | 2022-05-18 18:17:03.569948 | 0 天 00:00:05.461843 | char\_wb | 0.088337 | 4 | 0.118196 | 0.847089 | 0.887554 | 0.833333 | 完全的 |
| 19 | 19 | 0.847089 | 2022-05-18 18:17:58.219462 | 2022-05-18 18:18:00.642571 | 0 天 00:00:02.423109 | char\_wb | 0.084520 | 4 | 0.396571 | 0.847089 | 0.887554 | 0.833333 | 完全的 |
| 12 | 12 | 0.840491 | 2022-05-18 18:17:41.845179 | 2022-05-18 18:17:45.792068 | 0 天 00:00:03.946889 | char\_wb | 0.139578 | 7 | 0.107273 | 0.840491 | 0.877431 | 0.826389 | 完全的 |
| 13 | 13 | 0.840491 | 2022-05-18 18:17:45.862705 | 2022-05-18 18:17:49.657014 | 0 天 00:00:03.794309 | char\_wb | 0.154396 | 7 | 0.433669 | 0.840491 | 0.877431 | 0.826389 | 完全的 |
| 15 | 15 | 0.836255 | 2022-05-18 18:17:50.464948 | 2022-05-18 18:17:54.446481 | 0 天 00:00:03.981533 | char\_wb | 0.083253 | 7 | 0.106982 | 0.836255 | 0.881150 | 0.819444 | 完全的 |

<table><tbody><tr><td></td><td><div><pre id="__code_10"><span></span><code tabindex="0"><span># Best trial</span>
<span>print</span> <span>(</span><span>f</span><span>"Best value (f1): </span><span>{</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>value</span><span>}</span><span>"</span><span>)</span>
<span>print</span> <span>(</span><span>f</span><span>"Best hyperparameters: </span><span>{</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>params</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>)</span><span>}</span><span>"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
最佳值（f1）：0.8535985582060417
最佳超参数：{
  “分析仪”：“char_wb”，
  “ngram_max_range”：4，
  “学习率”：0.08981103667371809，
  “power_t”：0.2583427488720579
}

```

<table><tbody><tr><td></td><td><div><pre id="__code_11"><span></span><code><span># Save best parameter values</span>
<span>args</span> <span>=</span> <span>{</span><span>**</span><span>args</span><span>.</span><span>__dict__</span><span>,</span> <span>**</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>params</span><span>}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>args</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>,</span> <span>cls</span><span>=</span><span>NumpyEncoder</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “下”：是的，
  “干”：假，
  “分析仪”：“char_wb”，
  “ngram_max_range”：4，
  “阿尔法”：0.0001，
  “学习率”：0.08833689034118489，
  “power_t”：0.1181958972675695
}

```

...现在我们终于准备好从使用 Jupyter 笔记本转向 Python 脚本了。我们将重新审视我们迄今为止所做的一切，但这次使用适当的软件工程原则，例如面向对象编程 (OOP)、样式、测试等。 → [https://madewithml.com/#mlops](https://madewithml.com/#mlops)

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre id="__code_12"><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Optimization - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
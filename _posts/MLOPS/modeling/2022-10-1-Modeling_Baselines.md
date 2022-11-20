---
layout:     post
title:      建模基线
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Modeling Baselines

---

鼓励使用基线进行迭代建模。

## 直觉

基线是为迭代开发铺平道路的简单基准：

-   由于模型复杂度低，通过超参数调整进行快速实验。
-   发现数据问题、错误假设、代码中的错误等，因为模型本身并不复杂。
-   [帕累托原则](https://en.wikipedia.org/wiki/Pareto_principle)：可以用最少的初始努力实现良好的性能。

## 过程

这是建立基线的高级方法：

1.  从最简单的基线开始，以比较后续开发。这通常是一个随机（机会）模型。
2.  使用 IFTTT、辅助数据等开发基于规则的方法（如果可能）。
3.  _通过解决_限制和_激励_表示和模型架构来慢慢增加复杂性。
4.  权衡性能基线之间的_权衡_（性能、延迟、大小等）。
5.  随着数据集的增长，重新访问和迭代基线。

要考虑的权衡

在选择要进行的模型架构时，需要考虑哪些重要的权衡？如何优先考虑它们？

显示答案

这些权衡的优先级取决于您的上下文。

-   `performance`：考虑粗粒度和细粒度（例如每类）性能。
-   `latency`：您的模型对推理的响应速度有多快。
-   `size`: 你的模型有多大，你能支持它的存储吗？
-   `compute`：训练你的模型需要多少成本（美元、碳足迹等）？
-   `interpretability`: 你的模型需要解释它的预测吗？
-   `bias checks`：您的模型是否通过了关键偏差检查？
-   `time to develop`: 你需要多长时间来开发第一个版本？
-   `time to retrain`: 重新训练你的模型需要多长时间？如果您需要经常进行再培训，这一点非常重要。
-   `maintenance overhead`：维护模型版本需要谁和什么，因为 ML 的真正工作是在部署 v1 之后开始的。您不能像许多团队对传统软件所做的那样，将其交给您的站点可靠性团队来维护它。

迭代数据

还可以在您的数据集上设置基线。不要使用固定的数据集并在模型上迭代，而是选择一个好的基线并在数据集上迭代：

-   删除或修复数据样本（误报和否定）
-   准备和转换特征
-   扩大或巩固班级
-   合并辅助数据集
-   识别要提升的独特切片

## 分布式训练

需要为应用程序做的所有训练都发生在一个工作人员和一个加速器（CPU/GPU）上，但是，会考虑对非常大的模型或在处理大型数据集时进行分布式训练。分布式训练可能涉及：

-   **数据并行性**：工作人员收到较大数据集的不同切片。
    -   _同步训练_使用[AllReduce](https://tech.preferred.jp/en/blog/technologies-behind-distributed-deep-learning-allreduce/#:~:text=AllReduce%20is%20an%20operation%20that,of%20length%20N%20called%20A_p.)聚合梯度并在每批结束时更新所有工作人员的权重（同步）。
    -   _异步训练_使用通用参数服务器来更新权重，因为每个工作人员都在其数据片上进行训练（异步）。
-   **模型并行性**：所有工作人员使用相同的数据集，但模型在它们之间拆分（与数据并行性相比更难以实现，因为很难从反向传播中分离和组合信号）。

应用分布式训练有很多选择，例如 PyTorch 的[分布式包](https://pytorch.org/tutorials/beginner/dist_overview.html)、[Ray](https://ray.io/)、[Horovd](https://horovod.ai/)等。

## 优化

当数据或模型太大而无法训练时，分布式训练策略非常有用，但是当模型太大而无法部署时呢？以下模型压缩技术通常用于使大型模型适合现有基础架构：

-   [**修剪**](https://pytorch.org/tutorials/intermediate/pruning_tutorial.html)：删除权重（非结构化）或整个通道（结构化）以减小网络的大小。目标是保持模型的性能，同时增加其稀疏性。
-   [**量化**](https://pytorch.org/docs/stable/torch.quantization.html)：通过降低权重的精度（例如 32 位到 8 位）来减少权重的内存占用。可能会失去一些精度，但它不应该对性能产生太大影响。
-   [**蒸馏**](https://arxiv.org/abs/2011.14691)：训练较小的网络以“模仿”较大的网络，方法是让它重现较大网络层的输出。

![知识蒸馏](https://madewithml.com/static/images/mlops/baselines/kd.png)

在神经网络中提取知识 \[[来源](https://nni.readthedocs.io/en/latest/TrialExample/KDExample.html)\]

## 基线

每个应用程序的基线轨迹因任务而异。对于应用程序，将遵循以下路径：

1.  [随机的](https://madewithml.com/courses/mlops/baselines/#random)
2.  [基于规则](https://madewithml.com/courses/mlops/baselines/#rule-based)
3.  [简单机器学习](https://madewithml.com/courses/mlops/baselines/#simple-ml)

将激发对缓慢增加**表示**（例如文本向量化）和**架构**（例如逻辑回归）的复杂性的需求，并解决每个步骤的限制。

> 如果您不熟悉此处的建模概念，请务必查看[基础课程](https://madewithml.com/#foundations)。

笔记

使用的特定模型与本 MLOps 课程无关，因为主要关注将模型投入生产和维护所需的所有组件。因此，在继续学习本笔记本之后的其他课程时，请随意选择任何型号。

将首先设置一些将在不同基线实验中使用的函数。

<table><tbody><tr><td></td><td><div><pre id="__code_2"><span></span><code><span>def</span> <span>set_seeds</span><span>(</span><span>seed</span><span>=</span><span>42</span><span>):</span>
    <span>"""Set seeds for reproducibility."""</span>
    <span>np</span><span>.</span><span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
    <span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

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
<span><span><span>16</span></span></span></pre></div></td><td><div><pre id="__code_3"><span></span><code tabindex="0"><span>def</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>,</span> <span>stem</span><span>,</span> <span>min_freq</span><span>):</span>
    <span>"""Preprocess the data."""</span>
    <span>df</span><span>[</span><span>"text"</span><span>]</span> <span>=</span> <span>df</span><span>.</span><span>title</span> <span>+</span> <span>" "</span> <span>+</span> <span>df</span><span>.</span><span>description</span>  <span># feature engineering</span>
    <span>df</span><span>.</span><span>text</span> <span>=</span> <span>df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>clean_text</span><span>,</span> <span>lower</span><span>=</span><span>lower</span><span>,</span> <span>stem</span><span>=</span><span>stem</span><span>)</span>  <span># clean text</span><span></span>
<span></span>
    <span># Replace OOS tags with `other`</span>
    <span>oos_tags</span> <span>=</span> <span>[</span><span>item</span> <span>for</span> <span>item</span> <span>in</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>unique</span><span>()</span> <span>if</span> <span>item</span> <span>not</span> <span>in</span> <span>ACCEPTED_TAGS</span><span>]</span>
    <span>df</span><span>.</span><span>tag</span> <span>=</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>x</span><span>:</span> <span>"other"</span> <span>if</span> <span>x</span> <span>in</span> <span>oos_tags</span> <span>else</span> <span>x</span><span>)</span><span></span>
<span></span>
    <span># Replace tags below min_freq with `other`</span>
    <span>tags_above_freq</span> <span>=</span> <span>Counter</span><span>(</span><span>tag</span> <span>for</span> <span>tag</span> <span>in</span> <span>tags</span><span>.</span><span>elements</span><span>()</span>
                            <span>if</span> <span>(</span><span>tags</span><span>[</span><span>tag</span><span>]</span> <span>&gt;=</span> <span>min_freq</span><span>))</span>
    <span>df</span><span>.</span><span>tag</span> <span>=</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>tag</span><span>:</span> <span>tag</span> <span>if</span> <span>tag</span> <span>in</span> <span>tags_above_freq</span> <span>else</span> <span>None</span><span>)</span>
    <span>df</span><span>.</span><span>tag</span> <span>=</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>fillna</span><span>(</span><span>"other"</span><span>)</span><span></span>
<span></span>
    <span>return</span> <span>df</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_4"><span></span><code><span>def</span> <span>get_data_splits</span><span>(</span><span>X</span><span>,</span> <span>y</span><span>,</span> <span>train_size</span><span>=</span><span>0.7</span><span>):</span>
    <span>"""Generate balanced data splits."""</span>
    <span>X_train</span><span>,</span> <span>X_</span><span>,</span> <span>y_train</span><span>,</span> <span>y_</span> <span>=</span> <span>train_test_split</span><span>(</span>
        <span>X</span><span>,</span> <span>y</span><span>,</span> <span>train_size</span><span>=</span><span>train_size</span><span>,</span> <span>stratify</span><span>=</span><span>y</span><span>)</span>
    <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> <span>train_test_split</span><span>(</span>
        <span>X_</span><span>,</span> <span>y_</span><span>,</span> <span>train_size</span><span>=</span><span>0.5</span><span>,</span> <span>stratify</span><span>=</span><span>y_</span><span>)</span>
    <span>return</span> <span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span>
</code></pre></div></td></tr></tbody></table>

数据集很小，因此将使用整个数据集进行训练，但对于较大的数据集，应该始终在一个小子集上进行测试（在必要时进行改组之后），这样就不会在计算上浪费时间。

<table><tbody><tr><td></td><td><div><pre id="__code_5"><span></span><code><span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>  <span># shuffle</span>
<span>df</span> <span>=</span> <span>df</span><span>[:</span> <span>num_samples</span><span>]</span>  <span># None = all samples</span>
</code></pre></div></td></tr></tbody></table>

需要洗牌吗？

为什么打乱数据集很重要？

显示答案

_需要_打乱数据，因为数据是按时间顺序组织的。与早期项目相比，最新项目可能具有某些流行的功能或标签。如果在创建数据拆分之前不进行洗牌，那么模型将只会在较早的信号上进行训练并且无法泛化。但是，在其他情况下（例如时间序列预测），洗牌会导致数据泄露。

### 随机的

_动机_：想知道随机（机会）表现是什么样的。所有的努力都应该远远高于这个基线。

<table><tbody><tr><td></td><td><div><pre id="__code_6"><span></span><code><span>from</span> <span>sklearn.metrics</span> <span>import</span> <span>precision_recall_fscore_support</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_7"><span></span><code><span># Set up</span>
<span>set_seeds</span><span>()</span>
<span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>"labeled_projects.csv"</span><span>)</span>
<span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>
<span>df</span> <span>=</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>,</span> <span>min_freq</span><span>=</span><span>min_freq</span><span>)</span>
<span>label_encoder</span> <span>=</span> <span>LabelEncoder</span><span>()</span><span>.</span><span>fit</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>)</span>
<span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> \
    <span>get_data_splits</span><span>(</span><span>X</span><span>=</span><span>df</span><span>.</span><span>text</span><span>.</span><span>to_numpy</span><span>(),</span> <span>y</span><span>=</span><span>label_encoder</span><span>.</span><span>encode</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_8"><span></span><code><span># Label encoder</span>
<span>print</span> <span>(</span><span>label_encoder</span><span>)</span>
<span>print</span> <span>(</span><span>label_encoder</span><span>.</span><span>classes</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
<标签编码器(num_classes=4)>
['计算机视觉'，'mlops'，'自然语言处理'，'其他']

```

<table><tbody><tr><td></td><td><div><pre id="__code_9"><span></span><code tabindex="0"><span># Generate random predictions</span>
<span>y_pred</span> <span>=</span> <span>np</span><span>.</span><span>random</span><span>.</span><span>randint</span><span>(</span><span>low</span><span>=</span><span>0</span><span>,</span> <span>high</span><span>=</span><span>len</span><span>(</span><span>label_encoder</span><span>),</span> <span>size</span><span>=</span><span>len</span><span>(</span><span>y_test</span><span>))</span>
<span>print</span> <span>(</span><span>y_pred</span><span>.</span><span>shape</span><span>)</span>
<span>print</span> <span>(</span><span>y_pred</span><span>[</span><span>0</span><span>:</span><span>5</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
(144,)
[0 0 0 1 3]

```

<table><tbody><tr><td></td><td><div><pre id="__code_10"><span></span><code tabindex="0"><span># Evaluate</span>
<span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
<span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “精度”：0.31684880006233446，
  “召回”：0.2361111111111111，
  “f1”：0.2531624273393283
}

```

假设每个类别都有相同的概率。让使用训练拆分来找出真正的概率是多少。

<table><tbody><tr><td></td><td><div><pre id="__code_11"><span></span><code tabindex="0"><span># Class frequencies</span>
<span>p</span> <span>=</span> <span>[</span><span>Counter</span><span>(</span><span>y_test</span><span>)[</span><span>index</span><span>]</span><span>/</span><span>len</span><span>(</span><span>y_test</span><span>)</span> <span>for</span> <span>index</span> <span>in</span> <span>range</span><span>(</span><span>len</span><span>(</span><span>label_encoder</span><span>))]</span>
<span>p</span>
</code></pre></div></td></tr></tbody></table>

```
[0.375, 0.08333333333333333, 0.4027777777777778, 0.1388888888888889]

```

<table><tbody><tr><td></td><td><div><pre id="__code_12"><span></span><code tabindex="0"><span># Generate weighted random predictions</span>
<span>y_pred</span> <span>=</span> <span>np</span><span>.</span><span>random</span><span>.</span><span>choice</span><span>(</span><span>a</span><span>=</span><span>range</span><span>(</span><span>len</span><span>(</span><span>label_encoder</span><span>)),</span> <span>size</span><span>=</span><span>len</span><span>(</span><span>y_test</span><span>),</span> <span>p</span><span>=</span><span>p</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_13"><span></span><code tabindex="0"><span># Evaluate</span>
<span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
<span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “精度”：0.316412540257649，
  “召回”：0.3263888888888889，
  “f1”：0.31950372012322
}

```

_限制_：没有使用输入中的标记来影响预测，所以没有学到任何东西。

### 基于规则

_动机_：希望在输入中使用信号（以及领域专业知识和辅助数据）来确定标签。

<table><tbody><tr><td></td><td><div><pre id="__code_14"><span></span><code><span># Setup</span>
<span>set_seeds</span><span>()</span>
<span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>"labeled_projects.csv"</span><span>)</span>
<span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>
<span>df</span> <span>=</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>,</span> <span>min_freq</span><span>=</span><span>min_freq</span><span>)</span>
<span>label_encoder</span> <span>=</span> <span>LabelEncoder</span><span>()</span><span>.</span><span>fit</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>)</span>
<span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> \
    <span>get_data_splits</span><span>(</span><span>X</span><span>=</span><span>df</span><span>.</span><span>text</span><span>.</span><span>to_numpy</span><span>(),</span> <span>y</span><span>=</span><span>label_encoder</span><span>.</span><span>encode</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_15"><span></span><code><span>def</span> <span>get_tag</span><span>(</span><span>text</span><span>,</span> <span>aliases_by_tag</span><span>):</span>
    <span>"""If a token matches an alias,</span>
<span>    then add the corresponding tag class."""</span>
    <span>for</span> <span>tag</span><span>,</span> <span>aliases</span> <span>in</span> <span>aliases_by_tag</span><span>.</span><span>items</span><span>():</span>
        <span>if</span> <span>replace_dash</span><span>(</span><span>tag</span><span>)</span> <span>in</span> <span>text</span><span>:</span>
            <span>return</span> <span>tag</span>
        <span>for</span> <span>alias</span> <span>in</span> <span>aliases</span><span>:</span>
            <span>if</span> <span>alias</span> <span>in</span> <span>text</span><span>:</span>
                <span>return</span> <span>tag</span>
    <span>return</span> <span>None</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_16"><span></span><code><span># Sample</span>
<span>text</span> <span>=</span> <span>"A pretrained model hub for popular nlp models."</span>
<span>get_tag</span><span>(</span><span>text</span><span>=</span><span>clean_text</span><span>(</span><span>text</span><span>),</span> <span>aliases_by_tag</span><span>=</span><span>aliases_by_tag</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
“自然语言处理”

```

<table><tbody><tr><td></td><td><div><pre id="__code_17"><span></span><code><span># Prediction</span>
<span>tags</span> <span>=</span> <span>[]</span>
<span>for</span> <span>text</span> <span>in</span> <span>X_test</span><span>:</span>
    <span>tag</span> <span>=</span> <span>get_tag</span><span>(</span><span>text</span><span>,</span> <span>aliases_by_tag</span><span>=</span><span>aliases_by_tag</span><span>)</span>
    <span>tags</span><span>.</span><span>append</span><span>(</span><span>tag</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_18"><span></span><code tabindex="0"><span># Encode labels</span>
<span>y_pred</span> <span>=</span> <span>[</span><span>label_encoder</span><span>.</span><span>class_to_index</span><span>[</span><span>tag</span><span>]</span> <span>if</span> <span>tag</span> <span>is</span> <span>not</span> <span>None</span> <span>else</span> <span>-</span><span>1</span> <span>for</span> <span>tag</span> <span>in</span> <span>tags</span><span>]</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_19"><span></span><code tabindex="0"><span># Evaluate</span>
<span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
<span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “精度”：0.9097222222222222，
  “召回”：0.18055555555555555，
  “f1”：0.2919455654201417
}

```

为什么召回率这么低？

为什么准确率很高，但召回率却如此之低？

显示答案

当输入信号中没有使用这些特定的别名时，仅依赖别名会证明是灾难性的。为了改进这一点，可以构建一个包含相关术语的词袋。例如，将诸如`text classification`和之类的术语映射`named entity recognition`到`natural-language-processing`标签，但构建它是一项不平凡的任务。更不用说，随着数据环境的成熟，需要不断更新这些规则。

<table><tbody><tr><td></td><td><div><pre id="__code_20"><span></span><code><span># Pitfalls</span>
<span>text</span> <span>=</span> <span>"Transfer learning with transformers for text classification."</span>
<span>print</span> <span>(</span><span>get_tag</span><span>(</span><span>text</span><span>=</span><span>clean_text</span><span>(</span><span>text</span><span>),</span> <span>aliases_by_tag</span><span>=</span><span>aliases_by_tag</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
没有任何

```

小费

还可以使用[词干提取](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html)来进一步完善基于规则的流程：

<table><tbody><tr><td></td><td><div><pre id="__code_21"><span></span><code><span>from</span> <span>nltk.stem</span> <span>import</span> <span>PorterStemmer</span>
<span>stemmer</span> <span>=</span> <span>PorterStemmer</span><span>()</span>
<span>print</span> <span>(</span><span>stemmer</span><span>.</span><span>stem</span><span>(</span><span>"democracy"</span><span>))</span>
<span>print</span> <span>(</span><span>stemmer</span><span>.</span><span>stem</span><span>(</span><span>"democracies"</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
民主
民主

```

但是这些基于规则的方法只能在绝对条件匹配时产生具有高确定性的标签，因此最好不要在这种方法上花费太多精力。

_限制_：未能概括或学习任何隐式模式来预测标签，因为将输入中的标记视为孤立的实体。

### 矢量化

_动机_：

-   _表示_：使用词频-逆文档频率[(TF-IDF)](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)来捕获某个标记相对于所有输入对特定输入的重要性，而不是将输入文本中的单词视为孤立的标记。
-   _架构_：希望模型能够有意义地提取编码信号以预测输出标签。

到目前为止，已经将输入文本中的单词视为孤立的标记，并且还没有真正捕捉到标记之间的任何含义。让使用 TF-IDF（通过 Scikit-learn's [`TfidfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)）来捕获令牌对特定输入相对于所有输入的重要性。

<table><tbody><tr><td></td><td><div><pre id="__code_22"><span></span><code><span>from</span> <span>sklearn.feature_extraction.text</span> <span>import</span> <span>TfidfVectorizer</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_23"><span></span><code><span># Setup</span>
<span>set_seeds</span><span>()</span>
<span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>"labeled_projects.csv"</span><span>)</span>
<span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>
<span>df</span> <span>=</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>,</span> <span>min_freq</span><span>=</span><span>min_freq</span><span>)</span>
<span>label_encoder</span> <span>=</span> <span>LabelEncoder</span><span>()</span><span>.</span><span>fit</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>)</span>
<span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> \
    <span>get_data_splits</span><span>(</span><span>X</span><span>=</span><span>df</span><span>.</span><span>text</span><span>.</span><span>to_numpy</span><span>(),</span> <span>y</span><span>=</span><span>label_encoder</span><span>.</span><span>encode</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_24"><span></span><code><span># Saving raw X_test to compare with later</span>
<span>X_test_raw</span> <span>=</span> <span>X_test</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_25"><span></span><code tabindex="0"><span># Tf-idf</span>
<span>vectorizer</span> <span>=</span> <span>TfidfVectorizer</span><span>(</span><span>analyzer</span><span>=</span><span>"char"</span><span>,</span> <span>ngram_range</span><span>=</span><span>(</span><span>2</span><span>,</span><span>7</span><span>))</span>  <span># char n-grams</span>
<span>print</span> <span>(</span><span>X_train</span><span>[</span><span>0</span><span>])</span>
<span>X_train</span> <span>=</span> <span>vectorizer</span><span>.</span><span>fit_transform</span><span>(</span><span>X_train</span><span>)</span>
<span>X_val</span> <span>=</span> <span>vectorizer</span><span>.</span><span>transform</span><span>(</span><span>X_val</span><span>)</span>
<span>X_test</span> <span>=</span> <span>vectorizer</span><span>.</span><span>transform</span><span>(</span><span>X_test</span><span>)</span>
<span>print</span> <span>(</span><span>X_train</span><span>.</span><span>shape</span><span>)</span>  <span># scipy.sparse.csr_matrix</span>
</code></pre></div></td></tr></tbody></table>

```
tao 大规模基准跟踪对象多样化数据集跟踪对象 tao 包含 2 907 个高分辨率视频，捕获不同环境半分钟长
(668, 99664)

```

<table><tbody><tr><td></td><td><div><pre id="__code_26"><span></span><code><span># Class weights</span>
<span>counts</span> <span>=</span> <span>np</span><span>.</span><span>bincount</span><span>(</span><span>y_train</span><span>)</span>
<span>class_weights</span> <span>=</span> <span>{</span><span>i</span><span>:</span> <span>1.0</span><span>/</span><span>count</span> <span>for</span> <span>i</span><span>,</span> <span>count</span> <span>in</span> <span>enumerate</span><span>(</span><span>counts</span><span>)}</span>
<span>print</span> <span>(</span><span>f</span><span>"class counts: </span><span>{</span><span>counts</span><span>}</span><span>,</span><span>\n</span><span>class weights: </span><span>{</span><span>class_weights</span><span>}</span><span>"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
班级人数：[249 55 272 92]，
类权重：{0: 0.004016064257028112, 1: 0.01818181818181818, 2: 0.003676470588235294, 3: 0.010869565217391304}

```

### 数据不平衡

对于数据集，可能经常会注意到数据不平衡问题，其中一系列连续值（回归）或某些类别（分类）可能没有足够的数据量可供学习。这在训练时成为一个主要问题，因为模型将学习泛化到可用数据并在数据稀疏的区域表现不佳。有几种技术可以缓解数据不平衡，包括[重采样](https://github.com/scikit-learn-contrib/imbalanced-learn)、合并类权重、[增强](https://madewithml.com/courses/mlops/augmentation/)等。尽管理想的解决方案是为少数类收集更多数据！

> 将使用[imblearn 包](https://imbalanced-learn.org/stable/)来确保对少数类进行过采样以等于多数类（带有大多数样本的标签）。

```
pip install imbalanced-learn==0.8.1 -q

```

<table><tbody><tr><td></td><td><div><pre id="__code_28"><span></span><code><span>from</span> <span>imblearn.over_sampling</span> <span>import</span> <span>RandomOverSampler</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_29"><span></span><code><span># Oversample (training set)</span>
<span>oversample</span> <span>=</span> <span>RandomOverSampler</span><span>(</span><span>sampling_strategy</span><span>=</span><span>"all"</span><span>)</span>
<span>X_over</span><span>,</span> <span>y_over</span> <span>=</span> <span>oversample</span><span>.</span><span>fit_resample</span><span>(</span><span>X_train</span><span>,</span> <span>y_train</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

警告

重要的是，仅在火车拆分上应用采样，这样就不会在其他数据拆分中引入数据泄漏。

<table><tbody><tr><td></td><td><div><pre id="__code_30"><span></span><code><span># Class weights</span>
<span>counts</span> <span>=</span> <span>np</span><span>.</span><span>bincount</span><span>(</span><span>y_over</span><span>)</span>
<span>class_weights</span> <span>=</span> <span>{</span><span>i</span><span>:</span> <span>1.0</span><span>/</span><span>count</span> <span>for</span> <span>i</span><span>,</span> <span>count</span> <span>in</span> <span>enumerate</span><span>(</span><span>counts</span><span>)}</span>
<span>print</span> <span>(</span><span>f</span><span>"class counts: </span><span>{</span><span>counts</span><span>}</span><span>,</span><span>\n</span><span>class weights: </span><span>{</span><span>class_weights</span><span>}</span><span>"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
班级人数：[272 272 272 272]，
类权重：{0: 0.003676470588235294, 1: 0.003676470588235294, 2: 0.003676470588235294, 3: 0.003676470588235294}

```

_限制_：

-   **表示**：TF-IDF 表示不封装超出频率的太多信号，但需要更细粒度的令牌表示。
-   **架构**：希望开发能够以更符合上下文的方式使用更好表示的编码的模型。

### 机器学习

将使用随机梯度下降分类器 ( [SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) ) 作为模型。将使用对数损失，以便它有效地与 SGD 进行[逻辑回归。](https://madewithml.com/courses/foundations/logistic-regression/)

> 这样做是因为希望对训练过程（epochs）有更多的控制，而不是使用 scikit-learn 的默认二阶优化方法（例如[LGBFS](https://en.wikipedia.org/wiki/Limited-memory_BFGS)）进行逻辑回归。

<table><tbody><tr><td></td><td><div><pre id="__code_31"><span></span><code><span>from</span> <span>sklearn</span> <span>import</span> <span>metrics</span>
<span>from</span> <span>sklearn.linear_model</span> <span>import</span> <span>SGDClassifier</span>
<span>from</span> <span>sklearn.metrics</span> <span>import</span> <span>log_loss</span><span>,</span> <span>precision_recall_fscore_support</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_32"><span></span><code><span># Initialize model</span>
<span>model</span> <span>=</span> <span>SGDClassifier</span><span>(</span>
    <span>loss</span><span>=</span><span>"log"</span><span>,</span> <span>penalty</span><span>=</span><span>"l2"</span><span>,</span> <span>alpha</span><span>=</span><span>1e-4</span><span>,</span> <span>max_iter</span><span>=</span><span>1</span><span>,</span>
    <span>learning_rate</span><span>=</span><span>"constant"</span><span>,</span> <span>eta0</span><span>=</span><span>1e-1</span><span>,</span> <span>power_t</span><span>=</span><span>0.1</span><span>,</span>
    <span>warm_start</span><span>=</span><span>True</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

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
<span><span><span>16</span></span></span></pre></div></td><td><div><pre id="__code_33"><span></span><code><span># Train model</span>
<span>num_epochs</span> <span>=</span> <span>100</span>
<span>for</span> <span>epoch</span> <span>in</span> <span>range</span><span>(</span><span>num_epochs</span><span>):</span>
    <span># Training</span>
    <span>model</span><span>.</span><span>fit</span><span>(</span><span>X_over</span><span>,</span> <span>y_over</span><span>)</span><span></span>
<span></span>
    <span># Evaluation</span>
    <span>train_loss</span> <span>=</span> <span>log_loss</span><span>(</span><span>y_train</span><span>,</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_train</span><span>))</span>
    <span>val_loss</span> <span>=</span> <span>log_loss</span><span>(</span><span>y_val</span><span>,</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>))</span><span></span>
<span></span>
    <span>if</span> <span>not</span> <span>epoch</span><span>%</span><span>10</span><span>:</span>
        <span>print</span><span>(</span>
            <span>f</span><span>"Epoch: </span><span>{</span><span>epoch</span><span>:</span><span>02d</span><span>}</span><span> | "</span>
            <span>f</span><span>"train_loss: </span><span>{</span><span>train_loss</span><span>:</span><span>.5f</span><span>}</span><span>, "</span>
            <span>f</span><span>"val_loss: </span><span>{</span><span>val_loss</span><span>:</span><span>.5f</span><span>}</span><span>"</span>
        <span>)</span>
</code></pre></div></td></tr></tbody></table>

```
时代：00 | train_loss：1.16930，val_loss：1.21451
纪元：10 | train_loss：0.46116，val_loss：0.65903
纪元：20 | train_loss：0.31565，val_loss：0.56018
时代：30 | train_loss：0.25207，val_loss：0.51967
时代：40 | train_loss：0.21740，val_loss：0.49822
纪元：50 | train_loss：0.19615，val_loss：0.48529
时代：60 | train_loss：0.18249，val_loss：0.47708
纪元：70 | train_loss：0.17330，val_loss：0.47158
时代：80 | train_loss：0.16671，val_loss：0.46765
时代：90 | train_loss：0.16197，val_loss：0.46488

```

可以进一步优化训练管道，例如[提前停止](https://madewithml.com/courses/foundations/utilities/#early-stopping)将使用创建的验证集的功能。但是希望在建模阶段简化这个与模型无关的课程😉

警告

SGDClassifier有一个标志，您可以在[其中](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)`early_stopping`指定要用于验证的训练集的一部分。为什么这对来说是个坏主意？因为已经在训练集中应用了过采样，所以如果这样做，会引入数据泄漏。

<table><tbody><tr><td></td><td><div><pre id="__code_34"><span></span><code tabindex="0"><span># Evaluate</span>
<span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>X_test</span><span>)</span>
<span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
<span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “精度”：0.8753577441077441，
  “召回”：0.8680555555555556，
  “f1”：0.8654096949533866
}

```

小费

Scikit-learn 有一个称为[管道](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)的概念，它允许将转换和训练步骤组合到一个可调用函数中。

可以从头开始创建管道：

<table><tbody><tr><td></td><td><div><pre id="__code_35"><span></span><code><span># Create pipeline from scratch</span>
<span>from</span> <span>sklearn.pipeline</span> <span>import</span> <span>Pipeline</span>
<span>steps</span> <span>=</span> <span>((</span><span>"tfidf"</span><span>,</span> <span>TfidfVectorizer</span><span>()),</span> <span>(</span><span>"model"</span><span>,</span> <span>SGDClassifier</span><span>()))</span>
<span>pipe</span> <span>=</span> <span>Pipeline</span><span>(</span><span>steps</span><span>)</span>
<span>pipe</span><span>.</span><span>fit</span><span>(</span><span>X_train</span><span>,</span> <span>y_train</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

或使用训练有素的组件制作一个：

<table><tbody><tr><td></td><td><div><pre id="__code_36"><span></span><code><span># Make pipeline from existing components</span>
<span>from</span> <span>sklearn.pipeline</span> <span>import</span> <span>make_pipeline</span>
<span>pipe</span> <span>=</span> <span>make_pipeline</span><span>(</span><span>vectorizer</span><span>,</span> <span>model</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

_限制_：

-   _表示_：TF-IDF 表示没有封装太多频率以外的信号，但需要更细粒度的令牌表示，以说明令牌本身的重要性（[嵌入](https://madewithml.com/courses/foundations/embeddings/)）。
-   _架构_：希望开发能够以更符合上下文的方式使用更好表示的编码的模型。

<table><tbody><tr><td></td><td><div><pre id="__code_37"><span></span><code><span># Inference (with tokens similar to training data)</span>
<span>text</span> <span>=</span> <span>"Transfer learning with transformers for text classification."</span>
<span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>vectorizer</span><span>.</span><span>transform</span><span>([</span><span>text</span><span>]))</span>
<span>label_encoder</span><span>.</span><span>decode</span><span>(</span><span>y_pred</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
['自然语言处理']

```

<table><tbody><tr><td></td><td><div><pre id="__code_38"><span></span><code><span># Probabilities</span>
<span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>vectorizer</span><span>.</span><span>transform</span><span>([</span><span>text</span><span>]))</span>
<span>{</span><span>tag</span><span>:</span><span>y_prob</span><span>[</span><span>0</span><span>][</span><span>i</span><span>]</span> <span>for</span> <span>i</span><span>,</span> <span>tag</span> <span>in</span> <span>enumerate</span><span>(</span><span>label_encoder</span><span>.</span><span>classes</span><span>)}</span>
</code></pre></div></td></tr></tbody></table>

```
{'计算机视觉'：0.023672281234089494，
 'mlops'：0.004158589896756235，
 “自然语言处理”：0.9621906411391856，
 “其他”：0.009978487729968667}

```

<table><tbody><tr><td></td><td><div><pre id="__code_39"><span></span><code><span># Inference (with tokens not similar to training data)</span>
<span>text</span> <span>=</span> <span>"Interpretability methods for explaining model behavior."</span>
<span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>vectorizer</span><span>.</span><span>transform</span><span>([</span><span>text</span><span>]))</span>
<span>label_encoder</span><span>.</span><span>decode</span><span>(</span><span>y_pred</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
['自然语言处理']

```

<table><tbody><tr><td></td><td><div><pre id="__code_40"><span></span><code><span># Probabilities</span>
<span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>vectorizer</span><span>.</span><span>transform</span><span>([</span><span>text</span><span>]))</span>
<span>{</span><span>tag</span><span>:</span><span>y_prob</span><span>[</span><span>0</span><span>][</span><span>i</span><span>]</span> <span>for</span> <span>i</span><span>,</span> <span>tag</span> <span>in</span> <span>enumerate</span><span>(</span><span>label_encoder</span><span>.</span><span>classes</span><span>)}</span>
</code></pre></div></td></tr></tbody></table>

```
{'计算机视觉'：0.13150802188532523，
 'mlops'：0.11198040241517894，
 “自然语言处理”：0.584025872986128，
 “其他”：0.17248570271336786}

```

将创建一个自定义预测函数，如果多数类不高于某个 softmax 分数，则预测`other`该类。在[目标](https://madewithml.com/courses/mlops/design/#objectives)中，认为精度对来说非常重要，可以利用标签和 QA 工作流程来提高后续手动检查期间的召回率。

警告

模型可能会受到过度自信的影响，因此应用此限制可能不如想象的那么有效，尤其是对于更大的神经网络。有关更多信息，请参阅[评估课程的](https://madewithml.com/courses/mlops/evaluation/)[自信学习](https://madewithml.com/courses/mlops/evaluation/#confident-learning)部分。[](https://madewithml.com/courses/mlops/evaluation/)

<table><tbody><tr><td></td><td><div><pre id="__code_41"><span></span><code tabindex="0"><span># Determine first quantile softmax score for the correct class (on validation split)</span>
<span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>X_val</span><span>)</span>
<span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>)</span>
<span>threshold</span> <span>=</span> <span>np</span><span>.</span><span>quantile</span><span>([</span><span>y_prob</span><span>[</span><span>i</span><span>][</span><span>j</span><span>]</span> <span>for</span> <span>i</span><span>,</span> <span>j</span> <span>in</span> <span>enumerate</span><span>(</span><span>y_pred</span><span>)],</span> <span>q</span><span>=</span><span>0.25</span><span>)</span>  <span># Q1</span>
<span>threshold</span>
</code></pre></div></td></tr></tbody></table>

```
0.6742890218960005

```

警告

在验证拆分中执行此操作非常重要，因此不会在评估测试拆分之前使用训练拆分或泄漏信息来夸大值。

<table><tbody><tr><td></td><td><div><pre id="__code_42"><span></span><code tabindex="0"><span># Custom predict function</span>
<span>def</span> <span>custom_predict</span><span>(</span><span>y_prob</span><span>,</span> <span>threshold</span><span>,</span> <span>index</span><span>):</span>
    <span>"""Custom predict function that defaults</span>
<span>    to an index if conditions are not met."""</span>
    <span>y_pred</span> <span>=</span> <span>[</span><span>np</span><span>.</span><span>argmax</span><span>(</span><span>p</span><span>)</span> <span>if</span> <span>max</span><span>(</span><span>p</span><span>)</span> <span>&gt;</span> <span>threshold</span> <span>else</span> <span>index</span> <span>for</span> <span>p</span> <span>in</span> <span>y_prob</span><span>]</span>
    <span>return</span> <span>np</span><span>.</span><span>array</span><span>(</span><span>y_pred</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_43"><span></span><code tabindex="0"><span>def</span> <span>predict_tag</span><span>(</span><span>texts</span><span>):</span>
    <span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>vectorizer</span><span>.</span><span>transform</span><span>(</span><span>texts</span><span>))</span>
    <span>other_index</span> <span>=</span> <span>label_encoder</span><span>.</span><span>class_to_index</span><span>[</span><span>"other"</span><span>]</span>
    <span>y_pred</span> <span>=</span> <span>custom_predict</span><span>(</span><span>y_prob</span><span>=</span><span>y_prob</span><span>,</span> <span>threshold</span><span>=</span><span>threshold</span><span>,</span> <span>index</span><span>=</span><span>other_index</span><span>)</span>
    <span>return</span> <span>label_encoder</span><span>.</span><span>decode</span><span>(</span><span>y_pred</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_44"><span></span><code><span># Inference (with tokens not similar to training data)</span>
<span>text</span> <span>=</span> <span>"Interpretability methods for explaining model behavior."</span>
<span>predict_tag</span><span>(</span><span>texts</span><span>=</span><span>[</span><span>text</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
['其他']

```

<table><tbody><tr><td></td><td><div><pre id="__code_45"><span></span><code tabindex="0"><span># Evaluate</span>
<span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_test</span><span>)</span>
<span>y_pred</span> <span>=</span> <span>custom_predict</span><span>(</span><span>y_prob</span><span>=</span><span>y_prob</span><span>,</span> <span>threshold</span><span>=</span><span>threshold</span><span>,</span> <span>index</span><span>=</span><span>other_index</span><span>)</span>
<span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
<span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
<span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  “精度”：0.9116161616161617，
  “召回”：0.7569444444444444，
  “f1”：0.7929971988795519
}

```

小费

甚至可以使用每个类别的阈值，特别是因为有一些数据不平衡，这会影响模型对某些类别的信心。

<table><tbody><tr><td></td><td><div><pre id="__code_46"><span></span><code><span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>X_val</span><span>)</span>
<span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>)</span>
<span>class_thresholds</span> <span>=</span> <span>{}</span>
<span>for</span> <span>index</span> <span>in</span> <span>range</span><span>(</span><span>len</span><span>(</span><span>label_encoder</span><span>.</span><span>classes</span><span>)):</span>
    <span>class_thresholds</span><span>[</span><span>index</span><span>]</span> <span>=</span> <span>np</span><span>.</span><span>mean</span><span>(</span>
        <span>[</span><span>y_prob</span><span>[</span><span>i</span><span>][</span><span>index</span><span>]</span> <span>for</span> <span>i</span> <span>in</span> <span>np</span><span>.</span><span>where</span><span>(</span><span>y_pred</span><span>==</span><span>index</span><span>)[</span><span>0</span><span>]])</span>
</code></pre></div></td></tr></tbody></table>

> 这门 MLOps 课程实际上与模型无关（只要它产生概率分布），因此可以随意使用更复杂的表示（[嵌入](https://madewithml.com/courses/foundations/embeddings/)）和更复杂的架构（[CNN](https://madewithml.com/courses/foundations/convolutional-neural-networks/)、[变压器](https://madewithml.com/courses/foundations/transformers/)等）。将在其余课程中使用这个基本的逻辑回归模型，因为它简单、快速并且实际上具有相当的性能（与最先进的预训练变压器相比，f1 差异<10%）。

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
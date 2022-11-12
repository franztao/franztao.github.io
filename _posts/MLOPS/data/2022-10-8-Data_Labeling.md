---
layout:     post
title:      探索性数据分析
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - EDA

---
## 数据增强

___

## 直觉

我们经常希望通过数据增强来增加训练数据的大小和多样性。它涉及使用现有样本来生成合成但现实的示例。

1.  **拆分数据集**。我们希望首先拆分我们的数据集，因为如果我们允许将生成的样本放置在不同的数据拆分中，许多增强技术将导致某种形式的数据泄漏。
    
    > 例如，一些扩充涉及为句子中的某些关键标记生成同义词。如果我们允许从同一原始句子生成的句子进入不同的拆分，我们可能会在我们的不同拆分中泄漏具有几乎相同嵌入表示的样本。
    
2.  **增加训练拆分**。我们只想在训练集上应用数据增强，因为我们的验证和测试拆分应该用于提供对实际数据点的准确估计。
    
3.  **检查和验证**. 如果增强的数据样本不是我们的模型在生产中可能遇到的可能输入，那么仅仅为了增加我们的训练样本大小而增加是没有用的。
    

数据增强的确切方法很大程度上取决于数据类型和应用程序。以下是可以增强不同模式的数据的几种方法：

![数据增强类型](https://madewithml.com/static/images/mlops/augmentation/snorkel.png)

-   **一般**：归一化、平滑、随机噪声、合成过采样 ( [SMOTE](https://arxiv.org/abs/1106.1813) ) 等。
-   **自然语言处理 (NLP)**：替换（同义词、tfidf、嵌入、掩码模型）、随机噪声、拼写错误等。
-   **计算机视觉 (CV)**：裁剪、翻转、旋转、填充、饱和、增加亮度等。

警告

虽然某些数据模式（例如图像）的转换很容易检查和验证，但其他模式可能会引入静默错误。例如，改变文本中标记的顺序可以显着改变含义（“这真的很酷”→“这真的很酷吗”）。因此，重要的是测量我们的增强策略将引入的噪声，并对发生的转换进行精细控制。

## 图书馆

根据特征类型和任务，有许多数据增强库允许我们扩展训练数据。

### 自然语言处理 (NLP)

-   [NLPAug](https://github.com/makcedward/nlpaug)：NLP 的数据增强。
-   [TextAttack](https://github.com/QData/TextAttack)：NLP 中对抗性攻击、数据增强和模型训练的框架。
-   [TextAugment](https://github.com/dsfsi/textaugment)：文本增强库。

### 计算机视觉 (CV)

-   [Imgaug](https://github.com/aleju/imgaug)：用于机器学习实验的图像增强。
-   [Albumentations](https://github.com/albumentations-team/albumentations)：快速图像增强库。
-   [Augmentor](https://github.com/mdbloice/Augmentor)：用于机器学习的 Python 图像增强库。
-   [Kornia.augmentation](https://github.com/kornia/kornia)：在 GPU 中执行数据增强的模块。
-   [SOLT](https://github.com/MIPT-Oulu/solt)：深度学习的数据增强库，支持图像、分割掩码、标签和关键点。

### 其他

-   [Snorkel](https://github.com/snorkel-team/snorkel)：用于生成具有弱监督的训练数据的系统。
-   [DeltaPy⁠⁠](https://github.com/firmai/deltapy)：表格数据增强和特征工程。
-   [Audiomentations](https://github.com/iver56/audiomentations)：一个用于音频数据增强的 Python 库。
-   [Tsaug](https://github.com/arundo/tsaug)：用于时间序列增强的 Python 包。

## 应用

让我们使用[nlpaug](https://github.com/makcedward/nlpaug)库来扩充我们的数据集并评估生成样本的质量。

```
pip install nlpaug==1.1.0 transformers==3.0.2 -q
pip install snorkel==0.9.8 -q

```

<table><tbody><tr><td></td><td><div><pre id="__code_2"><span></span><code><span>import</span> <span>nlpaug.augmenter.word</span> <span>as</span> <span>naw</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_3"><span></span><code tabindex="0"><span># Load tokenizers and transformers</span>
<span>substitution</span> <span>=</span> <span>naw</span><span>.</span><span>ContextualWordEmbsAug</span><span>(</span><span>model_path</span><span>=</span><span>"distilbert-base-uncased"</span><span>,</span> <span>action</span><span>=</span><span>"substitute"</span><span>)</span>
<span>insertion</span> <span>=</span> <span>naw</span><span>.</span><span>ContextualWordEmbsAug</span><span>(</span><span>model_path</span><span>=</span><span>"distilbert-base-uncased"</span><span>,</span> <span>action</span><span>=</span><span>"insert"</span><span>)</span>
<span>text</span> <span>=</span> <span>"Conditional image generation using Variational Autoencoders and GANs."</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_4"><span></span><code><span># Substitutions</span>
<span>substitution</span><span>.</span><span>augment</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
使用变分信号和甘斯的分层风险映射。

```

替换对我们来说似乎不是一个好主意，因为某些关键字为我们的标签提供了强烈的信号，所以我们不想改变它们。另外，请注意，这些增强不是确定性的，每次运行时都会有所不同。让我们尝试插入...

<table><tbody><tr><td></td><td><div><pre id="__code_5"><span></span><code><span># Insertions</span>
<span>insertion</span><span>.</span><span>augment</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
使用多个变分自动编码器和甘斯的自动条件逆图像生成算法。

```

稍微好一点但仍然很脆弱，现在它可以潜在地插入可能影响误报标签出现的关键词。也许不是替换或插入新的标记，让我们尝试简单地将机器学习相关的关键字与其别名交换。我们将使用 Snorkel 的[转换函数](https://www.snorkel.org/use-cases/02-spam-data-augmentation-tutorial)来轻松实现这一点。

<table><tbody><tr><td></td><td><div><pre id="__code_6"><span></span><code><span># Replace dashes from tags &amp; aliases</span>
<span>def</span> <span>replace_dash</span><span>(</span><span>x</span><span>):</span>
    <span>return</span> <span>x</span><span>.</span><span>replace</span><span>(</span><span>"-"</span><span>,</span> <span>" "</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_7"><span></span><code><span># Aliases</span>
<span>aliases_by_tag</span> <span>=</span> <span>{</span>
    <span>"computer-vision"</span><span>:</span> <span>[</span><span>"cv"</span><span>,</span> <span>"vision"</span><span>],</span>
    <span>"mlops"</span><span>:</span> <span>[</span><span>"production"</span><span>],</span>
    <span>"natural-language-processing"</span><span>:</span> <span>[</span><span>"nlp"</span><span>,</span> <span>"nlproc"</span><span>]</span>
<span>}</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_8"><span></span><code><span># Flatten dict</span>
<span>flattened_aliases</span> <span>=</span> <span>{}</span>
<span>for</span> <span>tag</span><span>,</span> <span>aliases</span> <span>in</span> <span>aliases_by_tag</span><span>.</span><span>items</span><span>():</span>
    <span>tag</span> <span>=</span> <span>replace_dash</span><span>(</span><span>x</span><span>=</span><span>tag</span><span>)</span>
    <span>if</span> <span>len</span><span>(</span><span>aliases</span><span>):</span>
        <span>flattened_aliases</span><span>[</span><span>tag</span><span>]</span> <span>=</span> <span>aliases</span>
    <span>for</span> <span>alias</span> <span>in</span> <span>aliases</span><span>:</span>
        <span>_aliases</span> <span>=</span> <span>aliases</span> <span>+</span> <span>[</span><span>tag</span><span>]</span>
        <span>_aliases</span><span>.</span><span>remove</span><span>(</span><span>alias</span><span>)</span>
        <span>flattened_aliases</span><span>[</span><span>alias</span><span>]</span> <span>=</span> <span>_aliases</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_9"><span></span><code><span>print</span> <span>(</span><span>flattened_aliases</span><span>[</span><span>"natural language processing"</span><span>])</span>
<span>print</span> <span>(</span><span>flattened_aliases</span><span>[</span><span>"nlp"</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
['nlp', 'nlproc']
['nlproc', '自然语言处理']

```

> 现在我们将使用标签和别名，但我们可以使用[inflect](https://github.com/jaraco/inflect)`aliases_by_tag`包来解释多个标签，或者在替换别名之前应用词干提取等。[](https://github.com/jaraco/inflect)

<table><tbody><tr><td></td><td><div><pre id="__code_10"><span></span><code><span># We want to match with the whole word only</span>
<span>print</span> <span>(</span><span>"gan"</span> <span>in</span> <span>"This is a gan."</span><span>)</span>
<span>print</span> <span>(</span><span>"gan"</span> <span>in</span> <span>"This is gandalf."</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_11"><span></span><code><span># \b matches spaces</span>
<span>def</span> <span>find_word</span><span>(</span><span>word</span><span>,</span> <span>text</span><span>):</span>
    <span>word</span> <span>=</span> <span>word</span><span>.</span><span>replace</span><span>(</span><span>"+"</span><span>,</span> <span>"\+"</span><span>)</span>
    <span>pattern</span> <span>=</span> <span>re</span><span>.</span><span>compile</span><span>(</span><span>fr</span><span>"\b(</span><span>{</span><span>word</span><span>}</span><span>)\b"</span><span>,</span> <span>flags</span><span>=</span><span>re</span><span>.</span><span>IGNORECASE</span><span>)</span>
    <span>return</span> <span>pattern</span><span>.</span><span>search</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_12"><span></span><code><span># Correct behavior (single instance)</span>
<span>print</span> <span>(</span><span>find_word</span><span>(</span><span>"gan"</span><span>,</span> <span>"This is a gan."</span><span>))</span>
<span>print</span> <span>(</span><span>find_word</span><span>(</span><span>"gan"</span><span>,</span> <span>"This is gandalf."</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
<re.Match 对象；跨度=（10, 13），匹配='gan'>
没有任何

```

现在让我们使用 snorkel[`transformation_function`](https://snorkel.readthedocs.io/en/latest/packages/_autosummary/augmentation/snorkel.augmentation.transformation_function.html)系统地将这种转换应用于我们的数据。

<table><tbody><tr><td></td><td><div><pre id="__code_13"><span></span><code><span>from</span> <span>snorkel.augmentation</span> <span>import</span> <span>transformation_function</span>
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
<span><span><span>15</span></span></span></pre></div></td><td><div><pre id="__code_14"><span></span><code tabindex="0"><span>@transformation_function</span><span>()</span>
<span>def</span> <span>swap_aliases</span><span>(</span><span>x</span><span>):</span>
    <span>"""Swap ML keywords with their aliases."""</span>
    <span># Find all matches</span>
    <span>matches</span> <span>=</span> <span>[]</span>
    <span>for</span> <span>i</span><span>,</span> <span>tag</span> <span>in</span> <span>enumerate</span><span>(</span><span>flattened_aliases</span><span>):</span>
        <span>match</span> <span>=</span> <span>find_word</span><span>(</span><span>tag</span><span>,</span> <span>x</span><span>.</span><span>text</span><span>)</span>
        <span>if</span> <span>match</span><span>:</span>
            <span>matches</span><span>.</span><span>append</span><span>(</span><span>match</span><span>)</span>
    <span># Swap a random match with a random alias</span>
    <span>if</span> <span>len</span><span>(</span><span>matches</span><span>):</span>
        <span>match</span> <span>=</span> <span>random</span><span>.</span><span>choice</span><span>(</span><span>matches</span><span>)</span>
        <span>tag</span> <span>=</span> <span>x</span><span>.</span><span>text</span><span>[</span><span>match</span><span>.</span><span>start</span><span>():</span><span>match</span><span>.</span><span>end</span><span>()]</span>
        <span>x</span><span>.</span><span>text</span> <span>=</span> <span>f</span><span>"</span><span>{</span><span>x</span><span>.</span><span>text</span><span>[:</span><span>match</span><span>.</span><span>start</span><span>()]</span><span>}{</span><span>random</span><span>.</span><span>choice</span><span>(</span><span>flattened_aliases</span><span>[</span><span>tag</span><span>])</span><span>}{</span><span>x</span><span>.</span><span>text</span><span>[</span><span>match</span><span>.</span><span>end</span><span>():]</span><span>}</span><span>"</span>
    <span>return</span> <span>x</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_15"><span></span><code tabindex="0"><span># Swap</span>
<span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>3</span><span>):</span>
    <span>sample_df</span> <span>=</span> <span>pd</span><span>.</span><span>DataFrame</span><span>([{</span><span>"text"</span><span>:</span> <span>"a survey of reinforcement learning for nlp tasks."</span><span>}])</span>
    <span>sample_df</span><span>.</span><span>text</span> <span>=</span> <span>sample_df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>preprocess</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>)</span>
    <span>print</span> <span>(</span><span>swap_aliases</span><span>(</span><span>sample_df</span><span>.</span><span>iloc</span><span>[</span><span>0</span><span>])</span><span>.</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_16"><span></span><code tabindex="0"><span># Undesired behavior (needs contextual insight)</span>
<span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>3</span><span>):</span>
    <span>sample_df</span> <span>=</span> <span>pd</span><span>.</span><span>DataFrame</span><span>([{</span><span>"text"</span><span>:</span> <span>"Autogenerate your CV to apply for jobs using NLP."</span><span>}])</span>
    <span>sample_df</span><span>.</span><span>text</span> <span>=</span> <span>sample_df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>preprocess</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>)</span>
    <span>print</span> <span>(</span><span>swap_aliases</span><span>(</span><span>sample_df</span><span>.</span><span>iloc</span><span>[</span><span>0</span><span>])</span><span>.</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
使用 nlp 自动生成视觉应用作业
使用自然语言处理自动生成 cv 应用作业
使用 nlproc 自动生成 cv 应用作业

```

现在我们将定义一个[增强策略](https://snorkel.readthedocs.io/en/latest/packages/augmentation.html)来应用具有特定规则的转换函数（生成多少样本，是否保留原始数据点等）

<table><tbody><tr><td></td><td><div><pre id="__code_17"><span></span><code><span>from</span> <span>snorkel.augmentation</span> <span>import</span> <span>ApplyOnePolicy</span><span>,</span> <span>PandasTFApplier</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre id="__code_18"><span></span><code><span># Transformation function (TF) policy</span>
<span>policy</span> <span>=</span> <span>ApplyOnePolicy</span><span>(</span><span>n_per_original</span><span>=</span><span>5</span><span>,</span> <span>keep_original</span><span>=</span><span>True</span><span>)</span>
<span>tf_applier</span> <span>=</span> <span>PandasTFApplier</span><span>([</span><span>swap_aliases</span><span>],</span> <span>policy</span><span>)</span>
<span>train_df_augmented</span> <span>=</span> <span>tf_applier</span><span>.</span><span>apply</span><span>(</span><span>train_df</span><span>)</span>
<span>train_df_augmented</span><span>.</span><span>drop_duplicates</span><span>(</span><span>subset</span><span>=</span><span>[</span><span>"text"</span><span>],</span> <span>inplace</span><span>=</span><span>True</span><span>)</span>
<span>train_df_augmented</span><span>.</span><span>head</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

|  | 文本 | 标签 |
| --- | --- | --- |
| 0 | 拉普拉斯金字塔重建细化... | 计算机视觉 |
| 1 | 提取股票情绪新闻头条项目... | 自然语言处理 |
| 2 | 大坏 nlp 数据库集合 400 个 nlp 数据集... | 自然语言处理 |
| 2 | 大坏自然语言处理数据库... | 自然语言处理 |
| 2 | 大坏 nlproc 数据库收集 400 nlp 数据... | 自然语言处理 |

<table><tbody><tr><td></td><td><div><pre id="__code_19"><span></span><code><span>len</span><span>(</span><span>train_df</span><span>),</span> <span>len</span><span>(</span><span>train_df_augmented</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
(668, 913)

```

现在，我们将跳过数据增强，因为它非常变幻无常，并且从经验上看它并没有太大的提高性能。但是我们可以看到，一旦我们可以控制要扩充的词汇类型以及要扩充的内容，这将如何非常有效。

警告

无论我们使用什么方法，重要的是要验证我们不仅仅是为了增强而增强。我们可以通过执行任何现有的[数据验证测试](https://madewithml.com/courses/mlops/testing#data)，甚至创建特定的测试来应用于增强数据来做到这一点。

___

要引用此内容，请使用：
-   -   随着时间的推移，将标签工作重点放在边缘案例的长尾上

## 标记数据

就本课程而言，我们的数据已经被标记，因此我们将执行基本版本的 ELT（提取、加载、转换）来构建标记数据集。

> 在我们的[数据堆栈](https://madewithml.com/courses/mlops/labeling/#active-learning../data-stack/)和[编排](https://madewithml.com/courses/mlops/labeling/#active-learning../orchestration/)课程中，我们将构建一个现代数据堆栈并通过 DataOps 工作流以编程方式交付高质量数据。

-   [projects.csv](https://github.com/GokuMohandas/Made-With-ML/tree/main/datasets/projects.csv)：带有 id、创建时间、标题和描述的项目。
-   [tags.csv](https://github.com/GokuMohandas/Made-With-ML/tree/main/datasets/tags.csv)：项目的标签（标签类别），按 id。

回想一下，我们的[目标](https://madewithml.com/courses/mlops/design#objectives)是对传入的内容进行分类，以便社区可以轻松发现它们。这些数据资产将作为我们第一个模型的训练数据。

## 图书馆

我们可以使用用户提供的标签作为我们的标签，但是如果用户添加了错误的标签或忘记添加相关标签怎么办。为了消除对用户提供黄金标准标签的依赖，我们可以利用标签工具和平台。这些工具允许对数据集进行快速和有组织的标记，以确保其质量。而不是从头开始并要求我们的贴标者提供给定项目的所有相关标签，我们可以提供作者的原始标签并要求贴标者根据需要添加/删除。特定的标签工具可能需要定制或利用生态系统中的某些东西。

> 随着我们平台的增长，我们的数据集和标签需求也将增长，因此必须使用支持我们将依赖的工作流程的适当工具。

### 一般的

-   [Labelbox](https://labelbox.com/)：用于人工智能应用程序的高质量训练和验证数据的数据平台。
-   [Scale AI](https://scale.com/)：提供高质量训练数据的人工智能数据平台。
-   [Label Studio](https://github.com/heartexlabs/label-studio)：具有标准化输出格式的多类型数据标注和注释工具。
-   [通用数据工具](https://github.com/UniversalDataTool/universal-data-tool)：在简单的 Web 界面或桌面应用程序中协作和标记任何类型的数据、图像、文本或文档。
-   [Prodigy](https://github.com/explosion/prodigy-recipes)：Prodigy 的食谱，我们完全可编写脚本的注释工具。
-   [Superintendent](https://github.com/janfreyberg/superintendent)：一个基于 ipywidget 的交互式标签工具，用于为您的数据启用主动学习。

### 自然语言处理

-   [Doccano](https://github.com/doccano/doccano)：用于文本分类、序列标记和序列到序列任务的开源文本注释工具。
-   [BRAT](https://github.com/nlplab/brat)：一个快速的注释工具，可以满足您所有的文本注释需求。

### 计算机视觉

-   [LabelImg](https://github.com/tzutalin/labelImg)：一个图形图像注释工具和图像中的标签对象边界框。
-   [CVAT](https://github.com/openvinotoolkit/cvat)：一种免费的在线交互式视频和图像注释工具，用于计算机视觉。
-   [VoTT](https://github.com/Microsoft/VoTT)：一个用于从图像和视频构建端到端对象检测模型的电子应用程序。
-   [makeense.ai](https://github.com/SkalskiP/make-sense)：一个免费使用的用于标记照片的在线工具。
-   [remo](https://github.com/rediscovery-io/remo-python)：计算机视觉中用于注释和图像管理的应用程序。
-   [Labelai](https://github.com/aralroca/labelai)：一种用于标记图像的在线工具，可用于训练 AI 模型。

### 声音的

-   [Audino](https://github.com/midas-research/audino)：用于语音活动检测（VAD）、分类、说话人识别、自动语音识别、情感识别任务等的开源音频注释工具。
-   [audio-annotator](https://github.com/CrowdCurio/audio-annotator)：用于注释和标记音频文件的 JavaScript 接口。
-   [EchoML](https://github.com/ritazh/EchoML)：一个网络应用程序，用于播放、可视化和注释您的音频文件以进行机器学习。

### 各种各样的

-   [MedCAT](https://github.com/CogStack/MedCAT)：一种医学概念注释工具，可以从电子健康记录 (EHR) 中提取信息，并将其链接到 SNOMED-CT 和 UMLS 等生物医学本体。

通用标签解决方案

我们应该使用什么标准来评估使用什么标签平台？

显示答案

选择一个通用平台非常重要，该平台具有适用于您的数据模式的所有主要标签功能，并且能够轻松自定义体验。

-   连接到我们的数据源（DB、QA 等）有多容易？
-   进行更改（新功能、标签范例）有多容易？
-   我们的数据处理的安全性如何（本地、信任等）

然而，作为一种行业趋势，这种泛化与特异性之间的平衡很难达到。如此多的团队付出了前期努力来创建定制的标签平台或使用行业特定的利基标签工具。

## 主动学习

即使拥有强大的标签工具和成熟的工作流程，也很容易看出标签的复杂程度和成本。因此，许多团队采用主动学习来迭代地标记数据集并评估模型。

1.  标记一个小的初始数据集以训练模型。
2.  要求经过训练的模型对一些未标记的数据进行预测。
3.  根据以下内容确定要从未标记数据中标记哪些新数据点：
    -   预测类概率的熵
    -   具有最低预测、[校准](https://arxiv.org/abs/1706.04599)和置信度的样本（不确定性抽样）
    -   来自一组训练有素的模型的预测差异
4.  重复直到达到所需的性能。

> 这比标记整个数据集更具成本效益和速度。

![主动学习](https://madewithml.com/static/images/mlops/labeling/active_learning.png)

[主动学习文献调查](http://burrsettles.com/pub/settles.activelearning.pdf)

### 图书馆

-   [modAL](https://github.com/modAL-python/modAL)：Python 的模块化主动学习框架。
-   [libact](https://github.com/ntucllab/libact)：Python 中基于池的主动学习。
-   [ALiPy](https://github.com/NUAA-AL/ALiPy)：主动学习python工具箱，方便用户对主动学习方法的性能进行评估、比较和分析。

## 监管薄弱

如果我们有需要标记的样本，或者我们只是想验证现有标签，我们可以使用弱监督来生成标签，而不是手动标记所有标签。[我们可以通过标记函数](https://www.snorkel.org/use-cases/01-spam-tutorial)利用弱监督来标记我们现有的和新的数据，在那里我们可以创建基于关键字、模式表达式、知识库等的结构。我们可以随着时间的推移添加到标记函数中，甚至可以减轻不同数据之间的冲突标注功能。[在评估课程](https://madewithml.com/courses/mlops/labeling/#active-learning../evaluation/#slices)中，我们将使用这些标记函数来创建和评估我们的数据切片。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_7"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_7 > code"></button><code><span class="kn">from</span> <span class="nn">snorkel.labeling</span> <span class="kn">import</span> <span class="n">labeling_function</span><font></font>
<font></font>
<span class="nd">@labeling_function</span><span class="p">()</span>
<span class="k">def</span> <span class="nf">contains_tensorflow</span><span class="p">(</span><span class="n">text</span><span class="p">):</span>
    <span class="n">condition</span> <span class="o">=</span> <span class="nb">any</span><span class="p">(</span><span class="n">tag</span> <span class="ow">in</span> <span class="n">text</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span> <span class="k">for</span> <span class="n">tag</span> <span class="ow">in</span> <span class="p">(</span><span class="s2">"tensorflow"</span><span class="p">,</span> <span class="s2">"tf"</span><span class="p">))</span>
    <span class="k">return</span> <span class="s2">"tensorflow"</span> <span class="k">if</span> <span class="n">condition</span> <span class="k">else</span> <span class="kc">None</span>
</code></pre></div></td></tr></tbody></table>

> 验证标签（在建模之前）的一种简单方法是使用辅助数据集中的别名来为不同的类创建标签函数。然后我们可以寻找假阳性和假阴性来识别可能被错误标记的样本。实际上，我们将在[仪表板课程](https://madewithml.com/courses/mlops/labeling/#active-learning../dashboard/#inspection)中实现类似的检查方法，但使用经过训练的模型作为启发式方法。

## 迭代

标签不仅仅是一次性事件或我们重复相同的事情。随着新数据的可用，我们将希望战略性地标记适当的样本并改进我们缺乏[质量的数据](https://madewithml.com/courses/mlops/labeling/#active-learning../../foundations/data-quality/)[切片](https://madewithml.com/courses/mlops/labeling/#active-learning../testing/#evaluation)。标记新数据后，我们可以触发工作流以启动（重新）培训过程以部署我们系统的新版本。
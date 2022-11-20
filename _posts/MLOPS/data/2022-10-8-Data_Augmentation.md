---
layout:     post
title:      数据增强 
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Data Augmentation

---


在训练数据拆分上评估数据增强，以增加高质量训练样本的数量。

## 直觉

经常希望通过数据增强来增加训练数据的大小和多样性。它涉及使用现有样本来生成合成但现实的示例。

1.  **拆分数据集**。希望首先拆分数据集，因为如果允许将生成的样本放置在不同的数据拆分中，许多增强技术将导致某种形式的数据泄漏。
    
    > 例如，一些扩充涉及为句子中的某些关键标记生成同义词。如果允许从同一原始句子生成的句子进入不同的拆分，可能会在不同拆分中泄漏具有几乎相同嵌入表示的样本。
    
2.  **增加训练拆分**。只想在训练集上应用数据增强，因为验证和测试拆分应该用于提供对实际数据点的准确估计。
    
3.  **检查和验证**. 如果增强的数据样本不是模型在生产中可能遇到的可能输入，那么仅仅为了增加训练样本大小而增加是没有用的。
    

数据增强的确切方法很大程度上取决于数据类型和应用程序。以下是可以增强不同模式的数据的几种方法：

![数据增强类型](https://madewithml.com/static/images/mlops/augmentation/snorkel.png)

-   **一般**：归一化、平滑、随机噪声、合成过采样 ( [SMOTE](https://arxiv.org/abs/1106.1813) ) 等。
-   **Natural language processing (NLP)**: substitutions (synonyms, tfidf, embeddings, masked models), random noise, spelling errors, etc.
-   **Computer vision (CV)**: crop, flip, rotate, pad, saturate, increase brightness, etc.

Warning

While the transformations on some data modalities, such as images, are easy to inspect and validate, others may introduce silent errors. For example, shifting the order of tokens in text can significantly alter the meaning (“this is really cool” → “is this really cool”). Therefore, it’s important to measure the noise that our augmentation policies will introduce and do have granular control over the transformations that take place.

## Libraries

Depending on the feature types and tasks, there are many data augmentation libraries which allow us to extend our training data.

### Natural language processing (NLP)

-   [NLPAug](https://github.com/makcedward/nlpaug): data augmentation for NLP.
-   [TextAttack](https://github.com/QData/TextAttack): a framework for adversarial attacks, data augmentation, and model training in NLP.
-   [TextAugment](https://github.com/dsfsi/textaugment): text augmentation library.

### Computer vision (CV)

-   [Imgaug](https://github.com/aleju/imgaug): image augmentation for machine learning experiments.
-   [Albumentations](https://github.com/albumentations-team/albumentations): fast image augmentation library.
-   [Augmentor](https://github.com/mdbloice/Augmentor): image augmentation library in Python for machine learning.
-   [Kornia.augmentation](https://github.com/kornia/kornia): a module to perform data augmentation in the GPU.
-   [SOLT](https://github.com/MIPT-Oulu/solt): data augmentation library for Deep Learning, which supports images, segmentation masks, labels and key points.

### Other

-   [Snorkel](https://github.com/snorkel-team/snorkel): system for generating training data with weak supervision.
-   [DeltaPy⁠⁠](https://github.com/firmai/deltapy): tabular data augmentation and feature engineering.
-   [Audiomentations](https://github.com/iver56/audiomentations): a Python library for audio data augmentation.
-   [Tsaug](https://github.com/arundo/tsaug): a Python package for time series augmentation.

## Application

Let's use the [nlpaug](https://github.com/makcedward/nlpaug) library to augment our dataset and assess the quality of the generated samples.

```
pip install nlpaug==1.1.0 transformers==3.0.2 -q
pip install snorkel==0.9.8 -q

```

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>import</span> <span>nlpaug.augmenter.word</span> <span>as</span> <span>naw</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Load tokenizers and transformers</span>
<span>substitution</span> <span>=</span> <span>naw</span><span>.</span><span>ContextualWordEmbsAug</span><span>(</span><span>model_path</span><span>=</span><span>"distilbert-base-uncased"</span><span>,</span> <span>action</span><span>=</span><span>"substitute"</span><span>)</span>
<span>insertion</span> <span>=</span> <span>naw</span><span>.</span><span>ContextualWordEmbsAug</span><span>(</span><span>model_path</span><span>=</span><span>"distilbert-base-uncased"</span><span>,</span> <span>action</span><span>=</span><span>"insert"</span><span>)</span>
<span>text</span> <span>=</span> <span>"Conditional image generation using Variational Autoencoders and GANs."</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Substitutions</span>
<span>substitution</span><span>.</span><span>augment</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
hierarchical risk mapping using variational signals and gans.

```

Substitution doesn't seem like a great idea for us because there are certain keywords that provide strong signal for our tags so we don't want to alter those. Also, note that these augmentations are NOT deterministic and will vary every time we run them. Let's try insertion...

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Insertions</span>
<span>insertion</span><span>.</span><span>augment</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
automated conditional inverse image generation algorithms using multiple variational autoencoders and gans.

```

A little better but still quite fragile and now it can potentially insert key words that can influence false positive tags to appear. Maybe instead of substituting or inserting new tokens, let's try simply swapping machine learning related keywords with their aliases. We'll use Snorkel's [transformation functions](https://www.snorkel.org/use-cases/02-spam-data-augmentation-tutorial) to easily achieve this.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Replace dashes from tags &amp; aliases</span>
<span>def</span> <span>replace_dash</span><span>(</span><span>x</span><span>):</span>
    <span>return</span> <span>x</span><span>.</span><span>replace</span><span>(</span><span>"-"</span><span>,</span> <span>" "</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Aliases</span>
<span>aliases_by_tag</span> <span>=</span> <span>{</span>
    <span>"computer-vision"</span><span>:</span> <span>[</span><span>"cv"</span><span>,</span> <span>"vision"</span><span>],</span>
    <span>"mlops"</span><span>:</span> <span>[</span><span>"production"</span><span>],</span>
    <span>"natural-language-processing"</span><span>:</span> <span>[</span><span>"nlp"</span><span>,</span> <span>"nlproc"</span><span>]</span>
<span>}</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Flatten dict</span>
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

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>print</span> <span>(</span><span>flattened_aliases</span><span>[</span><span>"natural language processing"</span><span>])</span>
<span>print</span> <span>(</span><span>flattened_aliases</span><span>[</span><span>"nlp"</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
['nlp', 'nlproc']
['nlproc', 'natural language processing']

```

> For now we'll use tags and aliases as they are in `aliases_by_tag` but we could account for plurality of tags using the [inflect](https://github.com/jaraco/inflect) package or apply stemming before replacing aliases, etc.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># We want to match with the whole word only</span>
<span>print</span> <span>(</span><span>"gan"</span> <span>in</span> <span>"This is a gan."</span><span>)</span>
<span>print</span> <span>(</span><span>"gan"</span> <span>in</span> <span>"This is gandalf."</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># \b matches spaces</span>
<span>def</span> <span>find_word</span><span>(</span><span>word</span><span>,</span> <span>text</span><span>):</span>
    <span>word</span> <span>=</span> <span>word</span><span>.</span><span>replace</span><span>(</span><span>"+"</span><span>,</span> <span>"\+"</span><span>)</span>
    <span>pattern</span> <span>=</span> <span>re</span><span>.</span><span>compile</span><span>(</span><span>fr</span><span>"\b(</span><span>{</span><span>word</span><span>}</span><span>)\b"</span><span>,</span> <span>flags</span><span>=</span><span>re</span><span>.</span><span>IGNORECASE</span><span>)</span>
    <span>return</span> <span>pattern</span><span>.</span><span>search</span><span>(</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Correct behavior (single instance)</span>
<span>print</span> <span>(</span><span>find_word</span><span>(</span><span>"gan"</span><span>,</span> <span>"This is a gan."</span><span>))</span>
<span>print</span> <span>(</span><span>find_word</span><span>(</span><span>"gan"</span><span>,</span> <span>"This is gandalf."</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
<re.Match object; span=(10, 13), match='gan'>
None

```

Now let's use snorkel's [`transformation_function`](https://snorkel.readthedocs.io/en/latest/packages/_autosummary/augmentation/snorkel.augmentation.transformation_function.html) to systematically apply this transformation to our data.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>snorkel.augmentation</span> <span>import</span> <span>transformation_function</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span></pre></div></td><td><div><pre><span></span><code><span>@transformation_function</span><span>()</span>
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

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Swap</span>
<span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>3</span><span>):</span>
    <span>sample_df</span> <span>=</span> <span>pd</span><span>.</span><span>DataFrame</span><span>([{</span><span>"text"</span><span>:</span> <span>"a survey of reinforcement learning for nlp tasks."</span><span>}])</span>
    <span>sample_df</span><span>.</span><span>text</span> <span>=</span> <span>sample_df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>preprocess</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>)</span>
    <span>print</span> <span>(</span><span>swap_aliases</span><span>(</span><span>sample_df</span><span>.</span><span>iloc</span><span>[</span><span>0</span><span>])</span><span>.</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Undesired behavior (needs contextual insight)</span>
<span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>3</span><span>):</span>
    <span>sample_df</span> <span>=</span> <span>pd</span><span>.</span><span>DataFrame</span><span>([{</span><span>"text"</span><span>:</span> <span>"Autogenerate your CV to apply for jobs using NLP."</span><span>}])</span>
    <span>sample_df</span><span>.</span><span>text</span> <span>=</span> <span>sample_df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>preprocess</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>)</span>
    <span>print</span> <span>(</span><span>swap_aliases</span><span>(</span><span>sample_df</span><span>.</span><span>iloc</span><span>[</span><span>0</span><span>])</span><span>.</span><span>text</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
autogenerate vision apply jobs using nlp
autogenerate cv apply jobs using natural language processing
autogenerate cv apply jobs using nlproc

```

Now we'll define a [augmentation policy](https://snorkel.readthedocs.io/en/latest/packages/augmentation.html) to apply our transformation functions with certain rules (how many samples to generate, whether to keep the original data point, etc.)

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>snorkel.augmentation</span> <span>import</span> <span>ApplyOnePolicy</span><span>,</span> <span>PandasTFApplier</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Transformation function (TF) policy</span>
<span>policy</span> <span>=</span> <span>ApplyOnePolicy</span><span>(</span><span>n_per_original</span><span>=</span><span>5</span><span>,</span> <span>keep_original</span><span>=</span><span>True</span><span>)</span>
<span>tf_applier</span> <span>=</span> <span>PandasTFApplier</span><span>([</span><span>swap_aliases</span><span>],</span> <span>policy</span><span>)</span>
<span>train_df_augmented</span> <span>=</span> <span>tf_applier</span><span>.</span><span>apply</span><span>(</span><span>train_df</span><span>)</span>
<span>train_df_augmented</span><span>.</span><span>drop_duplicates</span><span>(</span><span>subset</span><span>=</span><span>[</span><span>"text"</span><span>],</span> <span>inplace</span><span>=</span><span>True</span><span>)</span>
<span>train_df_augmented</span><span>.</span><span>head</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

|  | text | tags |
| --- | --- | --- |
| 0 | laplacian pyramid reconstruction refinement se... | computer-vision |
| 1 | extract stock sentiment news headlines project... | natural-language-processing |
| 2 | big bad nlp database collection 400 nlp datasets... | natural-language-processing |
| 2 | big bad natural language processing database c... | natural-language-processing |
| 2 | big bad nlproc database collection 400 nlp dat... | natural-language-processing |

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>len</span><span>(</span><span>train_df</span><span>),</span> <span>len</span><span>(</span><span>train_df_augmented</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
(668, 913)

```

现在，将跳过数据增强，因为它非常变幻无常，并且从经验上看它并没有太大的提高性能。但是可以看到，一旦可以控制要扩充的词汇类型以及要扩充的内容，这将如何非常有效。

警告

无论使用什么方法，重要的是要验证不仅仅是为了增强而增强。可以通过执行任何现有的[数据验证测试](https://madewithml.com/courses/mlops/testing#data)，甚至创建特定的测试来应用于增强数据来做到这一点。

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Augmentation - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>

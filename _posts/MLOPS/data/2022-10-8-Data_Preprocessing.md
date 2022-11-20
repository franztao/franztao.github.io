---
layout:     post
title:      数据预处理
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Data Preprocessing

---



# 数据预处理

通过准备和转换对数据集进行预处理，以用于训练。



## Intuition

数据预处理可以分为两类过程：*准备*和*转换*。将探索常见的预处理技术，然后针对特定应用逐步完成相关过程。

> 警告
> 
> 某些预处理步骤`global`（不依赖于数据集，例如小写文本、删除停用词等）和其他步骤`local`（结构仅从训练拆分中学习，例如词汇、标准化等）。对于本地的、依赖于数据集的预处理步骤，要确保在预处理之前先[拆分](https://madewithml.com/courses/mlops/splitting/)数据以避免数据泄漏。

## 准备中

准备数据涉及组织和清理数据。

### 加入

与现有数据表执行 SQL 连接，将您需要的所有相关数据组织到一个视图中。这使得使用数据集变得更加容易。

```
SELECT * FROM A
INNER JOIN B on A.id == B.id

```

> 警告
> 
> 需要小心执行时间点有效连接以避免数据泄漏。例如，如果表 B 可能具有表 A 中的对象的特征，而这些特征在当时需要进行推理时不可用。

### 缺失值

首先，必须确定具有缺失值的行，一旦确定，有几种方法可以处理它们。

### 异常值（异常）

- 关于什么是“正常”预期值的工艺假设
  
  ```
  # Ex. Feature value must be within 2 standard deviations
  df[np.abs(df.A - df.A.mean()) <= (2 * df.A.std())]
  
  ```

- 注意不要删除重要的异常值（例如欺诈）

- 当应用转换（例如幂律）时，值可能不是异常值

- 异常可以是全局的（点）、上下文的（有条件的）或集体的（个体点不异常，集体是异常值）

### 特征工程

特征工程涉及以独特的方式组合特征以提取信号。

```
# Input
df.C = df.A + df.B

```



> tips
> 
> 特征工程可以与领域专家合作完成，领域专家可以指导设计和使用哪些特征。

### cleaning

清理数据涉及应用约束，使模型更容易从数据中提取信号。

- 使用领域专业知识和 EDA

- 通过过滤器应用约束

- 确保数据类型一致性

- 删除具有特定列值或空列值的数据点

- 图像（裁剪、调整大小、剪辑等）
  
  ```
  # Resize
  import cv2
  dims = (height, width)
  resized_img = cv2.resize(src=img, dsize=dims, interpolation=cv2.INTER_LINEAR)
  
  ```
  
  

- 文本（下部、词干、词形还原、正则表达式等）
  
  ```
  # Lower case the text
  text = text.lower()
  
  ```
  
  

## 转换

转换数据涉及特征编码和工程。

### 缩放

- 输入规模影响过程的模型需要

- 从训练拆分中学习构造并应用于其他拆分（本地）

- 不要盲目地缩放特征（例如分类特征）

- [标准化](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler)：将值重新调整为均值为 0，标准为 1
  
  ```
  # Standardization
  import numpy as np
  x = np.random.random(4) # values between 0 and 1
  print ("x:\n", x)
  print (f"mean: {np.mean(x):.2f}, std: {np.std(x):.2f}")
  x_standardized = (x - np.mean(x)) / np.std(x)
  print ("x_standardized:\n", x_standardized)
  print (f"mean: {np.mean(x_standardized):.2f}, std: {np.std(x_standardized):.2f}")
  
  ```
  
  x: [0.36769939 0.82302265 0.9891467  0.56200803]
  mean: 0.69, std: 0.24
  x_standardized: [-1.33285946  0.57695671  1.27375049 -0.51784775]
  mean: 0.00, std: 1.00

- [min-max](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.minmax_scale.html#sklearn.preprocessing.minmax_scale)：在最小值和最大值之间重新调整值
  
  ```
  # Min-max
  import numpy as np
  x = np.random.random(4) # values between 0 and 1
  print ("x:", x)
  print (f"min: {x.min():.2f}, max: {x.max():.2f}")
  x_scaled = (x - x.min()) / (x.max() - x.min())
  print ("x_scaled:", x_scaled)
  print (f"min: {x_scaled.min():.2f}, max: {x_scaled.max():.2f}")
  
  ```
  
  
  
  x: [0.20195674 0.99108855 0.73005081 0.02540603]
  min: 0.03, max: 0.99
  x_scaled: [0.18282479 1.         0.72968575 0.        ]
  min: 0.00, max: 1.00

- [分箱](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.KBinsDiscretizer.html)：使用分箱将连续特征转换为分类特征
  
  ```
  # Binning
  import numpy as np
  x = np.random.random(4) # values between 0 and 1
  print ("x:", x)
  bins = np.linspace(0, 1, 5) # bins between 0 and 1
  print ("bins:", bins)
  binned = np.digitize(x, bins)
  print ("binned:", binned)
  
  ```
  
  x: [0.54906364 0.1051404  0.2737904  0.2926313 ]
  bins: [0.   0.25 0.5  0.75 1.  ]
  binned: [3 1 2 2]

- 还有[更多](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing)！

### 编码

- 允许有效地表示数据（保持信号）和有效地（学习模式，例如 one-hot 与嵌入）

- [label](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html#sklearn.preprocessing.LabelEncoder)：分类值的唯一索引
  
  ```
  # Label encoding
  label_encoder.class_to_index = {
  "attention": 0,
  "autoencoders": 1,
  "convolutional-neural-networks": 2,
  "data-augmentation": 3,
  ... }
  label_encoder.transform(["attention", "data-augmentation"])
  
  ```
  
  
  
  array([2, 2, 1])

- [one-hot](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html#sklearn.preprocessing.OneHotEncoder)：表示为二进制向量
  
  ```
  # One-hot encoding
  one_hot_encoder.transform(["attention", "data-augmentation"])
  
  ```
  
  
  
  array([1, 0, 0, 1, 0, ..., 0])

- [嵌入](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)：能够表示上下文的密集表示
  
  ```
  # Embeddings
  self.embeddings = nn.Embedding(
      embedding_dim=embedding_dim, num_embeddings=vocab_size)
  x_in = self.embeddings(x_in)
  print (x_in.shape)
  
  ```
  
  
  
  (len(X), embedding_dim)

- 还有[更多](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing)！

### Extraction

- 从现有特征中提取信号

- 结合现有功能

- [迁移学习](https://en.wikipedia.org/wiki/Transfer_learning)：使用预训练模型作为特征提取器并对其结果进行微调

- [自动](https://en.wikipedia.org/wiki/Autoencoder)编码器：学习编码压缩知识表示的输入

- [主成分分析（PCA）](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html#sklearn.decomposition.PCA)：在较低维空间中对项目数据进行线性降维。
  
  ```
  # PCA
  import numpy as np
  from sklearn.decomposition import PCA
  X = np.array([[-1, -1, 3], [-2, -1, 2], [-3, -2, 1]])
  pca = PCA(n_components=2)
  pca.fit(X)
  print (pca.transform(X))
  print (pca.explained_variance_ratio_)
  print (pca.singular_values_)
  
  ```
  
  
  
  [[-1.44245791 -0.1744313]
   [-0.1148688 0.31291575]
   [ 1.55732672 -0.13848446]]
  [0.96838847 0.03161153]
  [2.12582835 0.38408396]

- [counts (ngram)](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)：文本的稀疏表示作为标记计数矩阵——如果特征值有很多有意义的、可分离的信号，则很有用。
  
  ```
  # Counts (ngram)
  from sklearn.feature_extraction.text import CountVectorizer
  y = [
      "acetyl acetone",
      "acetyl chloride",
      "chloride hydroxide",
  ]
  vectorizer = CountVectorizer()
  y = vectorizer.fit_transform(y)
  print (vectorizer.get_feature_names())
  print (y.toarray())
  # 💡 Repeat above with char-level ngram vectorizer
  # vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3)) # uni, bi and trigrams
  
  ```
  
  ['acetone', 'acetyl', 'chloride', 'hydroxide']
  [[1 1 0 0]
   [0 1 1 0]
   [0 0 1 1]]

- [similarity](https://github.com/dirty-cat/dirty_cat)：类似于计数向量化，但基于标记的相似性

- 还有[更多](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_extraction)！

> 随着时间的推移，通常会检索实体（用户、项目等）的特征值，并在不同项目中重用相同的特征。为确保检索到正确的特征值并避免重复工作，可以使用[特征存储](https://madewithml.com/courses/mlops/feature-store/)。

>  维度的诅咒
> 
> 如果一个特征有很多唯一值但每个唯一值都有足够的数据点（例如 URL 作为特征），该怎么办？
> 
> 显示答案
> 
> 可以使用[散列](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html)或使用它的属性而不是确切的实体本身来对数据进行编码。例如，通过用户的位置和收藏夹来表示用户而不是使用他们的用户 ID，或者使用其域而不是确切的 url 来表示网页。这种方法有效地减少了独特特征值的总数并增加了每个特征值的数据点数量。



## 应用

对于应用程序，将实施一些与数据集相关的预处理步骤。

### 特征工程

可以结合现有的输入特征来创建新的有意义的信号（帮助模型学习）。但是，如果不对不同的组合进行经验性试验，通常没有简单的方法可以知道某些特征组合是否有帮助。在这里，可以将项目的标题和描述分别用作特征，但会将它们组合起来创建一个输入特征。

```
# Input
df["text"] = df.title + " " + df.description

```



### clean

由于正在处理文本数据，因此可以应用一些常见的文本预处理步骤：

`!pip install nltk==3.7 -q`

```
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

```

```
nltk.download("stopwords")
STOPWORDS = stopwords.words("english")
stemmer = PorterStemmer()

```



```
def clean_text(text, lower=True, stem=False, stopwords=STOPWORDS):
    """Clean raw text."""
    # Lower
    if lower:
        text = text.lower()

    # Remove stopwords
    if len(stopwords):
        pattern = re.compile(r'\b(' + r"|".join(stopwords) + r")\b\s*")
        text = pattern.sub('', text)

    # Spacing and filters
    text = re.sub(
        r"([!\"'#$%&()*\+,-./:;<=>?@\\\[\]^_`{|}~])", r" \1 ", text
    )  # add spacing between objects to be filtered
    text = re.sub("[^A-Za-z0-9]+", " ", text)  # remove non alphanumeric chars
    text = re.sub(" +", " ", text)  # remove multiple spaces
    text = text.strip()  # strip white space at the ends

    # Remove links
    text = re.sub(r"http\S+", "", text)

    # Stemming
    if stem:
        text = " ".join([stemmer.stem(word, to_lowercase=lower) for word in text.split(" ")])

    return text

```

```
# Apply to dataframe
original_df = df.copy()
df.text = df.text.apply(clean_text, lower=True, stem=False)
print (f"{original_df.text.values[0]}\n{df.text.values[0]}")

```

YOLO 和 RCNN 在真实世界视频上的比较将理论带入实验很酷。可以轻松地在 Colab 中训练模型，并在几分钟内找到结果。
比较 yolo rcnn 真实世界视频带来理论实验很酷很容易训练模型 colab 找到结果分钟

> 警告
> 
> 将希望在它们变得更频繁时引入频率较低的特征，或者以巧妙的方式对它们进行编码（例如分箱、提取一般属性、常见的 n-gram、使用其他特征值进行平均编码等），以便可以减轻特征值维度问题，直到能够收集更多数据。

### 更换标签

根据[EDA](https://madewithml.com/courses/mlops/exploratory-data-analysis/)的发现，将应用几个约束来标记数据：

- 如果数据点有目前不支持的标签，将用`other`
- 如果某个标签没有*足够的*样本，会将其替换为`other`

```
import json
# Accepted tags (external constraint)
ACCEPTED_TAGS = ["natural-language-processing", "computer-vision", "mlops", "graph-learning"]# Out of scope (OOS) tags
oos_tags = [item for item in df.tag.unique() if item not in ACCEPTED_TAGS]
oos_tags


```

```
# Samples with OOS tags
oos_indices = df[df.tag.isin(oos_tags)].index
df[df.tag.isin(oos_tags)].head()

```





|     | ID  | 创建于                 | 标题                      | 描述                   | 标签   |
| --- | --- | ------------------- | ----------------------- | -------------------- | ---- |
| 3个  | 15  | 2020-02-28 23:55:26 | 很棒的蒙特卡洛树搜索              | 蒙特卡洛树搜索论文的精选列表...... | 强化学习 |
| 37  | 121 | 2020-03-24 04:56:38 | TensorFlow2 中的深度强化学习    | deep-rl-tf2 是一个实现... | 强化学习 |
| 67  | 218 | 2020-04-06 11:29:57 | 使用 TensorFlow2 的分布式强化学习 | 🐳 各种分布式资源的实现...     | 强化学习 |
| 74  | 239 | 2020-04-06 18:39:48 | Prophet：大规模预测           | 为...生成高质量预测的工具       | 时间序列 |
| 95  | 277 | 2020-04-07 00:30:33 | 强化学习课程                  | 课程学习应用于强化学习...       | 强化学习 |

```
# Replace this tag with "other"
df.tag = df.tag.apply(lambda x: "other" if x in oos_tags else x)
df.iloc[oos_indices].head()

```

|     | ID  | 创建于                 | 标题                      | 描述                   | 标签  |
| --- | --- | ------------------- | ----------------------- | -------------------- | --- |
| 3个  | 15  | 2020-02-28 23:55:26 | 很棒的蒙特卡洛树搜索              | 蒙特卡洛树搜索论文的精选列表...... | 其他  |
| 37  | 121 | 2020-03-24 04:56:38 | TensorFlow2 中的深度强化学习    | deep-rl-tf2 是一个实现... | 其他  |
| 67  | 218 | 2020-04-06 11:29:57 | 使用 TensorFlow2 的分布式强化学习 | 🐳 各种分布式资源的实现...     | 其他  |
| 74  | 239 | 2020-04-06 18:39:48 | Prophet：大规模预测           | 为...生成高质量预测的工具       | 其他  |
| 95  | 277 | 2020-04-07 00:30:33 | 强化学习课程                  | 课程学习应用于强化学习...       | 其他  |

还将限制映射到仅高于特定频率阈值的标签。没有足够项目的标签将没有足够的样本来建模它们的关系。

```
# Minimum frequency required for a tag
min_freq = 75
tags = Counter(df.tag.values)

```

```
# Tags that just made / missed the cut
@widgets.interact(min_freq=(0, tags.most_common()[0][1]))
def separate_tags_by_freq(min_freq=min_freq):
    tags_above_freq = Counter(tag for tag in tags.elements()
                                    if tags[tag] >= min_freq)
    tags_below_freq = Counter(tag for tag in tags.elements()
                                    if tags[tag] < min_freq)
    print ("Most popular tags:\n", tags_above_freq.most_common(3))
    print ("\nTags that just made the cut:\n", tags_above_freq.most_common()[-3:])
    print ("\nTags that just missed the cut:\n", tags_below_freq.most_common(3))
)))

```

Most popular tags:
 [('natural-language-processing', 388), ('computer-vision', 356), ('other', 87)]
Tags that just made the cut:
 [('computer-vision', 356), ('other', 87), ('mlops', 79)]
Tags that just missed the cut:
 [('graph-learning', 45)]

```
def filter(tag, include=[]):
    """Determine if a given tag is to be included."""
    if tag not in include:
        tag = None
    return tag

```

```
# Filter tags that have fewer than <min_freq> occurrences
tags_above_freq = Counter(tag for tag in tags.elements()
                          if (tags[tag] >= min_freq))
df.tag = df.tag.apply(filter, include=list(tags_above_freq.keys()))

```

```
# Fill None with other
df.tag = df.tag.fillna("other")

```



### 编码

将对输出标签进行编码，将为每个标签分配一个唯一索引。

```
import numpy as np
import random

```

```
# Get data
X = df.text.to_numpy()
y = df.tag

```



将编写自己的基于 scikit-learn[实现](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)的 LabelEncoder 。能够为想要创建的对象编写干净的类是一项非常有价值的技能。

```
class LabelEncoder(object):
    """Encode labels into unique indices"""
    def __init__(self, class_to_index={}):
        self.class_to_index = class_to_index or {}  # mutable defaults ;)
        self.index_to_class = {v: k for k, v in self.class_to_index.items()}
        self.classes = list(self.class_to_index.keys())

    def __len__(self):
        return len(self.class_to_index)

    def __str__(self):
        return f"<LabelEncoder(num_classes={len(self)})>"

    def fit(self, y):
        classes = np.unique(y)
        for i, class_ in enumerate(classes):
            self.class_to_index[class_] = i
        self.index_to_class = {v: k for k, v in self.class_to_index.items()}
        self.classes = list(self.class_to_index.keys())
        return self

    def encode(self, y):
        encoded = np.zeros((len(y)), dtype=int)
        for i, item in enumerate(y):
            encoded[i] = self.class_to_index[item]
        return encoded

    def decode(self, y):
        classes = []
        for i, item in enumerate(y):
            classes.append(self.index_to_class[item])
        return classes

    def save(self, fp):
        with open(fp, "w") as fp:
            contents = {"class_to_index": self.class_to_index}
            json.dump(contents, fp, indent=4, sort_keys=False)

    @classmethod
    def load(cls, fp):
        with open(fp, "r") as fp:
            kwargs = json.load(fp=fp)
        return cls(**kwargs)

```



> 如果您不熟悉装饰器，请从[Python 课程](https://madewithml.com/courses/foundations/python/#methods)`@classmethod`中了解更多信息。[](https://madewithml.com/courses/foundations/python/#methods)

```
# Encode
label_encoder = LabelEncoder()
label_encoder.fit(y)
num_classes = len(label_encoder)

```

```
label_encoder.class_to_index

```

{'computer-vision': 0,
 'mlops': 1,
 'natural-language-processing': 2,
 'other': 3}

```
label_encoder.index_to_class

```

{0: 'computer-vision',
 1: 'mlops',
 2: 'natural-language-processing',
 3: 'other'}

```
# Encode
label_encoder.encode(["computer-vision", "mlops", "mlops"])

```

array([0, 1, 1])

```
# Decode
label_encoder.decode(np.array([0, 1, 1]))

```

['computer-vision', 'mlops', 'mlops']

```

```

要对输入文本特征进行的许多*转换都是特定于模型的。*例如，对于简单的基线，可以做`label encoding`→`tf-idf`而对于更复杂的架构，可以做`label encoding`→ `one-hot encoding`→ `embeddings`。因此，在实施[基线](https://madewithml.com/courses/mlops/baselines/)时，将在下一组课程中介绍这些内容。

> 在下一节中，将对预处理后的数据集执行探索性数据分析 (EDA)。但是，步骤的顺序可以颠倒，具体取决于问题的定义程度。如果不确定如何准备数据，可以使用 EDA 来弄清楚，反之亦然。

本文主体源自以下链接：
```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
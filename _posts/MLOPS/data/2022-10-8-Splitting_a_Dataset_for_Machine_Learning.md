---
layout:     post
title:      拆分数据集以进行机器学习
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Splitting a Dataset for Machine Learning
---

适当拆分数据集以进行训练、验证和测试。

## Intuition

为了确定模型的有效性，需要有一个公正的测量方法。为此，将数据集拆分为`training`、`validation`和`testing`数据拆分。

1. 使用训练拆分来训练模型。
   
   > 在这里，模型将可以访问输入和输出以优化其内部权重。

2. 在训练拆分的每个循环（epoch）之后，将使用验证拆分来确定模型性能。
   
   > 在这里，模型不会使用输出来优化其权重，而是使用性能来优化训练超参数，例如学习率等。

3. 训练停止（epoch(s)）后，将使用测试拆分对模型进行一次性评估。
   
   > 这是衡量模型在新的、看不见的数据上表现的最佳方法。请注意，当性能改进不显着或可能指定的任何其他停止标准时，_训练会停止。_

> 创建适当的数据拆分
> 
> 应该关注哪些标准来确保正确的数据拆分？
> 
> > 显示答案
> > 
> > - 数据集（和每个数据拆分）应该代表将遇到的数据
> > - 输出值在所有拆分中的相等分布
> > - 如果以防止输入差异的方式组织数据，则打乱您的数据
> > - 如果您的任务可能遭受数据泄漏（例如`time-series`） ，请避免随机洗牌

> 需要在拆分之前先[清理](https://madewithml.com/courses/mlops/preprocessing/)数据，至少对于拆分所依赖的特征。所以这个过程更像是：预处理（全局，清洗）→分裂→预处理（局部，转换）。

## Naive split

首先将数据集拆分为三个数据拆分，用于训练、验证和测试。

```
from sklearn.model_selection import train_test_split
```

```
# Split sizes
train_size = 0.7
val_size = 0.15
test_size = 0.15
```

对于多类任务（每个输入都有一个标签），希望确保每个数据拆分具有相似的类分布。[`stratify`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)可以通过添加关键字参数来指定如何对拆分进行分层来实现这一点。

```
# Split (train)
X_train, X_, y_train, y_ = train_test_split(
    X, y, train_size=train_size, stratify=y)
```

```
print (f"train: {len(X_train)} ({(len(X_train) / len(X)):.2f})\n"
       f"remaining: {len(X_)} ({(len(X_) / len(X)):.2f})")
```

train: 668 (0.70)
remaining: 287 (0.30)

```
# Split (test)
X_val, X_test, y_val, y_test = train_test_split(
    X_, y_, train_size=0.5, stratify=y_)
```

```
print(f"train: {len(X_train)} ({len(X_train)/len(X):.2f})\n"
      f"val: {len(X_val)} ({len(X_val)/len(X):.2f})\n"
      f"test: {len(X_test)} ({len(X_test)/len(X):.2f})")
```

```
train: 668 (0.70)
val: 143 (0.15)
test: 144 (0.15)
```

```
# Get counts for each class
counts = {}
counts["train_counts"] = {tag: label_encoder.decode(y_train).count(tag) for tag in label_encoder.classes}
counts["val_counts"] = {tag: label_encoder.decode(y_val).count(tag) for tag in label_encoder.classes}
counts["test_counts"] = {tag: label_encoder.decode(y_test).count(tag) for tag in label_encoder.classes}
```

```
# View distributions
pd.DataFrame({
    "train": counts["train_counts"],
    "val": counts["val_counts"],
    "test": counts["test_counts"]
}).T.fillna(0)
```

|       | computer-vision | mlops | natural-language-processing | other |
| ----- | --------------- | ----- | --------------------------- | ----- |
| train | 249             | 55    | 272                         | 92    |
| val   | 53              | 12    | 58                          | 20    |
| test  | 54              | 12    | 58                          | 20    |

很难比较这些，因为训练和测试比例不同。让看看平衡后的分布是什么样子。需要将测试比率乘以多少才能得到与训练比率相同的数量？

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-11-20-13-00-27-image.png)

```
# Adjust counts across splits
for k in counts["val_counts"].keys():
    counts["val_counts"][k] = int(counts["val_counts"][k] * \
        (train_size/val_size))
for k in counts["test_counts"].keys():
    counts["test_counts"][k] = int(counts["test_counts"][k] * \
        (train_size/test_size))
```

| computer-vision | mlops | natural-language-processing | other |
| --- | --- | --- | --- | --- |
| train | 249 | 55  | 272 | 92  |
| val | 247 | 56  | 270 | 93  |
| test | 252 | 56  | 270 | 93  |

可以通过计算每个拆分的类计数与平均值（理想拆分）的标准差来查看原始数据拆分中有多少偏差。

$\sigma = \sqrt{\frac{(x - \bar{x})^2}{N}}$

```
# Standard deviation
np.mean(np.std(dist_df.to_numpy(), axis=0))
```

```
0.9851056877051131
```

```
# Split DataFrames
train_df = pd.DataFrame({"text": X_train, "tag": label_encoder.decode(y_train)})
val_df = pd.DataFrame({"text": X_val, "tag": label_encoder.decode(y_val)})
test_df = pd.DataFrame({"text": X_test, "tag": label_encoder.decode(y_test)})
train_df.head()
```

> 多标签分类
> 
> 如果有一个多标签分类任务，那么将通过[skmultilearn库应用](http://scikit.ml/index.html)[迭代分层](http://lpis.csd.auth.gr/publications/sechidis-ecmlpkdd-2011.pdf)，该库本质上将每个输入分成子集（其中每个标签都被单独考虑），然后从最少的“正面”开始分配样本样本并处理具有最多标签的输入。
> 
> ```
> from skmultilearn.model_selection import IterativeStratification
> def iterative_train_test_split(X, y, train_size):
>     """Custom iterative train test split which
>     'maintains balanced representation with respect
>     to order-th label combinations.'
>     """
>     stratifier = IterativeStratification(
>         n_splits=2, order=1, sample_distribution_per_fold=[1.0-train_size, train_size, ])
>     train_indices, test_indices = next(stratifier.split(X, y))
>     X_train, y_train = X[train_indices], y[train_indices]
>     X_test, y_test = X[test_indices], y[test_indices]
>     return X_train, X_test, y_train, y_test
> ```

> [迭代分层](http://scikit.ml/_modules/skmultilearn/model_selection/iterative_stratification.html#IterativeStratification)本质上会产生分裂，同时“试图保持关于顺序标签组合的平衡表示”。习惯于`order=1`迭代拆分，这意味着关心在拆分中提供每个标签的代表性分布。但是也可以考虑[更高阶的](https://arxiv.org/abs/1704.08756)标签关系，可能关心标签组合的分布。

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
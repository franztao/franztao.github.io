---
layout:     post
title:      系列30 生成模型3-模型表示，推断和学习
subtitle:   2022年10月
date:       2020-05-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Model
---

# 模型表示，推断和学习

上一小节从监督学习或者非监督学习的角度介绍了生成模型，这小节将从模型，推断和学习表示的角度分别介绍生成模型。

## 模型表示

首先从模型表示角度介绍，我们可以用“形神兼备”四个字来描述。

### “形”

“形”包括以下几个方面，可以理解为生成模型的概率图表示形式：

- 1. Discrete vs Continuous，从点的角度出发，也就是说节点的变量是离散随机变量还是连续随机变量。

- 2. Directed Model vs Undirected Model，从有向图和无向图的角度进行分类，有向图是贝叶斯模型，无向图是马尔可夫模型，这是从边的角度进行分析。

- 3. Latent Variational Model vs Fully Observed Model，区分为所有变量可完全观测或者含有部分隐变量。

- 4. Shadow vs Deep，这个是根据网络的层数来确定的。

- 5. Sparse vs Dense，此分类标准根据节点之间连接的权重稠密或者稀疏而定的。比如，Boltzmann Machines之间权重的连接就比HMM之间要稠密的多，最稠密的当然是完全图了。

### “神”

这个从“神”的角度来分，有一点抽象，哈哈哈！主要从以下两个方面来理解。

- 6. Parameteric Model vs Non-Parameteric Model，此分类描述的是参数是确定的，还是一个分布，参数不确定，比如，高斯过程就是Non-Parameteric Model，每个时刻的参数都服从不同的高斯分布。

- 7. Implicit Model vs Explicit Model，Implicit Model中最典型的就是GAN。Explicit Model的特征是对$P(X)$建模，而Implicit Model不直接考虑对$P(X)$的建模，只需要可从目标分布中采样即可。比如，GAN通过从目标分布中采样，来建立一个虚拟的分布。

## 推断

推断就很简单了，基本就是从计算可行性分析，

- 8. Tractable vs Intractable。

## 学习

学习的主要可以分为：

- 9. Likelihood-based Model vs Likelihood-free Model，极大似然估计求解，是使log似然达到最大之后，用求得的参数来进行采样。而Likelihood-free方法中，学习采用的方法和Likelihood无关。

## 小结

我们从模型表示，推断和学习表示的角度分别介绍生成模型，可以得到以下9种分类。

1. Discrete vs Continuous

2. Directed Model vs Undirected Model

3. Latent Variational Model vs Fully Observed Model

4. Shadow vs Deep

5. Sparse vs Dense

6. Parameteric Model vs Non-Parameteric Model

7. Implicit Model vs Explicit Model

8. Tractable vs Intractable

9. Likelihood-based Model vs Likelihood-free Model

而我们主要关注的是比较新的模型，所以重点介绍的是，1中的Discrete；2中的两个模型，Directed Model和Undirected Model；3中的Latent Variational Model；4中的Shadow vs Deep，其中深度生成模型是后面的重点；5中的Dense；6中的Parameteric Model；7中的Implicit Model（GAN）和Explicit Model；8中Tractable和Intractable都有讲到；9中的Likelihood-based Model和Likelihood-free Model都有。



参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)


更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-44-06-image.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-43-17-image.png)


转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

---
layout:     post
title:      系列30 生成模型4-分类
subtitle:   2022年10月
date:       2020-05-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Model
---

# Maximum Likelihood

从Likelihood-based Model和Likelihood-free Model两个方面分，是目前比较流行的一种分法。

## Likelihood-based Model

这是显式的估计概率密度函数，也就是Explicit Model。根据其是否可计算大致可以分成两类，tractable和intractable。

其中，Fully observed的算法一定是tractable，这样的模型结构相对很简单，典型算法有Autoregression Model。而另一类则是change of variable（Flow-based model），这里做简要的说明。假如$P(X)$非常复杂，那么我们可以对一个简单的分布$P(Z)$建模，然后寻找一个$X \mapsto Z$的映射$X=g(Z)$。那么，可得$Z = g^{-1}(X)$。此模型的主要目的就是学习这个映射$g(Z)$，可以得到

$$
\begin{equation}
    P_X(X) = P_Z(g^{-1}(X))
\end{equation}
$$

参数计算为$\frac{\partial g^{-1}(X)}{\partial X}$。

而关于Approximate Inference，包括两种，1. MCMC，这是一种Energy Based Model，因为其是基于随机采样的。2. 为确定性的变分推断，典型的算法有VAE。

## Likelihood-free Model

这是不显示的概率密度函数，也就是不直接对概率密度函数建模。比如说直接从样本分布中采样的GAN，通过模拟一个分布来直接进行采样，不需要通过MCMC采样。样本直接生成分布。还有直接采样的，比如Mento Calro算法，GSN等。

## 小结

我觉得主要是从函数学习方法的角度，来进行分类，也就是是否计算似然函数。个人觉得Likelihood-free Model是目前很重要的研究，以我做的科研为例，我觉得从未知分布中采样来逼近目标分布非常重要，如果给目标分布确定的形式会造成算法的局限性，所有舍弃分布的具体，使用采样来逼近非常重要，现在比较流行的有分布式强化学习中的分位点回归法。

参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)


更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-44-06-image.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-43-17-image.png)


转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

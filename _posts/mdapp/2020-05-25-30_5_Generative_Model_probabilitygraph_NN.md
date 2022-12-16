---
layout:     post
title:      生成模型5-概率图vs神经网络
subtitle:   2022年10月
date:       2020-05-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Model
---

# 概率图 vs 神经网络

概率图模型和神经网络之间并不是一个非黑即白的区别，它们之间有区别也有联系，但是很多部分同学都搞不清他们之间的区别。

首先我认为他们的核心区别在于，- 概率图模型是$P(X)$的表示，神经网络即时一个函数逼近器，对于一个输入的$X$，得到输出的$Y$，中间的部分都是权重。所以，他们两压根不是一个东西，概率图模式是对$P(X)$来建模，典型的概率生成模型。

概率图模型中主要讨论的是Bayesian Network，Boltzmann Machines；神经网络是广义连接主义，确定NN有CNN，RNN。在本节中，仅比较Beyesian Network和NN。

## Bayesian vs NN

本小节将从表示，推断，学习和适合问题四个角度出发进行比较。

### 模型表示

Bayesian Network是从结构化，权值之间相对稀疏，而且通常层数比较浅，符合条件独立假设。**其中最重要的是Bayesian Network具有可解释性，建模的时候具有真实的物理意义。**

而NN的层数，往往会比较深，而且权值连接很稠密，没有具体的物理意义。有的小伙伴会说，NN也具有可解释性，比如神经网络类似为一个滤波器，其可以抽象出更多的高层信息。这个东西，其实只是我们一厢情愿的，这个意义并不是在建模的时候赋予的。而是我们发现了其好的效果之后，在这里强行解释，有点“马后炮”的味道。NN的可解释性，并不关键，或者说我们都不关心。

## 推断

Bayesian Network中包括精确推断和近似推断，有MCMC和变分等方法。还有极大似然估计等等。

而神经网络的推断方法就非常的简单了，输入输出即可，没有太多的研究意义。

## 学习

Bayesian Network中常见的解决方法有Log似然梯度，EM算法等。

NN中常用的方法是梯度下降，由于这个层数很多，节点很多的时候求导很不好求，于是引入了BP算法。其实BP算法是一种高效的求导方法，其实**BP算法 = 链式求导法则+动态规划**。动态规划什么意思，就是递归+缓存。

实际上，可以感觉到Bayesian Network和神经网络都不是一个level的东西。**概率图是一个模型层次的，是对数据样本的建模。而神经网络中被称之为计算图，完全就是来计算用的。**

## 适合的问题

Bayesian Network更适合解决High Level Reasoning的问题，适合于做原因推断。

而NN更适合解决Low Level Reasoning的问题，不适合做原因推断，只能由于解决弱推理问题。其更适合表示学习。

## 小结

本章的内容比较简单，基本就是从表示，推断，学习和适合问题四个角度出发进行比较概率图模型和神经网络模型。其实这两个东西都不是一个level的，主要区别是概率图模型是对样本数据的建模，而神经网络只是一个函数逼近器而已。

参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)


更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)


转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

---
layout:     post
title:      生成模型1-定义
subtitle:   2022年10月
date:       2020-05-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Model
---
[TOC]

# 生成模型的定义

前面所详细描述的模型以浅层的机器学习为主。本章将承上启下引出后面深度机器学习的部分。本小节，主要讲述的是什么是生成模型，它是不是只是生成样本，生成数据？它的任务是什么？精准的定义是什么？

这个问题实际上在之前的章节中有过详细的介绍。这里更进一步总结。回忆一下，之前讲过的简单的生成模型，包括高斯混合分布（GMM），GMM的主要任务是聚类，属于非监督学习；而监督学习中的生成模型，最简单的有朴素贝叶斯模型，主要任务是分类。而Logistics regression显然不是生产模型，简单的说，LR模型主要是对$P(Y=1|X)$或$P(Y=0|X)$条件概率进行建模，并不关心样本$X$是什么样。

所以，对比一下可以发现，生成模型关注点是样本分布本身，解决的问题与任务无关，对样本分布建模。比如简单学习中，先对$P(X,Y)$建模，然后求$\sum_X P(Y|X)$来计算条件概率。在无监督学习中，直接对$P(X)$建模，由于有的时候，$P(X)$非常的复杂，直接对$P(X)$建模非常的困难。这是就会引入隐变量（Latent）$Z$，对$P(X,Z)$建模，然后$P(X) = \sum_Z P(X|Z)$。

生成模型关注的是样本分布本身，是对样本数据本身建模，所以一定和概率分布有关，往往被称之为“概率生成模型”。


参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)


更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)


转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

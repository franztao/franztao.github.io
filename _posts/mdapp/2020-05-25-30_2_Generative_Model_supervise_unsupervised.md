---
layout:     post
title:      系列30 生成模型2-监督vs非监督
subtitle:   2022年10月
date:       2020-05-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Model
---


# 监督 vs 非监督

监督或非监督学习，按照任务分可以将生成模型实现的功能分成以下几种，包括：{分类，回归，标记，降维，聚类，特征学习，密度估计，生产数据。

## 监督任务

监督任务中可以大致分为概率模型和非概率模型两类。实际上这两个模型之间并不是非黑即白的，两者之间的界限是模糊的，本节中做一个简单的介绍。

### 判别模型

判别模型是对条件概率分布建模$P(Y|X)$，典型的有Logistics Regression，最大熵马尔可夫模型（MEMM），条件随机场（CRF），这个模型听名字就很条件概率。

### 生成模型

生成模型大致可以分成以下几类：

- 1. Naive Bayes，此模型非常简单，主要是服从朴素贝叶斯假设。朴素贝叶斯假设描述的是，样本空间各维度之间相互独立，$P(X|Y)=\prod_{i=1}^p P(x_i|Y)$。

- 2. Mixture Model，其中的典型代表是混合高斯模型（GMM），此模型主要是用于聚类。模型可以简要的表示为$P(X|Z)\sim$ Gaussian Distribution.

- 3. Time-series Model，最基础的有隐马尔可夫模型（HMM），卡曼滤波（Kalman Filter），粒子滤波（Particle Filter）。

- 4. Non-Parameteric Model，此模型最重要的特点是参数空间无限化，参数不是一个确定的值，而是一个服从分布，比如Gaussian Process（GP）模型，此模型也是Bayesian Model的一种。

- 5. Mixed member Model，其代表是LDA模型。

- 6. Factorial Model，包括factor analysis，概率PCA模型（P-PCA），ICA，和稀疏编码（Sparse Coding）等等。

上述的六种模型都是浅层的生成模型，什么意思呢？简单的说就是模型的结构相对固定，变换不大，模型的层数也很较少。- 下面描述的是Deep生成模型，模型结构变化较大，而且层数较多。深度生成模型中，经常将神经网络和传统概率相结合。Deep之前的模型，比较固化，基本是用来解决特定的问题。

- 7. Energy based model，包括前面讲到的，Boltzmann Machines，Sigmoid Belief Network，Deep Belief Network，Deep Boltzmann Machines。其主要是基于玻尔兹曼分布的，而实际上玻尔兹曼分布为$\exp\{\mathrm{E}(\theta)\}$，可以看成是熵的形式。

- 8. Variational Automation Coder，变分自编码器。

- 9. GAN，生成对抗神经网络。

- 10. Flow-base model，基于流的模型。

### 非概率模型

包括PLA，Support Vector Machines（支持向量机），KNN（K近邻网络），Tree Model，神经网络（Neural Network）注意神经网络非概率模型，但是和判别模型并不是非黑即白的关系，也可以起到判别模型的作用。其大部分情况是发挥着非概率模型的作用。

## 非监督任务

非监督任务中，概率模型都是生成模型，和前文描述的监督学习中的概率模型是一样的。这章主要讲述是非概率模型。非概率模型包括，PCA（SVD分解），LSA（潜语义分析），K-means，Auto-encoder。

## 小结

本小节主要是从任务的角度介绍了一下，可以分为监督学习和非监督学习。实际上PCA推广之后就是概率PCA（P-PCA），然后进一步发展就是因子分析（FA）。K-means算法发展得到Gaussian Mixture Model（GMM）。从auto-Encoder发展得到VAE。从LSA模型发展得到PLSA，最后得到LDA模型。很多模型都是一步步发展出来的。


参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)


更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-44-06-image.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-43-17-image.png)


转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

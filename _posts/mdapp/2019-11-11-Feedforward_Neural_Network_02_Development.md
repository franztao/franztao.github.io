---
layout:     post
title:      Feedforward_Neural_Network_02_Development
subtitle:   2022年10月
date:       2019-11-11
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Feedforward
    - Neural
    - Network
    - 02
    - Development
---

    
\maketitle
本节主要是来讨论一下，机器学习的发展历史，看看如何从感知机到深度学习。
\section{从时间的发展角度来看}

1958年：up，首次提出了Perceptron Linear Algorithm (PLA)，这里就是我们机器学习的开端了。

1969年：down，Marvin Lee Minsky提出了，PLA has a limitation。因为PLA算法解决不了non-linear问题，比如说XOR问题。非常戏剧的是，这一年，Marvin Lee Minsky获得了图灵奖，他也是“人工智能之父”，第一位因为AI而获得图灵奖的科学家。

1981年：up，学者提出了Multiple Layer Perceptron (MLP)，可以用来解决非线性的问题，就是是最初的Feedforward Neural Network。

1986年：up，Hinton提出了将Back Propagation (BP)算法和MLP完美的融合在了一起，并且发展出了Recurrent Neural Network (RNN)算法。

1989年：up，提出了CNN。但是也迎来了人工智能的寒冬。down，在这一年中提出了一个Universal Apposhmation theorem，也就是一个大于1层的Hidden Layer就可以用来拟合任何的连续函数。那么这是就提出了一个疑问：1 layer is OK，why deep？并且，在BP算法中，随着深度的增加还会出现梯度消失的问题。

1993年和1995年，down，这一年中Support Vector Machine (SVM) + Kernel + Theory，获得了很好的效果。并且，Adaboost和Rondom Forest等Ensemble algorithm流派的提出，获得了很好的效果。

1997年，up，提出了LSTM，但是远不足以止住深度学习发展的颓势。

2006年，up，Hinton，提出了Deep Belief Network (RBM)和Deep Auto-encoder。

2009年，up，GPU的飞速发展。

2011年，up，Deep Learning运用到了语音(Speech)中。

2012年，up，斯坦福大学李飞飞教授，开办了一个非常重要的比赛和数据库ImageNet。

2013年，up，提出了Variational Automation Encode (VAE)算法。

2015年，up，提出了非常重要的Generative Adversarial Network (GAN)。

2016年，up，围棋上AlphaGo彻底引爆了Deep Learning。

2018年，up，提出了重要的Graphic Neural Network (GNN)，传统的神经网络是连接主义的，而GNN中将符合主义和连接主义进行了联合，使之具有推理的功能。

\section{总结}
其实Deep Learning的崛起是很多因素融合的结果。这些年来，主要都是在实践上的发展，而在机器学习理论上基本没有什么进步。它的发展得益于以下几点：1. data的则增加，big data 时代的到来；2. 分布式计算的发展；3. 硬件水平的发展。其实最主要的说白了就是效果，效果比SVM要更好，就占据了主要的地位。

计算机学科就是一门实践为主的科学，现在在实际上取得了很好的效果。之后随着理论研究的不断深入，我们一定可以不断的完善理论知识。之后AI方向的研究，也将是以深度学习为主流，而其他机器学习学派的知识和优点将不断地丰富深度学习，扩充深度学习，来给它更强大的效果。



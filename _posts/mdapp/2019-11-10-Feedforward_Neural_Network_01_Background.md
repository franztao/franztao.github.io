---
layout:     post
title:      Feedforward_Neural_Network_01_Background
subtitle:   2022年10月
date:       2019-11-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Feedforward
    - Neural
    - Network
    
    - Background
---

    


本节的主要目的是从一个较高的角度来介绍一下，什么是深度学习，并且给深度学习一个较好的总结，给大家一个较好的印象。机器学习是目前最火热的一个研究方向，而机器学习大致可以分为，频率派和贝叶斯派。频率派逐渐演变出了统计机器学习，而贝叶斯派逐渐演变出了PGM，也就是概率图模型。下面我们分开进行描述。

#  频率派}
统计机器学习方法基本就是由频率派的估计思想得到的。统计机器学习方法大概可以分成四种。

1. 正则化：$L_1,L_2$也就是之前提到的Lasso和岭回归，这实际上并没有产生新的模型，而是在之前模型的基础上进行了改进。我们可以把它描述为Loss function + regularized。用来抑制训练的过拟合。

2. 核化：最著名的就是我们之前提到的，Kernel Support Vector Machine (SVM)了。

3. 集成化：也就是Adaboost和Random Forest。

4. 层次化：层次化主要就是我们指的Neural Network，也就是神经网络，神经网络进一步发展就得到了我们现在研究的深度学习。而神经网络中比较著名的几类就是：1. 多层感知机(Multiple Layer Perception)；2. Auto-encode；3. CNN；4. RNN。这几个组合起来就是我们经常听到的Deep Network。

#  贝叶斯派}
贝叶斯派的估计方法就演化得到了概率图模型(Probability Graphic Model。他们大致可以分成以下三类：

1. 有向图：Bayesian Network，也就是Deep Directed Network，包括大家听得很多的：Variable Automation Encode (VAE)，Generative Adversarial Network (GAN)和Sigmoid Belief Network等等。

2. 无向图：Markov Network，也就是Deep Boltzmann Modeling，这就是我们的第二类图模型。

3. 有向图和无向图混合在一起，就是我们常说的Mixed Network，主要包括，Deep Belief Network等等。

而上述几个图模型，结合起来就是我们常说的Deep Generative Network，深度生成模型。

在我们狭义的深度学习的理解中，什么是深度学习，实际上就是统计学习方法中的层次化中的Deep Network。而广义的深度学习中，还应该包括，Deep Generative Network。而实际上绝大多数的深度学习者都不太了解Deep Generative Network，确实涉及到贝叶斯的理论，深度学习就会变得很难。而且它的训练也会变得非常的复杂。



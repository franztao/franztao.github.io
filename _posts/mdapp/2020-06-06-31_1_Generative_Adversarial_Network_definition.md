---
layout:     post
title:      GAN 1-什么是 Generative Adversarial Network
subtitle:   2022年10月
date:       2020-06-06
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Generative
    - Adversarial
    - Network
---

# 什么是Generative Adversarial Network？

首先，我们需要充分的了解什么是生成对抗网络（Generative Adversarial Network，GAN）？顾名思义，首先它是一种生成模型，它的核心是对样本数据建模。下面我们将举个例子来详细的说明一下什么是GAN。

首先，我是一个收藏家，我有很多的宝贝，但是，我最终的目标不仅仅是一个收藏家。我想高仿东西，成为工艺品大师（做仿品）。我要不惜一切代价的成为这方面的大师。但是，我做出来的东西不能只是我自己分辨不出来就够了，那就只能放在家里看，它需要接受大师们的检验，各位专家都看不出来这是仿品，就比较成功了。

我把我做出的东西，放到一个叫“一锤定音”节目现场，这个平台将鉴别出为假的东西就砸了，鉴别出为真的东西就拿去估值，就美了。节目流程如下所示：

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-12-10-23-49-11-image.png)

我们的目标是成为高水平的可以做“以假乱真”的高质量仿品的大师，有如下两个要求：

1. 鉴赏专家的水平足够高。

2. 作假的水平足够高。

国宝是古人做的，静态的，不可能发生变化的。而工艺品和作假的水平是变化的。三者中，国宝是静态的，其他的都是可变化的。

有可能有的同学会迷惑，这和生成模型之间有什么关系呢？如果一个仿品可以和国宝做的一模一样，不就相当于学到了真实数据的分布，可以完全模拟出真实数据。下一步则是，想办法将模型用数学语言描述。

本章节主要是对于概率生成模型进行了一个全面的介绍，起到一个承上启下的作用。回顾了之前写到的浅层概率生成模型，并引出了接下来要介绍的深度概率生成模型。并从任务（监督 vs 非监督），模型表示，模型推断，模型学习四个方面对概率生成模型做了分类。并从极大似然的角度重新对模型做了分类。并介绍了概率图模型和神经网络的区别，我觉得其中最重要的是，概率图模式是对样本数据建模，其图模型有具体的意义；而神经网络只是函数逼近器，只能被称为计算图。

参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)

转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

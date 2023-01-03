---
layout:     post
title:      系列31 GAN 2-Generative Adversarial Network 数学描述
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

# 数学语言描述

## 模型表示

工艺大师和鉴赏专家的水平会不断的提高，最终我们会培养一个高水平的工艺大师和一个高水平的鉴赏家。而最终的目的是培养一个高水平的工艺大师，而不是一个高水平的鉴赏家。鉴赏家只是衍生品，最终将达到两个目的，1. 足够的以假乱真；2. 真正的专家看不出来。

所以，我们需要加一些feedback，令工艺大师收到专家给出的反馈。并且鉴赏大师也要从工艺大师那里知道真实的情况来提升自己的水平。如下图所示：

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-12-10-23-49-35-image.png)

我们可以将古人，视为$P_{\text{data}}$，$\{x_i\}_{i=1}^N$，实际就是经验分布，通常我们将经验分布视为数据分布。

工艺品，是从一个模型分布$P_g$采样出来的，$P_g(x;\theta_g)$。我们本身不对$P_g$建模，而是用一个神经网络来逼近$P_g$。假设$z$来自一个简单分布，并增加噪声，$z\sim P_z(z)$。其中，$x=G(z;\theta_g)$

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-12-10-23-49-57-image.png)

鉴赏专家输出的是一个概率分布，同样也是一个神经网络，$D(x,\theta_d)$，其代表的是输入一个物品，判断其为国宝的概率。$D\to 1$是国宝，$D\to 0$是工艺品。模型如下所示：

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-12-10-23-50-10-image.png)

我们的目标有两个：

1. **高专家**：
   高水平的专家可以正确的分辨国宝和赝品。

$$
\begin{equation}
    \left\{
    \begin{array}{ll}
      \text{if $x$ is from $P_{data}$ then $D(x)$ $\uparrow$ } & \\
      \text{if $x$ is from $P_{g}$ then $1-D(x)$ $\downarrow$ } & \\
    \end{array}
    \right.
\end{equation}
$$

其中，我们将用对数似然函数的形式来进行表达。而$1-D(x)$中的$x$是来自$G(z)$的，那么，高专家部分的目标函数为：

$$
\begin{equation}
    \max_D \underbrace{\mathbb{E}_{x\sim P_{data}}[\log D(x)]}_{\frac{1}{N} \sum_{i=1}^N \log D(x_i)} +  \mathbb{E}_{\sim P_{z}}[\log (1-D(G(z)))]
\end{equation}
$$

2. **高大师**：
   高水平的大师的目的就是要造成高水平的鉴赏专家分辨不出来的工艺品，可以表示为：

$$
\begin{equation}
    \text{if $x$ is from $P_g$ then $\log(1-D(G(z)))$ $\uparrow$}
\end{equation}
$$

此目标表达为数学语言即为：

$$
\begin{equation}
    \min_G \mathbb{E}_{z\sim P_g}[\log(1-D(z))]
\end{equation}
$$

根据图2中的feedback流向，我们可以了解到，先优化鉴赏专家，再优化工艺大师。总优化目标是：

$$
\begin{equation}
    \min_G \max_D \mathbb{E}_{x\sim P_{data}}[\log D(x)] + \mathbb{E}_{z\sim P_{z}}[\log (1-D(G(z)))]
\end{equation}
$$

## 小结

GAN模型本身思想很简单，难点主要在于学习$\theta_g,\theta_d$。GAN中没有直接面向$P_g$建模，而是从一个可微的NN中采样来逼近$D_g(x;\theta_g)$。不是直接面对分布，而是绕过复杂的求解过程来近似。我们之前分析过，如果用NN来近似概率分布，这叫Implicit Density Model。下一步则是考虑如何求解全局最优解。

本章节主要是对于概率生成模型进行了一个全面的介绍，起到一个承上启下的作用。回顾了之前写到的浅层概率生成模型，并引出了接下来要介绍的深度概率生成模型。并从任务（监督 vs 非监督），模型表示，模型推断，模型学习四个方面对概率生成模型做了分类。并从极大似然的角度重新对模型做了分类。并介绍了概率图模型和神经网络的区别，我觉得其中最重要的是，概率图模式是对样本数据建模，其图模型有具体的意义；而神经网络只是函数逼近器，只能被称为计算图。

参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)

转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

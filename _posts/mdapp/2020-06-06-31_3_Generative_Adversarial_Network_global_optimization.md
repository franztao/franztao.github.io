---
layout:     post
title:      系列31 GAN 3-Generative Adversarial Network 全局最优解
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

# 全局最优解

GAN模型表示汇总如下所示：

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-12-10-23-51-38-image.png)

$P_{data}$：$\{x_i\}_{i=1}^N$

$P_g(x;\theta_g)$：generator，$G(z;\theta_g)$

$y|x$：discriminater，$P(y=1|x)=D(x)$，$P(y=0|x)=1-D(x)$

$G(z;\theta_g)$和$D(x;\theta_d)$是两个多层感知机。GAN就是这样采用对抗学习，其最终目的就是$P_g = P_{data}$。目标函数中，记：

$$
\begin{equation}
    V(D,G) = \mathbb{E}_{x\sim P_{data}}[\log D(x)] + \mathbb{E}_{z\sim P_{z}}[\log (1-D(G(z)))]
\end{equation}
$$

最终的目标是令$P_g = P_{data}$，而$P_g $中的参数为$\theta_g$。在之前的极大似然估计思想中，

$$
\begin{equation}
    \theta_g = \arg\max_{\theta_g} \sum_{i=1}^N \log P_g(x_i)
\end{equation}
$$

而对$P_g(x_i)$比较复杂，通常采用EM算法和VI来进行近似，通过推导可以得出，最后的目标为：

$$
\arg\min_{\theta_g}KL(P_{data}\|P_g)
$$

对公式(5)的求解过程可以分成两步，而第一步为求解过程为fixed G，求解$\max_D V(G,D)$

$$
\begin{equation}
    \begin{split}
        \max_D V(D,G) = & \int P_{\text{data}} \log D dx + \int P_g \log(1-D) dx \\
        =& \int (P_{\text{data}} \log D dx + P_g \log(1-D)) dx
    \end{split}
\end{equation}
$$

通过求偏导来计算最优解：

$$
\begin{equation}
    \begin{split}
        \frac{\partial (V(D,G))}{\partial D} = & \frac{\partial}{\partial D} \int \left[ P_{\text{data}} \log D dx + P_g \log(1-D) \right]dx \\
        = &  \int \frac{\partial}{\partial D} \left[ P_{\text{data}} \log D dx + P_g \log(1-D) \right]dx \\
        = & 0 \\
    \end{split}
\end{equation}
$$

这一步的推导利用了微积分的基本定理，得到：

$$
\int P_{data}\cdot \frac{1}{D} + P_g \frac{-1}{1-D} dx = 0
$$

恒成立，所以有：

$$
\begin{equation}
    D^\ast = \frac{P_{\text{data}}}{P_{\text{data}} + P_{g}}
\end{equation}
$$

第二步，将求解的是：

$$
\begin{equation}
    \begin{split}
        \min_G \max_D V(D,G) = & \min_G V(D^\ast,G) \\
        = & \min_D \mathbb{E}_{x\sim P_{\text{data}}} \left[   \log \frac{P_{\text{data}}}{P_{\text{data}} + P_{g}}\right] + \mathbb{E}_{x\sim P_{g}} \left[   \log \frac{P_g}{P_{\text{data}} + P_{g}}\right]
    \end{split}
\end{equation}
$$

观察$\mathbb{E}_{x\sim P_{\text{data}}} \left[   \log \frac{P_{\text{data}}}{P_{\text{data}} + P_{g}}\right]$会发现这很像一个KL散度，但是$P_{\text{data}} + P_{g}$不是一个概率分布。所以，通过$\frac{P_{\text{data}} + P_{g}}{2}$来将其转换为一个概率分布。那么有，

$$
\begin{equation}
\begin{split}
    \min_G \max_D V(D,G) = & \min_G \mathbb{E}_{x\sim P_{\text{data}}} \left[   \log \frac{P_{\text{data}}}{\frac{P_{\text{data}} + P_{g}}{2}} \cdot \frac{1}{2}\right] + \mathbb{E}_{x\sim P_{g}} \left[   \log \frac{P_g}{\frac{P_{\text{data}} + P_{g}}{2}} \cdot \frac{1}{2}\right] \\
    = & \min_G \text{KL}\left[ P_{\text{data}} \| \frac{P_{\text{data}} + P_{g}}{2} \right] + \text{KL}\left[ P_{g} \| \frac{P_{\text{data}} + P_{g}}{2} \right] - \log 4 \\
    \geq & - \log 4
\end{split}
\end{equation}
$$

当且仅当$P_{\text{data}}  = P_{g} = \frac{P_{\text{data}} + P_{g}}{2}$时，等号成立。此时，$P^\ast_g = P_d,P^\ast_d = \frac{1}{2}$。很显然，大家想一想就知道，生成器模型分布最好当然是和数据分布是一样的，而此时判别器模型真的和假的都分不出，输出都是$\frac{1}{2}$。

# 总结

本章主要描述了什么是GAN，GAN是一种生成模型。其实，以前我对GAN的理解，只是它可以画图，生成和真实数据一样的图，并不知道它有什么用。通过系统的学习，我现在对生成模型的意义有了不一样的认识。本章主要介绍的是GAN的模型意义和模型表示，以及简单的求解过程。实际上，GAN中有很多很多的问题，这只是最基础的版本，介绍简单的思想而已，希望可以抛转引玉。

本章节主要是对于概率生成模型进行了一个全面的介绍，起到一个承上启下的作用。回顾了之前写到的浅层概率生成模型，并引出了接下来要介绍的深度概率生成模型。并从任务（监督 vs 非监督），模型表示，模型推断，模型学习四个方面对概率生成模型做了分类。并从极大似然的角度重新对模型做了分类。并介绍了概率图模型和神经网络的区别，我觉得其中最重要的是，概率图模式是对样本数据建模，其图模型有具体的意义；而神经网络只是函数逼近器，只能被称为计算图。

参考B站视频[【机器学习】【白板推导系列】](https://space.bilibili.com/97068901)

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)

转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

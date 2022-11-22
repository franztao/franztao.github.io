---
layout:     post
title:      Linear_Classfication_04
subtitle:   2022年10月
date:       2019-11-01
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Linear
    - Classfication
    - 04
---

    

在前面的两小节中我们，我们讨论了有关于线性分类问题中的硬分类问题，也就是感知机和Fisher线性判别分析。那么，我们接下来的部分需要讲讲软分类问题。软分类问题，可以大体上分为概率判别模型和概率生成模型，概率生成模型也就是高斯判别分析(Gaussian Discriminate Analysis)，朴素贝叶斯(Naive Bayes)。而线性判别模型也就是本章需要讲述的重点，Logistic Regression。

\section{从线性回归到线性分类}
线性回归的问题，我们可以看成这样一个形式，也就是$W^TX$。而线性分类的问题可以看成是$\{0,1\}$或者$[0,1]$的问题。其实，从从线性回归到线性分类之间通过一个映射，也就是Activate Function来实现的，通过这个映射我们可以实现$W^TX \longmapsto \{0,1\}$。

而在Logistic Regression中，我们将激活函数定义为：

$$
\begin{equation}
    \sigma(z)=\frac{1}{1+e^{-z}}
\end{equation}
$$

那么很显然会有如下的性质：

1.$\lim_{z\longrightarrow+\infty} \sigma(z) = 1$ 

2.$\lim_{z\longrightarrow 0 } \sigma(z) = \frac{1}{2}$

3.$\lim_{z\longrightarrow-\infty} \sigma(z) = 0$

那么，通过这样一个激活函数$\sigma$，我们就可以将实现$\mathbb{R}\longrightarrow (0,1)$。那么我们会得到以下的表达式：

$$
\begin{equation}
    p(y|x) = 
    \left\{
        \begin{array}{ll}
        p_1=p(y=1|x)=\sigma(w^Tx)=\frac{1}{1+exp\{-w^tx\}} & y=1 \\
        p_2=p(y=0|x)=1-p(y=1|x)=\frac{exp\{-w^tx\}}{1+exp\{-w^tx\}} & y=0 \\
    \end{array}
    \right.
\end{equation}
$$

而且，我们可以想一个办法来将两个表达式合二为一，那么有：

$$
\begin{equation}
    p(y|x) = p_1^y\cdot p_0^{1-y}  
\end{equation}
$$

\section{最大后验估计}

$$
\begin{equation}
    \begin{split}
        MLE = & \hat{w} = argmax_w \log p(y|x) \\
            = & argmax_w \log p(y_i|x_i) \\
            = & argmax_w \sum_{i=1}^N \log p(y_i|x_i) \\
            = & argmax_w \sum_{i=1}^N y\log p_1 + (1-y)\log p_2 \\
    \end{split}
\end{equation}
$$
    
我们令，

$$
\begin{equation}
    \frac{1}{1+exp\{-w^tx\}}=\varphi(x,w) \qquad \frac{exp\{-w^tx\}}{1+exp\{-w^tx\}}=1-\varphi(x,w)
\end{equation}
$$

那么，

$$
\begin{equation}
    MLE =  argmax_w \sum_{i=1}^N y\log \varphi(x,w) + (1-y)\log (1-\varphi(x,w))
\end{equation}
$$

实际上$y\log \varphi(x,w) + (1-y)\log (1-\varphi(x,w))$就是一个交叉熵(Cross Entropy)。那么，我们成功的找到了我们的优化目标函数，可以表述为MLE (max) $\longrightarrow$ Loss function (Min Cross Entropy)。所以，这个优化问题就转换成了一个Cross Entropy的优化问题，这样的方法就很多了。Cross Entropy属于信息论的知识，同学们可以自行补充。


---
layout:     post
title:      Exponential_Family_Distribution_02
subtitle:   2022年10月
date:       2022-10-29
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Exponential
    - Family
    - Distribution
    - 02
---
            


\maketitle

本节的主要内容是演示Guassian Distribution的指数族表达形式，将高斯函数的形式转换为指数族分布的通用表达形式。

指数族分布的基本形式可以表示为：
\begin{equation}
    p(x|y)=h(x)exp\left\{ \eta^T\varphi(x)-A(\eta) \right\}
\end{equation}

$\eta$：参数向量parameter，$\eta \in \mathbb{R}^p$。

$A(\eta)$：log partition function (配分函数)。

$\varphi(x)$：充分统计量sufficient statistics magnitude。

\section{思路分析}
高斯分布的概率密度函数可表示为：
\begin{equation}
    p(x|\mu,\sigma^2) = \frac{1}{\sqrt{2\pi}\sigma}exp\left\{ -\frac{(x-\mu)^2}{\sigma^2} \right\}
\end{equation}

观察指数族分布的表达形式，高斯分布的参数向量是有关于$\theta=(\mu,\sigma)$的。首先观察指数部分的第一部分$\eta^T\varphi(x)$，只有这个部分和$x$相关。那么把这个部分搞定，系数就是参数矩阵，剩下的就是配分函数了，而且配分函数是一个关于$\eta$的函数。

\section{将Guassian Distribution改写为指数族分布的形式}
具体推导过程如下所示：
\begin{align}
    p(x|\theta)= & \frac{1}{\sqrt{2\pi}\sigma}exp\left\{ -\frac{(x-\mu)^2}{2\sigma^2} \right\} \\
    = & \frac{1}{\sqrt{2\pi}\sigma}exp\left\{ -\frac{1}{2\sigma^2}(x^2-2\mu x + \mu^2) \right\} \\
    = & \frac{1}{\sqrt{2\pi}\sigma}exp\left\{ -\frac{x^2}{2\sigma^2}+\frac{\mu x}{\sigma^2}-\frac{\mu^2}{2\sigma^2} \right\} \\
    = & \frac{1}{\sqrt{2\pi}\sigma}exp\left\{
        \begin{pmatrix}
            \frac{\mu}{\sigma^2} \\
            -\frac{1}{2\sigma^2}
        \end{pmatrix}
        \begin{pmatrix}
            x & x^2 \\
        \end{pmatrix}
        -\frac{\mu^2}{2\sigma^2}
        \right\} \\
    = & exp\log \frac{1}{\sqrt{2\pi}\sigma} exp\left\{
        \begin{pmatrix}
            \frac{\mu}{\sigma^2} \\
            -\frac{1}{2\sigma^2}
        \end{pmatrix}
        \begin{pmatrix}
            x & x^2 \\
        \end{pmatrix}
        -\frac{\mu^2}{2\sigma^2}
        \right\} \displaybreak \\ 
    = & exp\left\{
        \begin{pmatrix}
            \frac{\mu}{\sigma^2} \\
            -\frac{1}{2\sigma^2}
        \end{pmatrix}
        \begin{pmatrix}
            x & x^2 \\
        \end{pmatrix}
        -\left(\frac{\mu^2}{2\sigma^2} -\frac{1}{2}\log 2\pi\sigma\right) 
        \right\}
\end{align}

令:
\begin{equation}
    \eta=
    \begin{pmatrix}
        \eta_1 \\
        \eta_2
    \end{pmatrix}
    =
    \begin{pmatrix}
        \frac{\mu}{\sigma^2} \\
        -\frac{1}{2\sigma^2}
    \end{pmatrix}
    \Longrightarrow
    \left\{
    \begin{array}{ll}
         \eta_1 = \frac{\mu}{\sigma^2} & \\
         \eta_2 = -\frac{1}{2\sigma^2} &
    \end{array}
    \right.
    \Longrightarrow
    \left\{
    \begin{array}{ll}
         \mu = -\frac{\eta_1}{2\eta_2} & \\
         \sigma^2 = -\frac{1}{2\eta_2} &
    \end{array}
    \right.
\end{equation}

到了现在，我们离最终的胜利只差一步了，
\begin{equation}
   \eta=
    \begin{pmatrix}
        \eta_1 \\
        \eta_2
    \end{pmatrix}
    \quad
    \varphi(x)=
    \begin{pmatrix}
        x \\
        x^2
    \end{pmatrix}   
\end{equation}
\begin{equation}
    A(\eta)=-\frac{\eta_1^2}{4\eta_2}+\frac{1}{2}\log (2\pi\cdot-\frac{1}{2\eta_2})=-\frac{\eta_1^2}{4\eta_2}+\frac{1}{2}\log(-\frac{\pi}{\eta_2})
\end{equation}

于是，Guassian Distribution成功的被我们化成了指数族分布的形式$exp\left\{ \eta^T\varphi(x)-A(\eta) \right\}$。

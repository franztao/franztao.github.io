---
layout:     post
title:      Bayes_Linear_Classification_01_Background
subtitle:   2022年10月
date:       2019-11-05
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Bayes
    - Linear
    - Classification
    - 01
    - Background
---

    
\maketitle

数据集$D=\{(x_i,y_i)\}^{N}_{i=1}$，其中$x_i\in\mathbb{R}^{p}$，$y_i\in\mathbb{R}$。

数据矩阵为：(这样可以保证每一行为一个数据点)

\begin{equation}
    X=(x_1, x_2, \cdots, x_N)^T=
    \begin{pmatrix}
    x_1^T \\ 
    x_2^T \\
    \vdots\\
    x_N^T \\
    \end{pmatrix} =
    \begin{pmatrix}
    x_{11} & x_{12} & \dots & x_{1p}\\
    x_{21} & x_{32} & \dots & x_{2p}\\
    \vdots & \vdots & \ddots & \vdots\\
    x_{N1} & x_{N2} & \dots & x_{Np}\\
    \end{pmatrix}_{N\times P}
\end{equation}
\begin{equation}
    Y=
    \begin{pmatrix}
    y_1 \\ 
    y_2 \\
    \vdots\\
    y_N \\
    \end{pmatrix}_{N\times 1}
\end{equation}

拟合函数我们假设为：$f(x) = w^Tx = x^Tw$。

预测值$y=f(x)+\varepsilon$，其中$\varepsilon$是一个Guassian Noise，并且$\varepsilon \sim \mathcal{N}(0,\sigma^2)$。

并且，$x,y,\varepsilon$都是Random variable。

\section{最小二乘估计(Least Square Estimation)}
这实际上就是一个利用数据点的极大似然估计(MLE)，并且有一个默认的隐含条件，也就是噪声$\varepsilon$符合Gaussian Distribution。我们的目标是通过估计找到$w$，使得：
\begin{equation}
    w_{MLE} = argmax_w p(Data|w)
\end{equation}

而如果仅仅只是这样来使用，很容易会出现过拟合的问题。所以，我们引入了Regularized LSE，也就是正则化最小二乘法。同时也有一个默认的隐含条件，也是噪声$\varepsilon$符合Gaussian Distribution。在Liner Regression中我们提到了有两种方法来进行思考，也就是Lasso和Ridge Regression。在这里我们可以使用一个Bayes公式，那么：
\begin{equation}
    \begin{split}
        p(w|Data) \propto p(Data|w)p(w) 
    \end{split}
\end{equation}
\begin{equation}
    w_{MAP} = argmax_w p(w|Data) = argmax_wp(Data|w)p(w) 
\end{equation}

那么假设$p(w)$符合一个高斯分布$\mathcal{N}(\mu_0,\Sigma_0)$时，这时是属于Ridge；而如果$p(w)$符合一个Laplace分布，这是就是Lasso。从概率的角度来思考和统计的角度来思想，我们其实获得的结果是一样的，这在Linear Regression中有证明。但是，我们只证明了Ridge的部分。

\section{贝叶斯估计与频率派估计}
其实在第一部分，我们讲的都是点估计，频率派估计的部分。因为在这些思路中，我们把参数$w$当成a unknown random variable。这实际上就是一个优化问题。而在Beyesian method中，认为$w$是一个随机变量，也就是一个分布，那么我们求的$w$不再是一个数了，而是一个分布。下面我们将要进行Bayes Linear Regression的部分。



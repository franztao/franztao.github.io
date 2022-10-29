---
layout:     post
title:      dsadsa
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - EDA

---    


\maketitle

数据集$D=\{(x_1, y_1), (x_2, y_2), \cdots, (x_N, y_N)\}$，其中$x_i\in\mathbb{R}^{p}$，$y_i\in\mathbb{R}$，$i=1, \ 2,\cdots,\ N$。

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

设拟合的函数为：$f(w)=W^T x$

\section{最小二乘估计：矩阵表示}
很简单可以得到损失函数(Loss function)为：
\begin{align}
     L(w) = & \sum_{i=1}^{N}||w^T x_i-y_i||^2 \\
          = & (w^T x_1-y_1, w^T x_2-y_2, \dots, w^T x_N-y_N)
          \begin{pmatrix}
            w^T x_1-y_1\\
            w^T x_2-y_2\\
            \vdots\\
            w^T x_N-y_N\\
          \end{pmatrix}                      
\end{align}

其中:
\begin{align}
    (w^T x_1-y_1, w^T x_2-y_2, \dots, w^T x_N-y_N) = & [(w^Tx_1, w^Tx_2, \cdots, w^Tx_N)-(y_1,y_2,\cdots,y_N)] \\
    \nonumber = & W^TX^T-Y^T
\end{align}

所以:
\begin{align}
    L(w) = & (W^TX^T-Y^T)(W^TX^T-Y^T)^T \\
    \nonumber = & (W^TX^T-Y^T)(XW-Y) \\
    \nonumber = & W^TX^TX - W^TX^TY - Y^TXW + Y^TY\\
    \nonumber = & W^TX^TX - 2W^TX^TY + Y^TY\\
\end{align}

那么我需要求的$w$，可记为$\hat{w}=argmin_{w} \ L(w)$。求得这个函数的方法可以使用对$w$求偏导的方法，那么有：
\begin{equation}
    \frac{\partial L(w)}{w}=2X^TXW-2X^TY=0
\end{equation}
解得：
\begin{equation}
    W=(X^TX)^{-1}X^TY
\end{equation}
    

\section{最小二乘估计：几何意义}
将$X$矩阵从列向量的角度来看，可以看成一个$p$维的向量空间$S$，为了简便计算，令$W^TX=X\beta$。可以看成Y向量到$S$的距离最短，那么将有约束条件：
\begin{equation}
    X^T(Y-X\beta) = 0
\end{equation}
\begin{equation}
    X^TY-X^TX\beta=0
\end{equation}
\begin{equation}
    \beta=(X^TX)^{-1}X^TY
\end{equation}

\section{最小二乘估计：概率角度}
假设一个分布$\varepsilon \sim \mathcal{N}(0,\sigma^2)$，那么所有的观测值可看为$y = w^Tx + \varepsilon$。因为$\varepsilon \sim \mathcal{N}(0,\sigma^2)$，那么$p(y|x;w) \sim \mathcal{N}(w^Tx, \sigma^2)$。我们的目的是求$w$使，$y$出现的概率最大，在这里可以使用极大似然估计(MLE)求解。首先写出$p(y|x;w)$的概率密度函数为：
\begin{equation}
    p(y|x;w)=\frac{1}{\sqrt{2\pi}\sigma}exp\left(-\frac{(y-w^Tx)^2}{2\sigma^2}\right)
\end{equation}
似然函数为$In\ p(y|x;w)$，使似然函数最大化的过程求解如下：
\begin{align}
    L(w) = & In\ p(y|x;w) = ln\prod_{i=1}^Np(y_i|x_i;w) \\
         = & \sum_{i=1}^Nln\ p(y_i|x_i;w) \\ 
         = & \sum_{i=1}^N \left( ln\frac{1}{\sqrt{2\pi}\sigma} + ln\ exp\left( -\frac{(y_i - w^Tx)^2}{2\sigma^2} \right) \right)
\end{align}

求解目标为$\hat{w} = argmax_w \ L(w)$，因为第一项其中并没有包含$w$，于是可以直接省略，那么有：
\begin{align}
    \hat{w} = & argmax_w \ L(w) \\ 
    \nonumber = & argmax_w \ \sum_{i=1}^{N}-\frac{(y_i - w^Tx_i)^2}{2\sigma^2} \\
    \nonumber = & argmin_w \ \sum_{i=1}^{N} (y_i - w^Tx_i)^2 \\
\end{align}

然后惊奇的发现后面的求解过程，和最小二乘法的矩阵表示方法的求解过程是一模一样的。那么我可以可以得到一个结论：最小二乘估计$\Longleftrightarrow$极大似然估计(噪声符合高斯分布)。那么我们的最小二乘估计中隐藏了一个假设条件，那就是噪声符合高斯分布。

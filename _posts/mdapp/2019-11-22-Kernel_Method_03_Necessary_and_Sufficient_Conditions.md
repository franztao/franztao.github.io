---
layout:     post
title:      Kernel_Method_03_Necessary_and_Sufficient_Conditions
subtitle:   2022年10月
date:       2019-11-22
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Kernel
    - Method
    - 03
    - Necessary
    - and
    - Sufficient
    - Conditions
---

    

在上一小节中，我们描述了正定核的两个定义，并且认为这两个定义之间是相互等价的。下面我们就要证明他们之间的等价性。
\section{充分性证明}
大家注意到在上一节的描述中，我似乎没有谈到对称性，实际上是因为对称性的证明比较的简单。就没有做过多的解释，那么我重新描述一下我们需要证明的问题。

已知：$K(x,z) = <\phi(x),\phi(z)>$，证：Gram Matrix是半正定的，且$K(x,z)$是对称矩阵。

对称性：已知：
$$
\begin{equation}
    K(x,z)=<\phi(x),\phi(z)> \qquad K(z,x) = <\phi(z),\phi(x)>
\end{equation}
$$

又因为，内积运算具有对称性，所以可以得到：
$$
\begin{equation}
    \phi(x),\phi(z)> = <\phi(z),\phi(x)>
\end{equation}
$$

所以，我们很容易得到：$K(x,z)=K(z,x)$，所以对称性得证。

~\\

正定性：我们想要证的是Gram Matrix$=K[K(x_i,x_j)]_{N\times N}$是半正定的。那么，对一个矩阵$A_{N\times N}$，我们如何判断这是一个半正定矩阵？大概有两种方法，1. 这个矩阵的所有特征值大于等于0；2. 对于$\forall \alpha \in \mathbb{R}^N,\ \alpha^T A \alpha \geq 0$。这个是充分必要条件。那么，这个问题上我们要使用的方法就是，对于$\forall \alpha \in \mathbb{R}^N,\ \alpha^T A \alpha \geq 0$。
\begin{align}
    \alpha^TK\alpha = & 
    \begin{bmatrix}
        \alpha_1 & \alpha_2 & \cdots & \alpha_N
    \end{bmatrix}
    \begin{bmatrix}
        K_{11} & K_{12} & \cdots & K_{1N} \\
        K_{21} & K_{22} & \cdots & K_{2N} \\
        \vdots & \vdots & \ddots & \vdots \\
        K_{N1} & K_{N2} & \cdots & K_{NN} \\
    \end{bmatrix}
    \begin{bmatrix}
        \alpha_1 \\
        \alpha_2 \\ 
        \vdots \\ 
        \alpha_N
    \end{bmatrix} \\
    = & \sum_{i=1}^N\sum_{j=1}^N \alpha_i\alpha_jK_{ij} \\
    = & \sum_{i=1}^N\sum_{j=1}^N \alpha_i\alpha_j<\phi(x_i),\phi(x_j)> \\
    = & \sum_{i=1}^N\sum_{j=1}^N \alpha_i\alpha_j\phi(x_i)^T\phi(x_j) \\ 
    = & \sum_{i=1}^N\phi(x_i)^T\sum_{j=1}^N\phi(x_j) \\
    = & \left[  \sum_{i=1}^N\phi(x_i) \right]^T \left[  \sum_{j=1}^N\phi(x_j) \right] \\
    = & \left|\left| \sum_{i=1}^N \alpha_i\phi(x_i) \right|\right|^2 \geq 0
\end{align}

所以，我们可以得到$K$是半正定的，必要性得证。

\section{必要性证明}
充分性得到证明之后，必要性的证明就会变得很简单了。这个证明可以被我们描述为：

已知：Gram Matrix是半正定的，且$K(x,z)$是对称矩阵。证：存在一个映射$\phi:\mathcal{X}\mapsto\mathbb{R}^p$，使得$K(x,z) = <\phi(x),\phi(z)>$。

对于我们建立的一个映射$\phi(x)= K(x,\cdot)$，我们可以得到$K(x,\cdot)K(z,\cdot) = K(x,z)$。所以有$K(x,z) = K(x,\cdot)K(z,\cdot) = \phi(x)\phi(z)$。我们就得证了，具体的理解可以参考我之前写的关于可再生核希尔伯特空间的理解。

\section{小结}
讲到这里，我们的核方法就讲完了。核这个东西是真的不好理解，讲到这大家应该有个印象了，这一节{ 配合再生核希尔伯特空间使用食用，效果更佳！}下面，我会编写对于Stein变分梯度下降论文的详细理解，这个方法真的很难！而这个系列的下一次，我们将进入到概率图模型，贝叶斯方法的大boss，终于要来了，想想就很激动了！













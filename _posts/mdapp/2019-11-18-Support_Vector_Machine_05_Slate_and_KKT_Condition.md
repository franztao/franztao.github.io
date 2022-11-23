---
layout:     post
title:      Support_Vector_Machine_05_Slate_and_KKT_Condition
subtitle:   2022年10月
date:       2019-11-18
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Support
    - Vector
    - Machine
    
    - Slate
    - and
    - KKT
    - Condition
---

首先，我们整理一下前面得到的有关约束优化的模型。我们可以描述为：

$$
\begin{equation}
    \left\{
        \begin{array}{ll}
        \min\ f(x) & \\
        s.t. \quad m_i(x)\leq 0, \ i = 1, 2, \cdots, M & \\
        \ \; \qquad n_j(x)= 0, \ j = 1, 2, \cdots, N & \\
        \end{array}
    \right.
\end{equation}
$$

其中，

$$
\begin{equation}
    D = \left\{ dom\ f \bigcap_{i=1}^M dom\ m_i \bigcap_{j=1}^N dom\ n_j \right\}
\end{equation}
$$

我们将模型进行简化可得：

$$
\begin{equation}
    \left\{
        \begin{array}{ll}
        \min\ f(x) & \\
        s.t. \quad m_i(x) & \\
        \end{array}
    \right.
    \Longrightarrow
    G = \{ (m,f)|x\in D \} = \{ (\mu,t)|x\in D \}
\end{equation}
$$

那么，我们的优化目标为：

$$
\begin{gather}
    p^\ast = inf\{ t|(\mu,t)\in G,\mu \leq 0 \} \\ 
    g(\lambda) = inf(t+\lambda\mu|(\mu,t)\in G)
\end{gather}
$$

通常来说，凸优化问题，不一定是强对偶问题。往往都是凸优化问题需要加上一些限定条件才可以构成强对偶问题。比如说slate condition，但是这些条件往往都是充分非必要的。这样的条件有很多种，slate condition只是其中一种，类似的还有KKT condition。

#  {Slate Condition}
下面简述一下Slate Condition，详细的证明过程就不做过多的描述。也就是$\exists \hat{x} \in relint\ D, \ s.t. \ \forall i \i = 1,2,\cdots,m,\ m_i(\hat{x}) \leq 0$。而relint的意思就是，relative interior，相对内部的意思。

而对于绝大部分的凸优化问题，通常Slate条件是成立的。而放松的Slate条件为：假设$M$中有$k$个仿射函数，$M-k$个仿射。而SVM是一个典型的凸二次规划问题，也就是目标函数$f$是凸函数，$m_i$是仿射函数，$n_j$为仿射。那么在几何上是什么意思呢？也就是限制至少有一个点在坐标系的左边，限制直线不是垂直的，这里需要结合Support Vector Machine 04中的几何解释来看。

#  {KKT Condition}
在上文中我们知道了Convex和Slate Condition可以得到强对偶关系，也就是$d^\ast = p^\ast$。但是这只是一个充分非必要条件。同样的在满足KKT Condition的情况下，我们也可以得出是一个强对偶问题，并且这是一个充分必要的条件。

我们在来回顾一下模型的原问题：

$$
\begin{equation}
    \left\{
        \begin{array}{ll}
        \min\ f(x) & \\
        s.t. \quad m_i(x)\leq 0, \ i = 1, 2, \cdots, M & \\
        \ \; \qquad n_j(x)= 0, \ j = 1, 2, \cdots, N & \\
        \end{array}
    \right.
\end{equation}
$$

而拉格朗日形式的表达为：

$$
\begin{equation}
    \mathcal{L}(x,\lambda) = f(x) + \sum_i \lambda_i m_i(x) + \sum_j \eta_j n_j(x) 
\end{equation}
$$

对于对偶问题，我们可以描述对应的$g(\lambda,\eta) = \min_x \mathcal{L}(x,\eta,\lambda)$；$d\ast \longleftarrow \lambda^\ast,\eta^\ast$。所以对偶问题(Dual Prob)也就是：

$$
\begin{equation}
    \left\{
        \begin{array}{ll}
        \max_{\lambda,\eta}\ g(\lambda,\eta) & \\
        s.t. \quad \lambda_i\geq 0, \ i = 1, 2, \cdots, M & \\
        \end{array}
    \right.
\end{equation}
$$

下面进行KKT条件的推导：

首先一定需要满足的是，在可行域以内。所以，一定会有：$m_i(x^\ast)\leq 0,n_i(x^\ast)=0,\lambda^\ast\geq 0$。并且还需要满足：

$$
\begin{equation}
    \begin{split}
        d^\ast 
        = & \max_{\lambda,\eta} g(\lambda,\eta) = g(\lambda^\ast,\eta^\ast) \\
        = & \min_x \mathcal{L}(x,\lambda^\ast,\eta^\ast) \\
        \leq & \mathcal{L}(x,\lambda^\ast,\eta^\ast),\quad \forall x\in D \\
        = & \mathcal{L}(x^\ast,\lambda^\ast,\eta^\ast) \\
        = & f(x^\ast) + \sum_i \lambda_i m_i(x^\ast) + \sum_j \eta_j n_j(x^\ast) \\
        = & f(x^\ast) + \sum_i \lambda_i m_i(x^\ast) \\
    \end{split}
\end{equation}
$$

上式中的$f(x^\ast)$也就是$p^\ast$，用因为$\lambda_i m_i(x^\ast) \leq 0$是必然存在的。所以，$d^\ast \leq f(x^\ast)$。这就是弱对偶关系，如果是强对偶关系，就需要我们需要在两个小于或等于号那取等才行。

第一，对于$\forall i = 0,1,2,\cdots,M$，都有$\sum_{i}\lambda_im_i = 0$。

第二，$ \min \mathcal{L}(x,\lambda^\ast,\eta^\ast),\quad \forall x\in D = \mathcal{L}(x^\ast,\lambda^\ast,\eta^\ast)$。也就是：

$$
\begin{equation}
    \frac{\partial \mathcal{L}(x,\lambda^\ast,\eta^\ast)}{\partial x}\mid_{x=x^\ast} = 0
\end{equation}
$$

所以，KKT条件就已经完成了，我们总结一下，KKT条件分成3个部分。

1. 可行条件：也就是需要满足定义域的条件，$m_i(x^\ast)\leq 0,n_i(x^\ast)=0,\lambda^\ast\geq 0$。

2. 互补松弛条件：$\lambda_im_i=0$。

3. 梯度为零：$\frac{\partial \mathcal{L}(x,\lambda^\ast,\eta^\ast)}{\partial x}\mid_{x=x^\ast} = 0$。

我们可以对比之前学习的SVM的KKT条件。

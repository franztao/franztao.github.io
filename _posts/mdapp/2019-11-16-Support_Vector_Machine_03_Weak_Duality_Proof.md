---
layout:     post
title:      Support_Vector_Machine_03_Weak_Duality_Proof
subtitle:   2022年10月
date:       2019-11-16
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Support
    - Vector
    - Machine
    - 03
    - Weak
    - Duality
    - Proof
---

在前面我们已经展示的Hard Margin和Soft Margin SVM的建模和求解。前面提到的SVM有三宝，间隔，对偶，核技巧。前面我们已经分析了间隔，大家对于其中用到的对偶，虽然我们用比较直觉性的方法进行了解释，但是估计大家还是有点懵逼。这节我们希望给到通用性的证明，这里实际上就是用到了约束优化问题。

#  {弱对偶性证明}
首先，我们需要证明约束优化问题的原问题和无约束问题之间的等价性。
##    {约束优化问题与无约束问题的等价性}
对于一个约束优化问题，我们可以写成：

$$
\begin{equation}
    \left\{
    \begin{array}{ll}
      \min_{x\in \mathcal{R}^p}f(x) & \\
      s.t. \quad m_i(x) \leq 0,\ i = 1,2,\cdots,N & \\
      \quad \ \; \quad n_i(x) = 0,\ i = 1,2,\cdots,N & \\
    \end{array}
    \right.
\end{equation}
$$

我们用拉格朗日函数来进行表示：

$$
\begin{equation}
    \mathcal{L}(x,\lambda,\eta) = f(x) + \sum_{i=1}^N\lambda_im_i + \sum_{i=1}^N\eta_in_i
\end{equation}
$$

我们可以等价的表示为：

$$
\begin{equation}
    \left\{
    \begin{array}{ll}
      \min_{x}\max_{\lambda,\eta}\  \mathcal{L}(x,\lambda,\eta) & \\
      s.t. \ \lambda_i \geq 0,\ i = 1,2,\cdots,N & \\
    \end{array}
    \right.
\end{equation}
$$

这就是将一个约束优化问题的原问题转换为无约束问题。那么这两种表达形式一定是等价的吗？我们可以来分析一下：

如果，$x$违反了约束条件$m_i(x) \leq 0$，那么有，$m_i(x) > 0$。且$\lambda_i>0$，那么很显然$max_{\lambda}\ \mathcal{L} = + \infty$。

如果，$x$符合约束条件$m_i(x) \leq 0$，那么很显然$max_{\lambda}\ \mathcal{L} \neq + \infty$。

那么：

$$
\begin{equation}
    \min_{x} \max_{\lambda,\eta} \ \mathcal{L}(x,\lambda,\eta) = \min_{x}\left\{ \max\ \mathcal{L}, +\infty \right\} = \min_{x}\left\{ \max\ \mathcal{L} \right\}
\end{equation}
$$

其实大家可以很明显的感觉到，这个等式自动的帮助我们过滤到了一半$m_i(x) \geq 0$的情况，这实际上就是一个隐含的约束条件，帮我们去掉了一部分不够好的解。

##    {证明弱对偶性}
原问题我们可以写为：

$$
\begin{equation}
    \left\{
    \begin{array}{ll}
      \min_{x}\max_{\lambda,\eta}\  \mathcal{L}(x,\lambda,\eta) & \\
      s.t. \ \lambda_i \geq 0,\ i = 1,2,\cdots,N & \\
    \end{array}
    \right.
\end{equation}
$$

而原问题的对偶问题则为：

$$
\begin{equation}
    \left\{
    \begin{array}{ll}
      \min_{\lambda,\eta}\max_{x}\  \mathcal{L}(x,\lambda,\eta) & \\
      s.t. \ \lambda_i \geq 0,\ i = 1,2,\cdots,N & \\
    \end{array}
    \right.
\end{equation}
$$

原问题是一个关于$x$的函数，而对偶问题是一个关于$\lambda,\eta$的最小化问题，而弱对偶性则可以描述为：对偶问题的解$\leq$原问题的解。为了简化表达，后面对偶问题的解我们用$d$来表示，而原问题的解我们用$p$来表示。那么我们用公式化的语言表达也就是：

$$
\begin{equation}
     \min_{\lambda,\eta}\max_{x}\  \mathcal{L}(x,\lambda,\eta) = d \leq  \min_{x}\max_{\lambda,\eta}\  \mathcal{L}(x,\lambda,\eta) = p
\end{equation}
$$

在前面我们使用感性的方法证明了$\max \min \ \mathcal{L} \leq \min \max \ \mathcal{L}$，下面我们给出严谨的证明：

很显然可以得到：

$$
\begin{equation}
    \min_{x}\ \mathcal{L}(x,\lambda,\eta) \leq \mathcal{L}(x,\lambda,\eta) \leq \max_{\lambda,\eta}\ \mathcal{L}(x,\lambda,\eta)
\end{equation}
$$

那么，$\min_{x}\ \mathcal{L}(x,\lambda,\eta)$可表示为一个与$x$无关的函数$A(\lambda,\eta)$，同理$\max_{\lambda,\eta}\ \mathcal{L}(x,\lambda,\eta)$可表示为一个与$\lambda,\eta$无关的函数$B(x)$。显然，我们可以得到一个恒等式：

$$
\begin{equation}
    A(\lambda,\eta) \leq B(x)
\end{equation}
$$

那么接下来就有：

$$
\begin{equation}
    \begin{split}
        A(\lambda,\eta) \leq & \min \ B(x) \\
        \max \ A(\lambda,\eta) \leq & \min \ B(x) \\
         \min_{\lambda,\eta}\max_{x}\  \mathcal{L}(x,\lambda,\eta) \leq & \min_{x}\max_{\lambda,\eta}\  \mathcal{L}(x,\lambda,\eta) 
    \end{split}
\end{equation}
$$

弱对偶性，证毕!!

---
layout:     post
title:      Gaussian_Process_02_Weight_Space
subtitle:   2022年10月
date:       2019-12-14
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Gaussian
    - Process
    - 02
    - Weight
    - Space
---

    

Gaussian Process在这里我们主要讲解的是Gaussian Process Regression。我们从Bayesian Linear Regression的角度来引出的Gaussian Progress Regression。

\section{Recall Bayesian Linear Regression}
首先，我们需要回顾一下Bayesian Linear Regression。

1. 首先对于一个，参数符合的分布，$p(w|Data) = \mathcal{N}(w|\mu_w,\Sigma_w)$。其中，$\mu_w = \sigma^{-2}A^{-1}X^TY$，$\Sigma_w = A^{-1}$，其中，$A=\sigma^{-2}X^TX+\Sigma_p^{-1}$。从这一步我们就成功的得到了在已知Data的情况下，未知参数的分布形式。

2. 在给定一个新的未知数向量$X^\ast$的情况下，我们可以首先利用noise-free形式：$f(x) = w^Tx = x^Tw$，然后再求得noise形式：$y=f(x)+\epsilon$，而$\epsilon \sim \mathcal{N}(0,\sigma^2)$。来获得我们想要的prediction值。这样，我们就可以得到：
\begin{gather}
    p(f(x^\ast)|Data,x^\ast) \sim \mathcal{N}({x^\ast}^T\mu_w, {x^\ast}^T\Sigma_w{x^\ast}) \\
    p(y^\ast|Data,x^\ast) \sim \mathcal{N}({x^\ast}^T\mu_w, {x^\ast}^T\Sigma_w{x^\ast}+\sigma^2)
\end{gather}

但是，问题马上就来了，因为很多时候，我们不能仅仅使用线性分类的方法来解决问题。现实生活中有许多非线性的问题来待我们求解。而一种经常使用的方法，也就是将数据投影到高维空间中来将非线性问题，转换成一个高维空间中的线性可分问题。或者是使用Bayesian Logistics Regression来进行分类。如果，是将数据投影到高维空间中的话，我们很自然的就想到了Kernel Bayesian Linear Regression。

那么这个非线性转换可以被我们写成：If $\phi:x\mapsto z$，$x\in \mathbb{R}^p$，$x\in\mathbb{R}^p$，$z\in\mathbb{R}^q$，$z=\phi(x)$。

\section{非线性转换后的表达}
数据集被我们描述为：$X = (x_1,x_2,\cdots,x_N)^T$，$Y = (y_1,y_2,\cdots,y_N)^T$。根据之前我们得到的Bayesian Linear Regression结果，我们代入可以得到：
\begin{equation}
    p(f(x^\ast)|X,Y,x^\ast) \sim \mathcal{N}({x^\ast}^T(\sigma^{2}A^{-1}X^TY),{x^\ast}^TA^{-1}x^\ast)
\end{equation}

而其中，$A = \sigma^{-2}X^TX+\Sigma_p^{-1}$，If $\phi:x\mapsto z$，$x\in \mathbb{R}^p$，$x\in\mathbb{R}^p$，$z\in\mathbb{R}^q$，$z=\phi(x)$(q>p)。这里的$\phi$是一个非线性转换。我们定义：$\Phi=(\phi(x_1),\phi(x_2),\cdots,\phi(x_N))^T_{N\times q}$。

转换之后为：$f(x) = \phi(x)^Tw$。那么，
\begin{equation}
    p(f(x^\ast)|X,Y,x^\ast) \sim \mathcal{N}(\sigma^{-2}{\phi(x^\ast)}^T(A^{-1}\Phi(X)^TY),{\phi(x^\ast)}^TA^{-1}\phi(x^\ast))
\end{equation}

而其中，$A=\sigma^{-2}\Phi(X)^T\Phi(X) + \Sigma_p^{-1}$。但是，很快我们又将面临一个新的问题，也就是$A^{-1}$应该如何计算呢？这里我们需要使用到一个公式为，{ Woodbury Formula公式：
\begin{equation}
    (A+UCV)^{-1} = A^{-1}-A^{-1}U(C^{-1}+VA^{-1}U)^{-1}VA^{-1}
\end{equation}
}

所以，
\begin{gather}
    \nonumber A=\sigma^{-2}\Phi(X)^T\Phi(X) + \Sigma_p^{-1} \\
    A\Sigma_p=\sigma^{-2}\Phi(X)^T\Phi(X)\Sigma_p + I \\
    \nonumber A\Sigma_p\Phi(X)^T=\sigma^{-2}\Phi(X)^T\Phi(X)\Sigma_p \Phi(X)^T + \Phi(X)^T =  \sigma^{-2}\Phi(X)^T(K+\sigma^2I)\\
    \nonumber \sigma^{-2}A^{-1}\Phi(X)^T = \Sigma_p\Phi(X)^T(K+\sigma^2I)^{-1}
\end{gather}

然后，两边同乘一个$\phi(x^\ast)$和$Y$就可以得到：
\begin{equation}
    \sigma^{-2}\phi(x^\ast)A^{-1}\Phi(X)^TY = \phi(x^\ast)\Sigma_p\Phi(X)^T(K+\sigma^2I)^{-1}Y 
\end{equation}

而这个$\sigma^{-2}\phi(x^\ast)A^{-1}\Phi(X)^TY$正好就是$p(f(x^\ast)|X,Y,x^\ast)$'s Expectation。而这里的$\Sigma_p=p(w)$是一个先验$\sim \mathcal{N}(0,\Sigma_p)$，而$\sigma^2$为先验分布的噪声，$X^\ast$是一个new input，而{ $K = \Phi\Sigma_p\Phi^T$}。所以，使用类似的方法我们可以得到，$p(f(x^\ast)|X,Y,x^\ast)$'s Covarience为：$\phi(x^\ast)^T\Sigma_p\phi(x^\ast) - \phi(x^\ast)^T\Sigma_p\Phi(X)^T(K+\sigma^2I)^{-1}\Phi(X)\Sigma_p\phi(x^\ast)$。所以：
\begin{equation}
    p(f(x^\ast)|X,Y,x^\ast) \sim \mathcal{N}(\phi(x^\ast)\Sigma_p\Phi(X)^T(K+\sigma^2I)^{-1}Y , \phi(x^\ast)^T\Sigma_p\phi(x^\ast) - \phi(x^\ast)^T\Sigma_p\Phi(X)^T(K+\sigma^2I)^{-1}\Phi(X)\Sigma_p\phi(x^\ast) )
\end{equation}

而大家注意观察一下，下面几个等式：
\begin{equation}
    \phi(x^\ast)^T\Sigma_p\Phi^T \qquad \phi(x^\ast)^T\Sigma_p\phi(x^\ast) \qquad
    \Phi\Sigma_p\Phi^T \qquad
    \Phi\Sigma_p\phi(x^\ast) 
\end{equation}

我们再来谢谢这里的这个$\Phi$是个什么东西？
\begin{equation}
    \Phi_{N\times q} = (\phi(x_1),\phi(x_2),\cdots,\phi(x_N))^T_{N\times q}
\end{equation}

所以大家想一想就知道了，公式(9)中的四个公式实际上是一个东西，而$\Phi(X)$只不过是将多个向量拼接在了一起而已。而$K(x,x')=\phi(x)^T\Sigma_p\phi(x')$，$x,x'$是两个不一样的样本，矩阵展开以后，形式都是一样的。那么下一个问题就是$K(x,x')$是否可以表达为一个Kernel Function的形式？那么，相关的探究就变得有趣了。

\section{Kernel Trick}
因为$\Sigma_p$是一个positive define matrix，并且它也是symmetry的。所以，令$\Sigma_p = (\Sigma_p^{\frac{1}{2}})^2$。那么，我们可以做如下的推导：
\begin{equation}
    \begin{split}
        K(x,x') 
        = & \phi(x)^T\Sigma_p^{\frac{1}{2}}\Sigma_p^{\frac{1}{2}}\phi(x') \\
        = & (\Sigma_p^{\frac{1}{2}}\phi(x))^T\cdot \Sigma_p^{\frac{1}{2}}\phi(x) \\
        = & <\varphi(x),\varphi(x')>
    \end{split}
\end{equation}

其中，$\varphi(x) = \Sigma_p^{\frac{1}{2}}\phi(x)$。那么，我们利用Kernel Trick可以有效的避免求$\phi(X)$，而是直接通过$K(x,x')$中包含的高维空间的转化。而{ Bayesian Linear Regression + Kernel Trick中就蕴含了一个Non-Linear Transformation inner product。}我们就可以将这个转换定义到一个核空间中，避免了直接来求这个复杂的转化。这也就是Kernel Trick。

看到了这里，大家很容易会产生一个疑惑，那就是，好像这里的GPR并没有和GP有一毛钱的关系。而实际上这里的GPR有两种不同的思考角度，也就是两种View，而这两种View可以得到equal result：

1. Weight-Space view，也就是我们这一小节所讲的东西。指的就是那两个等式，$f(x) = \phi(x)^Tw$和$y=f(x)+\epsilon$。在这里我们的研究对象就是$w$，假设$w$的先验，需要求得$w$的后验，所以是从Weight-Space的角度分析的。

2. Function-Space view，我们将$f(x)$看成是一个随机变量，$f(x)\sim GP(m(x),K(x,x'))$。这个我们会在后面的小节中进行详细的描述，大家就可以看到GP的思想在其中的运用了。

~\\

而有一句话对GPR的总结，非常的有意思，Gaussian Process Regress is the extension of Bayesian Linear Regression with kernel trick. 仔细想一想就知道了，我们把逻辑思路理一下，我们想用贝叶斯练习回归来解决非线性的问题，所以我们需要把输入空间投射到一个高维空间中，低维空间中的线性不可分问题将可以转化为高维空间中的线性可分问题。那么，我们就需要一个转换函数来完成这个工作，但是这个转换函数怎么求？有可能会很难求，而且维度很高。那么，我们就不求了，直接使用核技巧，也就是两个向量的内积等于一个核函数的值就可以了。这大概就是
本节中Weight-Space View的一个主线的思路。













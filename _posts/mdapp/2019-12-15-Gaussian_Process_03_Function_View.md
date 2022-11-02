---
layout:     post
title:      Gaussian_Process_03_Function_View
subtitle:   2022年10月
date:       2019-12-15
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Gaussian
    - Process
    - 03
    - Function
    - View
---

    
\maketitle
在上一小节中，我们从Weight-Space View来看Gaussian Process Regression，好像和Gaussian Process并没有什么关系。但是这一小节，我们从函数的角度来看就可以看到了。
\section{Recall Gaussian Process}
对于一组随机变量$\{ \xi_t \}_{t\in T}$，$T:$ continuous space or time。If：$\forall n \in N^+ \ (n\geq 1)$，Index：$\{t_1,t_2,\cdots,t_n \}$

\noindent $\longrightarrow$ random variable：$\{\xi_{t_1},\xi_{t_2},\cdots,\xi_{t_n}\}$。令$\xi_{1:n} = \{\xi_{t_1},\xi_{t_2},\cdots,\xi_{t_n}\}^T$。If $\xi_{1:n} \sim \mathcal{N}(\mu_{1:n},\Sigma_{1:n})$，那么我们称$\{ \xi_t \}_{t\in T}$ is a Gaussian Distribution。并且，$\xi_t \sim GP(m(t),k(t,s))$，$m(t)$为mean function，$k(t,s)$为covariance function。下面我们回到Weight-Space View中。

\section{Weight-Space view to Function-Space view}
在这里$w$是一个先验分布，$f(x)$是一个随机变量。$f(x) = \phi(x)^Tw,\ y = f(x)+\epsilon,\ \epsilon \sim \mathcal{N}(0,\sigma^2)$。在Bayesian的方法中，对于给定的先验信息(prior)：$w\sim \mathcal{N}(0,\Sigma_p)$。因为，$f(x) = \phi(x)^Tw$，所以可以得到：
\begin{equation}
    \mathbb{E}_w[f(x)] = \mathbb{E}_w[\phi(x)^Tw] =  \phi(x)^T\mathbb{E}_w[w] = 0
\end{equation}

那么对于$\forall x,x'\in \mathbb{R}^p$，
\begin{equation}
    \begin{split}
        cov(f(x),f(x')) 
        = & \mathbb{E}[(f(x)-\mathbb{E}[f(x)])(f(x')-\mathbb{E}[f(x')])] \\
        = & \mathbb{E}[f(x)f(x')] \\
        = & \mathbb{E}[\phi(x)^Tw\phi(x')^Tw] \\
        = & \mathbb{E}[\phi(x)^Tww^T\phi(x')] \\
    \end{split}
\end{equation}

因为$\phi(x')^Tw$的结果是一个实数，所以它的转置就等于它自己。又因为$w\sim \mathcal{N}(0,\Sigma_p)$，均值为0，协方差为$\Sigma_p$。并且有$\mathbb{E}[ww^T] = \mathbb{E}[(w-0)(w^T-0)]$，这个东西不就是协方差矩阵$cov(w) = \Sigma_p$。

而$\phi(x)^T\Sigma_p\phi(x')$是一个kernel function，前面我们已经证明过了，$\varphi(x) = \Sigma_p^{\frac{1}{2}}$。而$\phi(x)\Sigma_p\phi(x') = <\varphi(x),\varphi(x')> = K(x,x')$。

推导进行到了这里，我们就知道了$f(x)$的期望为0，协方差矩阵为一个核函数$K(x,x')$。那么我们是不是惊奇的发现，这个和我们高斯过程的定义：$\xi_t \sim GP(m(t),K(t,s))$，是多么惊人的相似呀。所以，这里可以启发我们：{ $f(x)$的组成是否可以看成一个GP，而$\{f(x)\}_{x\in\mathbb{R}^p}$。}那么，首先$f(x)$是一个function，而且$f(x)$还是一个服从高斯分布的随机变量，$m(t)$是一个mean function，$K(t,s)$是一个covariance function。为了加深大家的理解，我们做进一步清晰的对比：
\begin{equation}
    \left\{
        \begin{array}{ll}
            t \longrightarrow \xi_t, \ \{ \xi_t \}_{t\in T}\sim GP & \\
            x \longrightarrow f(x), \ \{ f(x) \}_{x\in \mathbb{R}^p}\sim GP & \\
\end{array}
\right.
\end{equation}

其实，我这样一对比，就非常的清晰了。在GPR的算法中，

1. Weight-Space view中关注的是$w$，即为：
\begin{equation}
    x^\ast \longrightarrow y^\ast \quad p(y^\ast|Data,x^\ast) = \int p(y^\ast|Data,x^\ast,w)p(w)dw
\end{equation}

又因为$w$本身就是从Data中，推导得到的，所以$p(y^\ast|Data,x^\ast,w) = p(y^\ast|x^\ast,w)$。

2. Function-Space view中关注的是$f(x)$，即为：
\begin{equation}
    p(y^\ast | Data,x^\ast)  = \int p(y^\ast | f(x),x^\ast)p(f(x))df(x)
\end{equation}

写到了这里，不知道大家有没有一定感觉了，这里就是把$f(x)$当成了一个随机变量来看的。这里也就是通过$f(x)$来直接推导出$y^\ast$。在Weight-Space View中，我们没有明确的提到GP，但是在Weight-Space view中，$f(x)$是符合GP的，只不过是没有显性的表示出来而已。我们可以用一个不是很恰当的例子来表述一个，Weight-Space view就是两个情侣之间，什么都有了，孩子都有了，但是就是没有领结婚证，那么他们两个之间的关系就会比较复杂。而Function-Space view就是两个情侣之间先领结婚证，在有了孩子，按部就班的来进行，所以他们之间的关系就会比较简单。

\section{Function-Space View}
上一小节中，我们从Weight-Space View过渡到了Function-Space View，而Weight指的就是参数。
\begin{equation}
    \begin{split}
        & \{f(x)\}_{x\in\mathbb{R}^p}\sim GP(m(x),K(x,x')) \\
        & m(x) = \mathbb{E}[f(x)] \quad K(x,x') = \mathbb{E}[(f(x)-m(x))(f(x')-m(x'))]
    \end{split}
\end{equation}

Regression问题被我们描述为：

Data：$\{ (x_i,y_i) \}_{i=1}^N$，$x=(x_1,x_2,\cdots,x_N)^T_{N\times p}$，$Y=(y_1,y_2,\cdots,y_N)^T_{N\times 1}$。又因为$f(x)$符合一个GP，所以，$f(x) \sim \mathcal{N}(\mu(x),K(x,x'))$。且$Y=f(x)+\epsilon$，所以$Y\sim \mathcal{N}(\mu(x),K(x,x')+\sigma^2I)$。那么，给定new input：$X^\ast = (x_1^\ast,x_2^\ast,\cdots,x_N^\ast)$，我们想要的Prediction output为$Y^\ast = f(x^\ast) + \epsilon$。那么，我们可以得到$Y$和$f(x^\ast)$的联合概率密度分布为：
\begin{equation}
    \begin{bmatrix}
        Y \\
        f(x^\ast)
    \end{bmatrix}
\sim
\mathcal{N}\left(
    \begin{bmatrix}
        \mu(x) \\
        \mu(x^\ast)
    \end{bmatrix}
    ,
    \begin{bmatrix}
        K(X,X)+\sigma^2I & K(X,X^\ast) \\
        K(X^\ast,X) & K(X^\ast,X^\ast) \\
    \end{bmatrix}
\right)
\end{equation}

在这里，我必须要首先列举一下，前面我们曾经提到的更加联合概率密度求边缘概率密度的方法。

已知，$X\sim \mathcal{N}(\mu,\Sigma)$，
\begin{equation}
    \begin{split}
        x = 
        \begin{bmatrix}
            x_a \\
            x_b
        \end{bmatrix}
        \qquad
        \mu = 
        \begin{bmatrix}
            \mu_a \\
            \mu_b
        \end{bmatrix}
        \qquad
        \Sigma = 
        \begin{bmatrix}
            \Sigma_{aa} & \Sigma_{ab}\\
            \Sigma_{ba} & \Sigma_{bb}\\
        \end{bmatrix}
    \end{split}
\end{equation}

而我们可以得到：
\begin{equation}
    \begin{split}
        & p(x_b|x_a)\sim \mathcal{N}(\mu_{b|a},\Sigma_{b|a}) \\
        & \mu_{b|a} = \Sigma_{ba}\Sigma_{aa}^{-1}(x_a - \mu_a)+\mu_b \\
        & \Sigma_{b|a} = \Sigma_{bb} - \Sigma_{ba}\Sigma_{aa}^{-1}\Sigma_{ab} \\
    \end{split}
\end{equation}

我们要求的概率为$p(f(x^\ast)|Y,X,x^\ast)$，就是一个我们要求的条件概率，有的同学可能就会有疑惑了，不应该是$p(f(x\ast)|Y)$吗？为什么这里可以把$X,x^\ast$给忽略掉了？因为$X$和$Y$相关，因为$Y=\phi(X)^Tw+\epsilon$。而$X^\ast$涵盖在了$f(x^\ast)$中，因为$f(x^\ast) = \phi(X^\ast)^Tw$。


所以，我们的目标也就是求$p(f(x\ast)|Y$，也就是{已知联合概率分布的情况下求条件概率分布。}

我们对比公式(8)和公式(9)就可以发现，$Y\rightarrow x_a,f(x^\ast)\rightarrow x_b,K(X,X)+\sigma^2I \rightarrow \Sigma_{aa},K(X,X^\ast) \rightarrow \Sigma_{ba},K(X\ast,X\ast)\rightarrow \Sigma_{bb}$。那么，我们可以令$p(f(x^\ast)|Y,X,x^\ast)\sim\mathcal{N}(\mu^\ast,\Sigma^\ast)$，代入之前获得的公式的结果我们就可以得到：
\begin{equation}
    \begin{split}
        \mu^\ast = & K(X^\ast,X)(K(X,X)+\sigma^2I)^{-1}(Y-\mu(X))+\mu(X^\ast) \\
        \Sigma^\ast = & 
        K(X^\ast,X^\ast)-K(X^\ast,X)(K(X,X)+\sigma^2I)^{-1}
    \end{split}
\end{equation}

并且，$y\ast = f(X^\ast) + \epsilon$。那么noise-free的形式可以被我们写完：$p(f(x^\ast)|Y,X,x^\ast) = \mathcal{N}(\mu^\ast,\Sigma^\ast)$。而$p(f(y^\ast)|Y,X,x^\ast) = \mathcal{N}(\mu^\ast_y,\Sigma^\ast_y)$，而$y^\ast = f(X^\ast) + \epsilon$，而$\mu_{y}^\ast = \mu^{\ast}$，$\Sigma_y^{\ast} = \Sigma^\ast + \sigma^2I$。

~\\

在Function-Space View中，$f(x)$本身是符合GP的，那么我们可以直接写出$Prediction$矩阵，并将其转化为已知联合概率密度分布求条件概率密度的问题。Function-Space View和Weight-Space View得到的结果是一样的，但是更加的简单。






















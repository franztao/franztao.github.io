---
layout:     post
title:      Kernel_Method_02_The_Definition_of_Positive_Kernel_Function
subtitle:   2022年10月
date:       2019-11-21
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Kernel
    - Method
    
    - The
    - Definition
    - of
    - Positive
    - Kernel
    - Function
---

上一节中，我们已经讲了什么是核函数，也讲了什么是核技巧，以及核技巧存在的意义是什么。我们首先想想，上一小节我们提到的核函数的定义。

对于一个映射$K$，我们有两个输入空间$\mathcal{X}\times\mathcal{X},\mathcal{X}\in\mathbb{R}^p$，可以形成一个映射$\mathcal{X}\times \mathcal{X}\mapsto\mathbb{R}$。对于，$\forall\ x,z \in \mathcal{X}$，存在一个映射$\phi:\mathcal{X}\mapsto \mathbb{R}$，使得$K(x,z)=<\phi(x),\phi(z)>$。那么这个$K(\cdot)$，就被我们称为核函数。(<>代表内积运算)

这既是我们上一节中将的核函数的定义，实际上这个核函数的精准定义，应该是正定核函数。在本小节中，我们将会介绍核函数的精准定义，什么是正定核函数？并介绍内积和希尔伯特空间(Hilbert Space)的定义。这一小节虽然看着会有些枯燥，实际上非常的重要。

#  核函数的定义}
核函数的定义，也就是对于一个映射$K$，存在一个映射$\mathcal{X}\times\mathcal{X}\mapsto \mathbb{R}$，对于$x,z\in \mathcal{X}$都成立，则称$K(x,z)$为核函数。

对比一下，我们就会发现，这个定义实际上比我们之前学的定义要简单很多。好像是个阉割版，下面我们来介绍两个正定核的定义方法。

#  正定核的定义}
正定核函数的定义有两个，我首先分别进行描述一下：

##    第一个定义}
现在存在一个映射$K:\mathcal{X}\times\mathcal{X}\mapsto\mathbb{R}$。对于$\forall x,z \in \mathcal{X}$。如果存在一个$\phi:\mathcal{X}\mapsto \mathbb{R}^p$，并且$\phi(x)\in\mathcal{H}$，使得$K(x,z) = <\phi(x),\phi(z)>$，那么称$K(x,z)$为正定核函数。

##    第二个定义}
对于一个映射$K:\mathcal{X}\times\mathcal{X}\mapsto\mathbb{R}$，对于$\forall x,z\in \mathcal{X}$，都有$K(x,z)$。如果$K(x,z)$满足，1. 对称性；2. 正定性；那么称$K(x,z)$为一个正定核函数。

我们来分析一个，首先什么是对称性？这个非常的好理解，也就是$K(x,z)=K(z,x)$。那么什么又是正定性呢？那就是任取$N$个元素，$x_1,x_2,\cdots,x_N\in \mathcal{X}$，对应的Gram Matrix是半正定的，其中Gram Matrix用$K$来表示为$K=[K(x_i,x_j)]$。

对于第一个对称性，我们其实非常好理解，不就是内积嘛！有一定数学功底的同学一定知道，内积和距离是挂钩的，距离之间一定是对称的。那么正定性就要好好讨论一下了。我们知道这两个定义之间是等价的，为什么会有正定性呢？我们需要进行证明，这个证明可以被我们描述为：

$$
\begin{center}
    {
    $K(x,z) = <\phi(x),\phi(z)> \Longleftrightarrow$ Gram Matrix是半正定矩阵
    }
\end{center}
$$

这个等式的证明我们留到下一节再来进行，这里我们首先需要学习一个很重要的概念叫做，希尔伯特空间($\mathcal{H}$:Hilbert Space)。小编之前被这个概念搞得头晕，特别还有一个叫再生核希尔伯特空间的玩意，太恶心了。

#  Hilbert Space ($\mathcal{H}$)}
{ Hilbert Space是一个完备的，可能是无限维的，被赋予内积运算的线性空间。}下面我们对这个概念进行逐字逐句的分析。

\textbf{线性空间}：也就是向量空间，这个空间的元素就是向量，向量之间满足加法和乘法的封闭性，实际上也就是线性表示。空间中的任意两个向量都可以由基向量线性表示。

\textbf{完备的}：完备性简单的认为就是对极限的操作是封闭的。我们怎么理解呢？若有一个序列为$\{K_n\}$，这里强调一下Hilbert Space是一个函数空间，空间中的元素就是函数。所以，$K_n$就是一个函数。那么就会有：

$$
\begin{equation}
    \lim_{n\longrightarrow +\infty} K_n = K \in \mathcal{H}
\end{equation}
$$

所以，我们理解一下就是会和无限维这个重要的概念挂钩。我理解的主要是Hilbert Space在无限维满足线性关系。

\textbf{内积}：内积应该满足三个定义，1. 正定性；2. 对称性；3. 线性。下面我们逐个来进行解释：

1. 对称性：也就是$f,g\in \mathcal{H}$，那么就会有$<f,g> = <g,f>$。其中，$f,g$是函数，我们可以认为Hilbert Space是基于函数的，向量是一个特殊的表达。其实，也就是函数可以看成一个无限维的向量。大家在这里是不是看到了无限维和完备性的引用，他们的定义之间是在相互铺垫的。

2. 正定性：也就是$<f,f> \leq 0$，等号当且仅当$f=0$是成立。

3. 线性也就是满足：$<r_1f_1+r_2f_2, g> = r_1<f_1,g>+r_2<f_2,g>$。

描述上述三条性质的原因是什么呢？也就是我们要证明一个空间中加入一些运算。如果，判断这个运算是不是内积运算，我们需要知道这个运算满不满足上述三个条件。

~\\

现在我们介绍了大致的基本概念了，我们回到这样一个问题，对于正定核我们为什么要有两个定义？这个思想和我们之前学到的Kernel Trick非常的类似了，Kernel Trick跳过了寻找$\phi$这个过程。因为，直接用定义不好找，$
\phi(x)$非常的难找，特别是将函数看成一个无限维的向量。这个$\phi(x)$怎么找？找的到个鬼。那么，我们也想跳过这个寻找$\phi(x)$这个过程。那么这就是第二个定义存在的意义，虽然，第二个定义没有第一个定义那么简洁。第二个定义给了我们一个判断核函数的好办法，直接跳过了寻找$\phi(x)$这个过程。那么这两定义之间是否等价？废话，肯定是等价的呀，哈哈哈。那么，我们下一小节中来证明一下。

---
layout:     post
title:      Markov_Chain_Monte_Carlo_04_Gibbs_Sampling
subtitle:   2022年10月
date:       2022-10-30
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Markov
    - Chain
    - Monte
    - Carlo
    - 04
    - Gibbs
    - Sampling
---
            

\maketitle
如果我们要向一个高维的分布$P(Z) = P(Z_1,Z_2,\cdots,Z_N)$中进行采样。那么我们怎么来进行采样呢？我们的思想就是一维一维的来，在对每一维进行采样的时候固定住其他的维度，这就是Gibbs Sampling。

我们首先规定一个$z_{-i}$是去除$z_i$后的序列，$\{ z_1,z_2,\cdots,z_{i-1},z_{i+1},\cdots,z_N \}$。
\section{A Example}
假设$t$时刻，我们获得的样本为$z_1^{(t)},z_2^{(t)},z_3^{(t)}$。

那么$t+1$时刻，我们的采样顺序为：
\begin{equation}
    \begin{split}
        & z_1^{(t+1)} \sim P(z_1|z_2^{(t)},z_3^{(t)}) \\
        & z_2^{(t+1)} \sim P(z_2|z_1^{(t+1)},z_3^{(t)}) \\ 
        & z_3^{(t+1)} \sim P(z_3|z_1^{(t+1)},z_2^{(t+1)})
    \end{split}
\end{equation}

从这个例子中，我们应该可以大致理解固定其他的维度然后进行一维一维采样的意思了。而实际上Gibbs是一种特殊的MH采样，为什么呢？我们来证明一下。

\section{接受率$\alpha$的计算}
我们首先回顾一下，MH采样的方法。我们的目的是从$Q(Z|Z^{(t)})$中采样获得$Z^\ast$，然后计算接受率
\begin{equation}
    \alpha = \min \left( 1, \frac{P(Z^\ast)Q(Z|Z^\ast)}{P(Z)Q(Z^\ast|Z)}  \right)
\end{equation}

首先我们来看$Q(Z|Z^{(t)})$：
\begin{equation}
    \begin{split}
        Q(Z|Z^{(t)}) = Q(Z_i,Z_{-i}|Z^{(t)}_i,Z^{(t)}_{-i})
    \end{split}
\end{equation}

假设我们现在是在对第$i$维进行采样，我们只要关注$P(Z_i^\ast | Z_{-i})$。所以，我们可以得到：$Q(Z|Z^{(t)}) = P(Z_i^\ast | Z_{-i}^{(t)})$。

已经成功的将$Q(Z|Z^{(t)})$做了等价转换以后。那么我们想要求的$\alpha$可以被我们成功的转换成如下的形式：
\begin{equation}
    \alpha = \min \left( 1, \frac{P(Z^\ast_{i}|Z^\ast_{-i})P(Z^\ast_{-i})P(Z_i|Z^\ast_{-i})}{P(Z_i|Z_{-i})P(Z_{-i})P(Z^\ast_i|Z_{-i})} \right)
\end{equation}

计算到了这里，我们还是不好进行计算，上面和下面好像还是不好消除。如果我们可以得到$Z_{-i}^\ast$和$Z_{-i}$之间的关系就好了。下面我们会得出一个重要的结论来帮助我们计算$\alpha$的具体值。首先我们来举一个例子：

那么假设当$t=1$的时刻，有一个样本为：$Z_1^{(1)},Z_2^{(1)},Z_3^{(1)}$。

当$t=2$的时刻，我们假设先对第一维进行采样就可以得到：$Z_1^{(2)},Z_2^{(1)},Z_3^{(1)}$。

很显然$Z_2^{(1)},Z_3^{(1)}$根本没有发生变化。我们可以得到$Z_{-1} = Z_{-1}^\ast$。也就是在Gibbs采样时，采样前后只关注于一个维度，其他的维度我们都没有关注到。所以就可以得到结论：
\begin{equation}
    Z_{-i} = Z_{-i}^\ast
\end{equation}

那么，我们把这个结论代入到公式(4)中，就可以得到：
\begin{equation}
    \alpha = \min \left( 1, \frac{P(Z^\ast_{i}|Z^\ast_{-i})P(Z^\ast_{-i})P(Z_i|Z^\ast_{-i})}{P(Z_i|Z_{-i}^\ast)P(Z_{-i}^\ast)P(Z^\ast_i|Z_{-i}^\ast)} \right) = 1
\end{equation}

那么计算出接受率为1，也就是每次都必定被接受。所以，每次从$Q(Z|Z^{(t)}) = P(Z_i^\ast|Z_{-i})$中进行采样得到$Z^\ast_{i}$即可，一维一维的进行采样就可以采到整个高维的分布，各个维度上的样本。

所以，解释到了这里，大家基本就可以知道Gibbs Samplings是$\alpha = 1$的MH Sampling的意义了。在Gibbs Sampling中$\alpha=1$，而且状态转移矩阵$Q(Z|Z^{(t)}) = P(Z^\ast_{i}|Z^{(t)}_{-i})$，所以Gibbs Sampling就是把目标分布$P$对应的条件概率当作状态转移分布$Q$。

这里我们需要额外提醒一下，使用Gibbs Sampling是有使用前提的，也就是固定其他维度后的一维分布时方便进行采样的，如果固定其他维度的时候得到的一维分布仍然是非常难进行采样的，那么使用Gibbs Sampling也是没有用的。


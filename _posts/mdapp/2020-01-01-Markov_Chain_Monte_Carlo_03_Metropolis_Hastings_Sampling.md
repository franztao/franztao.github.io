---
layout:     post
title:      Markov_Chain_Monte_Carlo_03_Metropolis_Hastings_Sampling
subtitle:   2022年10月
date:       2020-01-01
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Markov
    - Chain
    - Monte
    - Carlo
    - 03
    - Metropolis
    - Hastings
    - Sampling
---

    

上一节中我们讲解了Detailed Balance，这是平稳分布的充分必要条件。Detailed Balance为：

$$
\begin{equation}
    \pi(x)P(x\mapsto x^\ast) = \pi(x^\ast)P(x^\ast \mapsto x)
\end{equation}
$$

这里的$P(x\mapsto x^\ast)$实际上就是条件概率$P(z^\ast|x^\ast)$，这样写只是便于理解。

首先，我们需要明确一点，我们想要求的是后验概率分布$P(Z)$，也就是我们推断问题的核心目标。我们求$P(Z)$主要是为了求在$P(Z)$概率分布下的一个相关函数的期望，也就是：

$$
\begin{equation}
    \mathbb{E}_{P(Z)}[f(Z)] \approx \frac{1}{N} \sum_{i=1}^N f(z^{(i)})
\end{equation}
$$

而我们是通过采样来得到$P(Z) \sim \{ z^{(1)},z^{(2)},\cdots, z^{(N)} \}$样本点。$\pi(x)$是最终的平稳分布，可以看成我们这里的$P(Z)$，下面的问题就是求出概率转移矩阵$P_{ij}$，才能满足Detailed Balance条件。知道了上面的条件以后，我们每次这样进行采样，$x_1\sim P(x|x_1)$，$x_2\sim P(x|x_1)$，$x_3\sim P(x|x_2)$，$\cdots$，$x_N$。最终就可以得到我们想要的$N$个样本。

#  {Proposal Matrix}
那我们怎么来找这个状态转移矩阵$P_{ij}$呢？首先我们可以随机一个状态转移矩阵$Q_{ij}$，也就是Proposal Matrix。

那么肯定是：

$$
\begin{equation}
    P(Z)Q(Z^\ast|Z)  \neq P(Z^\ast)Q(Z|Z^\ast)
\end{equation}
$$

那么我们就要想办法找到$Q_{ij}$使得：

$$
\begin{equation}
    P(Z)Q(Z^\ast|Z)  = P(Z^\ast)Q(Z|Z^\ast)
\end{equation}
$$

那么，我们怎么来解决这个问题呢？我们可以在左右两边乘上一个因子来解决这个问题。也就是，

$$
\begin{equation}
    P(Z)\underbrace{Q(Z^\ast|Z)\alpha(Z^\ast,Z)}_{P(Z\mapsto Z^\ast)}  = P(Z^\ast)\underbrace{Q(Z|Z^\ast)\alpha(Z,Z^\ast)}_{P(Z^\ast\mapsto Z)}
\end{equation}
$$

而$\alpha(z,z^\ast)$定义为接收率，大小为：

$$
\begin{equation}
    \alpha(z,z^\ast) 
    = \min \left( 1, \frac{P(Z^\ast)Q(Z|Z^\ast)}{P(Z)Q(Z^\ast|Z)}  \right)
\end{equation}
$$

这样定义就行了？就可以满足Detailed Balance吗？我们可以证明一下，

$$
\begin{equation}
    \begin{split}
        P(Z)Q(Z^\ast|Z)\alpha(Z,Z^\ast) 
        = & P(Z)Q(Z^\ast|Z)\min \left( 1, \frac{P(Z^\ast)Q(Z|Z^\ast)}{P(Z)Q(Z^\ast|Z)}  \right) \\
        = & \min (P(Z)Q(Z^\ast|Z), P(Z^\ast)Q(Z|Z^\ast)) \\
        = & P(Z^\ast)Q(Z|Z^\ast) \min \left( \frac{P(Z)Q(Z^\ast|Z)}{P(Z^\ast)Q(Z|Z^\ast)}, 1 \right) \\
        = & P(Z^\ast)Q(Z|Z^\ast)\alpha(Z^\ast,Z) 
    \end{split}
\end{equation}
$$

那么我们就成功的证明了：

$$
\begin{equation}
    P(Z)\underbrace{Q(Z^\ast|Z)\alpha(Z^\ast,Z)}_{P(Z\mapsto Z^\ast)}  = P(Z^\ast)\underbrace{Q(Z|Z^\ast)\alpha(Z,Z^\ast)}_{P(Z^\ast\mapsto Z)}
\end{equation}
$$

所以，$P(Z)$在转移矩阵$Q(Z|Z^\ast)\alpha(Z^\ast,Z)$下是一个平稳分布，也就是一个马尔可夫链，通过在这个马尔可夫链中采样就可以得到我们的相应的数据样本点了。实际上这就是大名鼎鼎的Metropolis-Hastings采样法。

#  {Metropolis-Hastings Sampling}
第一步，我们从一个均匀分布中进行采样，$u\sim U(0,1)$；

第二步，从$Q(Z|Z^{(i-1)})$中进行采样得到样本点$Z^\ast$；

第三步，计算接受率，$\alpha = \min \left( 1, \frac{P(Z^\ast)Q(Z|Z^\ast)}{P(Z)Q(Z^\ast|Z)}  \right)$。注意，这里的$P(Z) = \frac{\hat{P}(Z)}{Z_p}$。其中$Z_p$指的是归一化因子，几乎非常难以计算，所以一般是未知的。而$\hat{P}(Z) = $ likelihood $\times$ prior。所以这里的$P(Z)$和$P(Z^\ast)$就是$\hat{P}(Z)$和$\hat{P}(Z^\ast)$。由于归一化因子被抵消了，干脆就直接写成了$P(Z)$和$P(Z^\ast)$。

第四步，如果$u \leq \alpha$时$Z^{i} = Z^\ast$，不然$Z^{i} = Z^{(i-1)}$。

这样执行了$N$次，就可以得到$\{ Z^{(1)},Z^{(2)},\cdots,Z^{(N)} \}$个样本点。


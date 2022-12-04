---
layout:     post
title:      Kalman_Filter_01_Introduction
subtitle:   2022年10月
date:       2020-01-16
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Kalman
    - Filter
    
    - Introduction
---

    

我们知道在概率图模型中，加入了time的因素，就得到了Dynamic Model，实际上也就说我们通常所说的State Space Model。

\textbf{如果状态是离散的}，就是我们上一节提到了Hidden Markov Model (HMM)；\textbf{如果状态是连续的}，如果状态之间的关系是线性的，就是Linear Dynamic System (Kalman Filter)，或者说是Linear Gaussian Model；如果状态之间的关系是Non-Linear的或者Non-Gaussian的，那么也就是Particle Filter。我们这一章主要描述的就是Kalman Filter。

#  Dynamic Model Introduction}
第一类问题，Learning问题，即为在已知观测序列$O$的情况下求解$P(\pi|O)$。其中，模型可以描述为$\pi\{ \lambda,\mathcal{A},\mathcal{B} \}$。代表性的就是Hidden Markov Model。

第二类问题就是Inference问题，大致可以分为Decoding，Probability of Evidence，Filtering，Smoothing和Prediction五类问题。这里中Hidden Markov Model 05 Conclusion我们有非常详细的描述。详情可以关注Hidden Markov Model。

#  Kalman Filtering: Linear Gaussian Model}
Filtering问题就是求$P(z_t|x_1,x_2,\cdots,x_t)$，实际上就是一个Marginal Posterior问题。对于Linear关系，Linear主要反映在相邻时刻的两个状态之间的转移关系，当前时刻的隐变量状态和观测状态之间的关系。描述如下所示：

$$
\begin{equation}
    \begin{split}
        & z_t = A\cdot z_{t-1} + B + \epsilon \\
        & x_t = C\cdot z_{t} + D + \delta
    \end{split}
\end{equation}
$$

$z_t,z_{t-1}$和$x_t,z_t$之间体现了线性的关系。而$\epsilon,\delta$是符合Gaussian Distribution的，$\epsilon \sim \mathcal{N}(0,Q),\delta \sim \mathcal{N}(0,R)$。所以，大家都明白了Linear和Gaussian都是从何而来的，所以Kalman Filtering被称为Linear Gaussian Model更合适。

Filtering是一类问题的总称，我们之前在Hidden Markov Model中有详细的讨论过。那么，我们回顾一下Hidden Markov Model的基本信息做一个对比。

HMM：$\lambda=\{ \pi,\mathcal{A},\mathcal{B} \}$。

状态转移矩阵：

$$
\begin{equation}
    \begin{split}
        & A=[a_{ij}] \quad a_{ij} = P(i_{t+1}=q_j|i_t=q_i) \\
        & B=[b_j(k)] \quad b_j{k} = P(o_t=v_t|i_t=q_j)
    \end{split}
\end{equation}
$$

那么，对于Kalman Filtering来说，状态转移矩阵，发射概率，初始矩阵，模型参数我们可以做出类似的表达：

$$
\begin{align}
    & P(z_t|z_{t-1}) \sim \mathcal{N}(A\cdot z_{t-1} + B, Q) \\
    & P(x_t|z_{t}) \sim \mathcal{N}(C\cdot z_{t} + D, R) \\
    & z_1 \sim \mathcal{N}(\mu_1,\Sigma_1) \\
    & \theta = \{ A, B, C, D, Q, R, \mu_1, \Sigma_1 \}
\end{align}
$$

在这一小节中，我们已经了解了基础的相关概念，那下一小节中，我们将描述了Filtering问题的建模和求解。
















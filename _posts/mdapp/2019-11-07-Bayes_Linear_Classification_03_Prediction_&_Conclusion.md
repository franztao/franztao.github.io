---
layout:     post
title:      Bayes_Linear_Classification_03_Prediction_&_Conclusion
subtitle:   2022年10月
date:       2019-11-07
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Bayes
    - Linear
    - Classification
    
    - Prediction
    - Conclusion
---

    

根据上一节中提到的Inference，我们已经成功的推断出了$p(w|Data)$的分布。表述如下所示：

$$
\begin{equation}
    p(W|X,Y) \sim \mathcal{N}(\mu_w, \Sigma_w)
\end{equation}
$$

其中，

$$
\begin{equation}
    \Sigma_w^{-1}=\sigma^{-2}X^TX+\Sigma_p^{-1} \qquad \mu_m = \sigma^{-2}A^{-1}X^TY \qquad \Sigma_w^{-1}=A
\end{equation}
$$

而我们的Prediction过程，可以被描述为，给定一个$x^\ast$如果计算得到$y^\ast$。而我们的模型建立如下所示：

$$
\begin{equation}
\left\{
\begin{array}{ll}
      f(x)=w^TX = x^Tw & \\
      y = f(x) + \varepsilon & \varepsilon \sim \mathcal{N}(0,\sigma^2)
\end{array}
\right.    
\end{equation}
$$

#  Prediction}
模型预测的第一步为，

$$
\begin{equation}
    f(x^\ast) = {x^\ast}^T w 
\end{equation}
$$

而在Inference部分，我们得到了$p(w|Data)\sim \mathcal{N}(\mu_w,\Sigma_w)$。所以，我们可以推断出，

$$
\begin{equation}
    f(x^\ast) = {x^\ast}^T w \sim \mathcal{N}({x^\ast}^T\mu_w, {x^\ast}^T\Sigma_w{x^\ast})
\end{equation}
$$

那么公式(5)我们可以写作：

$$
\begin{equation}
    p(f(x^\ast)|Data,x^\ast) \sim \mathcal{N}({x^\ast}^T\mu_w, {x^\ast}^T\Sigma_w{x^\ast})
\end{equation}
$$

又因为$y = f(x) + \varepsilon$，所以

$$
\begin{equation}
    p(y^\ast|Data,x^\ast) \sim \mathcal{N}({x^\ast}^T\mu_w, {x^\ast}^T\Sigma_w{x^\ast}+\sigma^2)
\end{equation}
$$

那么计算到这里，我们的模型预测也算是完成了。

#  Conclusion}
Data：$D=\{(x_i,y_i)\}^{N}_{i=1}$，其中$x_i\in\mathbb{R}^{p}$，$y_i\in\mathbb{R}$。

Model：

$$
\begin{equation}
\left\{
\begin{array}{ll}
      f(x)=w^TX = x^Tw & \\
      y = f(x) + \varepsilon & \varepsilon \sim \mathcal{N}(0,\sigma^2)
\end{array}
\right.    
\end{equation}
$$

Bayesian Method：$w$不在是一个未知的常数，$w$而是一个概率分布。
贝叶斯线性分类可以被分成两个部分，Inference和Prediction。

1. Inference：$p(w|Data)$是一个posterior分布，假定$p(w|Data)\sim\mathcal{N}(\mu_w, \Sigma_w) \propto likelihood \times prior$。这里使用了共轭的小技巧，得到posterior一定是一个Gaussian Distribution。在这一步中，我们的关键是求出$\mu_w=?,\Sigma_w=?$。

2. Prediction：这个问题实际上也就是，给定一个$x^\ast$如果计算得到$y^\ast$。我们可以描述为：

$$
\begin{equation}
    p(y^\ast|Data,x^\ast) = \int_w p(y^\ast|w,Data,x^\ast)p(w|Data,x^\ast) dw 
\end{equation}
$$

又因为，$w$就是从Data中引出的，所以$p(y^\ast|w,Data,x^\ast)=p(y^\ast|w,x^\ast)$。并且，$w$的获得与$x^\ast$没有关系，所以$p(w|Data)$。所以，

$$
\begin{equation}
    p(y^\ast|Data,x^\ast) = \int_w p(y^\ast|w,x^\ast)p(w|Data) dw = \mathbb{E}_{w\sim p(w|Data)}[p(y^\ast|w,x^\ast)] 
\end{equation}
$$


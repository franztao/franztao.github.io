---
layout:     post
title:      [笔记]深度学习中GPU和显存分析
subtitle:   2022年10月
date:       2022-10-25
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - gpu,nvidia-smi
---

- 何为“资源”

- 不同操作都耗费什么资源

- 如何充分的利用有限的资源

- 如何合理选择显卡

并纠正几个误区：

- 显存和[GPU](https://so.csdn.net/so/search?q=GPU&spm=1001.2101.3001.7020)等价，使用GPU主要看显存的使用？

- Batch Size 越大，程序越快，而且近似成正比？

- 显存占用越多，程序越快？

- 显存占用大小和batch size大小成正比？

## 

**0 预备知识**

`nvidia-smi`是Nvidia显卡命令行管理套件，基于NVML库，旨在管理和监控Nvidia GPU设备。

![d7423dba23c214495913a8309efe1e16.png](https://img-blog.csdnimg.cn/img_convert/d7423dba23c214495913a8309efe1e16.png)

nvidia-smi的输出

这是nvidia-smi命令的输出，其中最重要的两个指标：

- 显存占用

- GPU利用率

显存占用和GPU利用率是两个不一样的东西，显卡是由GPU计算单元和显存等组成的，显存和GPU的关系有点类似于内存和CPU的关系。

这里推荐一个好用的小工具：`gpustat`,直接`pip install gpustat`即可安装，gpustat基于`nvidia-smi`，可以提供更美观简洁的展示，结合watch命令，可以动态实时监控GPU的使用情况。

```go
watch --color -n1 gpustat -cpu
```

![5b86f597d005de4380aeb76a07716761.png](https://img-blog.csdnimg.cn/img_convert/5b86f597d005de4380aeb76a07716761.png)

gpustat 输出

显存可以看成是空间，类似于内存。

- 显存用于存放模型，数据

- 显存越大，所能运行的网络也就越大

GPU计算单元类似于CPU中的核，用来进行数值计算。衡量计算量的单位是flop： the number of floating-point multiplication-adds，浮点数先乘后加算一个flop。计算能力越强大，速度越快。衡量计算能力的单位是flops：每秒能执行的flop数量

![ffbddf9eda2e1306808a45f209923ce9.png](https://img-blog.csdnimg.cn/img_convert/ffbddf9eda2e1306808a45f209923ce9.png)

## 

**1. 显存分析**

## 1.1 存储指标

![a8e928d03f721301ffaebd2276a5fd8a.png](https://img-blog.csdnimg.cn/img_convert/a8e928d03f721301ffaebd2276a5fd8a.png)

`K`、`M`，`G`，`T`是以1024为底，而`KB` 、`MB`，`GB`，`TB`以1000为底。不过一般来说，在估算显存大小的时候，我们不需要严格的区分这二者。

在深度学习中会用到各种各样的数值类型，数值类型命名规范一般为`TypeNum`，比如Int64、Float32、Double64。

- Type：有Int，Float，Double等

- Num: 一般是 8，16，32，64，128，表示该类型所占据的比特数目

常用的数值类型如下图所示：

![17eeb5f7aa5bc0338455700856545725.png](https://img-blog.csdnimg.cn/img_convert/17eeb5f7aa5bc0338455700856545725.png)

常用的数值类型

其中Float32 是在深度学习中最常用的数值类型，称为单精度浮点数，每一个单精度浮点数占用4Byte的显存。

举例来说：有一个1000x1000的 矩阵，float32，那么占用的显存差不多就是

![5c9a6144c1fb0756bfbabde3b73039d9.png](https://img-blog.csdnimg.cn/img_convert/5c9a6144c1fb0756bfbabde3b73039d9.png)

2x3x256x256的四维数组（BxCxHxW）占用显存为：24M

## 1.2 神经网络显存占用

神经网络模型占用的显存包括：

- 模型自身的参数

- 模型的输出

举例来说，对于如下图所示的一个全连接网络(不考虑偏置项b)

![c11cc9fece62cd32211539fd6f7df729.png](https://img-blog.csdnimg.cn/img_convert/c11cc9fece62cd32211539fd6f7df729.png)

模型的输入输出和参数

模型的显存占用包括：

- 参数：二维数组 W

- 模型的输出：二维数组 Y

输入X可以看成是上一层的输出，因此把它的显存占用归于上一层。

这么看来显存占用就是W和Y两个数组？

并非如此！！！

下面细细分析。

## 1.2.1 参数的显存占用

只有有参数的层，才会有显存占用。这部份的显存占用和输入无关，模型加载完成之后就会占用。

有参数的层主要包括：

- 卷积

- 全连接

- BatchNorm

- Embedding层

- ... ...

无参数的层：

- 多数的激活层(Sigmoid/ReLU)

- 池化层

- Dropout

- ... ...

更具体的来说，模型的参数数目(这里均不考虑偏置项b)为：

- Linear(M->N): 参数数目：M×N

- Conv2d(Cin, Cout, K): 参数数目：Cin × Cout × K × K

- BatchNorm(N): 参数数目：2N

- Embedding(N,W): 参数数目：N × W

参数占用显存 = 参数数目×n

n = 4 ：float32

n = 2 : float16

n = 8 : double64

在PyTorch中，当你执行完`model=MyGreatModel().cuda()`之后就会占用相应的显存，占用的显存大小基本与上述分析的显存差不多（会稍大一些，因为其它开销）。

## 1.2.2 梯度与动量的显存占用

举例来说， 优化器如果是SGD：

![ef3263e27392c292ad8935ccc7c760b2.png](https://img-blog.csdnimg.cn/img_convert/ef3263e27392c292ad8935ccc7c760b2.png)

这时候还需要保存动量， 因此显存x3

如果是Adam优化器，动量占用的显存更多，显存x4

总结一下，模型中与输入无关的显存占用包括：

- 参数 W

- 梯度 dW（一般与参数一样）

- 优化器的动量（普通SGD没有动量，momentum-SGD动量与梯度一样，Adam优化器动量的数量是梯度的两倍）

## 1.2.3 输入输出的显存占用

这部份的显存主要看输出的feature map 的形状。

![2018db8682d0ba9ab48f37f0a5e84ac3.png](https://img-blog.csdnimg.cn/img_convert/2018db8682d0ba9ab48f37f0a5e84ac3.png)

feature map

比如卷积的输入输出满足以下关系：

![edad5cfdab6a2e95bbeb4e2b4c752039.png](https://img-blog.csdnimg.cn/img_convert/edad5cfdab6a2e95bbeb4e2b4c752039.png)

据此可以计算出每一层输出的Tensor的形状，然后就能计算出相应的显存占用。

模型输出的显存占用，总结如下：

- 需要计算每一层的feature map的形状（多维数组的形状）

- 模型输出的显存占用与 batch size 成正比

- 需要保存输出对应的梯度用以反向传播（链式法则）

- 模型输出不需要存储相应的动量信息（因为不需要执行优化）

深度学习中神经网络的显存占用，我们可以得到如下公式：

```go
显存占用 = 模型显存占用 + batch_size × 每个样本的显存占用
```

可以看出显存不是和batch-size简单的成正比，尤其是模型自身比较复杂的情况下：比如全连接很大，Embedding层很大

另外需要注意：

- 输入（数据，图片）一般不需要计算梯度

- 神经网络的每一层输入输出都需要保存下来，用来反向传播，但是在某些特殊的情况下，我们可以不要保存输入。比如ReLU，在PyTorch中，使用`nn.ReLU(inplace = True)` 能将激活函数ReLU的输出直接覆盖保存于模型的输入之中，节省不少显存。感兴趣的读者可以思考一下，这时候是如何反向传播的（提示：y=relu(x) -> dx = dy.copy();dx[y<=0]=0）

## 1.3 节省显存的方法

在深度学习中，一般占用显存最多的是卷积等层的输出，模型参数占用的显存相对较少，而且不太好优化。

节省显存一般有如下方法：

- 降低batch-size

- 下采样(NCHW -> (1/4)*NCHW)

- 减少全连接层（一般只留最后一层分类用的全连接层）

## 

**2 计算量分析**

计算量的定义，之前已经讲过了，计算量越大，操作越费时，运行神经网络花费的时间越多。

## 2.1 常用操作的计算量

常用的操作计算量如下：

- 全连接层：BxMxN , B是batch size，M是输入形状，N是输出形状。

![c2cb5d97cb98e6cd7eee7a4ed2b8521e.png](https://img-blog.csdnimg.cn/img_convert/c2cb5d97cb98e6cd7eee7a4ed2b8521e.png)

卷积的计算量分析

![addbe9c206b3578506734dd74bbaa65c.png](https://img-blog.csdnimg.cn/img_convert/addbe9c206b3578506734dd74bbaa65c.png)

- ReLU的计算量：BHWC

## 2.2 AlexNet 分析

AlexNet的分析如下图，左边是每一层的参数数目（不是显存占用），右边是消耗的计算资源

![112ca0f394e9c05f12de54ac46cd9ccc.png](https://img-blog.csdnimg.cn/img_convert/112ca0f394e9c05f12de54ac46cd9ccc.png)

AlexNet分析

可以看出：

- 全连接层占据了绝大多数的参数

- 卷积层的计算量最大

## 2.3 减少卷积层的计算量

今年谷歌提出的MobileNet，利用了一种被称为DepthWise Convolution的技术，将神经网络运行速度提升许多，它的核心思想就是把一个卷积操作拆分成两个相对简单的操作的组合。如图所示, 左边是原始卷积操作，右边是两个特殊而又简单的卷积操作的组合（上面类似于池化的操作，但是有权重，下面类似于全连接操作）。

![5eac35d8ea37006c865f1a54f96f5476.png](https://img-blog.csdnimg.cn/img_convert/5eac35d8ea37006c865f1a54f96f5476.png)

Depthwise Convolution

这种操作使得：

- 显存占用变多(每一步的输出都要保存

![758a02ac2346795565ba96da89036d07.png](https://img-blog.csdnimg.cn/img_convert/758a02ac2346795565ba96da89036d07.png)

## 2.4 常用模型 显存/计算复杂度/准确率

去年一篇论文(http://link.zhihu.com/?target=https%3A//arxiv.org/abs/1605.07678)总结了当时常用模型的各项指标，横座标是计算复杂度（越往右越慢，越耗时），纵座标是准确率（越高越好），圆的面积是参数数量（不是显存占用）。左上角我画了一个红色小圆，那是最理想的模型的的特点：快，效果好，占用显存小。

![666ac7ce73fa1cbd22a79cb838253549.png](https://img-blog.csdnimg.cn/img_convert/666ac7ce73fa1cbd22a79cb838253549.png)

常见模型计算量/显存/准确率 

## 

**3 总结**

## 3.1 建议

- 时间更宝贵，尽可能使模型变快（减少flop）

- 显存占用不是和batch size简单成正比，模型自身的参数及其延伸出来的数据也要占据显存

- batch size越大，速度未必越快。在你充分利用计算资源的时候，加大batch size在速度上的提升很有限

尤其是batch-size，假定GPU处理单元已经充分利用的情况下：

- 增大batch size能增大速度，但是很有限（主要是并行计算的优化）

- 增大batch size能减缓梯度震荡，需要更少的迭代优化次数，收敛的更快，但是每次迭代耗时更长。

- 增大batch size使得一个epoch所能进行的优化次数变少，收敛可能变慢，从而需要更多时间才能收敛（比如batch_size 变成全部样本数目）。

## 3.2 关于显卡选购

当前市面上常用的显卡指标如下：

![77ab9108cd08ae700f2d74fa35ac74f8.png](https://img-blog.csdnimg.cn/img_convert/77ab9108cd08ae700f2d74fa35ac74f8.png)

常见显卡指标

更多显卡的更多指标请参阅

http://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units

显然GTX 1080TI性价比最高，速度超越新Titan X，价格却便宜很多，显存也只少了1个G（据说故意阉割掉一个G，不然全面超越了Titan X怕激起买Titan X人的民愤~）。

- K80性价比很低（速度慢，而且贼贵）

- 注意GTX TITAN和Nvidia TITAN的区别，别被骗

本文都是针对单机单卡的分析，分布式的情况会和这个有所区别。在分析计算量的时候，只分析了前向传播，反向传播计算量一般会与前向传播有细微的差别。

---
layout:     post
title:      AI需求上线checkList清单
subtitle:   2022年4月
date:       2022-4-3
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Blog
---

# motivation

为什么要做checklist，人最多关注不超过7个的目标，在复杂度极高的ML系统上，有许多细节，但是这些细节不可能一个人一步确定。
清单革命，每个人都会犯错，分为 “无知之错”与“无能之错”，"无知之错"是不知道而犯的错，这种错可以被原谅；另一种"无能之错"是能力不足而犯的错，这种错是不可被原谅的。此外，团队犯错的几率比个人低很多，因为每个人都有关注的清单点，所以会大幅降低出错的概率。

# 需求阶段

1. 应该选择什么样的项目？

2. **调试深度网络（DN）非常棘手**

> 训练深度学习模型需要数百万次的迭代，因此查找 bug 的过程非常艰难，而且容易崩坏。

3. **度量和学习**

> 一般我们安排这些复杂的实验，使其通宵运行，到第二天清晨时，我们希望得到足够的信息来采取下一步行动。在早期阶段，这些实验不应超过 12 小时，这是一条良好的经验法则。

4. 成本

> 一个模型为什么会表现好，机理上有什么改变
> 
> 1. 这个项目是在解决什么问题，为什么会有这个项目。
> 2. 这个项目的运行环境是什么，需要什么环境依赖；
> 3. 这个项目的代码逻辑是怎样的，输入和输出分别是什么，输入和输出的格式分别是什么。
> 4. 这个代码每一个文件都是什么含义，解决了什么问题；
> 5. 该项目是否能够正确运行，运行部署中是否会存在问题；
> 6. 这个项目如果要适配我的数据，完成我的任务，如何进行迁移和嵌入；
> 7. 这个项目存在哪些不足，有哪些可以借鉴的点，后期如果我要优化的话，可以提哪些点。

# 数据阶段

创建一个深度学习数据集

1. **公开及学术数据集**

2. **自定义数据集**

> 高质量数据集应该包括以下特征：
> 
> - 类别均衡
> 
> - 数据充足
> 
> - 数据和标记中有高质量信息
> 
> - 数据和标记错误非常小
> 
> - 与你的问题相关

3. 不要一次爬取所有数据

优秀数据集的特征：

> - 尽可能使用公共数据集；
> 
> - 寻找可以获取高质量、多样化样本的最佳网站；
> 
> - 分析错误并过滤掉与实际问题无关的样本；
> 
> - 迭代地创建你的样本；
> 
> - 平衡每个类别的样本数；
> 
> - 训练之前先整理样本；
> 
> - 收集足够的样本。如果样本不够，应用迁移学习。

# 算法设计阶段

> • Establish a baseline  
>    ◦ Compute metrics for the baseline  
>    ◦ Analyze errors for area of improvements  
> • Select network structure  
>    ◦ CNN, LSTM…  
> • Implement a deep network  
>    ◦ Code debugging and validation  
>    ◦ Parameter initialization  
>    ◦ Compute loss and metrics  
>    ◦ Choose hyper-parameters  
>    ◦ Visualize, validate and summarize result  
>    ◦ Analyze errors  
>    ◦ Add layers and nodes  
>    ◦ Optimization  
> • Hyper-parameters fine tunings  
> • Try our model variants

# 训练评估阶段

在为深度神经网络排除故障方面，人们总是太快、太早地下结论了。在了解如何排除故障前，我们要先考虑要寻找什么，再花费数小时时间追踪故障。这部分我们将讨论如何可视化深度学习模型和性能指标。

# check 工具

1. 文件名改下，都成只有数字和大小写26字母的字符串，不包含其他符号
2. pip install torchsnooperimport torchsnooper# 对于函数，使用修饰器@torchsnooper.snoop()# 如果不是函数，使用 with 语句来激活 TorchSnooper，把训练的那个循环装进 with 语句中去。with torchsnooper.snoop():    原本的代码
3. @pysnooper.snoop()

> 策略：
> 
> - 把正则化因子设置为 0；
> 
> - 不要其他正则化（包括 dropouts);
> 
> - 使用默认设置的 Adam 优化器；
> 
> - 使用 ReLU;
> 
> - 不要数据增强；
> 
> - 更少的深度网络层；
> 
> - 扩大输入数据，但不要非必要预处理；
> 
> - 不要在长时间训练迭代或者大 batch size 上浪费时间。

> 数据：
> 
> - 可视化并检查输入数据（在数据预处理之后，馈送到模型之前）；
> 
> - 检查输入标签的准确率（在数据扰动之后）；
> 
> - 不要一遍又一遍的馈送同一 batch 的数据；
> 
> - 适当的缩放输入数据（一般可缩放到区间 (-1, 1) 之间，且具有零均值）；
> 
> - 检查输出的范围（如，在区间 (-1, 1) 之间）；
> 
> - 总是使用训练集的平均值/方差来重新调节验证/测试集；
> 
> - 模型所有的输入数据有同样的维度；
> 
> - 获取数据集的整体质量（是否有太多异常值或者坏样本）。

模型：

> - 模型参数准确的初始化，权重不要全部设定为 0；
> 
> - 对激活或者梯度消失/爆炸的网络层做 debug（从最右边到最左边）；
> 
> - 对权重大部分是 0 或者权重太大的网络层做 debug；
> 
> - 检查并测试损失函数；
> 
> - 对预训练模型，输入数据范围要匹配模型中使用的范围；
> 
> - 推理和测试中的 Dropout 应该总是关掉。

**模型 & 数据集设计变化**

> - 在验证数据集中分析误差（糟糕的预测结果）；
> 
> - 监控激活函数。在激活函数不以零为中心或非正态分布时，考虑批归一化或层归一化；
> 
> - 监控无效节点的比例；
> 
> - 使用梯度截断（尤其是 NLP 任务中）来控制梯度爆炸问题；
> 
> - Shuffle 数据集（手动或通过程序）；
> 
> - 平衡数据集（每个类别具备相似数量的样本）。

- 不要使用太大的线性层。因为nn.Linear(m,n)使用的是的内存，线性层太大很容易超出现有显存。
- 不要在太长的序列上使用RNN。因为RNN反向传播使用的是BPTT算法，其需要的内存和输入序列的长度呈线性关系。
- model(x) 前用 model.train() 和 model.eval() 切换网络状态。
- 不需要计算梯度的代码块用 with torch.no_grad() 包含起来。
- model.eval() 和 torch.no_grad() 的区别在于，model.eval() 是将网络切换为测试状态，例如 BN 和dropout在训练和测试阶段使用不同的计算方法。torch.no_grad() 是关闭 PyTorch 张量的自动求导机制，以减少存储使用和加速计算，得到的结果无法进行 loss.backward()。
- model.zero_grad()会把整个模型的参数的梯度都归零, 而optimizer.zero_grad()只会把传入其中的参数的梯度归零.
- torch.nn.CrossEntropyLoss 的输入不需要经过 Softmax。torch.nn.CrossEntropyLoss 等价于 torch.nn.functional.log_softmax + torch.nn.NLLLoss。
- loss.backward() 前用 optimizer.zero_grad() 清除累积梯度。
- torch.utils.data.DataLoader 中尽量设置 pin_memory=True，对特别小的数据集如 MNIST 设置 pin_memory=False 反而更快一些。num_workers 的设置需要在实验中找到最快的取值。
- 用 del 及时删除不用的中间变量，节约 GPU 存储。
- 使用 inplace 操作可节约 GPU 存储，如x = torch.nn.functional.relu(x, inplace=True)
- 减少 CPU 和 GPU 之间的数据传输。例如如果你想知道一个 epoch 中每个 mini-batch 的 loss 和准确率，先将它们累积在 GPU 中等一个 epoch 结束之后一起传输回 CPU 会比每个 mini-batch 都进行一次 GPU 到 CPU 的传输更快。
- 使用半精度浮点数 half() 会有一定的速度提升，具体效率依赖于 GPU 型号。需要小心数值精度过低带来的稳定性问题。
- 时常使用 assert tensor.size() == (N, D, H, W) 作为调试手段，确保张量维度和你设想中一致。
- 除了标记 y 外，尽量少使用一维张量，使用 n*1 的二维张量代替，可以避免一些意想不到的一维张量计算结果。
- 统计代码各部分耗时
- with torch.autograd.profiler.profile(enabled=True, use_cuda=False) as profile:    ...print(profile)# 或者在命令行运行python -m torch.utils.bottleneck main.py
- 使用TorchSnooper来调试PyTorch代码，程序在执行的时候，就会自动 print 出来每一行的执行结果的 tensor 的形状、数据类型、设备、是否需要梯度的信息。
- 保存图片为tiff格式

# 部署阶段

## check 工具

1. 建议0: 了解代码中的瓶颈在哪里
   
   > nvidia-smi, htop, iotop, nvtop, py-spy, strace 等命令行工具应该成为你最好的朋友。你的训练pipeline是CPU-bound? IO-bound 还是GPU-bound? 这些工具将帮助你找到答案。

2. 数据预处理
- 建议1: 如果可能的话，将所有或部分数据移动到 RAM。
  
  > NVidia Dali 这样的库提供 GPU加速的 JPEG 解码。如果在数据处理pipeline中遇到 IO 瓶颈，这绝对值得一试。SSD 磁盘的存取时间约为0.08-0.16毫秒。RAM 的访问时间为纳秒。

- 建议2: 性能分析。测量。比较。每次你对pipeline进行任何改动时，都要仔细评估它对整体的影响。
  
  ```
  # Profile CPU bottlenecks
  python -m cProfile training_script.py --profiling
  # Profile GPU bottlenecks
  nvprof --print-gpu-trace python train_mnist.py
  # Profile system calls bottlenecks
  strace -fcT python training_script.py -e trace=open,close,read
  ```

- 建议3: 线下预处理所有数据

- 建议4: 调整 DataLoader 的workers数量
  
  > 尽可能地减少输入数据的通道深度

```
class MySegmentationDataset(Dataset):
  ...
  def __getitem__(self, index):
    image = cv2.imread(self.images[index])
    target = cv2.imread(self.masks[index])

    # No data normalization and type casting here
    return torch.from_numpy(image).permute(2,0,1).contiguous(),
           torch.from_numpy(target).permute(2,0,1).contiguous()

class Normalize(nn.Module):
    # https://github.com/BloodAxe/pytorch-toolbelt/blob/develop/pytorch_toolbelt/modules/normalize.py
    def __init__(self, mean, std):
        super().__init__()
        self.register_buffer("mean", torch.tensor(mean).float().reshape(1, len(mean), 1, 1).contiguous())
        self.register_buffer("std", torch.tensor(std).float().reshape(1, len(std), 1, 1).reciprocal().contiguous())

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return (input.to(self.mean.type) - self.mean) * self.std

class MySegmentationModel(nn.Module):
  def __init__(self):
    self.normalize = Normalize([0.221 * 255], [0.242 * 255])
    self.loss = nn.CrossEntropyLoss()

  def forward(self, image, target):
    image = self.normalize(image)
    output = self.backbone(image)

    if target is not None:
      loss = self.loss(output, target.long())
      return loss

    return output
```

## 配置

1. cudnn - check

2. no_grad - check

3. [GPU 利用率低常见原因分析及优化](https://mp.weixin.qq.com/s/jXFFIwoovb8q2YTO-O9w8g)

4. JIT-compilation - check

5. [优化神经网络训练的17种方法](https://mp.weixin.qq.com/s/WUN0150C7Zk1Add7y22jDw)

6. [加速 PyTorch 模型训练的 9 个技巧](https://mp.weixin.qq.com/s/Fu4cmInN2ql7B9nzb8ywuA)

7. 小显存如何训练大模型 
   
   ```
   自动混合精度（AMP）训练
   '''
   # Creates model and optimizer in default precision
   model = Net().cuda()
   optimizer = optim.SGD(model.parameters(), ...)
   ```

8. Creates a GradScaler once at the beginning of training.
   
   ```
   scaler = GradScaler()
   for epoch in epochs:
    for input, target in data:
        optimizer.zero_grad()
   
        # Runs the forward pass with autocasting.
        with autocast():
            output = model(input)
            loss = loss_fn(output, target)
   
        # Scales loss.  Calls backward() on scaled loss to create scaled gradients.
        # Backward passes under autocast are not recommended.
        # Backward ops run in the same dtype autocast chose for corresponding forward ops.
        scaler.scale(loss).backward()
   
        # scaler.step() first unscales the gradients of the optimizer's assigned params.
        # If these gradients do not contain infs or NaNs, optimizer.step() is then called,
        # otherwise, optimizer.step() is skipped.
        scaler.step(optimizer)
   
        # Updates the scale for next iteration.
        scaler.update()
   ```

9. 梯度积累
   
   > 当你在混合精度训练中使用梯度累积时，scale应该为有效批次进行校准，scale更新应该以有效批次的粒度进行。
   > 当你在分布式数据并行（DDP）训练中使用梯度累积时，使用no_sync()上下文管理器来禁用前M-1步的梯度全还原，这可以增加训练的速度。

10. 梯度检查点
    
    ```
    bert = AutoModel.from_pretrained(pretrained_model_name)
    bert.config.gradient_checkpointing=True
    ```

11. [优化PyTorch的速度和内存效率](https://mp.weixin.qq.com/s/ShgNdizIPzeXOREoz8rgJA)

# 上线阶段

首先是算法质量：

> 基本算法指标：准确率、召回率，一方面使用历史标注做总体分析，另一方面是在线随机query的自测，当然这里要算去重，也要带频次。
> 体验指标：满意度和SBS自测，考虑用户体验，看最终的效果，一方面新版本的胜出率要高一些，另一方面整体满意度也要变好。

然后是算法服务性能：

> 单进程自动化用例，也就是必过的case，放置引入问题，甚至出现bug，未知情况的报错等。
> 压测。单、2/4/8/16等多进程的压测，观测平均和50%、90%、99%分位点耗时，观测内存等占用是否符合预期，另外注意使用的query要分两种，一种是随机的，一种是复杂的（尽可能走过多一些复杂流程的，说白了就是看看极端坏的情况）。
> bn在训练时记得打开更新（特别是tf的小伙伴，容易漏），不然可能出现的问题是训练时loss下降很快，测试感觉模型就没收敛



# reference

[GitHub - Mountchicken/Efficient-Deep-Learning: A bag of tricks to speed up your deep learning process](https://github.com/Mountchicken/Efficient-Deep-Learning)

> ## Efficient Coding
> 
> - Strategies to code efficiently.
> - [Efficient Coding](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md)
>   - [Use Vscode](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#1-you-shouldnt-miss-vscode)
>   - [Auto code formating](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#2-automatically-format-your-code)
>   - [Pre-commit hook](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#3-use-a-pre-commit-hook-to-check-your-code)
>   - [Learn to use git](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#4-learn-to-use-git)
>   - [Grammarly](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#5-use-grammarly-to-check-your-writing)
>   - [StackOverflow](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#6-search-on-stackoverflow-first)
>   - [Auto docstring](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Coding.md#7-automatically-format-your-docstring)
> 
> ## Efficient Data Processing
> 
> - Strategies to speed up your data processing.
> - [Efficient Data Processing](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md)
>   - [SSD](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md#11-use-ssd-instead)
>   - [num_workers and pin_memory](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md#12-multiple-workers-and-pinmemory-in-dataloader)
>   - [LMDB file](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md#21-efficient-data-storage-methods)
>   - [Albumentations](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md#22-efficient-data-augmentation-library)
>   - [Data augmentation on GPU](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_DataProcessing.md#23-data-augmentation-on-gpu)
>   
>   
>   
>   ## Efficient Training
>   
>   - Strategies to speed up your training process.
>   - [Efficient Traininig](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md)
>     - [cudnn.benchmark=True](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#11-set-cudnnbenchmarktrue)
>     - [Set gradients to None during back propagation](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#12-set-gradients-to-none-during-back-propagation)
>     - [Turn off debugging APIs](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#13-turn-off-debugging)
>     - [Turn off gradient computation during validation](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#14-turn-off-gradient-computation-during-validation)
>     - [Use another optimizer AdamW](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#21-use-another-optimizer-adamw)
>     - [Learning rate schedule](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#22-learning-rate-schedule)
>     - [Useful combination, Adam with 3e-4](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#23-best-combination-adam-with-3e-4)
>     - [LR Warm up and Cosine Learning Rate Decay](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#24-lr-warm-up-and-cosine-learning-rate-decay)
>     - [L2 decay](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Training.md#25-l2-decay)
> 
> ## Efficient GPUtilization
> 
> - Strategies to have a better GPU utilization.
> - [Efficient GPUtilization](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md)
>   - [CUDA out of memory solutions](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md#1-cuda-out-of-memory-solutions)
>   - [Automatic Mixed Precision (AMP)](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md#21-automatic-mixed-precisionamp)
>   - [Gradient Accumulation](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md#22-gradient-accumulation)
>   - [Gradient Checkpoint](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md#23-gradient-checkpoint)
>   - [Data parallelization training](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_GPUtilization.md#31-distributed-model-training)
> 
> ## Efficient Tools
> 
> - A list of useful tools.
> - [Efficient Tools](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md)
>   - [Torchinfo: Visualize Network Architecture](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#1-torchinfo-visualize-network-architecture)
>   - [drawio: Free graphing software](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#2-drawio-free-graphing-software)
>   - [Octotree: Free gitHub code tree](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#3-octotree-free-github-code-tree)
>   - [ACRONYMIFY: Name your paper with a cool acronyms](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#4-acronymify-name-your-paper-with-a-cool-acronyms)
>   - [Linggle: Grammer checker](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#5-linggle-grammer-checker)
>   - [AI pair programmer: Github Copilot](https://github.com/Mountchicken/Efficient-Deep-Learning/blob/main/Efficient_Tools.md#6-ai-pair-programmer-github-copilot)

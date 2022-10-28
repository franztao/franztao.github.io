---
layout:     post
title:      monitoring
subtitle:   2022年10月
date:       2022-10-27
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - monitoring

---

了解如何监控 ML 系统以识别和解决漂移源，以防止模型性能下降。

## intution

尽管我们已经训练并彻底评估了我们的模型，但一旦我们部署到生产环境，真正的工作就开始了。这是传统软件工程与 ML 开发之间的根本区别之一。传统上，使用基于规则的确定性软件，大部分工作发生在初始阶段，一旦部署，我们的系统就会按照我们定义的方式工作。但是对于机器学习，我们并没有明确定义事物的工作原理，而是使用数据来构建概率解决方案。这种方法会随着时间的推移而出现自然的性能下降以及意外行为，因为暴露给模型的数据将与训练过的数据不同。这不是我们应该试图避免的事情，而是尽可能地理解和减轻。在本课中，我们'[漂移](https://madewithml.com/courses/mlops/monitoring/#drift)检测。

## 系统运行状况

确保我们的模型运行良好的第一步是确保实际系统正常运行。这可以包括特定于服务请求的指标，例如延迟、吞吐量、错误率等，以及基础设施利用率，例如 CPU/GPU 利用率、内存等。

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-10-27-15-34-33-cba3cf6f-569f-4b6b-bce4-6f733ded96f9.jpeg)

幸运的是，大多数云提供商甚至编排层都将通过仪表板免费提供对我们系统健康状况的洞察。如果我们不这样做，我们可以轻松地使用[Grafana](https://grafana.com/)、[Datadog](https://www.datadoghq.com/)等从日志中提取系统性能指标，以创建自定义仪表板并设置警报。

## 表现

不幸的是，仅仅监控系统的健康状况并不足以捕捉我们模型的潜在问题。因此，很自然地，要监控的下一层指标涉及模型的性能。这些可以是我们在模型评估期间使用的定量评估指标（准确度、精度、f1 等），也可以是模型影响的关键业务指标（ROI、点击率等）。

自部署模型以来，仅分析整个时间跨度内的累积性能指标通常是不够的。相反，我们还应该检查对我们的应用程序很重要的一段时间内的性能（例如每天）。这些滑动指标可能更能反映我们系统的健康状况，并且我们可能能够通过不使用历史数据掩盖问题来更快地识别问题

```
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme()
```

```
# Generate data
hourly_f1 = list(np.random.randint(low=94, high=98, size=24*20)) + \
            list(np.random.randint(low=92, high=96, size=24*5)) + \
            list(np.random.randint(low=88, high=96, size=24*5)) + \
            list(np.random.randint(low=86, high=92, size=24*5))
```

```
# Cumulative f1
cumulative_f1 = [np.mean(hourly_f1[:n]) for n in range(1, len(hourly_f1)+1)]
print (f"Average cumulative f1 on the last day: {np.mean(cumulative_f1[-24:]):.1f}")
```

```
# Sliding f1
window_size = 24
sliding_f1 = np.convolve(hourly_f1, np.ones(window_size)/window_size, mode="valid")
print (f"Average sliding f1 on the last day: {np.mean(sliding_f1[-24:]):.1f}")
```

```
plt.ylim([80, 100])
plt.hlines(y=90, xmin=0, xmax=len(hourly_f1), colors="blue", linestyles="dashed", label="threshold")
plt.plot(cumulative_f1, label="cumulative")
plt.plot(sliding_f1, label="sliding")
plt.legend()
```

![性能漂移](https://madewithml.com/static/images/mlops/monitoring/performance_drift.png)

> 我们可能需要监控各种窗口大小的指标，以尽快发现性能下降。在这里，我们监控的是整体 f1，但我们可以对数据切片、单个类等执行相同的操作。例如，如果我们监控特定标签的性能，我们可能能够快速捕捉为发布的新算法该标签（例如新的transformer架构）。

## 延迟的结果

我们可能并不总是有可用的真实结果来确定模型在生产投入上的表现。如果实际数据存在明显滞后或需要注释，则尤其如此。为了缓解这种情况，我们可以：

- 设计一个可以帮助我们*估计*模型性能的**近似信号。**例如，在我们的标签预测任务中，我们可以使用作者赋予项目的实际标签作为中间标签，直到我们验证了来自注释管道的标签。
- 标记我们实时数据集的一小部分以估计性能。该子集应尽量代表实时数据中的各种分布。

## 重要性加权

然而，近似信号并不总是适用于每种情况，因为 ML 系统的输出没有反馈，或者它太延迟了。对于这些情况，最近的一项研究依赖于在所有情况下都可用的唯一组件：输入数据。

![曼陀林的重要性加权](https://madewithml.com/static/images/mlops/monitoring/mandoline.png)

[Mandoline：分布转移下的模型评估](https://arxiv.org/abs/2107.00643)

核心思想是开发切片功能，可能会捕捉我们的数据可能经历分布变化的方式。这些切片功能应捕获明显的切片，例如类标签或不同的分类特征值，但也应捕获基于隐式元数据（不是显式特征列的数据的隐藏方面）的切片。然后将这些切片函数应用于我们的标记数据集，以创建具有相应标签的矩阵。相同的切片函数应用于我们未标记的生产数据，以近似加权标签的内容。有了这个，我们可以确定大概的性能！这里的直觉是，我们可以根据标记切片矩阵和未标记切片矩阵之间的相似性更好地近似未标记数据集的性能。

> 如果我们等待基于性能来捕捉模型衰减，它可能已经对依赖它的下游业务管道造成了重大损害。我们需要在实际性能下降之前采用更细粒度的监控来识别模型漂移的*来源*。

## 漂移

我们需要首先了解可能导致模型性能下降（模型漂移）的不同类型的问题。做到这一点的最好方法是查看我们正在尝试建模的所有移动部分以及每个部分如何体验漂移。

![](C:\Users\franztao\AppData\Roaming\marktext\images\2022-10-27-15-40-46-image.png)

### 数据漂移

*当生产*数据的分布与*训练*数据的分布不同时，就会发生数据漂移，也称为特征漂移或协变量偏移。该模型无法处理特征空间中的这种漂移，因此它的预测可能不可靠。漂移的实际原因可归因于现实世界中的自然变化，也可归因于系统性问题，例如丢失数据、管道错误、架构更改等。检查漂移的数据并沿着其管道追溯以识别引入漂移的时间和地点。

> 除了只查看输入数据的分布，我们还希望确保在训练和服务期间检索和处理输入数据的工作流程是相同的，以避免训练-服务偏差。但是，如果我们从相同的源位置检索我们的特征用于训练和服务，我们可以跳过这一步，即。从[功能商店](https://madewithml.com/courses/mlops/feature-store/)。

![数据漂移](https://madewithml.com/static/images/mlops/monitoring/data_drift.png)

> 随着数据开始漂移，我们可能还没有注意到模型性能的显着下降，特别是如果模型能够很好地插值。然而，这是一个很好的机会，可以[在](https://madewithml.com/courses/mlops/monitoring/#solutions)漂移开始影响性能之前进行重新训练。

### 目标漂移

除了输入数据发生变化外，与数据漂移一样，我们还可以体验结果的漂移。这可能是分布的变化，也可能是具有分类任务的新类的删除或添加。尽管再训练可以减轻导致目标漂移的性能衰减，但通常可以通过有关新类、模式更改等的适当管道间通信来避免这种情况。

### 概念漂移

除了输入和输出数据漂移之外，我们还可以得到它们之间的实际关系漂移。这种概念漂移使我们的模型无效，因为它学会在原始输入和输出之间映射的模式不再相关。概念漂移可能以[各种模式](https://link.springer.com/article/10.1007/s11227-018-2674-1)发生：

![概念漂移](https://madewithml.com/static/images/mlops/monitoring/concept_drift.png)

- 在一段时间内逐渐
- 由于外部事件而突然
- 由于反复发生的事件而定期

> 我们讨论的所有不同类型的漂移都可以同时发生，这会使识别漂移的来源变得复杂。

## 定位漂移

现在我们已经确定了不同类型的漂移，我们需要学习如何定位以及测量它的频率。以下是我们需要考虑的约束：

- **参考窗口**：用于比较生产数据分布以识别漂移的一组点。
- **测试窗口**：与参考窗口比较以确定是否发生漂移的点集。

由于我们正在处理在线漂移检测（即检测实时生产数据中的漂移，而不是过去的批次数据），我们可以采用[固定或滑动窗口方法](https://onlinelibrary.wiley.com/doi/full/10.1002/widm.1381)来识别我们的点集进行比较。通常，参考窗口是训练数据的一个固定的、最近的子集，而测试窗口会随着时间的推移而滑动。

[Scikit-multiflow](https://scikit-multiflow.github.io/)提供了一个工具包，用于直接在流数据上进行概念漂移检测[技术。](https://scikit-multiflow.readthedocs.io/en/stable/api/api.html#module-skmultiflow.drift_detection)该软件包提供了窗口化、移动平均功能（包括动态预处理），甚至还提供了一些围绕概念的方法，例如[逐渐概念漂移](https://scikit-multiflow.readthedocs.io/en/stable/api/generated/skmultiflow.drift_detection.EDDM.html#skmultiflow-drift-detection-eddm)。

> 我们还可以同时比较各种窗口大小，以确保较小的漂移情况不会被大窗口大小平均。

## 测量漂移

一旦我们有了想要比较的点的窗口，我们就需要知道如何比较它们。

```
import great_expectations as ge
import json
import pandas as pd
from urllib.request import urlopen
```
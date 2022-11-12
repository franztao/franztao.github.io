---
layout:     post
title:      机器学习系统设计
subtitle:   2022年10月
date:       2022-10-27
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Machine Learning Systems Design

---



## 直觉

在本课程中，我们将讨论处理特征、从中学习、对模型进行试验和为它们提供服务的不同选项。我们还将讨论基础架构编排和扩展它们的不同选项。

## 任务

在讨论 ML 任务所需的基础架构之前，我们需要先讨论一下 ML 任务的基本类型。

### 静止的

一项任务可能涉及不随时间变化的特征。例如，如果 API 对上传的图片进行分类，则所有输入特征都来自用户刚刚上传的图片。如果稍后上传相同的图像并使用相同的模型，则预测将保持不变。

### 动态的

任务还可能涉及随时间变化的特征。例如，如果您想预测用户是否会喜欢一部电影，您需要检索该用户行为的最新可用数据。使用完全相同的模型，您的预测会随着用户特征的变化而变化。

> 当涉及到如何存储、处理和检索数据（例如数据库、特征存储、流等）时，这种细微的差异可以推动关键的架构选择。

## 服务

第一个决定是通过批处理还是实时提供预测，这完全基于特征空间（有限与无限制）。我们从这里开始倒退，因为这个决定将决定许多关于处理、学习和实验的上游决定。

### 批量服务

我们可以对一组有限的输入进行批量预测，然后将其写入数据库以进行低延迟推理。当用户或下游进程实时发出推理请求时，会返回来自数据库的缓存结果（通常通过对 API 的请求以[查询](https://madewithml.com/courses/mlops/api/)[数据库](https://madewithml.com/courses/mlops/api/#request)）。[](https://madewithml.com/courses/mlops/api/)

![批量服务](https://madewithml.com/static/images/mlops/systems-design/batch_serving.png)

-   ✅ 生成和缓存预测，以便为用户提供非常快速的推理。
-   ✅ 该模型不需要作为它自己的服务进行旋转，因为它从未实时使用。
-   ❌ 如果用户开发了当前预测所基于的旧数据未捕获的新兴趣，则预测可能会变得陈旧。
-   ❌ 输入特征空间必须是有限的，因为我们需要在需要实时预测之前生成所有预测。

批量服务任务

哪些任务适合批量服务？

显示答案

_根据现有_用户的观看历史推荐他们喜欢的内容。然而，在我们第二天处理他们的历史记录之前，_新用户可能只会收到一些基于他们明确兴趣的通用推荐。_即使我们不进行批量服务，缓存非常流行的输入特征集（例如，明确兴趣的组合导致某些推荐内容）可能仍然有用，以便我们可以更快地提供这些预测。

### 实时服务

我们还可以提供实时预测，其中输入特征被实时馈送到模型以检索预测。

![实时服务](https://madewithml.com/static/images/mlops/systems-design/real_time_serving.png)

-   ✅ 可以产生更多最新的预测，从而产生更有意义的用户体验等。
-   ❌ 需要托管微服务来处理请求流量。
-   ❌ 需要实时监控，因为输入空间是无限的，这可能会产生错误的预测。

实时服务任务

在我们上面的批量服务示例任务中，实时服务如何显着改善内容推荐？

显示答案

通过批处理，我们使用用户的历史记录为离线用户生成内容推荐。在我们使用更新的用户功能在第二天处理批次之前，这些建议不会改变。但是用户的口味在一天中会发生显着变化（例如，用户正在搜索要观看的恐怖电影）。通过实时服务，我们可以使用这些最近的功能根据即时搜索推荐高度相关的内容。

> 除了将我们的模型包装为单独的、可扩展的微服务之外，我们还可以拥有一个专门构建的[模型服务器](https://madewithml.com/courses/mlops/api/#model-server)来无缝地检查、更新、服务、回滚等多个版本的模型。

## 加工

我们还可以控制用于生成实时预测的特征。

我们的用例不一定涉及随时间变化的实体特征，因此只有一个处理管道是有意义的。但是，并非 ML 应用程序中的所有实体都以这种方式工作。使用我们的内容推荐示例，给定用户可以具有随时间更新的某些特征，例如最喜欢的流派、点击率等。正如我们将在下面看到的，我们可以选择在以前的时间为用户批处理特征或者我们可以在流中处理可用的特征，并使用它们进行相关预测。

> [在我们的综合数据堆栈课程](https://madewithml.com/courses/mlops/data-stack/)中了解有关下面提到的不同数据系统的更多信息，以及如何在我们的[编排课程](https://madewithml.com/courses/mlops/orchestration/)中负责任地交付高质量数据。

### 批量处理

给定实体在前一个时间点的批处理特征，稍后用于生成实时预测。

![批量处理](https://madewithml.com/static/images/mlops/systems-design/batch_processing.png)

-   ✅ 可以离线执行繁重的特征计算，并准备好进行快速推理。
-   ❌ 功能可能会过时，因为它们是前一段时间预先确定的。当您的预测取决于最近发生的事件时，这可能是一个巨大的劣势。（例如，尽快发现欺诈交易）。

### 流处理

_使用给定实体的近乎_实时的流式特征对给定的一组输入进行推理。

![流处理](https://madewithml.com/static/images/mlops/systems-design/stream_processing.png)

-   ✅ 我们可以通过向模型提供实时、流式传输的特征来生成更好的预测。
-   ❌ 维护数据流存储（[Kafka](https://kafka.apache.org/)、[Kinesis](https://aws.amazon.com/kinesis/)等）和流处理（例如，使用[Beam](https://beam.apache.org/) \[Java、Python、Go、SQL\] 组合批处理/流式处理管道并在[Flink](https://flink.apache.org/)、[Spark](https://spark.apache.org/)等运行器上执行它们所需的额外基础设施）[数据流](https://cloud.google.com/dataflow)等）。

> 根据用户生成的实时历史推荐内容。请注意，使用相同的模型，但输入数据可以更改和增长。

如果我们无限减少每个批处理事件之间的时间，我们将[有效地进行](https://www.ververica.com/blog/batch-is-a-special-case-of-streaming)流（实时）处理，因为这些功能将始终是最新的。

小费

即使我们的应用程序需要流处理，如果技术上更容易，最好先用批处理实现系统。如果我们的任务是高风险的并且即使对于初始部署也需要流处理，我们仍然可以尝试对内部版本进行批处理。这可以让我们开始收集反馈，生成更多数据来标记，等等。

## 学习

到目前为止，虽然我们可以选择使用批处理/流式功能并提供批处理/实时预测，但我们一直保持模型固定。然而，这是我们必须根据用例和我们的基础设施允许的情况做出的另一个决定。

### 线下学习

传统的方法是离线训练我们的模型，然后将它们部署到推理中。随着新数据被标记、验证等，我们可能会定期离线重新训练它们，并在评估后部署它们。如果我们在[监控](https://madewithml.com/courses/mlops/monitoring/)过程中发现漂移等问题，我们也可能会加快再培训。

![离线学习](https://madewithml.com/static/images/mlops/systems-design/offline_learning.png)

-   ✅ 无需担心为计算配置资源，因为它发生在离线状态。
-   ✅ 不急于立即标记和验证最近的数据。
-   ❌ 模型可能会变得陈旧，并且可能无法适应最近的变化，直到某些监控警报触发重新训练。

### 在线学习

为了真正提供最明智的预测，我们应该有一个基于最新数据训练的模型。然而，不是使用昂贵的无状态批量学习，而是采用有状态和增量学习方法。在这里，模型像往常一样在初始数据集上离线训练，然后随着新数据的可用在单个实例或小批量级别随机更新。这消除了与对相同过去数据进行传统无状态、冗余训练相关的计算成本。

![在线学习](https://madewithml.com/static/images/mlops/systems-design/online_learning.png)

-   ✅ 模型了解分布变化，可以快速适应以提供高度知情的预测。
-   ✅ 有状态训练可以显着降低计算成本并提供更快的收敛速度。
-   ✅ 可用于发生事件为标签的任务（用户点击、时间序列等）
-   ❌ 对于涉及明确标记或延迟结果的任务可能无法执行。
-   ❌ 当模型从恶意的实时生产数据中学习时（通过监控和回滚来缓解），容易发生灾难性的推断。
-   ❌ 模型可能会遭受[灾难性遗忘](https://en.wikipedia.org/wiki/Catastrophic_interference)，因为我们会继续使用新数据对其进行更新。

那么新的特征值呢？

通过在线学习，我们如何在不从头开始重新训练的情况下编码新的特征值？

显示答案

我们可以使用巧妙的技巧来表示词汇外的特征值，例如基于映射特征值或散列的编码。例如，我们可能想对几家餐厅的名称进行编码，但我们的编码器并未明确映射。相反，我们可以选择根据其位置、美食等来表示餐厅，因此任何具有这些特征值的新餐厅都可以以与我们在训练期间可用的餐厅类似的方式表示。类似地，散列可以映射 OOV 值，但请记住，这是一种单向编码（无法反转散列以查看值是什么），我们必须选择足够大的散列大小以避免冲突（<10% ）。

## 基础设施

我们处理特征和提供预测的方式决定了我们如何部署应用程序。根据管道组件、规模等，我们有几种不同的部署方式。

### 计算引擎

AWS EC2、Google Compute、Azure VM、on-prem 等计算引擎可以跨多个工作人员启动我们的应用程序。

-   **优点**：易于部署和管理这些单一实例。
-   **缺点**：当我们确实需要扩展时，单独管理这些实例并不容易。

### 容器编排

通过[Kubernetes](https://kubernetes.io/) (K8s) 进行容器编排，用于托管部署、扩展等。有几个特定于 ML 的平台可以帮助我们通过[Seldon](https://www.seldon.io/tech/)、[KFServing](https://www.kubeflow.org/docs/components/kfserving/kfserving/)等控制平面对 K8s 进行**自我管理**。但是，也有**完全托管的**解决方案，例如如[SageMaker](https://aws.amazon.com/sagemaker/)、[Cortex](https://www.cortex.dev/)、[BentoML](https://www.bentoml.ai/)等。其中许多工具还具有附加功能，例如实验跟踪、监控等。[](https://www.seldon.io/tech/)[](https://www.kubeflow.org/docs/components/kfserving/kfserving/)[](https://aws.amazon.com/sagemaker/)[](https://www.cortex.dev/)[](https://www.bentoml.ai/)

![容器编排](https://madewithml.com/static/images/mlops/systems-design/managed.png)

-   **优点**：非常容易扩展我们的服务，因为所有管理器都具有适当的组件（负载平衡器、控制平面等）
-   **缺点**：可能会引入过多的复杂性开销。

### 无服务器

无服务器选项，例如[AWS Lambda](https://aws.amazon.com/lambda/)、[Google Cloud Functions](https://cloud.google.com/functions)等。

-   **优点**：无需管理任何服务器，它会根据请求流量自动扩展。
-   **缺点**：函数存储、有效负载等的大小限制基于提供者，通常没有加速器（GPU、TPU 等）

> 请务必探索与这些部署和服务选项相关的[CI/CD 工作流程](https://madewithml.com/courses/mlops/cicd/#serving)，以便您可以进行持续的培训、验证和服务流程。

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre id="__code_1"><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Systems design - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
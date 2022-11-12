---
layout:     post
title:      设计机器学习产品
subtitle:   2022年11月
date:       2022-11-12
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Blog
---


## 设计机器学习产品

___

用于指导机器学习系统开发周期的模板，该模板将产品需求、设计文档和项目考虑因素考虑在内。

## 概述

在本课程中，我们不仅会开发机器学习模型，还会讨论以可重现、可靠和稳健的方式将我们的模型投入生产所需的所有重要 ML 系统和软件设计组件。我们将从为我们将要构建的精确产品设置场景开始。虽然这是一门技术课程，但最初的产品设计过程非常关键，是区分优秀产品和平庸产品的关键。本课将提供如何思考 ML + 产品的结构。

## 模板

此模板旨在指导机器学习产品开发。虽然此模板最初将按顺序完成，但它自然会涉及基于迭代反馈的非线性参与。对于我们产品的每个主要版本，我们都应该遵循这个模板，这样所有的决策都是透明的和记录在案的。

[产品](https://madewithml.com/courses/mlops/design/#product)（_什么_和_原因_）→[工程](https://madewithml.com/courses/mlops/design/#engineering)（_如何_）→[项目](https://madewithml.com/courses/mlops/design/#project)（_谁_和_何时_）

虽然我们的文档会很详细，但我们可以通过浏览机器学习画布来开始这个过程：

[![机器学习画布](https://madewithml.com/static/images/mlops/design/ml_canvas.png)](https://madewithml.com/static/templates/ml-canvas.pdf)

👉   Download a PDF of the ML canvas to use for your own products → [ml-canvas.pdf](https://madewithml.com/static/templates/ml-canvas.pdf) (right click the link and hit "Save Link As...")

From this high-level canvas, we can create detailed documentation for each release:

```
# Documentation
📂 project/
├── 📄 Overview
├── 📂 release-1
| ├── 📄 product requirements [Product]
| ├── 📄 design documentation [Engineering]
| ├── 📄 project planning     [Project]
├── ...
└── 📂 release-n

```

> Throughout this lesson, we'll state and justify the assumptions we made to simplify the problem space.

## Product Management

\[_What_ & _Why_\]: motivate the need for the product and outline the objectives and key results.

Note

Each section below has a dropdown component called "Our task", which will discuss the specific topic with respect to the specific product that we're trying to build.

### Overview

#### Background

Set the scene for what we're trying to do through a customer-centric approach:

-   `customer`: profile of the customer we want to address
-   `goal`: main goal for the customer
-   `pains`: obstacles in the way of the customer achieving the goal
-   `gains`: what would make the job easier for the customer?

Our task

-   `customer`: machine learning developers and researchers.
-   `goal`: stay up-to-date on ML content for work, knowledge, etc.
-   `pains`: too much uncategorized content scattered around the internet.
-   `gains`: a central location with categorized content from trusted 3rd party sources.

#### Value proposition

Propose the value we can create through a product-centric approach:

-   `product`: what needs to be build to help the customer reach their goal?
-   `alleviates`: how will the product reduce pains?
-   `advantages`: how will the product create gains?

Our task

-   `product`: service that discovers and categorizes ML content from popular sources.
-   `alleviates`: timely display categorized content for customers to discover.
-   `advantages`: customers only have to visit our product to stay up-to-date.

![产品样机](https://madewithml.com/static/images/mlops/design/product.png)

> Yes, we actually did build this before realizing it exacerbated noise and hype. And so, we pivoted into teaching the community how to responsibly deliver value with ML.

#### Objectives

Breakdown the product into key objectives that we want to focus on.

Our task

-   Allow customers to add and categorize their own projects.
-   Discover ML content from trusted sources to bring into our platform.
-   Classify incoming content (with high precision) for our customers to easily discover. **\[OUR FOCUS\]**
-   Display categorized content on our platform (recent, popular, recommended, etc.)

### Solution

Describe the solution required to meet our objectives, including it's core features, integration, alternatives, constraints and what's out-of-scope.

> May require separate documentation (wireframes, user stories, mock-ups, etc.).

Our task

Develop a model that can classify the incoming content so that it can be organized by category on our platform.

`Core features`:

-   ML service that will predict the correct categories for incoming content. **\[OUR FOCUS\]**
-   user feedback process for incorrectly classified content.
-   workflows to categorize content that the service was incorrect about or not as confident in.
-   duplicate screening for content that already exists on the platform.

`Integrations`:

-   categorized content will be sent to the UI service to be displayed.
-   classification feedback from users will sent to labeling workflows.

`Alternatives`:

-   allow users to add content manually (bottleneck).

`Constraints`:

-   maintain low latency (>100ms) when classifying incoming content. **\[Latency\]**
-   only recommend tags from our list of approved tags. **\[Security\]**
-   avoid duplicate content from being added to the platform. **\[UI/UX\]**

`Out-of-scope`:

-   identify relevant tags beyond our approved list of tags.
-   using full-text HTML from content links to aid in classification.
-   interpretability for why we recommend certain tags.
-   identifying multiple categories (see [dataset](https://madewithml.com/courses/mlops/design/#dataset) section for details).

#### Feasibility

How feasible is our solution and do we have the required resources to deliver it (data, $, team, etc.)?

Our task

We have a dataset of ML content that our users have manually added to the platform. We'll need to assess if it has the necessary signals to meet our [objectives](https://madewithml.com/courses/mlops/design/#objectives).

| 
Sample data point

 |
| --- |
| 

```
1
2
3
4
5
6
7
```



 | 

```
{
    "id": 443,
    "created_on": "2020-04-10 17:51:39",
    "title": "AllenNLP Interpret",
    "description": "A Framework for Explaining Predictions of NLP Models",
    "tag": "natural-language-processing"
}

```



 |

## Engineering

\[_How_\]: can we engineer our approach for building the product.

### Data

Describe the training and production (batches/streams) sources of data.

Our task

-   **training**:
    -   access to [input data](https://github.com/GokuMohandas/Made-With-ML/blob/main/datasets/projects.csv) and [labels](https://github.com/GokuMohandas/Made-With-ML/blob/main/datasets/tags.csv) for training.
    -   information on feature origins and schemas.
    -   was there sampling of any kind applied to create this dataset?
    -   are we introducing any data leaks?
-   **production**:
    -   access to timely batches of ML content from scattered sources (Reddit, Twitter, etc.)
    -   how can we trust that this stream only has data that is consistent with what we have historically seen?

#### Labeling

Describe the labeling process and how we settled on the features and labels.

Our task

**Labeling**: labeled using categories of machine learning (a subset of which our platform is interested in).

**Features**: text features (title and description) to provide signal for the classification task.

**Labels**: reflect the content categories we currently display on our platform:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>[</span><span>'natural-language-processing'</span><span>,</span>
 <span>'computer-vision'</span><span>,</span>
 <span>'mlops'</span><span>,</span>
  <span>...</span>
 <span>'other'</span><span>]</span>
</code></pre></div></td></tr></tbody></table>

### Evaluation

Before we can model our objective, we need to be able to evaluate how we’re performing.

#### Metrics

One of the hardest challenges with evaluation is tying our core [objectives](https://madewithml.com/courses/mlops/design/#objectives) (may be qualitative) with quantitative metrics that our model can optimize on.

Our task

We want to be able to classify incoming data with high precision so we can display them properly. For the projects that we categorize as `other`, we can _recall_ any misclassified content using manual labeling workflows. We may also want to evaluate performance for specific classes or [slices](https://madewithml.com/courses/mlops/evaluation/#slices) of data.

What are our priorities

How do we decide which metrics to prioritize?

Show answer

It entirely depends on the specific task. For example, in an email spam detector, precision is very important because it's better than we some spam then completely miss an important email. Overtime, we need to iterate on our solution so all evaluation metrics improve but it's important to know which one's we can't comprise on from the get-go.

#### Offline evaluation

[Offline evaluation](https://madewithml.com/courses/mlops/evaluation/) requires a gold standard labeled dataset that we can use to benchmark all of our [modeling](https://madewithml.com/courses/mlops/design/#modeling).

Our task

We'll be using the [historical dataset](https://github.com/GokuMohandas/Made-With-ML/blob/main/datasets/projects.csv) for offline evaluation. We'll also be creating [slices](https://madewithml.com/courses/mlops/evaluation/#slices) of data that we want to evaluate in isolation.

#### Online evaluation

[Online evaluation](https://madewithml.com/courses/mlops/evaluation/#online-evaluation) ensures that our model continues to perform well in production and can be performed using labels or, in the event we don't readily have labels, [proxy signals](https://madewithml.com/courses/mlops/monitoring/#performance).

Our task

-   manually label a subset of incoming data to evaluate periodically.
-   asking the initial set of users viewing a newly categorized content if it's correctly classified.
-   allow users to report misclassified content by our model.

It's important that we measure real-time performance before committing to replace our existing version of the system.

-   Internal canary rollout, monitoring for proxy/actual performance, etc.
-   Rollout to the larger internal team for more feedback.
-   A/B rollout to a subset of the population to better understand UX, utility, etc.

> Not all releases have to be high stakes and external facing. We can always include internal releases, gather feedback and iterate until we’re ready to increase the scope.

### Modeling

While the specific methodology we employ can differ based on the problem, there are core principles we always want to follow:

-   **End-to-end utility**: the end result from every iteration should deliver minimum end-to-end utility so that we can benchmark iterations against each other and plug-and-play with the system.
-   **Manual before ML**: incorporate deterministic components where we define the rules before using probabilistic ones that infer rules from data → [baselines](https://madewithml.com/courses/mlops/baselines).
-   **Augment vs. automate**: allow the system to supplement the decision making process as opposed to making the final decision.
-   **Internal vs. external**: not all early releases have to be end-user facing. We can use early versions for internal validation, feedback, data collection, etc.
-   **Thorough**: every approach needs to be well [tested](https://madewithml.com/courses/mlops/testing/) (code, data + models) and [evaluated](https://madewithml.com/courses/mlops/evaluation/), so we can objectively benchmark different approaches.

Our task

-   v1: creating a gold-standard labeled dataset that is representative of the problem space.
-   v2: rule-based text matching approaches to categorize content.
-   v3: probabilistically predicting labels from content title and description.
-   v4: ...

Decouple POCs and implementations

Each of these approaches would involve proof-of-concept (POC) release and an implementation release after validating it's utility over previous approaches. We should decouple POCs and implementations because if a POC doesn't prove successful, then we can't do the implementation and all the associated planning is no longer applicable.

Utility in starting simple

Some of the earlier, simpler, approaches may not deliver on a certain performance objective. What are some advantages of still starting simple?

Show answer

-   get internal feedback on end-to-end utility.
-   perform A/B testing to understand UI/UX design.
-   deployed locally to start generating more data required for more complex approaches.

#### Feedback

How do we receive feedback on our system and incorporate it into the next iteration? This can involve both human-in-the-loop feedback as well as automatic feedback via [monitoring](https://madewithml.com/courses/mlops/monitoring/), etc.

Our task

-   enforce human-in-loop checks when there is low confidence in classifications.
-   allow users to report issues related to misclassification.

Always return to the value proposition

While it's important to iterate and optimize the internals of our workflows, it's even more important to ensure that our ML systems are actually making an impact. We need to constantly engage with stakeholders (management, users) to iterate on why our ML system exists.

![产品开发周期](https://madewithml.com/static/images/mlops/iteration/development_cycle.png)

## Project Management

\[_Who_ & _When_\]: organizing all the product requirements into manageable timelines so we can deliver on the vision.

### Team

Which teams and specific members from those teams need to be involved in this project? It’s important to consider even the minor features so that everyone is aware of it and so we can properly scope and prioritize our timelines. Keep in mind that this isn’t the only project that people might be working on.

Our task

-   **Product**: the members responsible for outlining the product requirements and approving them may involve product managers, executives, external stakeholders, etc.
-   **System design**:
    -   **Data engineering**: responsible for the data dependencies, which include robust workflows to continually deliver the data and ensuring that it’s properly validated and ready for downstream applications.
    -   **Machine learning**: develop the probabilistic systems with appropriate evaluation.
    -   **DevOps**: deploy the application and help autoscale based on traffic.
    -   **UI/UX**: consume the system’s outputs to deliver the new experience to the user.
    -   **Accessibility**: help educate the community for the new rollouts and to assist with decisions around sensitive issues.
    -   **Site reliability**: maintain the application and to potentially oversee that online evaluation/monitoring workflows are working as they should.
-   **Project**: the members responsible for iterative engagement with the product and engineering teams to ensure that the right product is being built and that it’s being built appropriately may include project managers, engineering managers, etc.

### Deliverables

We need to break down all the [objectives](https://madewithml.com/courses/mlops/design/#objectives) for a particular release into clear deliverables that specify the deliverable, contributors, dependencies, acceptance criteria and status. This will become the granular checklist that our teams will use to decide what to prioritize.

Our task

### Timeline

This is where the project scoping begins to take place. Often, the stakeholders will have a desired time for release and the functionality to be delivered. There _will_ be a lot of back and forth on this based on the results from the feasibility studies, so it's very important to be thorough and transparent to set expectations.

Our task

**v1**：对传入的内容（高精度）进行分类，以便我们的客户轻松发现。

-   XX 进行的勘探研究
-   被 XX 推送给开发人员进行 A/B 测试
-   被 XX 推送到登台
-   被 XX 催促

> 这是一个极其简化的时间线。一个实际的时间线将描述来自所有不同团队的时间线，它们在指定的时间约束或版本发布时用垂直线堆叠在一起。

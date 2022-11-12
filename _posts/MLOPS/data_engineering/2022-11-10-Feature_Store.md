---
layout:     post
title:      特征仓库
subtitle:   2022年11月
date:       2022-11-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Feature Store

---


什么是特色商店
让我们通过按时间顺序查看开发人员在当前工作流程中面临的挑战来激发对功能存储的需求。假设我们有一项任务，我们需要使用实体（例如用户）的特征来预测某些东西。

重复：孤立的特征开发（对于每个独特的 ML 应用程序）可能导致重复工作（设置摄取管道、特征工程等）。
Solution：创建一个中央功能存储库，整个团队在其中贡献维护的功能，任何人都可以将其用于任何应用程序。
偏斜：我们可能有不同的管道来生成训练和服务的特征，这些管道可以通过细微的差异引入偏斜。
Solution：使用统一的管道创建特征并将它们存储在训练和服务管道从中提取的中心位置。
值：一旦我们建立了数据管道，我们需要确保我们的输入特征值是最新的，这样我们就不会处理陈旧的数据，同时保持时间点的正确性，这样我们就不会引入数据泄漏。
Solution：通过提取在进行预测时可用的内容来检索相应结果的输入特征。
时间点正确性是指将适当的最新输入特征值映射到观察到的结果. 这涉及知道时间（) 需要进行预测，以便我们可以收集特征值 (） 当时。

时间点正确性
在实际构建我们的特征存储时，我们需要有几个核心组件来应对这些挑战：

数据摄取：从各种来源（数据库、数据仓库等）摄取数据并保持更新的能力。
特征定义：定义实体和相应特征的能力
历史特征：检索历史特征以用于训练的能力。
在线特征：能够从低延迟来源检索特征以进行推理。
这些组件中的每一个都相当容易设置，但将它们连接在一起需要一个托管服务、用于交互的 SDK 层等。最好不要从头开始构建，而是利用一个生产就绪的功能存储选项，例如Feast , Hopsworks , Tecton , Rasgo等。当然，大型云提供商也有自己的功能存储选项（亚马逊的SageMaker Feature Store，谷歌的Vertex AI等）

小费

我们强烈建议您在完成之前的课程后探索本课程，因为主题（和代码）是迭代开发的。但是，我们确实创建了 使用交互式笔记本快速概览的功能存储库。

过度工程
并非所有机器学习平台都需要特征存储。事实上，我们的用例是一个没有从特征存储中受益的任务的完美示例。我们所有的数据点都是独立的、无状态的、来自客户端的，并且没有任何实体会随着时间的推移而发生变化。当我们需要为我们不断生成预测的实体拥有最新的特征时，特征存储的真正实用性就会大放异彩。比如用户在电商平台上的行为（点击、购买等），或者最近一个小时内送餐员的配送等。

我什么时候需要功能商店？
为了回答这个问题，让我们回顾一下功能存储解决的主要挑战：

重复：如果我们没有太多的 ML 应用程序/模型，我们真的不需要添加特征存储的额外复杂性来管理转换。所有特征转换都可以直接在模型处理中完成，也可以作为单独的函数完成。我们甚至可以将这些转换组织在一个单独的中央存储库中，供其他团队成员使用。但这很快就会变得难以使用，因为开发人员仍然需要知道要调用哪些转换以及哪些与他们的特定模型兼容等。
笔记

此外，如果转换是计算密集型的，那么它们将通过在不同应用程序的重复数据集上运行而产生大量成本（而不是拥有一个具有最新转换特征的中心位置）。

Skew：类似于重复工作，如果我们的转换可以绑定到模型或作为独立函数，那么我们可以重用相同的管道来生成用于训练和服务的特征值。但随着应用程序、功能和转换数量的增长，这变得复杂且计算密集。

价值：如果我们不使用需要在服务器端计算的特征（批处理或流式处理），那么我们不必担心时间点等概念。但是，如果我们是，一个特征存储可以让我们在所有数据源中检索适当的特征值，而开发人员不必担心使用不同的工具来处理不同的数据源（批处理、流式传输等）

盛宴
我们将利用Feast作为我们应用程序的功能存储，因为它易于本地设置、用于训练/服务的 SDK 等。


# Install Feast and dependencies
pip install feast==0.10.5 PyYAML==5.3.1 -q
👉 跟随互动笔记本 我们实现以下概念时的功能存储库。

设置
我们将在项目的根目录中创建一个功能存储库。Feast将为我们创建一个配置文件，我们将添加一个额外的features.py文件来定义我们的功能。

传统上，功能存储库将是它自己的隔离存储库，其他服务将使用它来读取/写入功能。


mkdir -p stores/feature
mkdir -p data
feast init --minimal --template local features
cd features
touch features.py
在 /content/features 中创建一个新的 Feast 存储库。
初始化的功能存储库（以及我们添加的附加文件）将包括：


features/
├── feature_store.yaml  - configuration
└── features.py         - feature definitions
我们将在feature_store.yaml文件中配置注册表和在线商店 (SQLite) 的位置。

批量处理
registry：包含有关我们的功能存储库的信息，例如数据源、功能视图等。由于它位于数据库中，而不是 Python 文件中，因此可以在生产中非常快速地访问它。
在线商店：数据库（本地 SQLite），用于存储已定义实体的（最新）特征，用于在线推理。
如果我们所有的功能定义看起来都有效，Feast 会将有关 Feast 对象的元数据同步到注册表。注册表是一个小型数据库，存储您在功能存储库中拥有的大部分相同信息。此步骤是必要的，因为生产功能服务基础设施在运行时将无法访问功能存储库中的 Python 文件，但它将能够有效且安全地从注册表中读取功能定义。

当我们在本地运行 Feast 时，线下商店通过 Pandas 时间点连接有效地表示。而在生产中，线下商店可能更强大，例如Google BigQuery、Amazon RedShift等。

我们将继续将其粘贴到我们的features/feature_store.yaml文件中（笔记本单元格会自动执行此操作）：


project: features
registry: ../stores/feature/registry.db
provider: local
online_store:
    path: ../stores/feature/online_store.db
数据摄取
第一步是与我们的数据源（数据库、数据仓库等）建立连接。Feast 要求其数据源来自文件 ( Parquet )、数据仓库 ( BigQuery ) 或数据流 ( Kafka / Kinesis )。features.json我们将从 DataOps 管道 (遍历每一行以收集特征值）。


import os
import pandas as pd

# Load labeled projects
projects = pd.read_csv("https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/projects.csv")
tags = pd.read_csv("https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/tags.csv")
df = pd.merge(projects, tags, on="id")
df["text"] = df.title + " " + df.description
df.drop(["title", "description"], axis=1, inplace=True)
df.head(5)

ID	创建于	标签	文本
0	6	2020-02-20 06:43:18	计算机视觉	YOLO 和 RCNN 在现实世界中的比较...
1	7	2020-02-20 06:47:21	计算机视觉	Show, Infer & Tell：C 的上下文推理...
2	9	2020-02-24 16:24:45	图学习	很棒的图分类我的集合...
3	15	2020-02-28 23:55:26	强化学习	令人敬畏的蒙特卡洛树搜索精选列表...
4	19	2020-03-03 13:54:31	图学习	扩散到矢量参考实现...


# Format timestamp
df.created_on = pd.to_datetime(df.created_on)

# Convert to parquet
DATA_DIR = Path(os.getcwd(), "data")
df.to_parquet(
    Path(DATA_DIR, "features.parquet"),
    compression=None,
    allow_truncated_timestamps=True,
)
特征定义
现在我们已经准备好数据源，我们可以为特征存储定义我们的特征。


from datetime import datetime
from pathlib import Path
from feast import Entity, Feature, FeatureView, ValueType
from feast.data_source import FileSource
from google.protobuf.duration_pb2 import Duration
第一步是定义特征的位置（在我们的例子中是 FileSource）和每个数据点的时间戳列。


# Read data
START_TIME = "2020-02-17"
project_details = FileSource(
    path=str(Path(DATA_DIR, "features.parquet")),
    event_timestamp_column="created_on",
)
接下来，我们需要定义每个数据点所属的主要实体。在我们的例子中，每个项目都有一个唯一的 ID，其中包含文本和标签等功能。


# Define an entity
project = Entity(
    name="id",
    value_type=ValueType.INT64,
    description="project id",
)
最后，我们准备创建一个FeatureView ，它从数据源 ( ) 在特定时间段 ( ) 内加载features各种值类型的特定特征 ( )。inputttl


# Define a Feature View for each project
project_details_view = FeatureView(
    name="project_details",
    entities=["id"],
    ttl=Duration(
        seconds=(datetime.today() - datetime.strptime(START_TIME, "%Y-%m-%d")).days * 24 * 60 * 60
    ),
    features=[
        Feature(name="text", dtype=ValueType.STRING),
        Feature(name="tag", dtype=ValueType.STRING),
    ],
    online=True,
    input=project_details,
    tags={},
)
因此，让我们继续通过将此代码移动到我们的features/features.py脚本中来定义我们的功能视图（笔记本单元会自动执行此操作）：

显示代码
一旦我们定义了我们的功能视图，我们就可以apply将我们的功能的版本控制定义推送到注册表以便快速访问。它还将配置我们在feature_store.yaml.


cd features
feast apply
注册实体 id
注册功能视图project_details 为 project_details部署
基础架构
历史特征
一旦我们注册了我们的特征定义以及数据源、实体定义等，我们就可以使用它来获取历史特征。这是通过使用提供的时间戳连接完成的，使用 pandas 进行本地设置或 BigQuery、Hive 等作为生产的离线数据库。


import pandas as pd
from feast import FeatureStore

# Identify entities
project_ids = df.id[0:3].to_list()
now = datetime.now()
timestamps = [datetime(now.year, now.month, now.day)]*len(project_ids)
entity_df = pd.DataFrame.from_dict({"id": project_ids, "event_timestamp": timestamps})
entity_df.head()
ID	event_timestamp
0	6	2022-06-23
1	7	2022-06-23
2	9	2022-06-23

# Get historical features
store = FeatureStore(repo_path="features")
training_df = store.get_historical_features(
    entity_df=entity_df,
    feature_refs=["project_details:text", "project_details:tag"],
).to_df()
training_df.head()
event_timestamp	ID	project_details__text	项目详情__标签
0	2022-06-23 00:00:00+00:00	6	YOLO 和 RCNN 在现实世界中的比较...	计算机视觉
1	2022-06-23 00:00:00+00:00	7	Show, Infer & Tell：C 的上下文推理...	计算机视觉
2	2022-06-23 00:00:00+00:00	9	很棒的图分类我的集合...	图学习
物化
对于在线推理，我们希望通过我们的在线商店快速检索特征，而不是从慢速连接中获取它们。但是，这些功能还没有出现在我们的在线商店中，所以我们需要先实现它们。


cd features
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
将 1 个功能视图具体化到 2022-06-23 19:16:05+00:00 到 sqlite 在线商店。
project_details 从 2020-02-17 19:16:06+00:00 到 2022-06-23 19:16:05+00:00: 
100%|███████████████ ███████████████████████████████████████████| 955/955 [00:00<00:00, 10596.97it/s]
这已将我们所有项目的功能移至在线商店，因为这是第一次实现在线商店。当我们随后运行该materialize-incremental命令时，Feast 会跟踪以前的具体化，因此我们只会具体化自上次尝试以来的新数据。

在线功能
一旦我们实现了特征（或在流场景中直接发送到在线商店），我们就可以使用在线商店来检索特征。


# Get online features
store = FeatureStore(repo_path="features")
feature_vector = store.get_online_features(
    feature_refs=["project_details:text", "project_details:tag"],
    entity_rows=[{"id": 6}],
).to_dict()
feature_vector

{'id': [6],
 'project_details__tag': ['computer-vision'],
 'project_details__text': ['Comparison between YOLO and RCNN on real world videos Bringing theory to experiment is cool. We can easily train models in colab and find the results in minutes.']}
建筑学
批量处理
我们上面实现的特征存储假设我们的任务需要批处理。这意味着对特定实体实例的推理请求可以使用从离线商店实现的功能。请注意，它们可能不是该实体的最新特征值。

批量处理
应用程序数据存储在数据库和/或数据仓库等中。它通过必要的管道为下游应用程序（分析、机器学习等）做好准备。
这些特征被写入离线存储，然后可用于检索历史训练数据以训练模型。在我们的本地设置中，这是通过 Pandas DataFrame 连接给定时间戳和实体 ID 的，但在生产环境中，Google BigQuery 或 Hive 之类的东西会收到功能请求。
一旦我们有了训练数据，我们就可以启动工作流程来优化、训练和验证模型。
我们可以逐步将特征具体化到在线商店，以便我们可以以低延迟检索实体的特征值。在我们的本地设置中，这是通过 SQLite 连接给定的一组实体，但在生产环境中，将使用 Redis 或 DynamoDB 之类的东西。
这些在线功能被传递到已部署的模型以生成将在下游使用的预测。
警告

如果我们的实体（项目）具有随时间变化的功能，我们将逐步将它们具体化到在线商店。但由于他们不这样做，这将被视为过度工程，但重要的是要知道如何将特征存储用于具有随时间变化的特征的实体。

流处理
某些应用程序可能需要流处理，我们需要近乎实时的特征值以低延迟提供最新的预测。虽然我们仍将使用离线商店来检索历史数据，但我们应用程序的实时事件数据将直接通过我们的数据流传输到在线商店进行服务。需要流处理的一个示例是，当我们想要在电子商务平台中检索实时用户会话行为（点击、购买）时，以便我们可以从目录中推荐合适的商品。

流处理
实时事件数据进入我们正在运行的数据流（Kafka / Kinesis等），在那里可以对其进行处理以生成特征。
这些功能被写入在线商店，然后可用于检索在线功能以低延迟提供服务。在我们的本地设置中，这是通过 SQLite 连接给定的一组实体，但在生产环境中，将使用 Redis 或 DynamoDB 之类的东西。
流式处理功能也从数据流写入到批处理数据源（数据仓库、数据库等），以供稍后处理以生成训练数据。
历史数据将被验证并用于生成用于训练模型的特征。这种情况发生的频率取决于是否存在数据注释滞后、计算约束等。
还有一些我们没有在这里可视化的组件，例如统一摄取层 (Spark)，它将来自不同数据源（仓库、数据库等）的数据连接到离线/在线商店，或低延迟服务（ <10 毫秒）。我们可以在官方的Feast 文档中阅读有关所有这些的更多信息，其中还包含使用 Feast 与 AWS、GCP 等设置功能存储的指南。

附加功能
许多功能商店提供商目前（或最近）尝试在功能商店平台中集成的其他功能包括：

transform：在从数据源中提取的原始数据之上直接应用全局预处理或特征工程的能力。
Current solution：在写入特征存储之前将转换作为单独的 Spark、Python 等工作流任务应用。
验证：断言期望和识别特征值上的数据漂移的能力。
Current solution：将数据测试和监控应用为上游工作流任务，然后再将其写入特征存储。
discover：我们团队中的任何人都可以轻松发现他们可以在其应用程序中利用的功能。
Current solution：在我们的特征存储之上添加一个数据发现引擎，例如Amundsen ，以使其他人能够搜索特征。
再现性
尽管我们可以在发布模型版本时继续使用DVC对训练数据进行版本化，但这可能不是必需的。当我们从源或计算特征中提取数据时，它们应该保存数据本身还是只保存操作？

版本化数据
如果 (1) 数据是可管理的，(2) 如果我们的团队是小型/早期 ML 或 (3) 如果对数据的更改不频繁，则这没关系。
但是随着数据变得越来越大并且我们不断复制它会发生什么。
版本化操作
我们可以保留数据的快照（与我们的项目分开）并提供操作和时间戳，我们可以对这些数据快照执行操作，以重新创建用于训练的精确数据工件。许多数据系统使用时间旅行来有效地实现这一目标。
但最终这也会导致数据存储量大。我们需要的是一个仅追加的数据源，其中所有更改都保存在日志中，而不是直接更改数据本身。因此，我们可以使用带有日志的数据系统来生成数据的版本，而不必存储数据本身的单独快照。
无论上述选择如何，功能商店在这里都非常有用。我们可以将这两个过程分开，以便在需要时更新特征，而不是将数据拉取和特征计算与建模时间耦合。而且我们仍然可以通过有效的时间点正确性、低延迟快照等来实现可重复性。这基本上创造了在任何时间点使用任何版本的数据集的能力。
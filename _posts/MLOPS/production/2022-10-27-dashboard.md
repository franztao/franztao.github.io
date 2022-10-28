---
layout:     post
title:      Dashboard
subtitle:   2022年10月
date:       2022-10-27
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Dashboard

---

创建一个交互式仪表板以使用 Streamlit 直观地检查我们的应用程序。

# intution

在开发应用程序时，有很多技术决策和结果（预处理、性能等）是我们系统不可或缺的。我们如何才能**有效地将其传达**给其他开发人员和业务利益相关者？一种选择是 Jupyter [notebook](https://madewithml.com/courses/foundations/notebooks/)，但它经常被代码弄得乱七八糟，对于非技术团队成员来说访问和运行并不容易。我们需要创建一个无需任何技术先决条件即可访问并有效传达关键发现的仪表板。如果我们的仪表板是交互式的，甚至为技术开发人员提供实用程序，那将更加有用。

## 流光

有一些很棒的工具选项，例如[Dash](https://plotly.com/dash/)、[Gradio](https://gradio.app/)、[Streamlit](https://streamlit.io/)、[Tableau](https://www.tableau.com/)、[Looker](https://looker.com/)等，用于创建仪表板以提供面向数据的见解。传统上，交互式仪表板是专门使用 HTML Javascript、CSS 等前端编程语言创建的。但是，鉴于许多从事机器学习工作的开发人员都在使用 Python，因此工具环境已经发展到弥合这一差距。这些工具现在允许 ML 开发人员在 Python 中创建交互式仪表板和可视化，同时通过 HTML、JS 和 CSS 提供完全自定义。我们将使用[Streamlit](https://streamlit.io/)创建我们的仪表板，因为它具有直观的 API、共享功能和提高社区采用率。

## 设置

使用 Streamlit，我们可以快速创建一个空的应用程序，并且随着我们的开发，UI 也会更新。

```
# Setup
pip install streamlit==1.10.0
mkdir streamlit
touch streamlit/app.py
streamlit run streamlit/app.py
```

```
您现在可以在浏览器中查看您的 Streamlit 应用程序。

  本地网址：http://localhost:8501
  网络网址：http://10.0.1.93:8501
```

这将在[http://localhost:8501](http://localhost:8501/)上自动为我们打开流光仪表板。

> 请务必将此包和版本添加到我们的`requirements.txt`文件中。

## API 参考

在为特定应用程序创建仪表板之前，我们需要了解不同的 Streamlit 组件。不要在本课中全部阅读它们，而是花几分钟时间阅读[API 参考](https://docs.streamlit.io/library/api-reference)。它很短，我们保证您会惊讶于仅使用 Python 就可以创建多少 UI 组件（样式文本、乳胶、表格、绘图等）。我们将详细探讨不同的组件，因为它们适用于为下面的特定仪表板创建不同的交互。

## Sections

`streamlit/app.py`我们将首先通过编辑脚本来概述我们希望在仪表板中包含的部分：

```
import pandas as pd
from pathlib import Path
import streamlit as st

from config import config
from tagifai import main, utils
```

```
# Title
st.title("MLOps Course · Made With ML")

# Sections
st.header("🔢 Data")
st.header("📊 Performance")
st.header("🚀 Inference")
```

要在仪表板上查看这些更改，我们可以刷新仪表板页面（按`R`）或设置它`Always rerun`（按`A`）。

![仪表板](https://madewithml.com/static/images/mlops/dashboard/sections.png)

### 数据

我们将保持仪表板简单，因此我们将只显示标记的项目。

```
st.header("Data")
projects_fp = Path(config.DATA_DIR, "labeled_projects.csv")
df = pd.read_csv(projects_fp)
st.text(f"Projects (count: {len(df)})")
st.write(df)
```

![数据](https://madewithml.com/static/images/mlops/dashboard/data.png)

### 表现

在本节中，我们将展示最新训练模型的性能。同样，我们将保持简单，但我们也可以通过访问模型存储来覆盖更多信息，例如以前部署的改进或回归。

```
st.header("📊 Performance")
performance_fp = Path(config.CONFIG_DIR, "performance.json")
performance = utils.load_dict(filepath=performance_fp)
st.text("Overall:")
st.write(performance["overall"])
tag = st.selectbox("Choose a tag: ", list(performance["class"].keys()))
st.write(performance["class"][tag])
tag = st.selectbox("Choose a slice: ", list(performance["slices"].keys()))
st.write(performance["slices"][tag])
```

![表现](https://madewithml.com/static/images/mlops/dashboard/performance.png)

### 推理

在推理部分，我们希望能够使用最新训练的模型进行快速预测。

```
st.header("🚀 Inference")
text = st.text_input("Enter text:", "Transfer learning with transformers for text classification.")
run_id = st.text_input("Enter run ID:", open(Path(config.CONFIG_DIR, "run_id.txt")).read())
prediction = main.predict_tag(text=text, run_id=run_id)
st.write(prediction)

```

![推理](https://madewithml.com/static/images/mlops/dashboard/inference.png)

> Tip
> 
> 我们的仪表板非常简单，但我们还可以使用更全面的仪表板来反映我们在[机器学习画布](https://madewithml.com/static/templates/ml-canvas.pdf)中涵盖的一些核心主题。
> 
> - 显示我们的[标签](https://madewithml.com/courses/mlops/labeling/)、[EDA](https://madewithml.com/courses/mlops/exploratory-data-analysis/)和[预处理](https://madewithml.com/courses/mlops/preprocessing/)开发阶段的发现。
> - 以交互方式查看[false +/-](https://madewithml.com/courses/mlops/evaluation/#confusion-matrix)并与注释管道连接，以便可以查看和合并对数据的更改。
> - 比较多个版本的性能，以可视化随时间推移的改进/回归（使用模型存储、git 标签等）



## 缓存

有时我们可能有涉及计算量大的操作的视图，例如加载数据或模型工件。最好的做法是通过使用[`@st.cache`](https://docs.streamlit.io/library/api-reference/performance/st.cache)装饰器将它们包装为单独的函数来缓存这些操作。这要求 Streamlit 通过其输入的特定组合来缓存该函数，以在使用相同输入调用该函数时提供相应的输出。

```
@st.cache()
def load_data():
    projects_fp = Path(config.DATA_DIR, "labeled_projects.csv")
    df = pd.read_csv(projects_fp)
    return df

```

## 部署

我们有几种不同的选项来部署和管理我们的 Streamlit 仪表板。我们可以使用 Streamlit 的[共享功能](https://blog.streamlit.io/introducing-streamlit-sharing/)（测试版），它允许我们直接从 GitHub 无缝部署仪表板。随着我们向存储库提交更改，我们的仪表板将继续保持更新。另一种选择是将 Streamlit 仪表板与我们的 API 服务一起部署。我们可以使用 docker-compose 来启动一个单独的容器，或者简单地将其添加到 API 服务的 Dockerfile 的[ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)并暴露适当的端口。后者可能是理想的，特别是如果您的仪表板不打算公开并且您希望增加安全性、性能等。
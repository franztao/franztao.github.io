---
layout:     post
title:      记录代码
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Documenting Code

---

为您的团队和您未来的自己记录代码。

#### Intuition

> 代码告诉你_怎么_做，注释告诉你_为什么_。——[杰夫·阿特伍德](https://en.wikipedia.org/wiki/Jeff_Atwood)

可以通过记录代码来进一步[组织](https://franztao.github.io/2022/10/10/Organization/)代码，让其他人（以及未来的自己）更容易轻松地导航和扩展它。在完成编写代码库的那一刻就最了解代码库，但幸运的是，记录它将使能够快速回到熟悉的心态。文档对开发人员来说可能意味着很多不同的东西，所以让定义最常见的组件：

- `comments`：关于为什么存在一段代码的简短描述。
- `typing`：函数输入和输出数据类型的规范，提供与函数消耗和产生的内容有关的信息。
- `docstrings`：对描述整体效用、参数、返回等的函数和类的有意义的描述。
- `docs`：呈现的网页，总结了所有的功能、类、工作流程、示例等。

> 目前，将在本地生成文档，但请务必查看[应用程序的自动生成](https://github.com/GokuMohandas/mlops-course)[文档页面](https://gokumohandas.github.io/mlops-course)。每次对代码库进行更改时，将在[CI/CD](https://franztao.github.io/2022/10/26/cicd/)课程中学习如何自动创建文档并使其保持最新。

> 代码协作
> 
> 您目前如何与团队中的其他人共享您的代码？有什么可以改进的？

#### Typing

对代码尽可能明确是很重要的。已经讨论过为变量、函数等选择显式名称，但可以显式的另一种方法是为函数的输入和输出定义类型。

到目前为止，函数看起来像这样：

```
def some_function(a, b):
    return c
```

但是可以使用打字来合并更多信息：

```
from typing import List
def some_function(a: List, b: int = 0) -> np.ndarray:
    return c
```

在这里定义了：

- 输入参数`a`是一个列表
- 输入参数`b`是一个整数，默认值为0
- 输出参数`c`是一个 NumPy 数组

可以使用许多其他数据类型，包括`List`、`Set`、`Dict`、和[更多](https://docs.python.org/3/library/typing.html)`Tuple`，以及包含的类型，例如,等。您还可以使用安装的包（例如）甚至自己定义的包中的类型类（例如）。[`Sequence`](https://docs.python.org/3/library/typing.html)`int``float``np.ndarray``LabelEncoder`

> 从 Python 3.9+ 开始，[内置了](https://docs.python.org/3/whatsnew/3.9.html#type-hinting-generics-in-standard-collections)常用类型，因此不再需要导入它们`from typing import List, Set, Dict, Tuple, Sequence`。

## 文档字符串

可以通过添加文档字符串来描述整体实用程序、参数、返回、异常等，从而使代码更加明确。让看一个例子：

```
from typing import List
def some_function(a: List, b: int = 0) -> np.ndarray:
    """Function description.

    ```python
    c = some_function(a=[], b=0)
    print (c)
    ```
    <pre>
    [[1 2]
     [3 4]]
    </pre>

    Args:
        a (List): description of `a`.
        b (int, optional): description of `b`. Defaults to 0.

    Raises:
        ValueError: Input list is not one-dimensional.

    Returns:
        np.ndarray: Description of `c`.

    """
    return c
```

让解压这个函数文档字符串的不同部分：

- `[Line 3]`: 函数整体效用的总结。
- `[Lines 5-12]`: 如何使用功能的例子。
- `[Lines 14-16]`: 函数输入参数的描述。
- `[Lines 18-19]`：函数中可能引发的任何异常。
- `[Lines 21-22]`：函数输出的描述。

[将在下面的文档](https://franztao.github.io/2022/10/10/Documentation/#docs)部分呈现这些文档字符串以生成：

![文档字符串](https://madewithml.com/static/images/mlops/documentation/docstrings.png)

花时间用文档字符串更新项目中的所有函数和类，并确保参考[存储库](https://github.com/GokuMohandas/mlops-course)作为指南。请注意，您可能必须将某些库显式导入某些脚本，因为`type`需要它。例如，没有在`data.py`脚本中明确使用 Pandas 库，但是，确实使用 pandas 数据帧作为输入参数。

```
# tagifai/data.py
import pandas as pd
from typing import List

def replace_oos_labels(df: pd.DataFrame, labels: List, label_col: str, oos_label: str = "other"):
    ...
```

> 理想情况下，会在开发函数和类时将文档字符串添加到它们中，而不是在最后一次完成。

> Tip
> 
> 如果使用[Visual Studio Code](https://code.visualstudio.com/)，请务必使用[Python Docstrings Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)扩展，这样您就可以`"""`在函数下键入，然后点击该Shift键生成模板文档字符串。它将使用输入信息甚至代码中的异常自动填充部分文档字符串！

![vscode 文档字符串生成](https://github.com/NilsJPWerner/autoDocstring/blob/13875f7e5d3a2ad2a2a7e42bad6a10d09fed7472/images/demo.gif?raw=true)

## 文档

所以正在经历所有这些努力，将类型和文档字符串包括到函数中，但它们都隐藏在脚本中。如果可以收集所有这些努力并**自动**将其显示为文档会怎样？好吧，这正是将对以下开源包所做的 → 最终结果[在这里](https://gokumohandas.github.io/mlops-course)。

1. 安装所需的包：
   
   `pip install mkdocs==1.3.0 mkdocstrings==0.18.1`
   
   不会将这些要求直接添加到`requirements.txt`文件中，而是将其与所需的核心库隔离开来。想这样做是因为不是每个人都需要创建文档，因为它不是核心机器学习操作（训练、推理等）。将调整`setup.py`脚本来实现这一点。将在一个`docs_packages`对象下定义这些包：
   
   ```
   # setup.py
   docs_packages = [
       "mkdocs==1.3.0",
       "mkdocstrings==0.18.1"
   ]
   ```
   
   然后将其添加到`setup()`脚本中的对象：

```
# Define our package
setup(
    ...
    install_requires=[required_packages],
    extras_require={
        "dev": docs_packages,
        "docs": docs_packages,
    },
)
```

   现在可以安装这个包：

   `python3 -m pip install -e ".[docs]"`

   还定义了一个`dev`选项，将在课程中更新该选项，以便开发人员可以在一次调用中安装所有必需的和额外的包，而不是一次调用每个额外的必需包。

   `python3 -m pip install -e ".[dev]"`

   创建了一个显式`doc`选项，因为用户只想下载文档包来生成文档（不需要其他包）。[当使用CI/CD 工作流](https://franztao.github.io/2022/10/26/cicd/)通过 GitHub Actions 自动生成文档时，将看到这一点。

2. 初始化 mkdocs
   
   `python3 -m mkdocs new .`
   
   这将创建以下文件：
   
   ```
   .
   ├─ docs/
   │  └─ index.md
   └─ mkdocs.yml
   ```

3. 将首先用项目的特定信息 覆盖`index.md`目录中的默认文件：`docs`
   
   ```
   ## Documentation
   
   - [Workflows](tagifai/main.md): main workflows.
   - [tagifai](tagifai/data.md): documentation of functionality.
   
   ## MLOps Lessons
   
   Learn how to combine machine learning with software engineering to develop, deploy & maintain production ML applications.
   
   - Lessons: [https://madewithml.com/](https://madewithml.com/#mlops)
   - Code: [GokuMohandas/mlops-course](https://github.com/GokuMohandas/mlops-course)
   ```

4. 接下来将为目录中的每个脚本创建文档文件`tagifai`：
   
   ```
   mkdir docs/tagifai
   cd docs/tagifai
   touch main.md utils.md data.md train.md evaluate.md predict.md
   cd ../../
   ```

> 让`docs`目录结构尽可能模仿项目的结构是有帮助的。随着在以后的课程中记录更多目录，这一点变得更加重要。

5. 接下来将添加`tagifai.<SCRIPT_NAME>`到`docs/tagifai`. `tagifai/<SCRIPT_NAME>.py`这将使用有关`mkdocstrings`插件的函数和类（使用它们的文档字符串）的信息填充文件。
   
   > 请务必查看[mkdocs 插件](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins)的完整列表。
   > 
   > ```
   > # docs/tagifai/data.md
   > ::: tagifai.data
   > ```

6. 最后，将在`mkdocs.yml`mkdocs 自动创建的文件中添加一些配置：
   
   ```
   # mkdocs.yml
   site_name: Made With ML
   site_url: https://madewithml.com/
   repo_url: https://github.com/GokuMohandas/mlops-course/
   nav:
     - Home: index.md
     - workflows:
       - main: tagifai/main.md
     - tagifai:
       - data: tagifai/data.md
       - evaluate: tagifai/evaluate.md
       - predict: tagifai/predict.md
       - train: tagifai/train.md
       - utils: tagifai/utils.md
   theme: readthedocs
   plugins:
     - mkdocstrings
   watch:
     - .  # reload docs for any file changes
   ```

7. 在本地提供文档：
   
   `python3 -m mkdocs serve`

## 出版

可以使用公共存储库的[GitHub 页面以及私有存储库的](https://www.mkdocs.org/user-guide/deploying-your-docs/)[私有文档](https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)轻松地免费提供文档。甚至可以将其托管在[自定义域](https://docs.github.com/en/github/working-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site)（例如公司的子域）上。

> 请务必查看为[应用程序自动生成的](https://github.com/GokuMohandas/mlops-course)[文档页面](https://gokumohandas.github.io/mlops-course)。每次对代码库进行更改时，将在[CI/CD](https://franztao.github.io/2022/10/26/cicd/)课程中学习如何自动创建文档并使文档保持最新。

## 信息架构构建

信息架构的逻辑呈现的 5 个过程

![图片](https://mmbiz.qpic.cn/mmbiz_png/crx0uzS8lVsxg18kRhfiaudabvzhfiazq4nGkbjjKzIMlcMRia8xTWMg3plZ8eOlRBAhnJcf4CoqAlR5vIxKmEvzA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

___

本文主体源自以下链接：

```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
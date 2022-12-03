---
layout:     post
title:      打包python代码库
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Packaging a Python Codebase

---

使用配置和虚拟环境来创建用于重现结果的设置。

## Intuition

到目前为止，一直在note本内部工作，这使能够非常快速地训练模型。但是，note本并不容易投入生产，而且并不总是能够控制环境（例如，Google Colab 会定期更新其软件包）。当使用[notebook](https://github.com/GokuMohandas/mlops-course/blob/main/notebooks/tagifai.ipynb)时，有一组预加载的包（`!pip list`在 notebook 中运行以查看所有包）。但是现在想要明确定义环境，以便可以在本地（为和团队成员）以及在部署到生产环境时重现它。在 Python 中打包时有[许多推荐的工具](https://packaging.python.org/guides/tool-recommendations/)，将使用经过验证的[Pip](https://pip.pypa.io/en/stable/)。

> 有许多替代依赖管理和打包工具，例如[Poetry](https://python-poetry.org/)，但这些新选项仍有许多变化。将坚持使用 Pip，因为它适用于应用程序，并且不想处理[长解决周期](https://github.com/python-poetry/poetry/issues/2094)之类的问题。

## 终端

在开始打包之前，需要一种创建文件和运行命令的方法。可以通过终端来执行此操作，这将允许运行 bash、zsh 等语言来执行命令。无论您的操作系统或命令行界面 (CLI) 编程语言如何，运行的所有命令都应该相同。

> Tip
> 
> 强烈建议您使用[iTerm2](https://iterm2.com/) (Mac) 或[ConEmu](https://conemu.github.io/) (Windows) 代替默认终端，因为它具有丰富的功能。

## 项目

虽然将在[下一课](https://franztao.github.io/2022/10/10/Organization/)中将代码从note本组织到脚本，但现在将创建主项目目录，以便可以将打包组件保存在那里。将调用主项目目录`mlops`，但您可以随意命名它。

```
# Create and change into the directory
mkdir mlops
cd mlops
```

## Python

要做的第一件事是设置正确的 Python 版本。将`3.7.13`专门使用版本，但任何版本的 Python 3 都应该可以使用。虽然您可以在线下载不同的 Python 版本，但强烈建议您使用版本管理器，例如[pyenv](https://github.com/pyenv/pyenv)。

> Pyenv 适用于 Mac 和 Linux，但如果你在 Windows 上，建议使用[pyenv-win](https://github.com/pyenv-win/pyenv-win)。



> 强烈建议使用 Python `3.7.13`，因为虽然使用其他版本的 Python 也可以，但可能会遇到与某些可能需要解决的包版本的冲突。

## 虚拟环境

接下来，将设置一个[虚拟环境](https://docs.python.org/3/library/venv.html)，以便为应用程序隔离所需的包。这也将使组件与可能具有不同依赖关系的其他项目分开。一旦创建了虚拟环境，将激活它并安装需要的包。

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pip setuptools wheel

```



让解开这里发生的事情：

1. 创建一个名为`venv`.
2. 激活虚拟环境。输入`deactivate`退出虚拟环境。
3. 升级所需的包，以便下载最新的包轮。

`venv`当列出项目中的目录时，虚拟环境目录应该是可见的：



会知道虚拟环境是活跃的，因为会在终端上显示它的名字。可以通过确保`pip freeze`不返回任何内容来进一步验证。

`(venv) ➜  mlops: pip freeze`

### 要求

将创建一个名为的单独文件`requirements.txt`，将在其中指定要安装的包（及其版本）。虽然可以将这些要求直接放在里面`setup.py`，但许多应用程序仍然在寻找一个单独的`requirements.txt`.

`touch requirements.txt`

应该将包及其版本添加到`requirements.txt`的项目中，因为项目需要它们。不建议先安装所有包然后再安装，`pip freeze > requirements.txt`因为它会将所有包的依赖项转储到文件中（即使是没有明确安装的包）。为了缓解这种情况，可以使用[pipreqs](https://github.com/bndr/pipreqs)、[pip-tools](https://github.com/jazzband/pip-tools)、[pipchill](https://github.com/rbanffy/pip-chill)等工具，它们只会列出非依赖项的包。但是，它们的依赖关系解析并不总是准确的，并且当您想为不同的任务（开发、测试等）分离包时不起作用。

> Tip
> 
> 如果遇到包版本之间的冲突，可以通过指定包需要高于某个版本而不是确切版本来放宽约束。还可以为所有包指定无版本，并允许 pip 解决所有冲突。然后可以看到实际安装了哪个版本并将该信息添加到`requirements.txt`文件中。
> 
> ```
> # requirements.txt
> <PACKAGE>==<VERSION>  # exact version
> <PACKAGE>==<VERSION>  # above version
> <PACKAGE>             # no version
> 
> ```



### 设置

让创建一个名为的文件`setup.py`，以提供有关如何设置虚拟环境的说明。

`touch setup.py`

```
# setup.py
from pathlib import Path
from setuptools import find_namespace_packages, setup

```





将从提取打包的需求开始`requirements.txt`：

```
# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

```





该`setup.py`文件的核心是`setup`描述如何设置包及其依赖项的对象。包将被调用`tagifai`，它将包含运行它所需的所有要求。前几行涵盖[元数据](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#metadata)（名称、描述等），然后定义需求。在这里声明需要等于或高于 3.7 的 Python 版本，然后将需要的包传递给`install_requires`.

```
# setup.py
setup(
    name="tagifai",
    version=0.1,
    description="Classify machine learning projects.",
    author="Goku Mohandas",
    author_email="goku@madewithml.com",
    url="https://madewithml.com/",
    python_requires=">=3.7",
    install_requires=[required_packages],
)

```





查看setup.py

```
from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

# Define our package
setup(
    name="tagifai",
    version=0.1,
    description="Classify machine learning projects.",
    author="Goku Mohandas",
    author_email="goku@madewithml.com",
    url="https://madewithml.com/",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
)

```

## 用法

`requirements.txt`文件中没有定义任何包，但如果定义了，可以使用该`setup.py`文件，现在可以像这样安装包：

```
python3 -m pip install -e .            # installs required packages only

```



> `-e`or标志以`--editable`开发模式安装项目，这样就可以进行更改而无需重新安装包。

现在，如果这样做，`pip freeze`应该看到它`tagifai`已安装。

`pip freeze`

```
# Editable install with no version control (tagifai==0.1)
-e /Users/goku/Documents/madewithml/mlops
```

还应该`tagifai.egg-info`在项目目录中看到一个目录：

```
mlops/
├── tagifai.egg-info/
├── venv/
├── requirements.txt
└── setup.py
```

setup.py 文件有许多替代方案，例如[`setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)和更新的[pyproject.toml](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)。

___

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-49-27-weixin.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2022-12-03-12-50-26-0ea6fc0f877f03a079f15c70641fa7b.jpg)



本文主体源自以下链接：

```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
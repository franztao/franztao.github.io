---
layout:     post
title:      生成文件
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Makefiles

---

为我们的应用程序流程组织命令的自动化工具。

## Intuition

尽管只完成了课程的一半，但已经有很多不同的命令需要跟踪。为了帮助组织一切，将使用[`Makefile`](https://opensource.com/article/18/8/what-how-makefile)一个自动化工具来组织命令。将首先在项目的根目录中创建此文件。

在顶部，`Makefile`需要指定希望所有命令在其中执行的 shell 环境：

```
# Makefile
SHELL = /bin/bash
```

## 成分

在我们的[Makefile](https://github.com/GokuMohandas/mlops-course/tree/main/Makefile)中，我们将创建一个规则列表。这些规则有一个`target`，有时`prerequisites`需要满足（可以是其他目标），在下一行，Tab后面跟着一个`recipe`，指定如何创建目标。

```
# Makefile
target: prerequisites
<TAB> recipe
```

例如，如果我们想创建一个规则来为我们的文件设置样式，我们可以将以下内容添加到我们的`Makefile`：

```
# Styling
style:
    black .
    flake8
    python3 -m isort .
```

> 制表符与空格
> 
> Makefile 要求缩进使用，而不是我们会收到错误的空格：
> 
> 生成文件：: *** 缺少分隔符。停止。
> 
> 幸运的是，即使其他文件使用空格，像 VSCode 这样的编辑器也会自动将缩进更改为制表符。

## 目标

`make <target>`我们可以通过在终端中键入来执行任何规则：

```
# Make a target
$ make style
```

`# Make a target $ make style`

同样，我们可以设置我们的`Makefile`用于创建虚拟环境：

```
# Environment
venv:
    python3 -m venv venv
    source venv/bin/activate && \
    python3 -m pip install pip setuptools wheel && \
    python3 -m pip install -e .
```

> `&&`表示我们希望这些命令在一个 shell 中执行（更多内容[见下文](https://madewithml.com/courses/mlops/makefile/#shells)）。

## PHONY

之所以这样称呼 Makefile，是因为传统上`targets`它们应该是我们可以*制作*的文件。但是，Makefile 也常被用作命令快捷方式，当 Makefile 目标和文件共享相同的名称时会导致混淆！例如，如果我们有一个名为`venv`（我们这样做）的文件，并且`target`在您的 Makefile 中有一个名为`venv`，当您运行时，`make venv`我们将收到此消息：

`$ make venv`

在这种情况下，这是预期的行为，因为如果虚拟环境已经存在，那么我们不想再次*创建*该目标。然而，有时，我们会命名我们的目标并希望它们执行，无论它是否作为实际文件存在。在这些情况下，我们希望[`PHONY`](https://www.gnu.org/software/make/manual/make.html#Phony-Targets)通过在目标上方添加以下行来在我们的 makefile 中定义一个目标：

`.PHONY: <target_name>`

我们的 Makefile 中的大多数规则都需要`PHONY`目标，因为我们希望即使存在共享目标名称的文件，它们也能执行。

```
# Styling
.PHONY: style
style:
    black .
    flake8
    isort .
```

## 先决条件

在我们制定目标之前，我们可以为它们附加先决条件。*这些可以是必须存在的文件目标，也可以是在创建*此目标之前需要执行的 PHONY 目标命令。例如，我们将*样式目标设置为**清理*目标的先决条件，以便所有文件在清理之前都适当地格式化。

```
# Cleaning
.PHONY: clean
clean: style
    find . -type f -name "*.DS_Store" -ls -delete
    find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
    find . | grep -E ".pytest_cache" | xargs rm -rf
    find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
    find . | grep -E ".trash" | xargs rm -rf
    rm -f .coverage
```

## 变量

我们还可以在 Makefile 中设置和使用[变量来组织我们所有的规则。](https://www.gnu.org/software/make/manual/make.html#Using-Variables)

- 我们可以直接在 Makefile 中设置变量。如果该变量未在 Makefile 中定义，则它将默认为具有相同名称的任何环境变量。
  
  ```
  # Set variable
  MESSAGE := "hello world"
  
  # Use variable
  greeting:
      @echo ${MESSAGE}
  
  ```

- 我们也可以像这样在执行规则时使用传入的变量（确保变量没有在 Makefile 中被覆盖）：
  
  `make greeting MESSAGE="hi"`

## Shells

规则配方中的每一行都将在单独的子 shell 中执行。但是对于某些方法，例如激活虚拟环境和加载包，我们希望在一个 shell 中执行所有步骤。为此，我们可以在[`.ONESHELL`](https://www.gnu.org/software/make/manual/make.html#One-Shell)任何目标之上添加特殊目标。

```
# Environment
.ONESHELL:
venv:
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install pip setuptools wheel
    python3 -m pip install -e .

```



然而，这仅在 Make 3.82 及更高版本中可用，大多数 Mac 当前使用的是 3.81 版本。您可以更新到当前版本，也可以`&&`像我们之前那样将您的命令链接起来：

```
# Environment
venv:
    python3 -m venv venv
    source venv/bin/activate && \
    python3 -m pip install pip setuptools wheel && \
    python3 -m pip install -e .

```



## 帮助

我们要添加到我们的`Makefile`（至少现在）的最后一件事是一个`help`目标到最顶层。此规则将为该 Makefile 的功能提供信息性消息：

```
.PHONY: help
help:
    @echo "Commands:"
    @echo "venv    : creates a virtual environment."
    @echo "style   : executes style formatting."
    @echo "clean   : cleans all unnecessary files."

```

`make help`

```

```

> Makefile的内容要[多得多](https://www.gnu.org/software/make/manual/make.html)，但这对于大多数应用 ML 项目来说已经足够了。

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
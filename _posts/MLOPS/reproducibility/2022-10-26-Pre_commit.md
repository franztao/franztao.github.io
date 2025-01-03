---

layout:     post
title:      预提交pre-commit
subtitle:   2022年10月
date:       2022-10-26
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Pre-commit

--- 

使用预提交 git 钩子来确保在提交之前进行检查。

## Intuition

在对本地存储库执行提交之前，心理待办事项列表上有很多项目，从样式、格式化、测试等。很容易忘记其中的一些步骤，尤其是当想要“推送到快速解决”。为了帮助管理所有这些重要步骤，可以使用预提交钩子，当尝试执行提交时，它会自动触发。

> 尽管可以直接在 CI/CD 管道中添加这些检查（例如通过 GitHub 操作），但在推送到远程主机之前验证提交并等待查看需要修复的内容再提交另一个 PR 之前要快得多。

## 安装

将使用[Pre-commit](https://pre-commit.com/)框架来帮助在提交时通过钩子自动执行重要检查。

```
# Install pre-commit
pip install pre-commit==2.19.0
pre-commit install
```

将把它添加到`setup.py`脚本而不是`requirements.txt`文件中，因为它不是机器学习操作的核心。

```
# setup.py
setup(
    ...
    extras_require={
        "dev": docs_packages + style_packages + test_packages + ["pre-commit==2.19.0"],
        "docs": docs_packages,
        "test": test_packages,
    },
)

```



## 配置

`.pre-commit-config.yaml`通过配置文件定义预提交钩子。可以从头开始创建 yaml 配置，也可以使用预提交 CLI 创建可以添加的示例配置。

```
# Simple config
pre-commit sample-config > .pre-commit-config.yaml
cat .pre-commit-config.yaml
```

```
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

```

## Hooks

在创建和使用钩子时，有几个选项可供选择。

### 内置

在示例配置中，可以看到 pre-commit 从它的存储库中添加了一些默认hook。它指定存储库的位置、版本以及要使用的特定hook ID。可以了解这些钩子的功能，并通过探索 pre-commit 的[内置](https://github.com/pre-commit/pre-commit-hooks)钩子来添加更多内容。其中许多还有其他参数，可以配置这些参数来自定义钩子。

```
# Inside .pre-commit-config.yaml
...
-   id: check-added-large-files
    args: ['--maxkb=1000']
    exclude: "notebooks/tagifai.ipynb"
...

```



> 一定要探索许多其他[内置的钩子](https://github.com/pre-commit/pre-commit-hooks)，因为在项目中使用了一些非常有用的钩子。例如，`check-merge-conflict`查看是否存在任何挥之不去的合并冲突字符串，或者`detect-aws-credentials`是否不小心将凭据暴露在文件中，等等。

_还可以通过使用可选的排除_键来排除某些文件被钩子处理。可以为每个钩子 ID 配置许多其他[可选键](https://pre-commit.com/#pre-commit-configyaml---hooks)。

```
# Inside .pre-commit-config.yaml
...
-   id: check-yaml
    exclude: "mkdocs.yml"
...

```



### Custom

除了 pre-commit 的内置钩子，还有许多自定义的、第 3 方[流行的钩子](https://pre-commit.com/hooks.html)可供选择。例如，如果想使用 Black 作为钩子应用格式检查，可以利用 Black 的 pre-commit 钩子。

```
# Inside .pre-commit-config.yaml
...
-   repo: https://github.com/psf/black
    rev: 20.8b1
    hooks:
    -   id: black
        args: []
        files: .
...

```

这个特定的钩子在 Black 存储库中的[.pre-commit-hooks.yaml](https://github.com/psf/black/blob/master/.pre-commit-hooks.yaml)下定义，其他自定义钩子也在其各自的包存储库下。

### 当地的

也可以创建自己的本地钩子，而无需配置单独的 .pre-commit-hooks.yaml。这里定义了两个 pre-commit 钩子，`test-non-training`并且`clean`，来运行在 Makefile 中定义的一些命令。同样，可以运行任何带有参数的入口命令来非常快速地创建钩子。

```
# Inside .pre-commit-config.yaml
...
- repo: local
  hooks:
    - id: test
      name: test
      entry: make
      args: ["test"]
      language: system
      pass_filenames: false
    - id: clean
      name: clean
      entry: make
      args: ["clean"]
      language: system
      pass_filenames: false

```

> 查看完整`.pre-commit-config.yaml`

```
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
        exclude: "config/run_id.txt"
    -   id: check-yaml
        exclude: "mkdocs.yml"
    -   id: check-added-large-files
        args: ['--maxkb=1000']
        exclude: "notebooks"
    -   id: check-ast
    -   id: check-json
    -   id: check-merge-conflict
    -   id: detect-aws-credentials
    -   id: detect-private-key
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
        args: []
        files: .
-   repo: https://gitlab.com/PyCQA/flake8
    rev: 3.9.2
    hooks:
    -   id: flake8
-   repo: https://github.com/PyCQA/isort
    rev: 5.10.1
    hooks:
    -   id: isort
        args: []
        files: .
-   repo: https://github.com/asottile/pyupgrade  # update python syntax
    rev: v2.34.0
    hooks:
    -   id: pyupgrade
        args: [--py36-plus]
- repo: local
hooks:
    - id: test
    name: test
    entry: make
    args: ["test"]
    language: system
    pass_filenames: false
    - id: clean
    name: clean
    entry: make
    args: ["clean"]
    language: system
    pass_filenames: false
```

## Commit

当尝试提交时，预提交hook将自动执行。将能够查看每个钩子是否通过或失败并进行任何更改。如果任何hook失败，必须修复相应的文件，或者在许多情况下，会自动重新格式化。

```
...
detect private key.....................................PASSED
black..................................................FAILED
...
```

如果任何钩子失败，需要一次`add`又一次`commit`地确保所有钩子都通过。

```
git add .
git commit -m <MESSAGE>
```

![预提交](https://madewithml.com/static/images/mlops/pre_commit/commit.png)

## Run

尽管预提交hook是在提交之前（预）运行，但可以手动触发所有或一组文件上的所有或单个hook。

```
# Run
pre-commit run --all-files  # run all hooks on all files
pre-commit run <HOOK_ID> --all-files # run one hook on all files
pre-commit run --files <PATH_TO_FILE>  # run all hooks on a file
pre-commit run <HOOK_ID> --files <PATH_TO_FILE> # run one hook on a file
```

## Skip

强烈建议不要跳过运行任何预提交hook，因为它们的存在是有原因的。但是对于一些非常紧急的、拯救世界的提交，可以使用 no-verify 标志。

```
# Commit without hooks
git commit -m <MESSAGE> --no-verify
```

> 强烈建议**不**要这样做，因为无论您的更改有多“小”，都不应强制推动任何提交。如果您不小心这样做并想清除缓存，`pre-commit run --all-files`请再次运行并执行提交消息操作。

## 更新

在`.pre-commit-config.yaml`配置文件中，必须为每个存储库指定版本，以便可以使用它们最新的hook。预提交有一个自动更新 CLI 命令，它将在这些版本可用时更新它们。

```
# Autoupdate
pre-commit autoupdate
```

还可以将此命令添加到`Makefile`创建开发环境时执行的命令，以便一切都是最新的。

```
# Makefile
.ONESHELL:
venv:
    python3 -m venv venv
    source venv/bin/activate && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install -e ".[dev]" && \
    pre-commit install && \
    pre-commit autoupdate
```

___

更多干货，第一时间更新在以下微信公众号：

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-44-06-image.png)

您的一点点支持，是我后续更多的创造和贡献

![](https://raw.githubusercontent.com/franztao/blog_picture/main/marktext/2023-01-10-23-43-17-image.png)



转载到请包括本文地址
更详细的转载事宜请参考[文章如何转载/引用](https://franztao.github.io/2022/12/04/%E6%96%87%E7%AB%A0%E5%A6%82%E4%BD%95%E8%BD%AC%E8%BD%BD%E5%92%8C%E5%BC%95%E7%94%A8/)

本文主体源自以下链接：

```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
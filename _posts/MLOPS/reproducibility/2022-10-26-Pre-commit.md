---
layout:     post
title:      预提交
subtitle:   2022年10月
date:       2022-10-26
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Pre-commit

--- 

## 直觉

在对本地存储库执行提交之前，我们的心理待办事项列表上有很多项目，从样式、格式化、测试等。很容易忘记其中的一些步骤，尤其是当我们想要“推送到快速解决”。为了帮助我们管理所有这些重要步骤，我们可以使用预提交钩子，当我们尝试执行提交时，它会自动触发。

> 尽管我们可以直接在 CI/CD 管道中添加这些检查（例如通过 GitHub 操作），但在推送到远程主机之前验证我们的提交并等待查看需要修复的内容再提交另一个 PR 之前要快得多。

## 安装

我们将使用[Pre-commit](https://pre-commit.com/)框架来帮助我们在提交时通过钩子自动执行重要检查。

```
# Install pre-commit
pip install pre-commit==2.19.0
pre-commit install

```

我们将把它添加到我们的`setup.py`脚本而不是我们的`requirements.txt`文件中，因为它不是机器学习操作的核心。

<table><tbody><tr><td></td><td><div><pre id="__code_2"><span></span><code tabindex="0"><span># setup.py</span>
<span>setup</span><span>(</span>
    <span>...</span>
    <span>extras_require</span><span>=</span><span>{</span>
<span>        <span>"dev"</span><span>:</span> <span>docs_packages</span> <span>+</span> <span>style_packages</span> <span>+</span> <span>test_packages</span> <span>+</span> <span>[</span><span>"pre-commit==2.19.0"</span><span>],</span>
</span>        <span>"docs"</span><span>:</span> <span>docs_packages</span><span>,</span>
        <span>"test"</span><span>:</span> <span>test_packages</span><span>,</span>
    <span>},</span>
<span>)</span>
</code></pre></div></td></tr></tbody></table>

## 配置

`.pre-commit-config.yaml`我们通过配置文件定义我们的预提交钩子。我们可以从头开始创建 yaml 配置，也可以使用预提交 CLI 创建可以添加的示例配置。

```
# Simple config
pre-commit sample-config > .pre-commit-config.yaml
cat .pre-commit-config.yaml

```

<table><tbody><tr><td></td><td><div><pre id="__code_4"><span></span><code><span># See https://pre-commit.com for more information</span><span></span>
<span># See https://pre-commit.com/hooks.html for more hooks</span><span></span>
<span>repos</span><span>:</span><span></span>
<span>-</span><span>   </span><span>repo</span><span>:</span><span> </span><span>https://github.com/pre-commit/pre-commit-hooks</span><span></span>
<span>    </span><span>rev</span><span>:</span><span> </span><span>v3.2.0</span><span></span>
<span>    </span><span>hooks</span><span>:</span><span></span>
<span>    </span><span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>trailing-whitespace</span><span></span>
<span>    </span><span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>end-of-file-fixer</span><span></span>
<span>    </span><span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>check-yaml</span><span></span>
<span>    </span><span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>check-added-large-files</span><span></span>
</code></pre></div></td></tr></tbody></table>

## 挂钩

在创建和使用钩子时，我们有几个选项可供选择。

### 内置

在示例配置中，我们可以看到 pre-commit 从它的存储库中添加了一些默认挂钩。它指定存储库的位置、版本以及要使用的特定挂钩 ID。我们可以了解这些钩子的功能，并通过探索 pre-commit 的[内置](https://github.com/pre-commit/pre-commit-hooks)钩子来添加更多内容。其中许多还有其他参数，我们可以配置这些参数来自定义钩子。

<table><tbody><tr><td></td><td><div><pre id="__code_5"><span></span><code><span># Inside .pre-commit-config.yaml</span><span></span>
<span>...</span><span></span>
<span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>check-added-large-files</span><span></span>
<span>    </span><span>args</span><span>:</span><span> </span><span>[</span><span>'--maxkb=1000'</span><span>]</span><span></span>
<span>    </span><span>exclude</span><span>:</span><span> </span><span>"notebooks/tagifai.ipynb"</span><span></span>
<span>...</span><span></span>
</code></pre></div></td></tr></tbody></table>

> 一定要探索许多其他[内置的钩子](https://github.com/pre-commit/pre-commit-hooks)，因为我们在项目中使用了一些非常有用的钩子。例如，`check-merge-conflict`查看是否存在任何挥之不去的合并冲突字符串，或者`detect-aws-credentials`我们是否不小心将凭据暴露在文件中，等等。

_我们还可以通过使用可选的排除_键来排除某些文件被钩子处理。我们可以为每个钩子 ID 配置许多其他[可选键。](https://pre-commit.com/#pre-commit-configyaml---hooks)

<table><tbody><tr><td></td><td><div><pre id="__code_6"><span></span><code><span># Inside .pre-commit-config.yaml</span><span></span>
<span>...</span><span></span>
<span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>check-yaml</span><span></span>
<span>    </span><span>exclude</span><span>:</span><span> </span><span>"mkdocs.yml"</span><span></span>
<span>...</span><span></span>
</code></pre></div></td></tr></tbody></table>

### 风俗

除了 pre-commit 的内置钩子，还有许多自定义的、第 3 方[流行的钩子](https://pre-commit.com/hooks.html)可供我们选择。例如，如果我们想使用 Black 作为钩子应用格式检查，我们可以利用 Black 的 pre-commit 钩子。

<table><tbody><tr><td></td><td><div><pre id="__code_7"><span></span><code><span># Inside .pre-commit-config.yaml</span><span></span>
<span>...</span><span></span>
<span>-</span><span>   </span><span>repo</span><span>:</span><span> </span><span>https://github.com/psf/black</span><span></span>
<span>    </span><span>rev</span><span>:</span><span> </span><span>20.8b1</span><span></span>
<span>    </span><span>hooks</span><span>:</span><span></span>
<span>    </span><span>-</span><span>   </span><span>id</span><span>:</span><span> </span><span>black</span><span></span>
<span>        </span><span>args</span><span>:</span><span> </span><span>[]</span><span></span>
<span>        </span><span>files</span><span>:</span><span> </span><span>.</span><span></span>
<span>...</span><span></span>
</code></pre></div></td></tr></tbody></table>

这个特定的钩子在 Black 存储库中的[.pre-commit-hooks.yaml](https://github.com/psf/black/blob/master/.pre-commit-hooks.yaml)下定义，其他自定义钩子也在其各自的包存储库下。

### 当地的

我们也可以创建自己的本地钩子，而无需配置单独的 .pre-commit-hooks.yaml。这里我们定义了两个 pre-commit 钩子，`test-non-training`并且`clean`，来运行我们在 Makefile 中定义的一些命令。同样，我们可以运行任何带有参数的入口命令来非常快速地创建钩子。

<table><tbody><tr><td><div><pre><span></span><span><span><span>1 </span></span></span>
<span><span><span>2 </span></span></span>
<span><span><span>3 </span></span></span>
<span><span><span>4 </span></span></span>
<span><span><span>5 </span></span></span>
<span><span><span>6 </span></span></span>
<span><span><span>7 </span></span></span>
<span><span><span>8 </span></span></span>
<span><span><span>9 </span></span></span>
<span><span><span>10 </span></span></span>
<span><span><span>11 </span></span></span>
<span><span><span>12 </span></span></span>
<span><span><span>13 </span></span></span>
<span><span><span>14 </span></span></span>
<span><span><span>15 </span></span></span>
<span><span><span>16</span></span></span></pre></div></td><td><div><pre id="__code_8"><span></span><code><span># Inside .pre-commit-config.yaml</span><span></span>
<span>...</span><span></span>
<span>-</span><span> </span><span>repo</span><span>:</span><span> </span><span>local</span><span></span>
<span>  </span><span>hooks</span><span>:</span><span></span>
<span>    </span><span>-</span><span> </span><span>id</span><span>:</span><span> </span><span>test</span><span></span>
<span>      </span><span>name</span><span>:</span><span> </span><span>test</span><span></span>
<span>      </span><span>entry</span><span>:</span><span> </span><span>make</span><span></span>
<span>      </span><span>args</span><span>:</span><span> </span><span>[</span><span>"test"</span><span>]</span><span></span>
<span>      </span><span>language</span><span>:</span><span> </span><span>system</span><span></span>
<span>      </span><span>pass_filenames</span><span>:</span><span> </span><span>false</span><span></span>
<span>    </span><span>-</span><span> </span><span>id</span><span>:</span><span> </span><span>clean</span><span></span>
<span>      </span><span>name</span><span>:</span><span> </span><span>clean</span><span></span>
<span>      </span><span>entry</span><span>:</span><span> </span><span>make</span><span></span>
<span>      </span><span>args</span><span>:</span><span> </span><span>[</span><span>"clean"</span><span>]</span><span></span>
<span>      </span><span>language</span><span>:</span><span> </span><span>system</span><span></span>
<span>      </span><span>pass_filenames</span><span>:</span><span> </span><span>false</span><span></span>
</code></pre></div></td></tr></tbody></table>

查看我们的完整`.pre-commit-config.yaml`

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

## 犯罪

当我们尝试提交时，我们的预提交挂钩将自动执行。我们将能够查看每个钩子是否通过或失败并进行任何更改。如果任何挂钩失败，我们必须修复相应的文件，或者在许多情况下，会自动重新格式化。

```
...
检测私钥.....................................通过
黑色....... .............................失败
...

```

如果任何钩子失败，我们需要一次`add`又一次`commit`地确保所有钩子都通过。

```
git add .
git commit -m <MESSAGE>

```

![预提交](https://madewithml.com/static/images/mlops/pre_commit/commit.png)

## 跑

尽管预提交挂钩是在提交之前（预）运行，但我们可以手动触发所有或一组文件上的所有或单个挂钩。

```
# Run
pre-commit run --all-files  # run all hooks on all files
pre-commit run <HOOK_ID> --all-files # run one hook on all files
pre-commit run --files <PATH_TO_FILE>  # run all hooks on a file
pre-commit run <HOOK_ID> --files <PATH_TO_FILE> # run one hook on a file

```

## 跳过

强烈建议不要跳过运行任何预提交挂钩，因为它们的存在是有原因的。但是对于一些非常紧急的、拯救世界的提交，我们可以使用 no-verify 标志。

```
# Commit without hooks
git commit -m <MESSAGE> --no-verify

```

> 强烈建议**不**要这样做，因为无论您的更改有多“小”，都不应强制推动任何提交。如果您不小心这样做并想清除缓存，`pre-commit run --all-files`请再次运行并执行提交消息操作。

## 更新

在我们的`.pre-commit-config.yaml`配置文件中，我们必须为每个存储库指定版本，以便我们可以使用它们最新的挂钩。预提交有一个自动更新 CLI 命令，它将在这些版本可用时更新它们。

```
# Autoupdate
pre-commit autoupdate

```

我们还可以将此命令添加到`Makefile`创建开发环境时执行的命令，以便一切都是最新的。

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

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre id="__code_14"><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Pre-commit - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
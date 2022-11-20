---
layout:     post
title:      组织机器学习代码
subtitle:   2022年10月
date:       2022-10-10
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Organizing Machine Learning Code

---

## 组织机器学习代码

从笔记本转移到 Python 脚本时组织代码。

## 直觉

有组织的代码就是有可读的、可重现的、健壮的代码。您的团队、经理，最重要的是，您未来的自己，将感谢您为组织工作付出的最初努力。在本课中，将讨论如何将代码从[笔记本](https://github.com/GokuMohandas/mlops-course/blob/main/notebooks/tagifai.ipynb)迁移和组织到 Python 脚本。

## 编辑

在开始编码之前，需要一个空间来完成它。代码编辑器有多种选择，例如[VSCode](https://code.visualstudio.com/)、[Atom](https://atom.io/)、[Sublime](https://www.sublimetext.com/)、[PyCharm](https://www.jetbrains.com/pycharm/)、[Vim](https://www.vim.org/)等，它们都提供独特的功能，同时提供代码编辑和执行的基本操作。由于 VSCode 的简单性、多语言支持、附加组件和不断增长的行业采用，将使用 VSCode 来编辑和执行代码。

> 欢迎您使用任何编辑器，但将使用一些可能特定于 VSCode 的附加组件。

1.  从源代码为您的系统安装 VSCode：[https ://code.visualstudio.com/](https://code.visualstudio.com/)
2.  打开命令面板（在 mac`F1`上是Cmd++ Shift）`P`→ 输入“首选项：打开设置（UI）”→ 点击Enter
3.  调整您想要的任何相关设置（间距、字体大小等）
4.  安装[VSCode 扩展](https://marketplace.visualstudio.com/)（使用编辑器左侧面板上的乐高积木图标）

推荐的 VSCode 扩展

我建议安装这些扩展，你可以通过复制/粘贴这个命令：

```
code --install-extension 74th.monokai-charcoal-high-contrast
code --install-extension alefragnani.project-manager
code --install-extension bierner.markdown-preview-github-styles
code --install-extension bradgashler.htmltagwrap
code --install-extension christian-kohler.path-intellisense
code --install-extension euskadi31.json-pretty-printer
code --install-extension formulahendry.auto-close-tag
code --install-extension formulahendry.auto-rename-tag
code --install-extension kamikillerto.vscode-colorize
code --install-extension mechatroner.rainbow-csv
code --install-extension mikestead.dotenv
code --install-extension mohsen1.prettify-json
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-vscode.sublime-keybindings
code --install-extension njpwerner.autodocstring
code --install-extension PKief.material-icon-theme
code --install-extension redhat.vscode-yaml
code --install-extension ritwickdey.live-sass
code --install-extension ritwickdey.LiveServer
code --install-extension shardulm94.trailing-spaces
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension zhuangtongfa.material-theme

```

如果您添加自己的扩展并希望与他人共享，只需运行此命令即可生成命令列表：

```
code --list-extensions | xargs -L 1 echo code --install-extension

```

一旦都设置好 VSCode，可以从创建项目目录开始，将使用它来组织所有的脚本。有很多方法可以启动一个项目，但这里是推荐的路径：

1.  使用终端创建目录 ( `mkdir <PROJECT_NAME>`)。
2.  Change into the project directory you just made (`cd <PROJECT_NAME>`).
3.  Start VSCode from this directory by typing `code .`
    
    > To open VSCode directly from the terminal with a `code $PATH` command, open the Command Palette (`F1` or Cmd + Shift + `P` on mac) → type "Shell Command: Install 'code' command in PATH" → hit Enter → restart the terminal.
    
4.  Open a terminal within VSCode (`View` > `Terminal`) to continue creating scripts (`touch <FILE_NAME>`) or additional subdirectories (`mkdir <SUBDIR>`) as needed.

![代码](https://madewithml.com/static/images/mlops/organization/vscode.png)

## Setup

### README

We'll start our organization with a `README.md` file, which will provide information on the files in our directory, instructions to execute operations, etc. We'll constantly keep this file updated so that we can catalogue information for the future.

Let's start by adding the instructions we used for creating a [virtual environment](https://madewithml.com/courses/mlops/packaging/#virtual-environment):

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Inside README.md</span><span></span>
python3 -m venv venv<span></span>
<span>source</span> venv/bin/activate<span></span>
python3 -m pip install pip setuptools wheel<span></span>
python3 -m pip install -e .<span></span>
</code></pre></div></td></tr></tbody></table>

If you press the Preview button located on the top right of the editor (button enclosed in red circle in the image below), you can see what the `README.md` will look like when we push to remote host for [git](https://madewithml.com/courses/mlops/git/).

![自述文件](https://madewithml.com/static/images/mlops/organization/readme.png)

### Configurations

Next we'll create a configuration directory called `config` where we can store components that will be required for our application. Inside this directory, we'll create a `config.py` and a `args.json`.

```
mkdir config
touch config/main.py config/args.json

```

```
config/
├── args.json       - arguments
└── config.py       - configuration setup

```

Inside `config.py`, we'll add the code to define key directory locations (we'll add more configurations in later lessons as they're needed):

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># config.py</span>
<span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span><span></span>
<span></span>
<span># Directories</span>
<span>BASE_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>__file__</span><span>)</span><span>.</span><span>parent</span><span>.</span><span>parent</span><span>.</span><span>absolute</span><span>()</span>
<span>CONFIG_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"config"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

and inside `args.json`, we'll add the parameters that are relevant to data processing and model training.

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span></pre></div></td><td><div><pre><span></span><code><span>{</span><span></span>
<span>    </span><span>"shuffle"</span><span>:</span><span> </span><span>true</span><span>,</span><span></span>
<span>    </span><span>"subset"</span><span>:</span><span> </span><span>null</span><span>,</span><span></span>
<span>    </span><span>"min_freq"</span><span>:</span><span> </span><span>75</span><span>,</span><span></span>
<span>    </span><span>"lower"</span><span>:</span><span> </span><span>true</span><span>,</span><span></span>
<span>    </span><span>"stem"</span><span>:</span><span> </span><span>false</span><span>,</span><span></span>
<span>    </span><span>"analyzer"</span><span>:</span><span> </span><span>"char"</span><span>,</span><span></span>
<span>    </span><span>"ngram_max_range"</span><span>:</span><span> </span><span>7</span><span>,</span><span></span>
<span>    </span><span>"alpha"</span><span>:</span><span> </span><span>1e-4</span><span>,</span><span></span>
<span>    </span><span>"learning_rate"</span><span>:</span><span> </span><span>1e-1</span><span>,</span><span></span>
<span>    </span><span>"power_t"</span><span>:</span><span> </span><span>0.1</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>

### Operations

We'll start by creating our package directory (`tagifai`) inside our project directory (`mlops`). Inside this package directory, we will create a `main.py` file that will define the core operations we want to be able to execute.

```
mkdir tagifai
touch tagifai/main.py

```

```
tagifai/
└── main.py       - training/optimization pipelines

```

We'll define these core operations inside `main.py` as we move code from notebooks to the appropriate scripts [below](https://madewithml.com/courses/mlops/organization/#project):

-   `elt_data`: extract, load and transform data.
-   `optimize`: tune hyperparameters to optimize for objective.
-   `train_model`: train a model using best parameters from optimization study.
-   `load_artifacts`: load trained artifacts from a given run.
-   `predict_tag`: predict a tag for a given input.

### Utilities

Before we start moving code from our notebook, we should be intentional about _how_ we move functionality over to scripts. It's common to have ad-hoc processes inside notebooks because it maintains state as long as the notebook is running. For example, we may set seeds in our notebooks like so:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Set seeds</span>
<span>np</span><span>.</span><span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
<span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

But in our scripts, we should wrap this functionality as a clean, reuseable function with the appropriate parameters:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>def</span> <span>set_seeds</span><span>(</span><span>seed</span><span>=</span><span>42</span><span>):</span>
    <span>"""Set seeds for reproducibility."""</span>
    <span>np</span><span>.</span><span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
    <span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

We can store all of these inside a `utils.py` file inside our `tagifai` package directory.

```
tagifai/
├── main.py       - training/optimization pipelines
└── utils.py      - supplementary utilities

```

View utils.py

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span></pre></div></td><td><div><pre><span></span><code><span>import</span> <span>json</span>
<span>import</span> <span>numpy</span> <span>as</span> <span>np</span>
<span>import</span> <span>random</span><span></span>
<span></span>
<span>def</span> <span>load_dict</span><span>(</span><span>filepath</span><span>):</span>
    <span>"""Load a dictionary from a JSON's filepath."""</span>
    <span>with</span> <span>open</span><span>(</span><span>filepath</span><span>,</span> <span>"r"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
        <span>d</span> <span>=</span> <span>json</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>)</span>
    <span>return</span> <span>d</span><span></span>
<span></span>
<span>def</span> <span>save_dict</span><span>(</span><span>d</span><span>,</span> <span>filepath</span><span>,</span> <span>cls</span><span>=</span><span>None</span><span>,</span> <span>sortkeys</span><span>=</span><span>False</span><span>):</span>
    <span>"""Save a dictionary to a specific location."""</span>
    <span>with</span> <span>open</span><span>(</span><span>filepath</span><span>,</span> <span>"w"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
        <span>json</span><span>.</span><span>dump</span><span>(</span><span>d</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>,</span> <span>fp</span><span>=</span><span>fp</span><span>,</span> <span>cls</span><span>=</span><span>cls</span><span>,</span> <span>sort_keys</span><span>=</span><span>sortkeys</span><span>)</span><span></span>
<span></span>
<span>def</span> <span>set_seeds</span><span>(</span><span>seed</span><span>=</span><span>42</span><span>):</span>
    <span>"""Set seed for reproducibility."""</span>
    <span># Set seeds</span>
    <span>np</span><span>.</span><span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
    <span>random</span><span>.</span><span>seed</span><span>(</span><span>seed</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

> Don't worry about formatting our scripts just yet. We'll be automating all of it in our [styling](https://madewithml.com/courses/mlops/styling/) lesson.

## Project

When it comes to migrating our code from notebooks to scripts, it's best to organize based on utility. For example, we can create scripts for the various stages of ML development such as data processing, training, evaluation, prediction, etc.:

We'll create the different python files to wrap our data and ML functionality:

```
cd tagifai
touch data.py train.py evaluate.py predict.py

```

```
tagifai/
├── data.py       - data processing utilities
├── evaluate.py   - evaluation components
├── main.py       - training/optimization pipelines
├── predict.py    - inference utilities
├── train.py      - training utilities
└── utils.py      - supplementary utilities

```

> We may have additional scripts in other projects, as they are necessary. For example, we'd typically have a `models.py` script we define explicit model architectures in Pytorch, Tensorflow, etc.

Organizing our code base this way also makes it easier for us to understand (or modify) the code base. We could've placed all the code into one `main.py` script but as our project grows, it will be hard to navigate one monolithic file. On the other hand, we could've assumed a more granular stance by breaking down `data.py` into `split.py`, `preprocess.py`, etc. This might make more sense if we have multiple ways of splitting, preprocessing, etc. (ex. a library for ML operations) but for our task, it's sufficient to be at this higher level of organization.

## Principles

Through the migration process below, we'll be using several core software engineering principles repeatedly.

#### Wrapping functionality into functions

How do we decide when specific lines of code should be wrapped as a separate function? Functions should be atomic in that they each have a [single responsibility](https://en.wikipedia.org/wiki/Single-responsibility_principle) so that we can easily [test](https://madewithml.com/courses/mlops/testing/) them. If not, we'll need to split them into more granular units. For example, we could replace tags in our projects with these lines:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>oos_tags</span> <span>=</span> <span>[</span><span>item</span> <span>for</span> <span>item</span> <span>in</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>unique</span><span>()</span> <span>if</span> <span>item</span> <span>not</span> <span>in</span> <span>tags_dict</span><span>.</span><span>keys</span><span>()]</span>
<span>df</span><span>.</span><span>tag</span> <span>=</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>x</span><span>:</span> <span>"other"</span> <span>if</span> <span>x</span> <span>in</span> <span>oos_tags</span> <span>else</span> <span>x</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

────   compared to   ────

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>def</span> <span>replace_oos_tags</span><span>(</span><span>df</span><span>,</span> <span>tags_dict</span><span>):</span>
    <span>"""Replace out of scope (oos) tags."""</span>
    <span>oos_tags</span> <span>=</span> <span>[</span><span>item</span> <span>for</span> <span>item</span> <span>in</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>unique</span><span>()</span> <span>if</span> <span>item</span> <span>not</span> <span>in</span> <span>tags_dict</span><span>.</span><span>keys</span><span>()]</span>
    <span>df</span><span>.</span><span>tag</span> <span>=</span> <span>df</span><span>.</span><span>tag</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>x</span><span>:</span> <span>"other"</span> <span>if</span> <span>x</span> <span>in</span> <span>oos_tags</span> <span>else</span> <span>x</span><span>)</span>
    <span>return</span> <span>df</span>
</code></pre></div></td></tr></tbody></table>

It's better to wrap them as a separate function because we may want to:

-   repeat this functionality in other parts of the project or in other projects.
-   test that these tags are actually being replaced properly.

#### Composing generalized functions

| 
Specific

 |
| --- |
| 

```
1
2
3
4
5
```



 | 

```
def replace_oos_tags(df, tags_dict):
    """Replace out of scope (oos) tags."""
    oos_tags = [item for item in df.tag.unique() if item not in tags_dict.keys()]
    df.tag = df.tag.apply(lambda x: "other" if x in oos_tags else x)
    return df

```



 |

────   compared to   ────

| 
Generalized

 |
| --- |
| 

```
1
2
3
4
5
```



 | 

```
def replace_oos_labels(df, labels, label_col, oos_label="other"):
    """Replace out of scope (oos) labels."""
    oos_tags = [item for item in df[label_col].unique() if item not in labels]
    df[label_col] = df[label_col].apply(lambda x: oos_label if x in oos_tags else x)
    return df

```



 |

This way when the names of columns change or we want to replace with different labels, it's very easy to adjust our code. This also includes using generalized names in the functions such as `label` instead of the name of the specific label column (ex. `tag`). It also allows others to reuse this functionality for their use cases.

> However, it's important not to force generalization if it involves a lot of effort. We can spend time later if we see the similar functionality reoccurring.

## 🔢  Data

### Load

Load and save data

First, we'll name and create the directory to save our data assets to (raw data, labeled data, etc.):

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># config/config.py</span>
<span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
<span>import</span> <span>pretty_errors</span><span></span>
<span></span>
<span># Directories</span>
<span>BASE_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>__file__</span><span>)</span><span>.</span><span>parent</span><span>.</span><span>parent</span><span>.</span><span>absolute</span><span>()</span>
<span><span>CONFIG_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"config"</span><span>)</span>
</span><span>DATA_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"data"</span><span>)</span><span></span>
<span></span>
<span><span># Create dirs</span>
</span><span>DATA_DIR</span><span>.</span><span>mkdir</span><span>(</span><span>parents</span><span>=</span><span>True</span><span>,</span> <span>exist_ok</span><span>=</span><span>True</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

Next, we'll add the location of our raw data assets to our `config.py`. It's important that we store this information in our central configuration file so we can easily discover and update it if needed, as opposed to being deeply buried inside the code somewhere.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># config/config.py</span>
<span>...</span>
<span># Assets</span>
<span>PROJECTS_URL</span> <span>=</span> <span>"https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/projects.csv"</span>
<span>TAGS_URL</span> <span>=</span> <span>"https://raw.githubusercontent.com/GokuMohandas/Made-With-ML/main/datasets/tags.csv"</span>
</code></pre></div></td></tr></tbody></table>

Since this is a main operation, we'll define it in `main.py`:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>import</span> <span>pandas</span> <span>as</span> <span>pd</span>
<span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
<span>import</span> <span>warnings</span><span></span>
<span></span>
<span>from</span> <span>config</span> <span>import</span> <span>config</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>utils</span><span></span>
<span></span>
<span>warnings</span><span>.</span><span>filterwarnings</span><span>(</span><span>"ignore"</span><span>)</span><span></span>
<span></span>
<span>def</span> <span>elt_data</span><span>():</span>
    <span>"""Extract, load and transform our data assets."""</span>
    <span># Extract + Load</span>
    <span>projects</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>config</span><span>.</span><span>PROJECTS_URL</span><span>)</span>
    <span>tags</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>config</span><span>.</span><span>TAGS_URL</span><span>)</span>
    <span>projects</span><span>.</span><span>to_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"projects.csv"</span><span>),</span> <span>index</span><span>=</span><span>False</span><span>)</span>
    <span>tags</span><span>.</span><span>to_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"tags.csv"</span><span>),</span> <span>index</span><span>=</span><span>False</span><span>)</span><span></span>
<span></span>
    <span># Transform</span>
    <span>df</span> <span>=</span> <span>pd</span><span>.</span><span>merge</span><span>(</span><span>projects</span><span>,</span> <span>tags</span><span>,</span> <span>on</span><span>=</span><span>"id"</span><span>)</span>
    <span>df</span> <span>=</span> <span>df</span><span>[</span><span>df</span><span>.</span><span>tag</span><span>.</span><span>notnull</span><span>()]</span>  <span># drop rows w/ no tag</span>
    <span>df</span><span>.</span><span>to_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"labeled_projects.csv"</span><span>),</span> <span>index</span><span>=</span><span>False</span><span>)</span><span></span>
<span></span>
    <span>logger</span><span>.</span><span>info</span><span>(</span><span>"✅ Saved data!"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

Before we can use this operation, we need to make sure we have the necessary packages loaded into our environment. Libraries such as `pathlib`, `json`, etc. are preloaded with native Python, but packages like `NumPy` are not. Let's load the required packages and add them to our `requirements.txt` file.

```
pip install numpy==1.19.5 pandas==1.3.5 pretty-errors==1.2.19

```

```
# Add to requirements.txt
numpy==1.19.5
pandas==1.3.5
pretty-errors==1.2.19

```

> We can fetch the exact version of the packages we used in our notebook by running `pip freeze` in a code cell.

Though we're not using the NumPy package for this `elt_data()` operation, our Python interpreter will still require it because we invoke the `utils.py` script with the line `from tagifai import utils`, which does use NumPy in its header. So if we don't install the package in our virtual environment, we'll receive an error.

We'll run the operation using the Python interpreter via the terminal (type `python` in the terminal and types the commands below).

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>tagifai</span> <span>import</span> <span>main</span>
<span>main</span><span>.</span><span>elt_data</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

We could also call this operation directly through the `main.py` script but we'll have to change it every time we want to run a new operation.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>elt_data</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

We'll learn about a much easier way to execute these operations in our [CLI lesson](https://madewithml.com/courses/mlops/cli/). But for now, either of the methods above will produce the same result.

```
✅ Saved data!

```

We should also see the data assets saved to our `data` directory:

```
data/
├── projects.csv
└── tags.csv

```

Why save the raw data?

Why do we need to save our raw data? Why not just load it from the URL and save the downstream assets (labels, features, etc.)?

Show answer

We'll be using the raw data to generate labeled data and other downstream assets (ex. features). If the source of our raw data changes, then we'll no longer be able to produce our downstream assets. By saving it locally, we can always reproduce our results without any external dependencies. We'll also be executing [data validation](https://madewithml.com/courses/mlops/testing/#data) checks on the raw data before applying transformations on it.

However, as our dataset grows, it may not scale to save the raw data or even labels or features. We'll talk about more scalable alternatives in our [versioning](https://madewithml.com/courses/mlops/versioning/#operations) lesson where we aren't saving the physical data but the instructions to retrieve them from a specific point in time.

### Preprocess

Preprocess features

Next, we're going to define the functions for preprocessing our input features. We'll be using these functions when we are preparing the data prior to training our model. We won't be saving the preprocessed data to a file because different experiment may preprocess them differently.

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/data.py</span>
<span>def</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>,</span> <span>stem</span><span>,</span> <span>min_freq</span><span>):</span>
    <span>"""Preprocess the data."""</span>
    <span>df</span><span>[</span><span>"text"</span><span>]</span> <span>=</span> <span>df</span><span>.</span><span>title</span> <span>+</span> <span>" "</span> <span>+</span> <span>df</span><span>.</span><span>description</span>  <span># feature engineering</span>
    <span>df</span><span>.</span><span>text</span> <span>=</span> <span>df</span><span>.</span><span>text</span><span>.</span><span>apply</span><span>(</span><span>clean_text</span><span>,</span> <span>lower</span><span>=</span><span>lower</span><span>,</span> <span>stem</span><span>=</span><span>stem</span><span>)</span>  <span># clean text</span>
    <span>df</span> <span>=</span> <span>replace_oos_labels</span><span>(</span>
        <span>df</span><span>=</span><span>df</span><span>,</span> <span>labels</span><span>=</span><span>config</span><span>.</span><span>ACCEPTED_TAGS</span><span>,</span> <span>label_col</span><span>=</span><span>"tag"</span><span>,</span> <span>oos_label</span><span>=</span><span>"other"</span>
    <span>)</span>  <span># replace OOS labels</span>
    <span>df</span> <span>=</span> <span>replace_minority_labels</span><span>(</span>
        <span>df</span><span>=</span><span>df</span><span>,</span> <span>label_col</span><span>=</span><span>"tag"</span><span>,</span> <span>min_freq</span><span>=</span><span>min_freq</span><span>,</span> <span>new_label</span><span>=</span><span>"other"</span>
    <span>)</span>  <span># replace labels below min freq</span><span></span>
<span></span>
    <span>return</span> <span>df</span>
</code></pre></div></td></tr></tbody></table>

This function uses the `clean_text()` function which we can define right above it:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span>
<span>28</span>
<span>29</span>
<span>30</span>
<span>31</span>
<span>32</span>
<span>33</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/data.py</span>
<span>from</span> <span>nltk.stem</span> <span>import</span> <span>PorterStemmer</span>
<span>import</span> <span>re</span><span></span>
<span></span>
<span>from</span> <span>config</span> <span>import</span> <span>config</span><span></span>
<span></span>
<span>def</span> <span>clean_text</span><span>(</span><span>text</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>,</span> <span>stopwords</span><span>=</span><span>config</span><span>.</span><span>STOPWORDS</span><span>):</span>
    <span>"""Clean raw text."""</span>
    <span># Lower</span>
    <span>if</span> <span>lower</span><span>:</span>
        <span>text</span> <span>=</span> <span>text</span><span>.</span><span>lower</span><span>()</span><span></span>
<span></span>
    <span># Remove stopwords</span>
    <span>if</span> <span>len</span><span>(</span><span>stopwords</span><span>):</span>
        <span>pattern</span> <span>=</span> <span>re</span><span>.</span><span>compile</span><span>(</span><span>r</span><span>'\b('</span> <span>+</span> <span>r</span><span>"|"</span><span>.</span><span>join</span><span>(</span><span>stopwords</span><span>)</span> <span>+</span> <span>r</span><span>")\b\s*"</span><span>)</span>
        <span>text</span> <span>=</span> <span>pattern</span><span>.</span><span>sub</span><span>(</span><span>''</span><span>,</span> <span>text</span><span>)</span><span></span>
<span></span>
    <span># Spacing and filters</span>
    <span>text</span> <span>=</span> <span>re</span><span>.</span><span>sub</span><span>(</span>
        <span>r</span><span>"([!</span><span>\"</span><span>'#$%&amp;()*\+,-./:;&lt;=&gt;?@</span><span>\\</span><span>\[\]^_`{|}~])"</span><span>,</span> <span>r</span><span>" \1 "</span><span>,</span> <span>text</span>
    <span>)</span>  <span># add spacing between objects to be filtered</span>
    <span>text</span> <span>=</span> <span>re</span><span>.</span><span>sub</span><span>(</span><span>"[^A-Za-z0-9]+"</span><span>,</span> <span>" "</span><span>,</span> <span>text</span><span>)</span>  <span># remove non alphanumeric chars</span>
    <span>text</span> <span>=</span> <span>re</span><span>.</span><span>sub</span><span>(</span><span>" +"</span><span>,</span> <span>" "</span><span>,</span> <span>text</span><span>)</span>  <span># remove multiple spaces</span>
    <span>text</span> <span>=</span> <span>text</span><span>.</span><span>strip</span><span>()</span>  <span># strip white space at the ends</span><span></span>
<span></span>
    <span># Remove links</span>
    <span>text</span> <span>=</span> <span>re</span><span>.</span><span>sub</span><span>(</span><span>r</span><span>"http\S+"</span><span>,</span> <span>""</span><span>,</span> <span>text</span><span>)</span><span></span>
<span></span>
    <span># Stemming</span>
    <span>if</span> <span>stem</span><span>:</span>
        <span>text</span> <span>=</span> <span>" "</span><span>.</span><span>join</span><span>([</span><span>stemmer</span><span>.</span><span>stem</span><span>(</span><span>word</span><span>,</span> <span>to_lowercase</span><span>=</span><span>lower</span><span>)</span> <span>for</span> <span>word</span> <span>in</span> <span>text</span><span>.</span><span>split</span><span>(</span><span>" "</span><span>)])</span><span></span>
<span></span>
    <span>return</span> <span>text</span>
</code></pre></div></td></tr></tbody></table>

Install required packages and add to `requirements.txt`:

```
# Add to requirements.txt
nltk==3.7

```

Notice that we're using an explicit set of stopwords instead of NLTK's default list:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># NLTK's default stopwords</span>
<span>nltk</span><span>.</span><span>download</span><span>(</span><span>"stopwords"</span><span>)</span>
<span>STOPWORDS</span> <span>=</span> <span>stopwords</span><span>.</span><span>words</span><span>(</span><span>"english"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

This is because we want to have full visibility into exactly what words we're filtering. The general list may have some valuable terms we may wish to keep and vice versa.

```
# config/config.py
STOPWORDS = [
    "i",
    "me",
    "my",
    ...
    "won't",
    "wouldn",
    "wouldn't",
]

```

Next, we need to define the two functions we're calling from `data.py`:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/data.py</span>
<span>from</span> <span>collections</span> <span>import</span> <span>Counter</span><span></span>
<span></span>
<span>def</span> <span>replace_oos_labels</span><span>(</span><span>df</span><span>,</span> <span>labels</span><span>,</span> <span>label_col</span><span>,</span> <span>oos_label</span><span>=</span><span>"other"</span><span>):</span>
    <span>"""Replace out of scope (oos) labels."""</span>
    <span>oos_tags</span> <span>=</span> <span>[</span><span>item</span> <span>for</span> <span>item</span> <span>in</span> <span>df</span><span>[</span><span>label_col</span><span>]</span><span>.</span><span>unique</span><span>()</span> <span>if</span> <span>item</span> <span>not</span> <span>in</span> <span>labels</span><span>]</span>
    <span>df</span><span>[</span><span>label_col</span><span>]</span> <span>=</span> <span>df</span><span>[</span><span>label_col</span><span>]</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>x</span><span>:</span> <span>oos_label</span> <span>if</span> <span>x</span> <span>in</span> <span>oos_tags</span> <span>else</span> <span>x</span><span>)</span>
    <span>return</span> <span>df</span><span></span>
<span></span>
<span>def</span> <span>replace_minority_labels</span><span>(</span><span>df</span><span>,</span> <span>label_col</span><span>,</span> <span>min_freq</span><span>,</span> <span>new_label</span><span>=</span><span>"other"</span><span>):</span>
    <span>"""Replace minority labels with another label."""</span>
    <span>labels</span> <span>=</span> <span>Counter</span><span>(</span><span>df</span><span>[</span><span>label_col</span><span>]</span><span>.</span><span>values</span><span>)</span>
    <span>labels_above_freq</span> <span>=</span> <span>Counter</span><span>(</span><span>label</span> <span>for</span> <span>label</span> <span>in</span> <span>labels</span><span>.</span><span>elements</span><span>()</span> <span>if</span> <span>(</span><span>labels</span><span>[</span><span>label</span><span>]</span> <span>&gt;=</span> <span>min_freq</span><span>))</span>
    <span>df</span><span>[</span><span>label_col</span><span>]</span> <span>=</span> <span>df</span><span>[</span><span>label_col</span><span>]</span><span>.</span><span>apply</span><span>(</span><span>lambda</span> <span>label</span><span>:</span> <span>label</span> <span>if</span> <span>label</span> <span>in</span> <span>labels_above_freq</span> <span>else</span> <span>None</span><span>)</span>
    <span>df</span><span>[</span><span>label_col</span><span>]</span> <span>=</span> <span>df</span><span>[</span><span>label_col</span><span>]</span><span>.</span><span>fillna</span><span>(</span><span>new_label</span><span>)</span>
    <span>return</span> <span>df</span>
</code></pre></div></td></tr></tbody></table>

### Encode

Encode labels

Now let's define the encoder for our labels, which we'll use prior to splitting our dataset:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span>
<span>28</span>
<span>29</span>
<span>30</span>
<span>31</span>
<span>32</span>
<span>33</span>
<span>34</span>
<span>35</span>
<span>36</span>
<span>37</span>
<span>38</span>
<span>39</span>
<span>40</span>
<span>41</span>
<span>42</span>
<span>43</span>
<span>44</span>
<span>45</span>
<span>46</span>
<span>47</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/data.py</span>
<span>import</span> <span>json</span>
<span>import</span> <span>numpy</span> <span>as</span> <span>np</span><span></span>
<span></span>
<span>class</span> <span>LabelEncoder</span><span>(</span><span>object</span><span>):</span>
    <span>"""Encode labels into unique indices."""</span>
    <span>def</span> <span>__init__</span><span>(</span><span>self</span><span>,</span> <span>class_to_index</span><span>=</span><span>{}):</span>
        <span>self</span><span>.</span><span>class_to_index</span> <span>=</span> <span>class_to_index</span> <span>or</span> <span>{}</span>  <span># mutable defaults ;)</span>
        <span>self</span><span>.</span><span>index_to_class</span> <span>=</span> <span>{</span><span>v</span><span>:</span> <span>k</span> <span>for</span> <span>k</span><span>,</span> <span>v</span> <span>in</span> <span>self</span><span>.</span><span>class_to_index</span><span>.</span><span>items</span><span>()}</span>
        <span>self</span><span>.</span><span>classes</span> <span>=</span> <span>list</span><span>(</span><span>self</span><span>.</span><span>class_to_index</span><span>.</span><span>keys</span><span>())</span><span></span>
<span></span>
    <span>def</span> <span>__len__</span><span>(</span><span>self</span><span>):</span>
        <span>return</span> <span>len</span><span>(</span><span>self</span><span>.</span><span>class_to_index</span><span>)</span><span></span>
<span></span>
    <span>def</span> <span>__str__</span><span>(</span><span>self</span><span>):</span>
        <span>return</span> <span>f</span><span>"&lt;LabelEncoder(num_classes=</span><span>{</span><span>len</span><span>(</span><span>self</span><span>)</span><span>}</span><span>)&gt;"</span><span></span>
<span></span>
    <span>def</span> <span>fit</span><span>(</span><span>self</span><span>,</span> <span>y</span><span>):</span>
        <span>classes</span> <span>=</span> <span>np</span><span>.</span><span>unique</span><span>(</span><span>y</span><span>)</span>
        <span>for</span> <span>i</span><span>,</span> <span>class_</span> <span>in</span> <span>enumerate</span><span>(</span><span>classes</span><span>):</span>
            <span>self</span><span>.</span><span>class_to_index</span><span>[</span><span>class_</span><span>]</span> <span>=</span> <span>i</span>
        <span>self</span><span>.</span><span>index_to_class</span> <span>=</span> <span>{</span><span>v</span><span>:</span> <span>k</span> <span>for</span> <span>k</span><span>,</span> <span>v</span> <span>in</span> <span>self</span><span>.</span><span>class_to_index</span><span>.</span><span>items</span><span>()}</span>
        <span>self</span><span>.</span><span>classes</span> <span>=</span> <span>list</span><span>(</span><span>self</span><span>.</span><span>class_to_index</span><span>.</span><span>keys</span><span>())</span>
        <span>return</span> <span>self</span><span></span>
<span></span>
    <span>def</span> <span>encode</span><span>(</span><span>self</span><span>,</span> <span>y</span><span>):</span>
        <span>encoded</span> <span>=</span> <span>np</span><span>.</span><span>zeros</span><span>((</span><span>len</span><span>(</span><span>y</span><span>)),</span> <span>dtype</span><span>=</span><span>int</span><span>)</span>
        <span>for</span> <span>i</span><span>,</span> <span>item</span> <span>in</span> <span>enumerate</span><span>(</span><span>y</span><span>):</span>
            <span>encoded</span><span>[</span><span>i</span><span>]</span> <span>=</span> <span>self</span><span>.</span><span>class_to_index</span><span>[</span><span>item</span><span>]</span>
        <span>return</span> <span>encoded</span><span></span>
<span></span>
    <span>def</span> <span>decode</span><span>(</span><span>self</span><span>,</span> <span>y</span><span>):</span>
        <span>classes</span> <span>=</span> <span>[]</span>
        <span>for</span> <span>i</span><span>,</span> <span>item</span> <span>in</span> <span>enumerate</span><span>(</span><span>y</span><span>):</span>
            <span>classes</span><span>.</span><span>append</span><span>(</span><span>self</span><span>.</span><span>index_to_class</span><span>[</span><span>item</span><span>])</span>
        <span>return</span> <span>classes</span><span></span>
<span></span>
    <span>def</span> <span>save</span><span>(</span><span>self</span><span>,</span> <span>fp</span><span>):</span>
        <span>with</span> <span>open</span><span>(</span><span>fp</span><span>,</span> <span>"w"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
            <span>contents</span> <span>=</span> <span>{</span><span>"class_to_index"</span><span>:</span> <span>self</span><span>.</span><span>class_to_index</span><span>}</span>
            <span>json</span><span>.</span><span>dump</span><span>(</span><span>contents</span><span>,</span> <span>fp</span><span>,</span> <span>indent</span><span>=</span><span>4</span><span>,</span> <span>sort_keys</span><span>=</span><span>False</span><span>)</span><span></span>
<span></span>
    <span>@classmethod</span>
    <span>def</span> <span>load</span><span>(</span><span>cls</span><span>,</span> <span>fp</span><span>):</span>
        <span>with</span> <span>open</span><span>(</span><span>fp</span><span>,</span> <span>"r"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
            <span>kwargs</span> <span>=</span> <span>json</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>=</span><span>fp</span><span>)</span>
        <span>return</span> <span>cls</span><span>(</span><span>**</span><span>kwargs</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

### Split

Split dataset

And finally, we'll conclude our data operations with our split function:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>sklearn.model_selection</span> <span>import</span> <span>train_test_split</span><span></span>
<span></span>
<span>def</span> <span>get_data_splits</span><span>(</span><span>X</span><span>,</span> <span>y</span><span>,</span> <span>train_size</span><span>=</span><span>0.7</span><span>):</span>
    <span>"""Generate balanced data splits."""</span>
    <span>X_train</span><span>,</span> <span>X_</span><span>,</span> <span>y_train</span><span>,</span> <span>y_</span> <span>=</span> <span>train_test_split</span><span>(</span>
        <span>X</span><span>,</span> <span>y</span><span>,</span> <span>train_size</span><span>=</span><span>train_size</span><span>,</span> <span>stratify</span><span>=</span><span>y</span><span>)</span>
    <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> <span>train_test_split</span><span>(</span>
        <span>X_</span><span>,</span> <span>y_</span><span>,</span> <span>train_size</span><span>=</span><span>0.5</span><span>,</span> <span>stratify</span><span>=</span><span>y_</span><span>)</span>
    <span>return</span> <span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span>
</code></pre></div></td></tr></tbody></table>

Install required packages and add to `requirements.txt`:

```
pip install scikit-learn==0.24.2

```

```
# Add to requirements.txt
scikit-learn==0.24.2

```

## 📈  Modeling

### Train

Train w/ default args

Now we're ready to kick off the training process. We'll start by defining the operation in our `main.py`:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>import</span> <span>json</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>data</span><span>,</span> <span>train</span><span>,</span> <span>utils</span><span></span>
<span></span>
<span>def</span> <span>train_model</span><span>(</span><span>args_fp</span><span>):</span>
    <span>"""Train a model given arguments."""</span>
    <span># Load labeled data</span>
    <span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"labeled_projects.csv"</span><span>))</span><span></span>
<span></span>
    <span># Train</span>
    <span>args</span> <span>=</span> <span>Namespace</span><span>(</span><span>**</span><span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>args_fp</span><span>))</span>
    <span>artifacts</span> <span>=</span> <span>train</span><span>.</span><span>train</span><span>(</span><span>df</span><span>=</span><span>df</span><span>,</span> <span>args</span><span>=</span><span>args</span><span>)</span>
    <span>performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>]</span>
    <span>print</span><span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

We'll be adding more to our `train_model()` operation when we factor in experiment tracking but, for now, it's quite simple. This function calls for a `train()` function inside our `train.py` script:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span>
<span>28</span>
<span>29</span>
<span>30</span>
<span>31</span>
<span>32</span>
<span>33</span>
<span>34</span>
<span>35</span>
<span>36</span>
<span>37</span>
<span>38</span>
<span>39</span>
<span>40</span>
<span>41</span>
<span>42</span>
<span>43</span>
<span>44</span>
<span>45</span>
<span>46</span>
<span>47</span>
<span>48</span>
<span>49</span>
<span>50</span>
<span>51</span>
<span>52</span>
<span>53</span>
<span>54</span>
<span>55</span>
<span>56</span>
<span>57</span>
<span>58</span>
<span>59</span>
<span>60</span>
<span>61</span>
<span>62</span>
<span>63</span>
<span>64</span>
<span>65</span>
<span>66</span>
<span>67</span>
<span>68</span>
<span>69</span>
<span>70</span>
<span>71</span>
<span>72</span>
<span>73</span>
<span>74</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/train.py</span>
<span>from</span> <span>imblearn.over_sampling</span> <span>import</span> <span>RandomOverSampler</span>
<span>import</span> <span>json</span>
<span>import</span> <span>numpy</span> <span>as</span> <span>np</span>
<span>import</span> <span>pandas</span> <span>as</span> <span>pd</span>
<span>from</span> <span>sklearn.feature_extraction.text</span> <span>import</span> <span>TfidfVectorizer</span>
<span>from</span> <span>sklearn.linear_model</span> <span>import</span> <span>SGDClassifier</span>
<span>from</span> <span>sklearn.metrics</span> <span>import</span> <span>log_loss</span><span></span>
<span></span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>data</span><span>,</span> <span>predict</span><span>,</span> <span>utils</span><span></span>
<span></span>
<span></span>
<span>def</span> <span>train</span><span>(</span><span>args</span><span>,</span> <span>df</span><span>,</span> <span>trial</span><span>=</span><span>None</span><span>):</span>
<span>"""Train model on data."""</span><span></span>
<span></span>
    <span># Setup</span>
    <span>utils</span><span>.</span><span>set_seeds</span><span>()</span>
    <span>if</span> <span>args</span><span>.</span><span>shuffle</span><span>:</span> <span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>
    <span>df</span> <span>=</span> <span>df</span><span>[:</span> <span>args</span><span>.</span><span>subset</span><span>]</span>  <span># None = all samples</span>
    <span>df</span> <span>=</span> <span>data</span><span>.</span><span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>=</span><span>args</span><span>.</span><span>lower</span><span>,</span> <span>stem</span><span>=</span><span>args</span><span>.</span><span>stem</span><span>)</span>
    <span>label_encoder</span> <span>=</span> <span>data</span><span>.</span><span>LabelEncoder</span><span>()</span><span>.</span><span>fit</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>)</span>
    <span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> \
        <span>data</span><span>.</span><span>get_data_splits</span><span>(</span><span>X</span><span>=</span><span>df</span><span>.</span><span>text</span><span>.</span><span>to_numpy</span><span>(),</span> <span>y</span><span>=</span><span>label_encoder</span><span>.</span><span>encode</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>))</span>
    <span>test_df</span> <span>=</span> <span>pd</span><span>.</span><span>DataFrame</span><span>({</span><span>"text"</span><span>:</span> <span>X_test</span><span>,</span> <span>"tag"</span><span>:</span> <span>label_encoder</span><span>.</span><span>decode</span><span>(</span><span>y_test</span><span>)})</span><span></span>
<span></span>
    <span># Tf-idf</span>
    <span>vectorizer</span> <span>=</span> <span>TfidfVectorizer</span><span>(</span><span>analyzer</span><span>=</span><span>args</span><span>.</span><span>analyzer</span><span>,</span> <span>ngram_range</span><span>=</span><span>(</span><span>2</span><span>,</span><span>args</span><span>.</span><span>ngram_max_range</span><span>))</span>  <span># char n-grams</span>
    <span>X_train</span> <span>=</span> <span>vectorizer</span><span>.</span><span>fit_transform</span><span>(</span><span>X_train</span><span>)</span>
    <span>X_val</span> <span>=</span> <span>vectorizer</span><span>.</span><span>transform</span><span>(</span><span>X_val</span><span>)</span>
    <span>X_test</span> <span>=</span> <span>vectorizer</span><span>.</span><span>transform</span><span>(</span><span>X_test</span><span>)</span><span></span>
<span></span>
    <span># Oversample</span>
    <span>oversample</span> <span>=</span> <span>RandomOverSampler</span><span>(</span><span>sampling_strategy</span><span>=</span><span>"all"</span><span>)</span>
    <span>X_over</span><span>,</span> <span>y_over</span> <span>=</span> <span>oversample</span><span>.</span><span>fit_resample</span><span>(</span><span>X_train</span><span>,</span> <span>y_train</span><span>)</span><span></span>
<span></span>
    <span># Model</span>
    <span>model</span> <span>=</span> <span>SGDClassifier</span><span>(</span>
        <span>loss</span><span>=</span><span>"log"</span><span>,</span> <span>penalty</span><span>=</span><span>"l2"</span><span>,</span> <span>alpha</span><span>=</span><span>args</span><span>.</span><span>alpha</span><span>,</span> <span>max_iter</span><span>=</span><span>1</span><span>,</span>
        <span>learning_rate</span><span>=</span><span>"constant"</span><span>,</span> <span>eta0</span><span>=</span><span>args</span><span>.</span><span>learning_rate</span><span>,</span> <span>power_t</span><span>=</span><span>args</span><span>.</span><span>power_t</span><span>,</span>
        <span>warm_start</span><span>=</span><span>True</span><span>)</span><span></span>
<span></span>
    <span># Training</span>
    <span>for</span> <span>epoch</span> <span>in</span> <span>range</span><span>(</span><span>args</span><span>.</span><span>num_epochs</span><span>):</span>
        <span>model</span><span>.</span><span>fit</span><span>(</span><span>X_over</span><span>,</span> <span>y_over</span><span>)</span>
        <span>train_loss</span> <span>=</span> <span>log_loss</span><span>(</span><span>y_train</span><span>,</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_train</span><span>))</span>
        <span>val_loss</span> <span>=</span> <span>log_loss</span><span>(</span><span>y_val</span><span>,</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>))</span>
        <span>if</span> <span>not</span> <span>epoch</span><span>%</span><span>10</span><span>:</span>
            <span>print</span><span>(</span>
                <span>f</span><span>"Epoch: </span><span>{</span><span>epoch</span><span>:</span><span>02d</span><span>}</span><span> | "</span>
                <span>f</span><span>"train_loss: </span><span>{</span><span>train_loss</span><span>:</span><span>.5f</span><span>}</span><span>, "</span>
                <span>f</span><span>"val_loss: </span><span>{</span><span>val_loss</span><span>:</span><span>.5f</span><span>}</span><span>"</span>
            <span>)</span><span></span>
<span></span>
    <span># Threshold</span>
<span>    <span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>X_val</span><span>)</span>
</span><span>    <span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>)</span>
</span>    <span>args</span><span>.</span><span>threshold</span> <span>=</span> <span>np</span><span>.</span><span>quantile</span><span>(</span>
        <span>[</span><span>y_prob</span><span>[</span><span>i</span><span>][</span><span>j</span><span>]</span> <span>for</span> <span>i</span><span>,</span> <span>j</span> <span>in</span> <span>enumerate</span><span>(</span><span>y_pred</span><span>)],</span> <span>q</span><span>=</span><span>0.25</span><span>)</span>  <span># Q1</span><span></span>
<span></span>
    <span># Evaluation</span>
    <span>other_index</span> <span>=</span> <span>label_encoder</span><span>.</span><span>class_to_index</span><span>[</span><span>"other"</span><span>]</span>
    <span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_test</span><span>)</span>
    <span>y_pred</span> <span>=</span> <span>predict</span><span>.</span><span>custom_predict</span><span>(</span><span>y_prob</span><span>=</span><span>y_prob</span><span>,</span> <span>threshold</span><span>=</span><span>args</span><span>.</span><span>threshold</span><span>,</span> <span>index</span><span>=</span><span>other_index</span><span>)</span>
    <span>performance</span> <span>=</span> <span>evaluate</span><span>.</span><span>get_metrics</span><span>(</span>
        <span>y_true</span><span>=</span><span>y_test</span><span>,</span> <span>y_pred</span><span>=</span><span>y_pred</span><span>,</span> <span>classes</span><span>=</span><span>label_encoder</span><span>.</span><span>classes</span><span>,</span> <span>df</span><span>=</span><span>test_df</span>
    <span>)</span><span></span>
<span></span>
    <span>return</span> <span>{</span>
        <span>"args"</span><span>:</span> <span>args</span><span>,</span>
        <span>"label_encoder"</span><span>:</span> <span>label_encoder</span><span>,</span>
        <span>"vectorizer"</span><span>:</span> <span>vectorizer</span><span>,</span>
        <span>"model"</span><span>:</span> <span>model</span><span>,</span>
        <span>"performance"</span><span>:</span> <span>performance</span><span>,</span>
    <span>}</span>
</code></pre></div></td></tr></tbody></table>

This `train()` function calls two external functions (`predict.custom_predict()` from `predict.py` and `evaluate.get_metrics()` from `evaluate.py`):

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># tagifai/predict.py</span>
<span>import</span> <span>numpy</span> <span>as</span> <span>np</span><span></span>
<span></span>
<span>def</span> <span>custom_predict</span><span>(</span><span>y_prob</span><span>,</span> <span>threshold</span><span>,</span> <span>index</span><span>):</span>
    <span>"""Custom predict function that defaults</span>
<span>    to an index if conditions are not met."""</span>
    <span>y_pred</span> <span>=</span> <span>[</span><span>np</span><span>.</span><span>argmax</span><span>(</span><span>p</span><span>)</span> <span>if</span> <span>max</span><span>(</span><span>p</span><span>)</span> <span>&gt;</span> <span>threshold</span> <span>else</span> <span>index</span> <span>for</span> <span>p</span> <span>in</span> <span>y_prob</span><span>]</span>
    <span>return</span> <span>np</span><span>.</span><span>array</span><span>(</span><span>y_pred</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span>
<span>28</span>
<span>29</span>
<span>30</span>
<span>31</span>
<span>32</span>
<span>33</span>
<span>34</span>
<span>35</span>
<span>36</span>
<span>37</span>
<span>38</span>
<span>39</span>
<span>40</span>
<span>41</span>
<span>42</span>
<span>43</span>
<span>44</span>
<span>45</span>
<span>46</span>
<span>47</span>
<span>48</span>
<span>49</span>
<span>50</span>
<span>51</span>
<span>52</span>
<span>53</span>
<span>54</span>
<span>55</span>
<span>56</span>
<span>57</span>
<span>58</span>
<span>59</span>
<span>60</span>
<span>61</span>
<span>62</span>
<span>63</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/evaluate.py</span>
<span>import</span> <span>numpy</span> <span>as</span> <span>np</span>
<span>from</span> <span>sklearn.metrics</span> <span>import</span> <span>precision_recall_fscore_support</span>
<span>from</span> <span>snorkel.slicing</span> <span>import</span> <span>PandasSFApplier</span>
<span>from</span> <span>snorkel.slicing</span> <span>import</span> <span>slicing_function</span><span></span>
<span></span>
<span>@slicing_function</span><span>()</span>
<span>def</span> <span>nlp_cnn</span><span>(</span><span>x</span><span>):</span>
    <span>"""NLP Projects that use convolution."""</span>
    <span>nlp_projects</span> <span>=</span> <span>"natural-language-processing"</span> <span>in</span> <span>x</span><span>.</span><span>tag</span>
    <span>convolution_projects</span> <span>=</span> <span>"CNN"</span> <span>in</span> <span>x</span><span>.</span><span>text</span> <span>or</span> <span>"convolution"</span> <span>in</span> <span>x</span><span>.</span><span>text</span>
    <span>return</span> <span>(</span><span>nlp_projects</span> <span>and</span> <span>convolution_projects</span><span>)</span><span></span>
<span></span>
<span>@slicing_function</span><span>()</span>
<span>def</span> <span>short_text</span><span>(</span><span>x</span><span>):</span>
    <span>"""Projects with short titles and descriptions."""</span>
    <span>return</span> <span>len</span><span>(</span><span>x</span><span>.</span><span>text</span><span>.</span><span>split</span><span>())</span> <span>&lt;</span> <span>8</span>  <span># less than 8 words</span><span></span>
<span></span>
<span>def</span> <span>get_slice_metrics</span><span>(</span><span>y_true</span><span>,</span> <span>y_pred</span><span>,</span> <span>slices</span><span>):</span>
    <span>"""Generate metrics for slices of data."""</span>
    <span>metrics</span> <span>=</span> <span>{}</span>
    <span>for</span> <span>slice_name</span> <span>in</span> <span>slices</span><span>.</span><span>dtype</span><span>.</span><span>names</span><span>:</span>
        <span>mask</span> <span>=</span> <span>slices</span><span>[</span><span>slice_name</span><span>]</span><span>.</span><span>astype</span><span>(</span><span>bool</span><span>)</span>
        <span>if</span> <span>sum</span><span>(</span><span>mask</span><span>):</span>
            <span>slice_metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span>
                <span>y_true</span><span>[</span><span>mask</span><span>],</span> <span>y_pred</span><span>[</span><span>mask</span><span>],</span> <span>average</span><span>=</span><span>"micro"</span>
            <span>)</span>
            <span>metrics</span><span>[</span><span>slice_name</span><span>]</span> <span>=</span> <span>{}</span>
            <span>metrics</span><span>[</span><span>slice_name</span><span>][</span><span>"precision"</span><span>]</span> <span>=</span> <span>slice_metrics</span><span>[</span><span>0</span><span>]</span>
            <span>metrics</span><span>[</span><span>slice_name</span><span>][</span><span>"recall"</span><span>]</span> <span>=</span> <span>slice_metrics</span><span>[</span><span>1</span><span>]</span>
            <span>metrics</span><span>[</span><span>slice_name</span><span>][</span><span>"f1"</span><span>]</span> <span>=</span> <span>slice_metrics</span><span>[</span><span>2</span><span>]</span>
            <span>metrics</span><span>[</span><span>slice_name</span><span>][</span><span>"num_samples"</span><span>]</span> <span>=</span> <span>len</span><span>(</span><span>y_true</span><span>[</span><span>mask</span><span>])</span>
    <span>return</span> <span>metrics</span><span></span>
<span></span>
<span>def</span> <span>get_metrics</span><span>(</span><span>y_true</span><span>,</span> <span>y_pred</span><span>,</span> <span>classes</span><span>,</span> <span>df</span><span>=</span><span>None</span><span>):</span>
    <span>"""Performance metrics using ground truths and predictions."""</span>
    <span># Performance</span>
    <span>metrics</span> <span>=</span> <span>{</span><span>"overall"</span><span>:</span> <span>{},</span> <span>"class"</span><span>:</span> <span>{}}</span><span></span>
<span></span>
    <span># Overall metrics</span>
    <span>overall_metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_true</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
    <span>metrics</span><span>[</span><span>"overall"</span><span>][</span><span>"precision"</span><span>]</span> <span>=</span> <span>overall_metrics</span><span>[</span><span>0</span><span>]</span>
    <span>metrics</span><span>[</span><span>"overall"</span><span>][</span><span>"recall"</span><span>]</span> <span>=</span> <span>overall_metrics</span><span>[</span><span>1</span><span>]</span>
    <span>metrics</span><span>[</span><span>"overall"</span><span>][</span><span>"f1"</span><span>]</span> <span>=</span> <span>overall_metrics</span><span>[</span><span>2</span><span>]</span>
    <span>metrics</span><span>[</span><span>"overall"</span><span>][</span><span>"num_samples"</span><span>]</span> <span>=</span> <span>np</span><span>.</span><span>float64</span><span>(</span><span>len</span><span>(</span><span>y_true</span><span>))</span><span></span>
<span></span>
    <span># Per-class metrics</span>
    <span>class_metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_true</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>None</span><span>)</span>
    <span>for</span> <span>i</span><span>,</span> <span>_class</span> <span>in</span> <span>enumerate</span><span>(</span><span>classes</span><span>):</span>
        <span>metrics</span><span>[</span><span>"class"</span><span>][</span><span>_class</span><span>]</span> <span>=</span> <span>{</span>
            <span>"precision"</span><span>:</span> <span>class_metrics</span><span>[</span><span>0</span><span>][</span><span>i</span><span>],</span>
            <span>"recall"</span><span>:</span> <span>class_metrics</span><span>[</span><span>1</span><span>][</span><span>i</span><span>],</span>
            <span>"f1"</span><span>:</span> <span>class_metrics</span><span>[</span><span>2</span><span>][</span><span>i</span><span>],</span>
            <span>"num_samples"</span><span>:</span> <span>np</span><span>.</span><span>float64</span><span>(</span><span>class_metrics</span><span>[</span><span>3</span><span>][</span><span>i</span><span>]),</span>
        <span>}</span><span></span>
<span></span>
    <span># Slice metrics</span>
    <span>if</span> <span>df</span> <span>is</span> <span>not</span> <span>None</span><span>:</span>
        <span>slices</span> <span>=</span> <span>PandasSFApplier</span><span>([</span><span>nlp_cnn</span><span>,</span> <span>short_text</span><span>])</span><span>.</span><span>apply</span><span>(</span><span>df</span><span>)</span>
        <span>metrics</span><span>[</span><span>"slices"</span><span>]</span> <span>=</span> <span>get_slice_metrics</span><span>(</span>
            <span>y_true</span><span>=</span><span>y_true</span><span>,</span> <span>y_pred</span><span>=</span><span>y_pred</span><span>,</span> <span>slices</span><span>=</span><span>slices</span><span>)</span><span></span>
<span></span>
    <span>return</span> <span>metrics</span>
</code></pre></div></td></tr></tbody></table>

Install required packages and add to `requirements.txt`:

```
pip install imbalanced-learn==0.8.1 snorkel==0.9.8

```

```
# Add to requirements.txt
imbalanced-learn==0.8.1
snorkel==0.9.8

```

Commands to train a model:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>config</span> <span>import</span> <span>config</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>main</span>
<span>args_fp</span> <span>=</span> <span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"args.json"</span><span>)</span>
<span>main</span><span>.</span><span>train_model</span><span>(</span><span>args_fp</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
Epoch: 00 | train_loss: 1.16783, val_loss: 1.20177
Epoch: 10 | train_loss: 0.46262, val_loss: 0.62612
Epoch: 20 | train_loss: 0.31599, val_loss: 0.51986
Epoch: 30 | train_loss: 0.25191, val_loss: 0.47544
Epoch: 40 | train_loss: 0.21720, val_loss: 0.45176
Epoch: 50 | train_loss: 0.19610, val_loss: 0.43770
Epoch: 60 | train_loss: 0.18221, val_loss: 0.42857
Epoch: 70 | train_loss: 0.17291, val_loss: 0.42246
Epoch: 80 | train_loss: 0.16643, val_loss: 0.41818
Epoch: 90 | train_loss: 0.16160, val_loss: 0.41528
{
  "overall": {
    "precision": 0.8990934378802025,
    "recall": 0.8194444444444444,
    "f1": 0.838280325954406,
    "num_samples": 144.0
  },
  "class": {
    "computer-vision": {
      "precision": 0.975,
      "recall": 0.7222222222222222,
      "f1": 0.8297872340425532,
      "num_samples": 54.0
    },
    "mlops": {
      "precision": 0.9090909090909091,
      "recall": 0.8333333333333334,
      "f1": 0.8695652173913043,
      "num_samples": 12.0
    },
    "natural-language-processing": {
      "precision": 0.9803921568627451,
      "recall": 0.8620689655172413,
      "f1": 0.9174311926605505,
      "num_samples": 58.0
    },
    "other": {
      "precision": 0.4523809523809524,
      "recall": 0.95,
      "f1": 0.6129032258064516,
      "num_samples": 20.0
    }
  },
  "slices": {
    "nlp_cnn": {
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0,
      "num_samples": 1
    },
    "short_text": {
      "precision": 0.8,
      "recall": 0.8,
      "f1": 0.8000000000000002,
      "num_samples": 5
    }
  }
}

```

### Optimize

Optimize args

Now that we can train one model, we're ready to train many models to optimize our hyperparameters:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>import</span> <span>mlflow</span>
<span>from</span> <span>numpyencoder</span> <span>import</span> <span>NumpyEncoder</span>
<span>import</span> <span>optuna</span>
<span>from</span> <span>optuna.integration.mlflow</span> <span>import</span> <span>MLflowCallback</span><span></span>
<span></span>
<span>def</span> <span>optimize</span><span>(</span><span>study_name</span><span>,</span> <span>num_trials</span><span>):</span>
    <span>"""Optimize hyperparameters."""</span>
    <span># Load labeled data</span>
    <span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"labeled_projects.csv"</span><span>))</span><span></span>
<span></span>
    <span># Optimize</span>
    <span>pruner</span> <span>=</span> <span>optuna</span><span>.</span><span>pruners</span><span>.</span><span>MedianPruner</span><span>(</span><span>n_startup_trials</span><span>=</span><span>5</span><span>,</span> <span>n_warmup_steps</span><span>=</span><span>5</span><span>)</span>
    <span>study</span> <span>=</span> <span>optuna</span><span>.</span><span>create_study</span><span>(</span><span>study_name</span><span>=</span><span>"optimization"</span><span>,</span> <span>direction</span><span>=</span><span>"maximize"</span><span>,</span> <span>pruner</span><span>=</span><span>pruner</span><span>)</span>
    <span>mlflow_callback</span> <span>=</span> <span>MLflowCallback</span><span>(</span>
        <span>tracking_uri</span><span>=</span><span>mlflow</span><span>.</span><span>get_tracking_uri</span><span>(),</span> <span>metric_name</span><span>=</span><span>"f1"</span><span>)</span>
    <span>study</span><span>.</span><span>optimize</span><span>(</span>
        <span>lambda</span> <span>trial</span><span>:</span> <span>train</span><span>.</span><span>objective</span><span>(</span><span>args</span><span>,</span> <span>df</span><span>,</span> <span>trial</span><span>),</span>
        <span>n_trials</span><span>=</span><span>num_trials</span><span>,</span>
        <span>callbacks</span><span>=</span><span>[</span><span>mlflow_callback</span><span>])</span><span></span>
<span></span>
    <span># Best trial</span>
    <span>trials_df</span> <span>=</span> <span>study</span><span>.</span><span>trials_dataframe</span><span>()</span>
    <span>trials_df</span> <span>=</span> <span>trials_df</span><span>.</span><span>sort_values</span><span>([</span><span>"user_attrs_f1"</span><span>],</span> <span>ascending</span><span>=</span><span>False</span><span>)</span>
    <span>utils</span><span>.</span><span>save_dict</span><span>({</span><span>**</span><span>args</span><span>.</span><span>__dict__</span><span>,</span> <span>**</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>params</span><span>},</span> <span>args_fp</span><span>,</span> <span>cls</span><span>=</span><span>NumpyEncoder</span><span>)</span>
    <span>print</span><span>(</span><span>f</span><span>"</span><span>\n</span><span>Best value (f1): </span><span>{</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>value</span><span>}</span><span>"</span><span>)</span>
    <span>print</span><span>(</span><span>f</span><span>"Best hyperparameters: </span><span>{</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>study</span><span>.</span><span>best_trial</span><span>.</span><span>params</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>)</span><span>}</span><span>"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

We'll define the `objective()` function inside `train.py`:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/train.py</span>
<span>def</span> <span>objective</span><span>(</span><span>args</span><span>,</span> <span>df</span><span>,</span> <span>trial</span><span>):</span>
    <span>"""Objective function for optimization trials."""</span>
    <span># Parameters to tune</span>
    <span>args</span><span>.</span><span>analyzer</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_categorical</span><span>(</span><span>"analyzer"</span><span>,</span> <span>[</span><span>"word"</span><span>,</span> <span>"char"</span><span>,</span> <span>"char_wb"</span><span>])</span>
    <span>args</span><span>.</span><span>ngram_max_range</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_int</span><span>(</span><span>"ngram_max_range"</span><span>,</span> <span>3</span><span>,</span> <span>10</span><span>)</span>
    <span>args</span><span>.</span><span>learning_rate</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_loguniform</span><span>(</span><span>"learning_rate"</span><span>,</span> <span>1e-2</span><span>,</span> <span>1e0</span><span>)</span>
    <span>args</span><span>.</span><span>power_t</span> <span>=</span> <span>trial</span><span>.</span><span>suggest_uniform</span><span>(</span><span>"power_t"</span><span>,</span> <span>0.1</span><span>,</span> <span>0.5</span><span>)</span><span></span>
<span></span>
    <span># Train &amp; evaluate</span>
    <span>artifacts</span> <span>=</span> <span>train</span><span>(</span><span>args</span><span>=</span><span>args</span><span>,</span> <span>df</span><span>=</span><span>df</span><span>,</span> <span>trial</span><span>=</span><span>trial</span><span>)</span><span></span>
<span></span>
    <span># Set additional attributes</span>
    <span>overall_performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>][</span><span>"overall"</span><span>]</span>
    <span>print</span><span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>overall_performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"precision"</span><span>,</span> <span>overall_performance</span><span>[</span><span>"precision"</span><span>])</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"recall"</span><span>,</span> <span>overall_performance</span><span>[</span><span>"recall"</span><span>])</span>
    <span>trial</span><span>.</span><span>set_user_attr</span><span>(</span><span>"f1"</span><span>,</span> <span>overall_performance</span><span>[</span><span>"f1"</span><span>])</span><span></span>
<span></span>
    <span>return</span> <span>overall_performance</span><span>[</span><span>"f1"</span><span>]</span>
</code></pre></div></td></tr></tbody></table>

Recall that in our notebook, we modified the `train()` function to include information about trials during optimization for pruning:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/train.py</span>
<span>import</span> <span>optuna</span><span></span>
<span></span>
<span>def</span> <span>train</span><span>():</span>
    <span>...</span>
    <span># Training</span>
    <span>for</span> <span>epoch</span> <span>in</span> <span>range</span><span>(</span><span>args</span><span>.</span><span>num_epochs</span><span>):</span>
        <span>...</span>
        <span># Pruning (for optimization in next section)</span>
        <span>if</span> <span>trial</span><span>:</span>
            <span>trial</span><span>.</span><span>report</span><span>(</span><span>val_loss</span><span>,</span> <span>epoch</span><span>)</span>
            <span>if</span> <span>trial</span><span>.</span><span>should_prune</span><span>():</span>
                <span>raise</span> <span>optuna</span><span>.</span><span>TrialPruned</span><span>()</span>
</code></pre></div></td></tr></tbody></table>

Since we're using the `MLflowCallback` here with Optuna, we can either allow all our experiments to be stored under the default `mlruns` directory that MLflow will create or we can configure that location:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># config/config.py</span>
<span>import</span> <span>mlflow</span>
<span>STORES_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"stores"</span><span>)</span>
<span>MODEL_REGISTRY</span> <span>=</span> <span>Path</span><span>(</span><span>STORES_DIR</span><span>,</span> <span>"model"</span><span>)</span>
<span>MODEL_REGISTRY</span><span>.</span><span>mkdir</span><span>(</span><span>parents</span><span>=</span><span>True</span><span>,</span> <span>exist_ok</span><span>=</span><span>True</span><span>)</span>
<span>mlflow</span><span>.</span><span>set_tracking_uri</span><span>(</span><span>"file://"</span> <span>+</span> <span>str</span><span>(</span><span>MODEL_REGISTRY</span><span>.</span><span>absolute</span><span>()))</span>
</code></pre></div></td></tr></tbody></table>

Install required packages and add to `requirements.txt`:

```
pip install mlflow==1.23.1 optuna==2.10.0 numpyencoder==0.3.0

```

```
# Add to requirements.txt
mlflow==1.23.1
numpyencoder==0.3.0
optuna==2.10.0

```

Commands to optimize hyperparameters:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>config</span> <span>import</span> <span>config</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>main</span>
<span>args_fp</span> <span>=</span> <span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"args.json"</span><span>)</span>
<span>main</span><span>.</span><span>optimize</span><span>(</span><span>args_fp</span><span>,</span> <span>study_name</span><span>=</span><span>"optimization"</span><span>,</span> <span>num_trials</span><span>=</span><span>20</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
A new study created in memory with name: optimization
...
Best value (f1): 0.8497010532479641
Best hyperparameters: {
    "analyzer": "char_wb",
    "ngram_max_range": 6,
    "learning_rate": 0.8616849162496086,
    "power_t": 0.21283622300887173
}

```

We should see our experiment in our model registry, located at `stores/model/`:

### Experiment tracking

Experiment tracking

Now that we have our optimized hyperparameters, we can train a model and store it's artifacts via experiment tracking. We'll start by modifying the `train()` operation in our `main.py` script:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span>
<span>22</span>
<span>23</span>
<span>24</span>
<span>25</span>
<span>26</span>
<span>27</span>
<span>28</span>
<span>29</span>
<span>30</span>
<span>31</span>
<span>32</span>
<span>33</span>
<span>34</span>
<span>35</span>
<span>36</span>
<span>37</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>import</span> <span>joblib</span>
<span>import</span> <span>tempfile</span><span></span>
<span></span>
<span>def</span> <span>train_model</span><span>(</span><span>args_fp</span><span>,</span> <span>experiment_name</span><span>,</span> <span>run_name</span><span>):</span>
    <span>"""Train a model given arguments."""</span>
    <span># Load labeled data</span>
    <span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>DATA_DIR</span><span>,</span> <span>"labeled_projects.csv"</span><span>))</span><span></span>
<span></span>
    <span># Train</span>
    <span>args</span> <span>=</span> <span>Namespace</span><span>(</span><span>**</span><span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>args_fp</span><span>))</span>
    <span>mlflow</span><span>.</span><span>set_experiment</span><span>(</span><span>experiment_name</span><span>=</span><span>experiment_name</span><span>)</span>
    <span>with</span> <span>mlflow</span><span>.</span><span>start_run</span><span>(</span><span>run_name</span><span>=</span><span>run_name</span><span>):</span>
        <span>run_id</span> <span>=</span> <span>mlflow</span><span>.</span><span>active_run</span><span>()</span><span>.</span><span>info</span><span>.</span><span>run_id</span>
        <span>print</span><span>(</span><span>f</span><span>"Run ID: </span><span>{</span><span>run_id</span><span>}</span><span>"</span><span>)</span>
        <span>artifacts</span> <span>=</span> <span>train</span><span>.</span><span>train</span><span>(</span><span>df</span><span>=</span><span>df</span><span>,</span> <span>args</span><span>=</span><span>args</span><span>)</span>
        <span>performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>]</span>
        <span>print</span><span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span><span></span>
<span></span>
        <span># Log metrics and parameters</span>
        <span>performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>]</span>
        <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"precision"</span><span>:</span> <span>performance</span><span>[</span><span>"overall"</span><span>][</span><span>"precision"</span><span>]})</span>
        <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"recall"</span><span>:</span> <span>performance</span><span>[</span><span>"overall"</span><span>][</span><span>"recall"</span><span>]})</span>
        <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"f1"</span><span>:</span> <span>performance</span><span>[</span><span>"overall"</span><span>][</span><span>"f1"</span><span>]})</span>
        <span>mlflow</span><span>.</span><span>log_params</span><span>(</span><span>vars</span><span>(</span><span>artifacts</span><span>[</span><span>"args"</span><span>]))</span><span></span>
<span></span>
        <span># Log artifacts</span>
        <span>with</span> <span>tempfile</span><span>.</span><span>TemporaryDirectory</span><span>()</span> <span>as</span> <span>dp</span><span>:</span>
            <span>artifacts</span><span>[</span><span>"label_encoder"</span><span>]</span><span>.</span><span>save</span><span>(</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"label_encoder.json"</span><span>))</span>
            <span>joblib</span><span>.</span><span>dump</span><span>(</span><span>artifacts</span><span>[</span><span>"vectorizer"</span><span>],</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"vectorizer.pkl"</span><span>))</span>
            <span>joblib</span><span>.</span><span>dump</span><span>(</span><span>artifacts</span><span>[</span><span>"model"</span><span>],</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"model.pkl"</span><span>))</span>
            <span>utils</span><span>.</span><span>save_dict</span><span>(</span><span>performance</span><span>,</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"performance.json"</span><span>))</span>
            <span>mlflow</span><span>.</span><span>log_artifacts</span><span>(</span><span>dp</span><span>)</span><span></span>
<span></span>
    <span># Save to config</span>
    <span>open</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"run_id.txt"</span><span>),</span> <span>"w"</span><span>)</span><span>.</span><span>write</span><span>(</span><span>run_id</span><span>)</span>
    <span>utils</span><span>.</span><span>save_dict</span><span>(</span><span>performance</span><span>,</span> <span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"performance.json"</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

There's a lot more happening inside our `train_model()` function but it's necessary in order to store all the metrics, parameters and artifacts. We're also going to update the `train()` function inside `train.py` so that the intermediate metrics are captured:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># tagifai/train.py</span>
<span>import</span> <span>mlflow</span><span></span>
<span></span>
<span>def</span> <span>train</span><span>():</span>
    <span>...</span>
    <span># Training</span>
    <span>for</span> <span>epoch</span> <span>in</span> <span>range</span><span>(</span><span>args</span><span>.</span><span>num_epochs</span><span>):</span>
        <span>...</span>
        <span># Log</span>
        <span>if</span> <span>not</span> <span>trial</span><span>:</span>
            <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"train_loss"</span><span>:</span> <span>train_loss</span><span>,</span> <span>"val_loss"</span><span>:</span> <span>val_loss</span><span>},</span> <span>step</span><span>=</span><span>epoch</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

Commands to train a model with experiment tracking:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>config</span> <span>import</span> <span>config</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>main</span>
<span>args_fp</span> <span>=</span> <span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"args.json"</span><span>)</span>
<span>main</span><span>.</span><span>train_model</span><span>(</span><span>args_fp</span><span>,</span> <span>experiment_name</span><span>=</span><span>"baselines"</span><span>,</span> <span>run_name</span><span>=</span><span>"sgd"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
Run ID: d91d9760b2e14a5fbbae9f3762f0afaf
Epoch: 00 | train_loss: 0.74266, val_loss: 0.83335
Epoch: 10 | train_loss: 0.21884, val_loss: 0.42853
Epoch: 20 | train_loss: 0.16632, val_loss: 0.39420
Epoch: 30 | train_loss: 0.15108, val_loss: 0.38396
Epoch: 40 | train_loss: 0.14589, val_loss: 0.38089
Epoch: 50 | train_loss: 0.14358, val_loss: 0.37992
Epoch: 60 | train_loss: 0.14084, val_loss: 0.37977
Epoch: 70 | train_loss: 0.14025, val_loss: 0.37828
Epoch: 80 | train_loss: 0.13983, val_loss: 0.37699
Epoch: 90 | train_loss: 0.13841, val_loss: 0.37772
{
  "overall": {
    "precision": 0.9026155077984347,
    "recall": 0.8333333333333334,
    "f1": 0.8497010532479641,
    "num_samples": 144.0
  },
  "class": {
    "computer-vision": {
      "precision": 0.975609756097561,
      "recall": 0.7407407407407407,
      "f1": 0.8421052631578947,
      "num_samples": 54.0
    },
    "mlops": {
      "precision": 0.9090909090909091,
      "recall": 0.8333333333333334,
      "f1": 0.8695652173913043,
      "num_samples": 12.0
    },
    "natural-language-processing": {
      "precision": 0.9807692307692307,
      "recall": 0.8793103448275862,
      "f1": 0.9272727272727272,
      "num_samples": 58.0
    },
    "other": {
      "precision": 0.475,
      "recall": 0.95,
      "f1": 0.6333333333333334,
      "num_samples": 20.0
    }
  },
  "slices": {
    "nlp_cnn": {
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0,
      "num_samples": 1
    },
    "short_text": {
      "precision": 0.8,
      "recall": 0.8,
      "f1": 0.8000000000000002,
      "num_samples": 5
    }
  }
}

```

Our configuration directory should now have a `performance.json` and a `run_id.txt` file. We're saving these so we can quickly access this metadata of the latest successful training. If we were considering several models as once, we could manually set the run\_id of the run we want to deploy or programmatically identify the best across experiments.

```
config/
├── args.json         - arguments
├── config.py         - configuration setup
├── performance.json  - performance metrics
└── run_id.txt        - ID of latest successful run

```

And we should see this specific experiment and run in our model registry:

```
stores/model/
├── 0/
└── 1/

```

### Predict

Predict texts

We're finally ready to use our trained model for inference. We'll add the operation to predict a tag to `main.py`:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>data</span><span>,</span> <span>predict</span><span>,</span> <span>train</span><span>,</span> <span>utils</span><span></span>
<span></span>
<span>def</span> <span>predict_tag</span><span>(</span><span>text</span><span>,</span> <span>run_id</span><span>=</span><span>None</span><span>):</span>
    <span>"""Predict tag for text."""</span>
    <span>if</span> <span>not</span> <span>run_id</span><span>:</span>
        <span>run_id</span> <span>=</span> <span>open</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"run_id.txt"</span><span>))</span><span>.</span><span>read</span><span>()</span>
    <span>artifacts</span> <span>=</span> <span>load_artifacts</span><span>(</span><span>run_id</span><span>=</span><span>run_id</span><span>)</span>
    <span>prediction</span> <span>=</span> <span>predict</span><span>.</span><span>predict</span><span>(</span><span>texts</span><span>=</span><span>[</span><span>text</span><span>],</span> <span>artifacts</span><span>=</span><span>artifacts</span><span>)</span>
    <span>print</span><span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>prediction</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
    <span>return</span> <span>prediction</span>
</code></pre></div></td></tr></tbody></table>

This involves creating the `load_artifacts()` function inside our `main.py` script:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span>
<span>17</span>
<span>18</span>
<span>19</span>
<span>20</span>
<span>21</span></pre></div></td><td><div><pre><span></span><code><span># tagifai/main.py</span>
<span>def</span> <span>load_artifacts</span><span>(</span><span>run_id</span><span>):</span>
    <span>"""Load artifacts for a given run_id."""</span>
    <span># Locate specifics artifacts directory</span>
    <span>experiment_id</span> <span>=</span> <span>mlflow</span><span>.</span><span>get_run</span><span>(</span><span>run_id</span><span>=</span><span>run_id</span><span>)</span><span>.</span><span>info</span><span>.</span><span>experiment_id</span>
    <span>artifacts_dir</span> <span>=</span> <span>Path</span><span>(</span><span>config</span><span>.</span><span>MODEL_REGISTRY</span><span>,</span> <span>experiment_id</span><span>,</span> <span>run_id</span><span>,</span> <span>"artifacts"</span><span>)</span><span></span>
<span></span>
    <span># Load objects from run</span>
    <span>args</span> <span>=</span> <span>Namespace</span><span>(</span><span>**</span><span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>Path</span><span>(</span><span>artifacts_dir</span><span>,</span> <span>"args.json"</span><span>)))</span>
    <span>vectorizer</span> <span>=</span> <span>joblib</span><span>.</span><span>load</span><span>(</span><span>Path</span><span>(</span><span>artifacts_dir</span><span>,</span> <span>"vectorizer.pkl"</span><span>))</span>
    <span>label_encoder</span> <span>=</span> <span>data</span><span>.</span><span>LabelEncoder</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>=</span><span>Path</span><span>(</span><span>artifacts_dir</span><span>,</span> <span>"label_encoder.json"</span><span>))</span>
    <span>model</span> <span>=</span> <span>joblib</span><span>.</span><span>load</span><span>(</span><span>Path</span><span>(</span><span>artifacts_dir</span><span>,</span> <span>"model.pkl"</span><span>))</span>
    <span>performance</span> <span>=</span> <span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>Path</span><span>(</span><span>artifacts_dir</span><span>,</span> <span>"performance.json"</span><span>))</span><span></span>
<span></span>
    <span>return</span> <span>{</span>
        <span>"args"</span><span>:</span> <span>args</span><span>,</span>
        <span>"label_encoder"</span><span>:</span> <span>label_encoder</span><span>,</span>
        <span>"vectorizer"</span><span>:</span> <span>vectorizer</span><span>,</span>
        <span>"model"</span><span>:</span> <span>model</span><span>,</span>
        <span>"performance"</span><span>:</span> <span>performance</span>
    <span>}</span>
</code></pre></div></td></tr></tbody></table>

and defining the `predict()` function inside `predict.py`:

<table><tbody><tr><td><div><pre><span></span><span> 1</span>
<span> 2</span>
<span> 3</span>
<span> 4</span>
<span> 5</span>
<span> 6</span>
<span> 7</span>
<span> 8</span>
<span> 9</span>
<span>10</span>
<span>11</span>
<span>12</span>
<span>13</span>
<span>14</span>
<span>15</span>
<span>16</span></pre></div></td><td><div><pre><span></span><code><span>def</span> <span>predict</span><span>(</span><span>texts</span><span>,</span> <span>artifacts</span><span>):</span>
    <span>"""Predict tags for given texts."""</span>
    <span>x</span> <span>=</span> <span>artifacts</span><span>[</span><span>"vectorizer"</span><span>]</span><span>.</span><span>transform</span><span>(</span><span>texts</span><span>)</span>
    <span>y_pred</span> <span>=</span> <span>custom_predict</span><span>(</span>
        <span>y_prob</span><span>=</span><span>artifacts</span><span>[</span><span>"model"</span><span>]</span><span>.</span><span>predict_proba</span><span>(</span><span>x</span><span>),</span>
        <span>threshold</span><span>=</span><span>artifacts</span><span>[</span><span>"args"</span><span>]</span><span>.</span><span>threshold</span><span>,</span>
        <span>index</span><span>=</span><span>artifacts</span><span>[</span><span>"label_encoder"</span><span>]</span><span>.</span><span>class_to_index</span><span>[</span><span>"other"</span><span>])</span>
    <span>tags</span> <span>=</span> <span>artifacts</span><span>[</span><span>"label_encoder"</span><span>]</span><span>.</span><span>decode</span><span>(</span><span>y_pred</span><span>)</span>
    <span>predictions</span> <span>=</span> <span>[</span>
        <span>{</span>
            <span>"input_text"</span><span>:</span> <span>texts</span><span>[</span><span>i</span><span>],</span>
            <span>"predicted_tags"</span><span>:</span> <span>tags</span><span>[</span><span>i</span><span>],</span>
        <span>}</span>
        <span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>len</span><span>(</span><span>tags</span><span>))</span>
    <span>]</span>
    <span>return</span> <span>predictions</span>
</code></pre></div></td></tr></tbody></table>

Commands to predict the tag for text:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>text</span> <span>=</span> <span>"Transfer learning with transformers for text classification."</span>
<span>run_id</span> <span>=</span> <span>open</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"run_id.txt"</span><span>))</span><span>.</span><span>read</span><span>()</span>
<span>predict_tag</span><span>(</span><span>text</span><span>=</span><span>text</span><span>,</span> <span>run_id</span><span>=</span><span>run_id</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
[
  {
    "input_text": "Transfer learning with transformers for text classification.",
    "predicted_tag": "natural-language-processing"
  }
]

```

> Don't worry about formatting our functions and classes just yet. We'll be covering how to properly do this in the [documentation](https://madewithml.com/courses/mlops/documentation/) lesson.

So many functions and classes...

As we migrated from notebooks to scripts, we had to define so many functions and classes. How can we improve this?

Show answer

As we work on more projects, we may find it useful to contribute our generalized functions and classes to a central repository. Provided that all the code is [tested](https://madewithml.com/courses/mlops/testing/) and [documented](https://madewithml.com/courses/mlops/documentation/), this can reduce boilerplate code and redundant efforts. To make this central repository available for everyone, we can [package](https://packaging.python.org/tutorials/packaging-projects/) it and share it publicly or keep it private with a PyPI mirror, etc.

```
# Ex. installing our public repo
pip install git+https://github.com/GokuMohandas/mlops-course#egg=tagifai

```

___

To cite this content, please use:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Organization - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>

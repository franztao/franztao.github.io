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

## 直觉

到目前为止，一直在笔记本内部工作，这使能够非常快速地训练模型。但是，笔记本并不容易投入生产，而且并不总是能够控制环境（例如，Google Colab 会定期更新其软件包）。当使用[notebook](https://github.com/GokuMohandas/mlops-course/blob/main/notebooks/tagifai.ipynb)时，有一组预加载的包（`!pip list`在 notebook 中运行以查看所有包）。但是现在想要明确定义环境，以便可以在本地（为和团队成员）以及在部署到生产环境时重现它。在 Python 中打包时有[许多推荐的工具](https://packaging.python.org/guides/tool-recommendations/)，将使用经过验证的[Pip](https://pip.pypa.io/en/stable/)。

> 有许多替代依赖管理和打包工具，例如[Poetry](https://python-poetry.org/)，但这些新选项仍有许多变化。将坚持使用 Pip，因为它适用于应用程序，并且不想处理[长解决周期](https://github.com/python-poetry/poetry/issues/2094)之类的问题。

## 终端

在开始打包之前，需要一种创建文件和运行命令的方法。可以通过终端来执行此操作，这将允许运行 bash、zsh 等语言来执行命令。无论您的操作系统或命令行界面 (CLI) 编程语言如何，运行的所有命令都应该相同。

小费

强烈建议您使用[iTerm2](https://iterm2.com/) (Mac) 或[ConEmu](https://conemu.github.io/) (Windows) 代替默认终端，因为它具有丰富的功能。

## 项目

While we'll organize our code from our notebook to scripts in the [next lesson](https://madewithml.com/courses/mlops/organization/), we'll create the main project directory now so that we can save our packaging components there. We'll call our main project directory `mlops` but feel free to name it anything you'd like.

```
# Create and change into the directory
mkdir mlops
cd mlops

```

## Python

First thing we'll do is set up the correct version of Python. We'll be using version `3.7.13` specifically but any version of Python 3 should work. Though you could download different Python versions online, we highly recommend using a version manager such as [pyenv](https://github.com/pyenv/pyenv).

> Pyenv works for Mac & Linux, but if you're on windows, we recommend using [pyenv-win](https://github.com/pyenv-win/pyenv-win).

brew install pyenv  
python --versionPython 3.6.9pyenv versionssystem  
\* 3.6.9pyenv install 3.7.13  
pyenv local 3.7.13system  
3.6.9  
\* 3.7.13python --versionPython 3.7.13

> We highly recommend using Python `3.7.13` because, while using another version of Python will work, we may face some conflicts with certain package versions that may need to be resolved.

## Virtual environment

Next, we'll set up a [virtual environment](https://docs.python.org/3/library/venv.html) so we can isolate the required packages for our application. This will also keep components separated from other projects which may have different dependencies. Once we create our virtual environment, we'll activate it and install our required packages.

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pip setuptools wheel

```

Let's unpack what's happening here:

1.  Creating a Python virtual environment named `venv`.
2.  Activate our virtual environment. Type `deactivate` to exit the virtual environment.
3.  Upgrading required packages so we download the latest package wheels.

Our virtual environment directory `venv` should be visible when we list the directories in our project:

```
mlops/
├── venv/
├── requirements.txt
└── setup.py

```

We'll know our virtual environment is active because we will it's name on the terminal. We can further validate by making sure `pip freeze` returns nothing.

```
(venv) ➜  mlops: pip freeze

```

### Requirements

We'll create a separate file called `requirements.txt` where we'll specify the packages (with their versions) that we want to install. While we could place these requirements directly inside `setup.py`, many applications still look for a separate `requirements.txt`.

We should be adding packages with their versions to our `requirements.txt` as we require them for our project. It's inadvisable to install all packages and then do `pip freeze > requirements.txt` because it dumps the dependencies of all our packages into the file (even the ones we didn't explicitly install). To mitigate this, there are tools such as [pipreqs](https://github.com/bndr/pipreqs), [pip-tools](https://github.com/jazzband/pip-tools), [pipchill](https://github.com/rbanffy/pip-chill), etc. that will only list the packages that are not dependencies. However, they're dependency resolving is not always accurate and don't work when you want to separate packages for different tasks (developing, testing, etc.).

Tip

If we experience conflicts between package versions, we can relax constraints by specifying that the package needs to be above a certain version, as opposed to the exact version. We could also specify no version for all packages and allow pip to resolve all conflicts. And then we can see which version were actually installed and add that information to our `requirements.txt` file.

```
# requirements.txt
<PACKAGE>==<VERSION>  # exact version
<PACKAGE>==<VERSION>  # above version
<PACKAGE>             # no version

```

### Setup

Let's create a file called `setup.py` to provide instructions on how to set up our virtual environment.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># setup.py</span>
<span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
<span>from</span> <span>setuptools</span> <span>import</span> <span>find_namespace_packages</span><span>,</span> <span>setup</span>
</code></pre></div></td></tr></tbody></table>

We'll start by extracting the require packaged from `requirements.txt`:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Load packages from requirements.txt</span>
<span>BASE_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>__file__</span><span>)</span><span>.</span><span>parent</span>
<span>with</span> <span>open</span><span>(</span><span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"requirements.txt"</span><span>),</span> <span>"r"</span><span>)</span> <span>as</span> <span>file</span><span>:</span>
    <span>required_packages</span> <span>=</span> <span>[</span><span>ln</span><span>.</span><span>strip</span><span>()</span> <span>for</span> <span>ln</span> <span>in</span> <span>file</span><span>.</span><span>readlines</span><span>()]</span>
</code></pre></div></td></tr></tbody></table>

The heart of the `setup.py` file is the `setup` object which describes how to set up our package and it's dependencies. Our package will be called `tagifai` and it will encompass all the requirements needed to run it. The first several lines cover [metadata](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#metadata) (name, description, etc.) and then we define the requirements. Here we're stating that we require a Python version equal to or above 3.7 and then passing in our required packages to `install_requires`.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># setup.py</span>
<span>setup</span><span>(</span>
    <span>name</span><span>=</span><span>"tagifai"</span><span>,</span>
    <span>version</span><span>=</span><span>0.1</span><span>,</span>
    <span>description</span><span>=</span><span>"Classify machine learning projects."</span><span>,</span>
    <span>author</span><span>=</span><span>"Goku Mohandas"</span><span>,</span>
    <span>author_email</span><span>=</span><span>"goku@madewithml.com"</span><span>,</span>
    <span>url</span><span>=</span><span>"https://madewithml.com/"</span><span>,</span>
    <span>python_requires</span><span>=</span><span>"&gt;=3.7"</span><span>,</span>
    <span>install_requires</span><span>=</span><span>[</span><span>required_packages</span><span>],</span>
<span>)</span>
</code></pre></div></td></tr></tbody></table>

View setup.py

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
<span>20</span></pre></div></td><td><div><pre><span></span><code><span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
<span>from</span> <span>setuptools</span> <span>import</span> <span>find_namespace_packages</span><span>,</span> <span>setup</span><span></span>
<span></span>
<span># Load packages from requirements.txt</span>
<span>BASE_DIR</span> <span>=</span> <span>Path</span><span>(</span><span>__file__</span><span>)</span><span>.</span><span>parent</span>
<span>with</span> <span>open</span><span>(</span><span>Path</span><span>(</span><span>BASE_DIR</span><span>,</span> <span>"requirements.txt"</span><span>),</span> <span>"r"</span><span>)</span> <span>as</span> <span>file</span><span>:</span>
    <span>required_packages</span> <span>=</span> <span>[</span><span>ln</span><span>.</span><span>strip</span><span>()</span> <span>for</span> <span>ln</span> <span>in</span> <span>file</span><span>.</span><span>readlines</span><span>()]</span><span></span>
<span></span>
<span># Define our package</span>
<span>setup</span><span>(</span>
    <span>name</span><span>=</span><span>"tagifai"</span><span>,</span>
    <span>version</span><span>=</span><span>0.1</span><span>,</span>
    <span>description</span><span>=</span><span>"Classify machine learning projects."</span><span>,</span>
    <span>author</span><span>=</span><span>"Goku Mohandas"</span><span>,</span>
    <span>author_email</span><span>=</span><span>"goku@madewithml.com"</span><span>,</span>
    <span>url</span><span>=</span><span>"https://madewithml.com/"</span><span>,</span>
    <span>python_requires</span><span>=</span><span>"&gt;=3.7"</span><span>,</span>
    <span>packages</span><span>=</span><span>find_namespace_packages</span><span>(),</span>
    <span>install_requires</span><span>=</span><span>[</span><span>required_packages</span><span>],</span>
<span>)</span>
</code></pre></div></td></tr></tbody></table>

## Usage

We don't have any packages defined in our `requirements.txt` file but if we did, we can use the `setup.py` file, we can now install our packages like so:

```
python3 -m pip install -e .            # installs required packages only

```

```
Obtaining file:///Users/goku/Documents/madewithml/mlops
  Preparing metadata (setup.py) ... done
Installing collected packages: tagifai
  Running setup.py develop for tagifai
Successfully installed tagifai-0.1

```

> The `-e` or `--editable` flag installs a project in develop mode so we can make changes without having to reinstall packages.

现在，如果这样做，`pip freeze`应该看到它`tagifai`已安装。

```
# 没有版本控制的可编辑安装 (tagifai==0.1)
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

setup.py 文件有许多替代品，例如pyproject.toml[`setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)和更新的[pyproject.toml](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)。

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Packaging - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
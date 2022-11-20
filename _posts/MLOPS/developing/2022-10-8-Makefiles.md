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

## 生成文件


## 直觉

尽管只完成了课程的一半，但已经有很多不同的命令需要跟踪。为了帮助组织一切，将使用[`Makefile`](https://opensource.com/article/18/8/what-how-makefile)一个自动化工具来组织命令。将首先在项目的根目录中创建此文件。

在顶部，`Makefile`需要指定希望所有命令在其中执行的 shell 环境：

```
# Makefile
SHELL = /bin/bash

```

## 成分

Inside our [Makefile](https://github.com/GokuMohandas/mlops-course/tree/main/Makefile), we'll be creating a list of rules. These rules have a `target` which can sometimes have `prerequisites` that need to be met (can be other targets) and on the next line a Tab followed by a `recipe` which specifies how to create the target.

```
# Makefile
target: prerequisites
<TAB> recipe

```

For example, if we wanted to create a rule for styling our files, we would add the following to our `Makefile`:

```
# Styling
style:
    black .
    flake8
    python3 -m isort .

```

Tabs vs. spaces

Makefiles require that indention be done with a , instead of spaces where we'll receive an error:

```
Makefile:: *** missing separator.  Stop.

```

Luckily, editors like VSCode automatically change indentation to tabs even if other files use spaces.

## Targets

We can execute any of the rules by typing `make <target>` in the terminal:

```
# Make a target
$ make style

```

```
black .
All done! ✨ 🍰 ✨
8 files left unchanged.
flake8
python3 -m isort .
Skipped 1 files

```

Similarly, we can set up our `Makefile` for creating a virtual environment:

```
# Environment
venv:
    python3 -m venv venv
    source venv/bin/activate && \
    python3 -m pip install pip setuptools wheel && \
    python3 -m pip install -e .

```

> `&&` signifies that we want these commands to execute in one shell (more on this [below](https://madewithml.com/courses/mlops/makefile/#shells)).

## PHONY

A Makefile is called as such because traditionally the `targets` are supposed to be files we can _make_. However, Makefiles are also commonly used as command shortcuts, which can lead to confusion when a Makefile target and a file share the same name! For example if we have a file called `venv` (which we do) and a `target` in your Makefile called `venv`, when you run `make venv` we'll get this message:

```
make: `venv' is up to date.

```

In this situation, this is the intended behavior because if a virtual environment already exists, then we don't want ot _make_ that target again. However, sometimes, we'll name our targets and want them to execute whether it exists as an actual file or not. In these scenarios, we want to define a [`PHONY`](https://www.gnu.org/software/make/manual/make.html#Phony-Targets) target in our makefile by adding this line above the target:

Most of the rules in our Makefile will require the `PHONY` target because we want them to execute even if there is a file sharing the target's name.

```
# Styling
.PHONY: style
style:
    black .
    flake8
    isort .

```

## Prerequisites

Before we make a target, we can attach prerequisites to them. These can either be file targets that must exist or PHONY target commands that need to be executed prior to _making_ this target. For example, we'll set the _style_ target as a prerequisite for the _clean_ target so that all files are formatted appropriately prior to cleaning them.

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

## Variables

We can also set and use [variables](https://www.gnu.org/software/make/manual/make.html#Using-Variables) inside our Makefile to organize all of our rules.

-   We can set the variables directly inside the Makefile. If the variable isn't defined in the Makefile, then it would default to any environment variable with the same name.
    
    ```
    # Set variable
    MESSAGE := "hello world"
    
    # Use variable
    greeting:
        @echo ${MESSAGE}
    
    ```
    
-   We can also use variables passed in when executing the rule like so (ensure that the variable is not overridden inside the Makefile):
    
    ```
    make greeting MESSAGE="hi"
    
    ```
    

## Shells

Each line in a recipe for a rule will execute in a separate sub-shell. However for certain recipes such as activating a virtual environment and loading packages, we want to execute all steps in one shell. To do this, we can add the [`.ONESHELL`](https://www.gnu.org/software/make/manual/make.html#One-Shell) special target above any target.

```
# Environment
.ONESHELL:
venv:
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install pip setuptools wheel
    python3 -m pip install -e .

```

However this is only available in Make version 3.82 and above and most Macs currently use version 3.81. You can either update to the current version or chain your commands with `&&` as we did previously:

```
# Environment
venv:
    python3 -m venv venv
    source venv/bin/activate && \
    python3 -m pip install pip setuptools wheel && \
    python3 -m pip install -e .

```

## Help

The last thing we'll add to our `Makefile` (for now at least) is a `help` target to the very top. This rule will provide an informative message for this Makefile's capabilities:

```
.PHONY: help
help:
    @echo "Commands:"
    @echo "venv    : creates a virtual environment."
    @echo "style   : executes style formatting."
    @echo "clean   : cleans all unnecessary files."

```

```
Commands:
venv    : creates a virtual environment.
style   : executes style formatting.
clean   : cleans all unnecessary files.

```

> Makefile还有很多[其他](https://www.gnu.org/software/make/manual/make.html)功能，但这对于大多数应用的 ML 项目来说已经足够了。

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Makefile - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
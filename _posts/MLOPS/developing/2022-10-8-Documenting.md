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

## 直觉

> 代码告诉你_怎么_做，注释告诉你_为什么_。——[杰夫·阿特伍德](https://en.wikipedia.org/wiki/Jeff_Atwood)

我们可以通过记录代码来进一步[组织](https://madewithml.com/courses/mlops/organization/)我们的代码，让其他人（以及我们未来的自己）更容易轻松地导航和扩展它。我们在完成编写代码库的那一刻就最了解我们的代码库，但幸运的是，记录它将使我们能够快速回到熟悉的心态。文档对开发人员来说可能意味着很多不同的东西，所以让我们定义最常见的组件：

-   `comments`：关于为什么存在一段代码的简短描述。
-   `typing`：函数输入和输出数据类型的规范，提供与函数消耗和产生的内容有关的信息。
-   `docstrings`：对描述整体效用、参数、返回等的函数和类的有意义的描述。
-   `docs`：呈现的网页，总结了所有的功能、类、工作流程、示例等。

> 目前，我们将在本地生成文档，但请务必查看我们[应用程序的自动生成](https://github.com/GokuMohandas/mlops-course)[文档页面](https://gokumohandas.github.io/mlops-course)。每次对代码库进行更改时，我们将在[CI/CD](https://madewithml.com/courses/mlops/cicd/)课程中学习如何自动创建文档并使其保持最新。[](https://github.com/GokuMohandas/mlops-course)[](https://madewithml.com/courses/mlops/cicd/)

代码协作

您目前如何与团队中的其他人共享您的代码？有什么可以改进的？

## 打字

It's important to be as explicit as possible with our code. We've already discussed choosing explicit names for variables, functions, etc. but another way we can be explicit is by defining the types for our function's inputs and outputs.

So far, our functions have looked like this:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>def</span> <span>some_function</span><span>(</span><span>a</span><span>,</span> <span>b</span><span>):</span>
    <span>return</span> <span>c</span>
</code></pre></div></td></tr></tbody></table>

But we can incorporate so much more information using typing:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>typing</span> <span>import</span> <span>List</span>
<span>def</span> <span>some_function</span><span>(</span><span>a</span><span>:</span> <span>List</span><span>,</span> <span>b</span><span>:</span> <span>int</span> <span>=</span> <span>0</span><span>)</span> <span>-&gt;</span> <span>np</span><span>.</span><span>ndarray</span><span>:</span>
    <span>return</span> <span>c</span>
</code></pre></div></td></tr></tbody></table>

Here we've defined:

-   input parameter `a` is a list
-   input parameter `b` is an integer with default value 0
-   output parameter `c` is a NumPy array

There are many other data types that we can work with, including `List`, `Set`, `Dict`, `Tuple`, `Sequence` and [more](https://docs.python.org/3/library/typing.html), as well as included types such as `int`, `float`, etc. You can also use types from packages we install (ex. `np.ndarray`) and even from our own defined classes (ex. `LabelEncoder`).

> Starting from Python 3.9+, common types are [built in](https://docs.python.org/3/whatsnew/3.9.html#type-hinting-generics-in-standard-collections) so we don't need to import them with `from typing import List, Set, Dict, Tuple, Sequence` anymore.

## Docstrings

We can make our code even more explicit by adding docstrings to describe overall utility, arguments, returns, exceptions and more. Let's take a look at an example:

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
<span>25</span></pre></div></td><td><div><pre><span></span><code><span>from</span> <span>typing</span> <span>import</span> <span>List</span>
<span>def</span> <span>some_function</span><span>(</span><span>a</span><span>:</span> <span>List</span><span>,</span> <span>b</span><span>:</span> <span>int</span> <span>=</span> <span>0</span><span>)</span> <span>-&gt;</span> <span>np</span><span>.</span><span>ndarray</span><span>:</span>
    <span>"""Function description.</span><span></span>
<span></span>
<span>    ```python</span>
<span>    c = some_function(a=[], b=0)</span>
<span>    print (c)</span>
<span>    ```</span>
<span>    &lt;pre&gt;</span>
<span>    [[1 2]</span>
<span>     [3 4]]</span>
<span>    &lt;/pre&gt;</span><span></span>
<span></span>
<span>    Args:</span>
<span>        a (List): description of `a`.</span>
<span>        b (int, optional): description of `b`. Defaults to 0.</span><span></span>
<span></span>
<span>    Raises:</span>
<span>        ValueError: Input list is not one-dimensional.</span><span></span>
<span></span>
<span>    Returns:</span>
<span>        np.ndarray: Description of `c`.</span><span></span>
<span></span>
<span>    """</span>
    <span>return</span> <span>c</span>
</code></pre></div></td></tr></tbody></table>

Let's unpack the different parts of this function's docstring:

-   `[Line 3]`: Summary of the overall utility of the function.
-   `[Lines 5-12]`: Example of how to use our function.
-   `[Lines 14-16]`: Description of the function's input arguments.
-   `[Lines 18-19]`: Any exceptions that may be raised in the function.
-   `[Lines 21-22]`: Description of the function's output(s).

We'll render these docstrings in the [docs](https://madewithml.com/courses/mlops/documentation/#docs) section below to produce this:

![文档字符串](https://madewithml.com/static/images/mlops/documentation/docstrings.png)

Take this time to update all the functions and classes in our project with docstrings and be sure to refer to the [repository](https://github.com/GokuMohandas/mlops-course) as a guide. Note that you my have to explicitly import some libraries to certain scripts because the `type` requires it. For example, we don't explicitly use the Pandas library in our `data.py` script, however, we do use pandas dataframes as input arguments.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># tagifai/data.py</span>
<span>import</span> <span>pandas</span> <span>as</span> <span>pd</span>
<span>from</span> <span>typing</span> <span>import</span> <span>List</span><span></span>
<span></span>
<span><span>def</span> <span>replace_oos_labels</span><span>(</span><span>df</span><span>:</span> <span>pd</span><span>.</span><span>DataFrame</span><span>,</span> <span>labels</span><span>:</span> <span>List</span><span>,</span> <span>label_col</span><span>:</span> <span>str</span><span>,</span> <span>oos_label</span><span>:</span> <span>str</span> <span>=</span> <span>"other"</span><span>):</span>
</span>    <span>...</span>
</code></pre></div></td></tr></tbody></table>

> Ideally we would add docstrings to our functions and classes as we develop them, as opposed to doing it all at once at the end.

Tip

If using [Visual Studio Code](https://code.visualstudio.com/), be sure to use the [Python Docstrings Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension so you can type `"""` under a function and then hit the Shift key to generate a template docstring. It will autofill parts of the docstring using the typing information and even exception in your code!

![vscode 文档字符串生成](https://github.com/NilsJPWerner/autoDocstring/blob/13875f7e5d3a2ad2a2a7e42bad6a10d09fed7472/images/demo.gif?raw=true)

## Docs

So we're going through all this effort of including typing and docstrings to our functions but it's all tucked away inside our scripts. What if we can collect all this effort and **automatically** surface it as documentation? Well that's exactly what we'll do with the following open-source packages → final result [here](https://gokumohandas.github.io/mlops-course).

1.  Install required packages:
    
    ```
    pip install mkdocs==1.3.0 mkdocstrings==0.18.1
    
    ```
    
    Instead of directly adding these requirements to our `requirements.txt` file, we're going to isolate it from our core required libraries. We want to do this because not everyone will need to create documentation as it's not a core machine learning operation (training, inference, etc.). We'll tweak our `setup.py` script to make this possible. We'll define these packages under a `docs_packages` object:
    
    ```
    # setup.py
    docs_packages = [
        "mkdocs==1.3.0",
        "mkdocstrings==0.18.1"
    ]
    
    ```
    
    and then we'll add this to `setup()` object in the script:
    
    <table><tbody><tr><td></td><td><div><pre><span></span><code><span># Define our package</span>
    <span>setup</span><span>(</span>
        <span>...</span>
        <span>install_requires</span><span>=</span><span>[</span><span>required_packages</span><span>],</span>
    <span>    <span>extras_require</span><span>=</span><span>{</span>
    </span><span>        <span>"dev"</span><span>:</span> <span>docs_packages</span><span>,</span>
    </span><span>        <span>"docs"</span><span>:</span> <span>docs_packages</span><span>,</span>
    </span><span>    <span>},</span>
    </span><span>)</span>
    </code></pre></div></td></tr></tbody></table>
    
    Now we can install this package with:
    
    ```
    python3 -m pip install -e ".[docs]"
    
    ```
    
    We're also defining a `dev` option which we'll update over the course so that developers can install all required and extra packages in one call, instead of calling each extra required packages one at a time.
    
    ```
    python3 -m pip install -e ".[dev]"
    
    ```
    
    We created an explicit `doc` option because a user will want to only download the documentation packages to generate documentation (none of the other packages will be required). We'll see this in action when we use [CI/CD workflows](https://madewithml.com/courses/mlops/cicd/) to autogenerate documentation via GitHub Actions.
2.  Initialize mkdocs
    
    This will create the following files:
    
    ```
    .
    ├─ docs/
    │  └─ index.md
    └─ mkdocs.yml
    
    ```
    
3.  We'll start by overwriting the default `index.md` file in our `docs` directory with information specific to our project:
    
    | 
    index.md
    
     |
    | --- |
    | 
    
    ```
     1
     2
     3
     4
     5
     6
     7
     8
     9
    10
    11
    ```
    
    
    
     | 
    
    ```
    ## Documentation
    
    - [Workflows](tagifai/main.md): main workflows.
    - [tagifai](tagifai/data.md): documentation of functionality.
    
    ## MLOps Lessons
    
    Learn how to combine machine learning with software engineering to build production-grade applications.
    
    - Lessons: [https://madewithml.com/](https://madewithml.com/#mlops)
    - Code: [GokuMohandas/mlops-course](https://github.com/GokuMohandas/mlops-course)
    
    ```
    
    
    
     |
    
4.  Next we'll create documentation files for each script in our `tagifai` directory:
    
    ```
    mkdir docs/tagifai
    cd docs/tagifai
    touch main.md utils.md data.md train.md evaluate.md predict.md
    cd ../../
    
    ```
    
    > It's helpful to have the `docs` directory structure mimic our project's structure as much as possible. This becomes even more important as we document more directories in future lessons.
    
5.  Next we'll add `tagifai.<SCRIPT_NAME>` to each file under `docs/tagifai`. This will populate the file with information about the functions and classes (using their docstrings) from `tagifai/<SCRIPT_NAME>.py` thanks to the `mkdocstrings` plugin.
    
    > Be sure to check out the complete list of [mkdocs plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins).
    > 
    > ```
    > # docs/tagifai/data.md
    > ::: tagifai.data
    > 
    > ```
    
6.  Finally, we'll add some configurations to our `mkdocs.yml` file that mkdocs automatically created:
    
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
    
7.  Serve our documentation locally:
    

## Publishing

We can easily serve our documentation for free using [GitHub pages](https://www.mkdocs.org/user-guide/deploying-your-docs/) for public repositories as wells as [private documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site) for private repositories. And we can even host it on a [custom domain](https://docs.github.com/en/github/working-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site) (ex. company's subdomain).

> Be sure to check out the auto-generated [documentation page](https://gokumohandas.github.io/mlops-course) for our [application](https://github.com/GokuMohandas/mlops-course). We'll learn how to automatically create and keep our docs up-to-date in our [CI/CD](https://madewithml.com/courses/mlops/cicd/) lesson every time we make changes to our code base.

___

To cite this content, please use:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Documentation - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
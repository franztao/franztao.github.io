---
layout:     post
title:      测试机器学习系统：代码、数据和模型
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Testing Machine Learning Systems: Code, Data and Models

---

## 直觉

在本课中，将学习如何测试代码、数据和模型，以构建可以可靠迭代的机器学习系统。测试是确保某些东西按预期工作的一种方式。被激励在开发周期中尽早实施测试并发现错误来源，以便可以降低[下游成本](https://assets.deepsource.io/39ed384/images/blog/cost-of-fixing-bugs/chart.jpg)和浪费时间。一旦设计了测试，可以在每次更改或添加到代码库时自动执行它们。

tip

强烈建议您在完成之前的课程_后_探索本课程，因为主题（和代码）是迭代开发的。但是，确实创建了 [testing-ml](https://github.com/GokuMohandas/testing-ml)存储库，可通过交互式note本快速概览。

### 测试类型

在开发周期的不同阶段使用了四种主要类型的测试：

1.  `Unit tests`：对每个具有[单一职责](https://en.wikipedia.org/wiki/Single-responsibility_principle)的单个组件进行测试（例如过滤列表的功能）。
2.  `Integration tests`：测试单个组件的组合功能（例如数据处理）。
3.  `System tests`：对给定输入（例如训练、推理等）的预期输出的系统设计进行测试。
4.  `Acceptance tests`：用于验证是否满足要求的测试，通常称为用户验收测试 (UAT)。
5.  `Regression tests`：基于之前看到的错误的测试，以确保新的更改不会重新引入它们。

虽然 ML 系统本质上是概率性的，但它们由许多确定性组件组成，可以以与传统软件系统类似的方式进行测试。当从测试代码转向测试[数据](https://madewithml.com/courses/mlops/testing//./#data)和[模型](https://madewithml.com/courses/mlops/testing//./#models)时，测试 ML 系统之间的区别就开始了。

![测试类型](https://madewithml.com/static/images/mlops/testing/tests.png)

> 还有许多其他类型的功能和非功能测试，例如冒烟测试（快速健康检查）、性能测试（负载、压力）、安全测试等，但可以在上面的系统测试中概括所有这些.

### 应该如何测试？

编写测试时使用的框架是[Arrange Act Assert](http://wiki.c2.com/?ArrangeActAssert)方法。

-   `Arrange`：设置不同的输入进行测试。
-   `Act`：将输入应用到要测试的组件上。
-   `Assert`：确认收到了预期的输出。

> `Cleaning`是此方法的非官方第四步，因为重要的是不要留下可能影响后续测试的先前测试的残留物。可以使用[pytest-randomly](https://github.com/pytest-dev/pytest-randomly)等包通过随机执行测试来测试状态依赖性。

在 Python 中，有许多工具，例如[unittest](https://docs.python.org/3/library/unittest.html)、[pytest](https://docs.pytest.org/en/stable/)等，可以让在遵守_Arrange Act Assert_框架的同时轻松实现测试。这些工具具有强大的内置功能，例如参数化、过滤器等，可以大规模测试许多条件。

### 应该测试什么？

在_安排_输入和_断言_预期输出时，应该测试输入和输出的哪些方面？

-   **输入**：数据类型、格式、长度、边缘情况（最小/最大、小/大等）
-   **输出**：数据类型、格式、异常、中间和最终输出

> [👉 将在下面介绍与数据](https://madewithml.com/courses/mlops/testing//./#data)和[模型](https://madewithml.com/courses/mlops/testing//./#models)有关的测试内容的具体细节。

## 最佳实践

不管使用什么框架，将测试与开发过程紧密结合是很重要的。

-   `atomic`：在创建函数和类时，需要确保它们具有[单一的职责](https://en.wikipedia.org/wiki/Single-responsibility_principle)，以便可以轻松地测试它们。如果没有，需要将它们拆分成更细粒度的组件。
-   `compose`：当创建新组件时，希望编写测试来验证它们的功能。这是确保可靠性和及早发现错误的好方法。
-   `reuse`：应该维护中央存储库，其中核心功能在源头进行测试并在许多项目中重用。这显着减少了每个新项目代码库的测试工作量。
-   `regression`：想解释回归测试中遇到的新错误，这样就可以确保将来不会重新引入相同的错误。
-   `coverage`：希望确保代码库[100% 覆盖](https://madewithml.com/courses/mlops/testing//#coverage)。这并不意味着要为每一行代码编写测试，而是要考虑每一行代码。
-   `automate`：如果忘记在提交到存储库之前运行测试，希望在对代码库进行更改时自动运行测试。将在后续课程中学习如何使用[预提交挂钩在本地执行此操作，并通过](https://madewithml.com/courses/mlops/testing//../pre-commit/)[GitHub 操作](https://madewithml.com/courses/mlops/testing//../cicd/#github-actions)远程执行此操作。

## 测试驱动开发

[测试驱动开发 (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)是在编写功能之前编写测试以确保始终编写测试的过程。这与先编写功能然后再编写测试形成对比。以下是对此的看法：

-   随着进步编写测试很好，但这确实意味着 100% 的正确性。
-   在进入代码或测试之前，最初的时间应该花在设计上。

如果这些测试没有意义并且不包含可能的输入、中间体和输出的领域，那么完美的覆盖并不意味着应用程序没有错误。因此，应该在面临错误时朝着更好的设计和敏捷性努力，快速解决它们并围绕它们编写测试用例以避免下一次。

## 应用

在[应用程序](https://github.com/GokuMohandas/mlops-course)中，将测试代码、数据和模型。将首先创建一个`tests`带有`code`子目录的单独目录来测试`tagifai`脚本。将在下面创建用于测试[数据](https://madewithml.com/courses/mlops/testing//#🔢nbsp-data)和[模型](https://madewithml.com/courses/mlops/testing//#🤖nbsp-models)的子目录。

```
mkdir tests
cd tests
mkdir app config model tagifai
touch <SCRIPTS>
cd ../

```

```
tests/
└── code/
│   ├── test_data.py
│   ├── test_evaluate.py
│   ├── test_main.py
│   ├── test_predict.py
│   └── test_utils.py

```

在学习了本课中的所有概念_后_，请随意编写测试并将它们组织在这些脚本中。建议使用[`tests`](https://github.com/GokuMohandas/mlops-course/tree/main/tests)在 GitHub 上的目录作为参考。

> 请注意，`tagifai/train.py`脚本没有相应的`tests/code/test_train.py`. 一些脚本具有带有依赖项（例如工件）的大型函数（例如`train.train()`、`train.optimize()`、等），通过.`predict.predict()``tests/code/test_main.py`

## 🧪 Pytest

将使用[pytest](https://docs.pytest.org/en/stable/)作为测试框架，因为它具有强大的内置功能，例如[参数化](https://madewithml.com/courses/mlops/testing//#parametrize)、[固定装置](https://madewithml.com/courses/mlops/testing//#fixtures)、[标记](https://madewithml.com/courses/mlops/testing//#markers)等。

```
pip install pytest==7.1.2

```

由于这个测试包不是核心机器学习操作的组成部分，让在中创建一个单独的列表`setup.py`并将其添加到`extras_require`：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">13 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">14</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_4"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_4 > code"></button><code><span class="c1"># setup.py</span>
<span class="n">test_packages</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s2">"pytest==7.1.2"</span><span class="p">,</span>
<span class="p">]</span><font></font>
<font></font>
<span class="c1"># Define our package</span>
<span class="n">setup</span><span class="p">(</span>
    <span class="o">...</span>
    <span class="n">extras_require</span><span class="o">=</span><span class="p">{</span>
<span class="hll">        <span class="s2">"dev"</span><span class="p">:</span> <span class="n">docs_packages</span> <span class="o">+</span> <span class="n">style_packages</span> <span class="o">+</span> <span class="n">test_packages</span><span class="p">,</span>
</span>        <span class="s2">"docs"</span><span class="p">:</span> <span class="n">docs_packages</span><span class="p">,</span>
        <span class="s2">"test"</span><span class="p">:</span> <span class="n">test_packages</span><span class="p">,</span>
    <span class="p">},</span>
<span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

创建了一个明确的`test`选项，因为用户只想下载测试包。[当使用CI/CD 工作流](https://madewithml.com/courses/mlops/testing//../cicd/)通过 GitHub Actions 运行测试时，将看到这一点。

### 配置

Pytest 期望测试在`tests`默认情况下组织在一个目录下。但是，也可以添加到现有`pyproject.toml`文件中以配置任何其他测试目录。进入目录后，pytest 会查找以 开头的 python 脚本，`tests_*.py`但也可以将其配置为读取任何其他文件模式。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_5"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_5 > code"></button><code><span class="c1"># Pytest</span><span class="w"></span>
<span class="k">[tool.pytest.ini_options]</span><span class="w"></span>
<span class="n">testpaths</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="p">[</span><span class="s">"tests"</span><span class="p">]</span><span class="w"></span>
<span class="n">python_files</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="s">"test_*.py"</span><span class="w"></span>
</code></pre></div></td></tr></tbody></table>

### 断言

让看看样本测试及其结果是什么样的。假设有一个简单的函数来确定水果是否脆：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_6"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_6 > code"></button><code><span class="c1"># food/fruits.py</span>
<span class="k">def</span> <span class="nf">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">fruit</span><span class="p">:</span>
        <span class="n">fruit</span> <span class="o">=</span> <span class="n">fruit</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
    <span class="k">if</span> <span class="n">fruit</span> <span class="ow">in</span> <span class="p">[</span><span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"watermelon"</span><span class="p">,</span> <span class="s2">"cherries"</span><span class="p">]:</span>
        <span class="k">return</span> <span class="kc">True</span>
    <span class="k">elif</span> <span class="n">fruit</span> <span class="ow">in</span> <span class="p">[</span><span class="s2">"orange"</span><span class="p">,</span> <span class="s2">"mango"</span><span class="p">,</span> <span class="s2">"strawberry"</span><span class="p">]:</span>
        <span class="k">return</span> <span class="kc">False</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="sa">f</span><span class="s2">"</span><span class="si">{</span><span class="n">fruit</span><span class="si">}</span><span class="s2"> not in known list of fruits."</span><span class="p">)</span>
    <span class="k">return</span> <span class="kc">False</span>
</code></pre></div></td></tr></tbody></table>

为了测试这个功能，可以使用[断言语句](https://docs.pytest.org/en/stable/assert.html)来映射输入和预期的输出。单词后面的语句`assert`必须返回 True。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_7"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_7 > code"></button><code><span class="c1"># tests/food/test_fruits.py</span>
<span class="k">def</span> <span class="nf">test_is_crisp</span><span class="p">():</span>
    <span class="k">assert</span> <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="s2">"apple"</span><span class="p">)</span>
    <span class="k">assert</span> <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="s2">"Apple"</span><span class="p">)</span>
    <span class="k">assert</span> <span class="ow">not</span> <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="s2">"orange"</span><span class="p">)</span>
    <span class="k">with</span> <span class="n">pytest</span><span class="o">.</span><span class="n">raises</span><span class="p">(</span><span class="ne">ValueError</span><span class="p">):</span>
        <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="kc">None</span><span class="p">)</span>
        <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="s2">"pear"</span><span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

> 还可以对[异常](https://docs.pytest.org/en/stable/assert.html#assertions-about-expected-exceptions)进行断言，就像在第 6-8 行中所做的那样，其中 with 语句下的所有操作都应该引发指定的异常。

`assert`在项目中使用的例子

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><code><span class="c1"># tests/code/test_evaluate.py</span>
<span class="k">def</span> <span class="nf">test_get_metrics</span><span class="p">():</span>
    <span class="n">y_true</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">])</span>
    <span class="n">y_pred</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">])</span>
    <span class="n">classes</span> <span class="o">=</span> <span class="p">[</span><span class="s2">"a"</span><span class="p">,</span> <span class="s2">"b"</span><span class="p">]</span>
    <span class="n">performance</span> <span class="o">=</span> <span class="n">evaluate</span><span class="o">.</span><span class="n">get_metrics</span><span class="p">(</span><span class="n">y_true</span><span class="o">=</span><span class="n">y_true</span><span class="p">,</span> <span class="n">y_pred</span><span class="o">=</span><span class="n">y_pred</span><span class="p">,</span> <span class="n">classes</span><span class="o">=</span><span class="n">classes</span><span class="p">,</span> <span class="n">df</span><span class="o">=</span><span class="kc">None</span><span class="p">)</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"overall"</span><span class="p">][</span><span class="s2">"precision"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">2</span><span class="o">/</span><span class="mi">4</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"overall"</span><span class="p">][</span><span class="s2">"recall"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">2</span><span class="o">/</span><span class="mi">4</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"class"</span><span class="p">][</span><span class="s2">"a"</span><span class="p">][</span><span class="s2">"precision"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">1</span><span class="o">/</span><span class="mi">2</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"class"</span><span class="p">][</span><span class="s2">"a"</span><span class="p">][</span><span class="s2">"recall"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">1</span><span class="o">/</span><span class="mi">2</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"class"</span><span class="p">][</span><span class="s2">"b"</span><span class="p">][</span><span class="s2">"precision"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">1</span><span class="o">/</span><span class="mi">2</span>
    <span class="k">assert</span> <span class="n">performance</span><span class="p">[</span><span class="s2">"class"</span><span class="p">][</span><span class="s2">"b"</span><span class="p">][</span><span class="s2">"recall"</span><span class="p">]</span> <span class="o">==</span> <span class="mi">1</span><span class="o">/</span><span class="mi">2</span>
</code></pre></div></td></tr></tbody></table>

### 执行

可以使用几个不同的粒度级别执行上面的测试：

```
python3 -m pytest                                           # all tests
python3 -m pytest tests/food                                # tests under a directory
python3 -m pytest tests/food/test_fruits.py                 # tests for a single file
python3 -m pytest tests/food/test_fruits.py::test_is_crisp  # tests for a single function

```

在上面运行特定测试将产生以下输出：

```
python3 -m pytest tests/food/test_fruits.py::test_is_crisp

```

```
测试/食物/test_fruits.py::test_is_crisp 。[100%]

```

如果在此测试中的任何断言失败，将看到失败的断言，以及函数的预期和实际输出。

```
测试/食物/test_fruits.py F [100%]

    def test_is_crisp():
> 断言 is_crisp(水果="橙色")
E AssertionError: assert False 
E + where False = is_crisp(fruit='orange')

```

tip

重要的是要测试[上面](https://madewithml.com/courses/mlops/testing//#how-should-we-test)概述的各种输入和预期输出，并且**永远不要假设测试是微不足道的**。在上面的例子中，如果函数没有考虑大小写，测试“apple”和“Apple”是很重要的！

### 课程

还可以通过创建测试类来测试类及其各自的功能。在测试类中，可以选择定义在设置或拆除类实例或使用类方法时自动执行的[函数。](https://docs.pytest.org/en/stable/xunit_setup.html)

-   `setup_class`：为任何类实例设置状态。
-   `teardown_class`: 拆除 setup\_class 中创建的状态。
-   `setup_method`：在每个方法之前调用以设置任何状态。
-   `teardown_method`：在每个方法之后调用以拆除任何状态。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">13 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">14 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">15 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">16 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">17 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">18 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">19 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">20 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">21 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">22 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">23 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">24 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">25</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_10"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_10 > code"></button><code><span class="k">class</span> <span class="nc">Fruit</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span><font></font>
<font></font>
<span class="k">class</span> <span class="nc">TestFruit</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="nd">@classmethod</span>
    <span class="k">def</span> <span class="nf">setup_class</span><span class="p">(</span><span class="bp">cls</span><span class="p">):</span>
        <span class="sd">"""Set up the state for any class instance."""</span>
        <span class="k">pass</span><font></font>
<font></font>
    <span class="nd">@classmethod</span>
    <span class="k">def</span> <span class="nf">teardown_class</span><span class="p">(</span><span class="bp">cls</span><span class="p">):</span>
        <span class="sd">"""Teardown the state created in setup_class."""</span>
        <span class="k">pass</span><font></font>
<font></font>
    <span class="k">def</span> <span class="nf">setup_method</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">"""Called before every method to setup any state."""</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">fruit</span> <span class="o">=</span> <span class="n">Fruit</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s2">"apple"</span><span class="p">)</span><font></font>
<font></font>
    <span class="k">def</span> <span class="nf">teardown_method</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">"""Called after every method to teardown any state."""</span>
        <span class="k">del</span> <span class="bp">self</span><span class="o">.</span><span class="n">fruit</span><font></font>
<font></font>
    <span class="k">def</span> <span class="nf">test_init</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">assert</span> <span class="bp">self</span><span class="o">.</span><span class="n">fruit</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s2">"apple"</span>
</code></pre></div></td></tr></tbody></table>

可以通过指定类名来为类执行所有测试：

```
python3 -m pytest tests/food/test_fruits.py::TestFruit

```

```
测试/食物/test_fruits.py::TestFruit 。[100%]

```

`class`在项目中测试 a 的示例

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">13 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">14 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">15 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">16 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">17 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">18 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">19 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">20 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">21 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">22 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">23 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">24 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">25 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">26 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">27 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">28 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">29 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">30 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">31 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">32 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">33 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">34 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">35 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">36 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">37 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">38 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">39 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">40 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">41 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">42 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">43 </font></font></span>
<font style="vertical-align: inherit;"><span class="normal"><font style="vertical-align: inherit;">48 </font></span><span class="normal"><font style="vertical-align: inherit;">49 </font></span></font><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">45 </font></font></span>
<font style="vertical-align: inherit;"><span class="normal"><font style="vertical-align: inherit;">7 </font></span><span class="normal"><font style="vertical-align: inherit;">_ </font></span><span class="normal"><font style="vertical-align: inherit;">_ </font></span><span class="normal"><font style="vertical-align: inherit;">_ </font></span><span class="normal"><font style="vertical-align: inherit;">51 </font></span><span class="normal"><font style="vertical-align: inherit;">52 </font></span><span class="normal"><font style="vertical-align: inherit;">53 </font></span><span class="normal"><font style="vertical-align: inherit;">54 </font></span><span class="normal"><font style="vertical-align: inherit;">55 </font></span><span class="normal"><font style="vertical-align: inherit;">56 </font></span><span class="normal"><font style="vertical-align: inherit;">57</font></span></font><span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">58 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">59</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><code><span class="c1"># tests/code/test_data.py</span>
<span class="k">class</span> <span class="nc">TestLabelEncoder</span><span class="p">:</span>
<span class="nd">@classmethod</span>
<span class="k">def</span> <span class="nf">setup_class</span><span class="p">(</span><span class="bp">cls</span><span class="p">):</span>
    <span class="sd">"""Called before every class initialization."""</span>
    <span class="k">pass</span><font></font>
<font></font>
<span class="nd">@classmethod</span>
<span class="k">def</span> <span class="nf">teardown_class</span><span class="p">(</span><span class="bp">cls</span><span class="p">):</span>
    <span class="sd">"""Called after every class initialization."""</span>
    <span class="k">pass</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">setup_method</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="sd">"""Called before every method."""</span>
    <span class="bp">self</span><span class="o">.</span><span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">()</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">teardown_method</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="sd">"""Called after every method."""</span>
    <span class="k">del</span> <span class="bp">self</span><span class="o">.</span><span class="n">label_encoder</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_empty_init</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">()</span>
    <span class="k">assert</span> <span class="n">label_encoder</span><span class="o">.</span><span class="n">index_to_class</span> <span class="o">==</span> <span class="p">{}</span>
    <span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">classes</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_dict_init</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="n">class_to_index</span> <span class="o">=</span> <span class="p">{</span><span class="s2">"apple"</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span> <span class="s2">"banana"</span><span class="p">:</span> <span class="mi">1</span><span class="p">}</span>
    <span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">(</span><span class="n">class_to_index</span><span class="o">=</span><span class="n">class_to_index</span><span class="p">)</span>
    <span class="k">assert</span> <span class="n">label_encoder</span><span class="o">.</span><span class="n">index_to_class</span> <span class="o">==</span> <span class="p">{</span><span class="mi">0</span><span class="p">:</span> <span class="s2">"apple"</span><span class="p">,</span> <span class="mi">1</span><span class="p">:</span> <span class="s2">"banana"</span><span class="p">}</span>
    <span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">classes</span><span class="p">)</span> <span class="o">==</span> <span class="mi">2</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_len</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">label_encoder</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_save_and_load</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="k">with</span> <span class="n">tempfile</span><span class="o">.</span><span class="n">TemporaryDirectory</span><span class="p">()</span> <span class="k">as</span> <span class="n">dp</span><span class="p">:</span>
        <span class="n">fp</span> <span class="o">=</span> <span class="n">Path</span><span class="p">(</span><span class="n">dp</span><span class="p">,</span> <span class="s2">"label_encoder.json"</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">fp</span><span class="o">=</span><span class="n">fp</span><span class="p">)</span>
        <span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">fp</span><span class="o">=</span><span class="n">fp</span><span class="p">)</span>
        <span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">classes</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_str</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="k">assert</span> <span class="nb">str</span><span class="p">(</span><span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">())</span> <span class="o">==</span> <span class="s2">"&lt;LabelEncoder(num_classes=0)&gt;"</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_fit</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">()</span>
    <span class="n">label_encoder</span><span class="o">.</span><span class="n">fit</span><span class="p">([</span><span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"banana"</span><span class="p">])</span>
    <span class="k">assert</span> <span class="s2">"apple"</span> <span class="ow">in</span> <span class="n">label_encoder</span><span class="o">.</span><span class="n">class_to_index</span>
    <span class="k">assert</span> <span class="s2">"banana"</span> <span class="ow">in</span> <span class="n">label_encoder</span><span class="o">.</span><span class="n">class_to_index</span>
    <span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">classes</span><span class="p">)</span> <span class="o">==</span> <span class="mi">2</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_encode_decode</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="n">class_to_index</span> <span class="o">=</span> <span class="p">{</span><span class="s2">"apple"</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span> <span class="s2">"banana"</span><span class="p">:</span> <span class="mi">1</span><span class="p">}</span>
    <span class="n">y_encoded</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">]</span>
    <span class="n">y_decoded</span> <span class="o">=</span> <span class="p">[</span><span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"banana"</span><span class="p">]</span>
    <span class="n">label_encoder</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">(</span><span class="n">class_to_index</span><span class="o">=</span><span class="n">class_to_index</span><span class="p">)</span>
    <span class="n">label_encoder</span><span class="o">.</span><span class="n">fit</span><span class="p">([</span><span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"apple"</span><span class="p">,</span> <span class="s2">"banana"</span><span class="p">])</span>
    <span class="k">assert</span> <span class="n">np</span><span class="o">.</span><span class="n">array_equal</span><span class="p">(</span><span class="n">label_encoder</span><span class="o">.</span><span class="n">encode</span><span class="p">(</span><span class="n">y_decoded</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">y_encoded</span><span class="p">))</span>
    <span class="k">assert</span> <span class="n">label_encoder</span><span class="o">.</span><span class="n">decode</span><span class="p">(</span><span class="n">y_encoded</span><span class="p">)</span> <span class="o">==</span> <span class="n">y_decoded</span>
</code></pre></div></td></tr></tbody></table>

### 参数化

到目前为止，在测试中，必须创建单独的断言语句来验证输入和预期输出的不同组合。然而，这里有一点冗余，因为输入总是作为参数输入到函数中，并且输出与预期输出进行比较。为了消除这种冗余，pytest 有一个[`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/parametrize.html)装饰器，它允许将输入和输出表示为参数。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_12"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_12 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"fruit, crisp"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span><span class="s2">"apple"</span><span class="p">,</span> <span class="kc">True</span><span class="p">),</span>
        <span class="p">(</span><span class="s2">"Apple"</span><span class="p">,</span> <span class="kc">True</span><span class="p">),</span>
        <span class="p">(</span><span class="s2">"orange"</span><span class="p">,</span> <span class="kc">False</span><span class="p">),</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_is_crisp_parametrize</span><span class="p">(</span><span class="n">fruit</span><span class="p">,</span> <span class="n">crisp</span><span class="p">):</span>
    <span class="k">assert</span> <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="n">fruit</span><span class="p">)</span> <span class="o">==</span> <span class="n">crisp</span>
</code></pre></div></td></tr></tbody></table>

```
python3 -m pytest 测试/食物/test_is_crisp_parametrize.py ...    [100%]

```

1.  `[Line 2]`：定义装饰器下的参数名称，例如。“fruit, crisp”（注意这是一个字符串）。
2.  `[Lines 3-7]`：提供步骤 1 中参数的值组合列表。
3.  `[Line 9]`：将参数名称传递给测试函数。
4.  `[Line 10]`：包括必要的断言语句，这些语句将为步骤 2 中列表中的每个组合执行。

同样，也可以传入一个异常作为预期结果：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_13"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_13 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"fruit, exception"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span><span class="s2">"pear"</span><span class="p">,</span> <span class="ne">ValueError</span><span class="p">),</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_is_crisp_exceptions</span><span class="p">(</span><span class="n">fruit</span><span class="p">,</span> <span class="n">exception</span><span class="p">):</span>
    <span class="k">with</span> <span class="n">pytest</span><span class="o">.</span><span class="n">raises</span><span class="p">(</span><span class="n">exception</span><span class="p">):</span>
        <span class="n">is_crisp</span><span class="p">(</span><span class="n">fruit</span><span class="o">=</span><span class="n">fruit</span><span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

`parametrize`项目中的示例

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">13 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">14 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">15 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">16 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">17 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">18 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">19 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">20</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><code><span class="c1"># tests/code/test_data.py</span>
<span class="kn">from</span> <span class="nn">tagifai</span> <span class="kn">import</span> <span class="n">data</span>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"text, lower, stem, stopwords, cleaned_text"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span><span class="s2">"Hello worlds"</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="p">[],</span> <span class="s2">"Hello worlds"</span><span class="p">),</span>
        <span class="p">(</span><span class="s2">"Hello worlds"</span><span class="p">,</span> <span class="kc">True</span><span class="p">,</span> <span class="kc">False</span><span class="p">,</span> <span class="p">[],</span> <span class="s2">"hello worlds"</span><span class="p">),</span>
        <span class="o">...</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_preprocess</span><span class="p">(</span><span class="n">text</span><span class="p">,</span> <span class="n">lower</span><span class="p">,</span> <span class="n">stem</span><span class="p">,</span> <span class="n">stopwords</span><span class="p">,</span> <span class="n">cleaned_text</span><span class="p">):</span>
    <span class="k">assert</span> <span class="p">(</span>
        <span class="n">data</span><span class="o">.</span><span class="n">clean_text</span><span class="p">(</span>
            <span class="n">text</span><span class="o">=</span><span class="n">text</span><span class="p">,</span>
            <span class="n">lower</span><span class="o">=</span><span class="n">lower</span><span class="p">,</span>
            <span class="n">stem</span><span class="o">=</span><span class="n">stem</span><span class="p">,</span>
            <span class="n">stopwords</span><span class="o">=</span><span class="n">stopwords</span><span class="p">,</span>
        <span class="p">)</span>
        <span class="o">==</span> <span class="n">cleaned_text</span>
    <span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

### 夹具

参数化允许减少测试函数内部的冗余，但是如何减少不同测试函数之间的冗余呢？例如，假设不同的函数都有一个数据框作为输入。在这里，可以使用pytest的内置[fixture](https://docs.pytest.org/en/stable/fixture.html)，它是一个在test函数之前执行的函数。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_14"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_14 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">fixture</span>
<span class="k">def</span> <span class="nf">my_fruit</span><span class="p">():</span>
    <span class="n">fruit</span> <span class="o">=</span> <span class="n">Fruit</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="s2">"apple"</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">fruit</span><font></font>
<font></font>
<span class="k">def</span> <span class="nf">test_fruit</span><span class="p">(</span><span class="n">my_fruit</span><span class="p">):</span>
    <span class="k">assert</span> <span class="n">my_fruit</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s2">"apple"</span>
</code></pre></div></td></tr></tbody></table>

> 请注意，fixture 的名称和 test 函数的输入是相同的 ( `my_fruit`)。

也可以将fixture 应用到类中，当调用类中的任何方法时都会调用fixture 函数。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_15"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_15 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">usefixtures</span><span class="p">(</span><span class="s2">"my_fruit"</span><span class="p">)</span>
<span class="k">class</span> <span class="nc">TestFruit</span><span class="p">:</span>
    <span class="o">...</span>
</code></pre></div></td></tr></tbody></table>

`fixtures`项目中的示例

In our project, we use fixtures to efficiently pass a set of inputs (ex. Pandas DataFrame) to different testing functions that require them (cleaning, splitting, etc.).

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"> 1</span>
<span class="normal"> 2</span>
<span class="normal"> 3</span>
<span class="normal"> 4</span>
<span class="normal"> 5</span>
<span class="normal"> 6</span>
<span class="normal"> 7</span>
<span class="normal"> 8</span>
<span class="normal"> 9</span>
<span class="normal">10</span>
<span class="normal">11</span>
<span class="normal">12</span>
<span class="normal">13</span>
<span class="normal">14</span>
<span class="normal">15</span>
<span class="normal">16</span>
<span class="normal">17</span>
<span class="normal">18</span>
<span class="normal">19</span>
<span class="normal">20</span>
<span class="normal">21</span>
<span class="normal">22</span>
<span class="normal">23</span>
<span class="normal">24</span>
<span class="normal">25</span>
<span class="normal">26</span>
<span class="normal">27</span>
<span class="normal">28</span>
<span class="normal">29</span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><code><span class="c1"># tests/code/test_data.py</span>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">fixture</span><span class="p">(</span><span class="n">scope</span><span class="o">=</span><span class="s2">"module"</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">df</span><span class="p">():</span>
    <span class="n">data</span> <span class="o">=</span> <span class="p">[</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a0"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b0"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c0"</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a1"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b1"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c1"</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a2"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b2"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c1"</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a3"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b3"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c2"</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a4"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b4"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c2"</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="s2">"a5"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"b5"</span><span class="p">,</span> <span class="s2">"tag"</span><span class="p">:</span> <span class="s2">"c2"</span><span class="p">},</span>
    <span class="p">]</span>
    <span class="n">df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">data</span> <span class="o">*</span> <span class="mi">10</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">df</span><font></font>
<font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"labels, unique_labels"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">([],</span> <span class="p">[</span><span class="s2">"other"</span><span class="p">]),</span>  <span class="c1"># no set of approved labels</span>
        <span class="p">([</span><span class="s2">"c3"</span><span class="p">],</span> <span class="p">[</span><span class="s2">"other"</span><span class="p">]),</span>  <span class="c1"># no overlap b/w approved/actual labels</span>
        <span class="p">([</span><span class="s2">"c0"</span><span class="p">],</span> <span class="p">[</span><span class="s2">"c0"</span><span class="p">,</span> <span class="s2">"other"</span><span class="p">]),</span>  <span class="c1"># partial overlap</span>
        <span class="p">([</span><span class="s2">"c0"</span><span class="p">,</span> <span class="s2">"c1"</span><span class="p">,</span> <span class="s2">"c2"</span><span class="p">],</span> <span class="p">[</span><span class="s2">"c0"</span><span class="p">,</span> <span class="s2">"c1"</span><span class="p">,</span> <span class="s2">"c2"</span><span class="p">]),</span>  <span class="c1"># complete overlap</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_replace_oos_labels</span><span class="p">(</span><span class="n">df</span><span class="p">,</span> <span class="n">labels</span><span class="p">,</span> <span class="n">unique_labels</span><span class="p">):</span>
    <span class="n">replaced_df</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">replace_oos_labels</span><span class="p">(</span>
        <span class="n">df</span><span class="o">=</span><span class="n">df</span><span class="o">.</span><span class="n">copy</span><span class="p">(),</span> <span class="n">labels</span><span class="o">=</span><span class="n">labels</span><span class="p">,</span> <span class="n">label_col</span><span class="o">=</span><span class="s2">"tag"</span><span class="p">,</span> <span class="n">oos_label</span><span class="o">=</span><span class="s2">"other"</span>
    <span class="p">)</span>
    <span class="k">assert</span> <span class="nb">set</span><span class="p">(</span><span class="n">replaced_df</span><span class="o">.</span><span class="n">tag</span><span class="o">.</span><span class="n">unique</span><span class="p">())</span> <span class="o">==</span> <span class="nb">set</span><span class="p">(</span><span class="n">unique_labels</span><span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

Note that we don't use the `df` fixture directly (we pass in `df.copy()`) inside our parametrized test function. If we did, then we'd be changing `df`'s values after each parametrization.

Tip

在围绕数据集创建固定装置时，最佳做法是创建一个仍遵循相同架构的简化版本。例如，在上面的数据框夹具中，正在创建一个较小的数据框，它仍然具有与实际数据框相同的列名。虽然可以加载实际数据集，但随着数据集随时间变化（新标签、删除标签、非常大的数据集等），它可能会导致问题

Fixtures 可以有不同的范围，这取决于如何使用它们。例如，`df`夹具具有模块范围，因为不想在每次测试后都重新创建它，而是希望为模块中的所有测试只创建一次（`tests/test_data.py`）。

-   `function`: 每次测试后，fixture 都会被销毁。`[default]`
-   `class`：夹具在类中的最后一次测试后被销毁。
-   `module`：夹具在模块（脚本）中的最后一次测试后被销毁。
-   `package`：夹具在包中的最后一次测试后被销毁。
-   `session`：夹具在会话的最后一次测试后被销毁。

功能是最低级别的范围，而[会话](https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session)是最高级别。首先执行最高级别的范围固定装置。

> 通常，当在一个特定的测试文件中有许多夹具时，可以将它们全部组织在一个`fixtures.py`脚本中并根据需要调用它们。

### 标记

已经能够以各种粒度级别（所有测试、脚本、函数等）执行测试，但可以使用[标记](https://docs.pytest.org/en/stable/mark.html)创建自定义粒度。已经使用了一种类型的标记（参数化），但还有其他几种[内置标记](https://docs.pytest.org/en/stable/mark.html#mark)。例如，[`skipif`](https://docs.pytest.org/en/stable/skipping.html#id1)如果满足条件，标记允许跳过测试的执行。例如，假设只想在 GPU 可用时测试训练模型：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_16"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_16 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">skipif</span><span class="p">(</span>
    <span class="ow">not</span> <span class="n">torch</span><span class="o">.</span><span class="n">cuda</span><span class="o">.</span><span class="n">is_available</span><span class="p">(),</span>
    <span class="n">reason</span><span class="o">=</span><span class="s2">"Full training tests require a GPU."</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_training</span><span class="p">():</span>
    <span class="k">pass</span>
</code></pre></div></td></tr></tbody></table>

[除了一些保留](https://docs.pytest.org/en/stable/reference.html#marks)的标记名称外，还可以创建自己的自定义标记。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_17"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_17 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">fruits</span>
<span class="k">def</span> <span class="nf">test_fruit</span><span class="p">(</span><span class="n">my_fruit</span><span class="p">):</span>
    <span class="k">assert</span> <span class="n">my_fruit</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s2">"apple"</span>
</code></pre></div></td></tr></tbody></table>

`-m`可以使用需要（区分大小写）标记表达式的标志来执行它们，如下所示：

```
pytest -m "fruits"      #  runs all tests marked with `fruits`
pytest -m "not fruits"  #  runs all tests besides those marked with `fruits`

```

tip

使用标记的正确方法是明确列出在[pyproject.toml](https://github.com/GokuMohandas/mlops-course/blob/main/pyproject.toml)文件中创建的标记。在这里，可以指定必须在此文件中使用`--strict-markers`标志定义所有标记，然后在`markers`列表中声明标记（以及有关它们的一些信息）：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_19"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_19 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">training</span>
<span class="k">def</span> <span class="nf">test_train_model</span><span class="p">():</span>
    <span class="k">assert</span> <span class="o">...</span>
</code></pre></div></td></tr></tbody></table>

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_20"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_20 > code"></button><code><span class="c1"># Pytest</span><span class="w"></span>
<span class="k">[tool.pytest.ini_options]</span><span class="w"></span>
<span class="n">testpaths</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="p">[</span><span class="s">"tests"</span><span class="p">]</span><span class="w"></span>
<span class="n">python_files</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="s">"test_*.py"</span><span class="w"></span>
<span class="n">addopts</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="s">"--strict-markers --disable-pytest-warnings"</span><span class="w"></span>
<span class="hll"><span class="n">markers</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
</span><span class="hll"><span class="w">    </span><span class="s">"training: tests that involve training"</span><span class="p">,</span><span class="w"></span>
</span><span class="hll"><span class="p">]</span><span class="w"></span>
</span></code></pre></div></td></tr></tbody></table>

完成此操作后，可以通过执行查看所有现有的标记列表，`pytest --markers`当尝试使用此处未定义的新标记时会收到错误消息。

### 覆盖范围

当为应用程序的组件开发测试时，重要的是要知道对代码库的覆盖程度以及知道是否遗漏了任何东西。可以使用[Coverage](https://coverage.readthedocs.io/)库来跟踪和可视化测试占代码库的多少。使用 pytest，由于[pytest-cov](https://pytest-cov.readthedocs.io/)插件，使用这个包变得更加容易。

```
pip install pytest-cov==2.10.1

```

将把它添加到`setup.py`脚本中：

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_22"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_22 > code"></button><code><span class="c1"># setup.py</span>
<span class="n">test_packages</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s2">"pytest==7.1.2"</span><span class="p">,</span>
    <span class="s2">"pytest-cov==2.10.1"</span>
<span class="p">]</span>
</code></pre></div></td></tr></tbody></table>

```
python3 -m pytest --cov tagifai --cov-report html

```

![pytest](https://madewithml.com/static/images/mlops/testing/pytest.png)

在这里，要求覆盖 tagifai 和 app 目录中的所有代码，并以 HTML 格式生成报告。当运行它时，将看到测试目录中的测试正在执行，而覆盖插件正在跟踪应用程序中的哪些行正在执行。测试完成后，可以查看生成的报告（默认为`htmlcov/index.html`）并单击各个文件以查看哪些部分未被任何测试覆盖。当忘记测试某些条件、异常等时，这尤其有用。

![测试覆盖率](https://madewithml.com/static/images/mlops/testing/coverage.png)

warning

虽然有 100% 的覆盖率，但这并不意味着应用程序是完美的。覆盖率只是表示在测试中执行的一段代码，不一定是它的每一部分都经过测试，更不用说彻底测试了。因此，覆盖率**永远**不应被用作正确性的表示。但是，将覆盖率保持在 100% 非常有用，这样就可以知道新功能何时尚未测试。在 CI/CD 课程中，将了解在推送到特定分支时如何使用 GitHub 操作来实现 100% 的覆盖率。

### 排除项

有时编写测试来覆盖应用程序中的每一行是没有意义的，但仍然希望考虑这些行，以便可以保持 100% 的覆盖率。应用排除时，有两个级别的权限：

1.  通过添加此评论来原谅行`# pragma: no cover, <MESSAGE>`
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_24"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_24 > code"></button><code><span class="k">if</span> <span class="n">trial</span><span class="p">:</span>  <span class="c1"># pragma: no cover, optuna pruning</span>
        <span class="n">trial</span><span class="o">.</span><span class="n">report</span><span class="p">(</span><span class="n">val_loss</span><span class="p">,</span> <span class="n">epoch</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">trial</span><span class="o">.</span><span class="n">should_prune</span><span class="p">():</span>
            <span class="k">raise</span> <span class="n">optuna</span><span class="o">.</span><span class="n">TrialPruned</span><span class="p">()</span>
    </code></pre></div></td></tr></tbody></table>
    
2.  `pyproject.toml`通过在配置中指定文件来排除文件：
    

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_25"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_25 > code"></button><code><span class="c1"># Pytest coverage</span><span class="w"></span>
<span class="k">[tool.coverage.run]</span><span class="w"></span>
<span class="n">omit</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="p">[</span><span class="s">"app/gunicorn.py"</span><span class="p">]</span><span class="w"></span>
</code></pre></div></td></tr></tbody></table>

> 重点是能够通过评论为这些排除项添加理由，以便团队可以遵循推理。

现在已经有了测试传统软件的基础，让在机器学习系统的背景下深入测试数据和模型。


## 型号

测试 ML 系统的最后一个方面涉及在训练、评估、推理和部署期间测试模型。

### 训练

希望在开发训练管道时迭代地编写测试，以便可以快速发现错误。这一点尤为重要，因为与传统软件不同，ML 系统可以运行完成而不会引发任何异常/错误，但可能会产生不正确的系统。还希望快速捕获错误以节省时间和计算。

-   检查模型输出的形状和值
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_59"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_59 > code"></button><code><span class="k">assert</span> <span class="n">model</span><span class="p">(</span><span class="n">inputs</span><span class="p">)</span><span class="o">.</span><span class="n">shape</span> <span class="o">==</span> <span class="n">torch</span><span class="o">.</span><span class="n">Size</span><span class="p">([</span><span class="nb">len</span><span class="p">(</span><span class="n">inputs</span><span class="p">),</span> <span class="n">num_classes</span><span class="p">])</span>
    </code></pre></div></td></tr></tbody></table>
    
-   在一批训练后检查损失是否减少
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_60"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_60 > code"></button><code><span class="k">assert</span> <span class="n">epoch_loss</span> <span class="o">&lt;</span> <span class="n">prev_epoch_loss</span>
    </code></pre></div></td></tr></tbody></table>
    
-   批量过拟合
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_61"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_61 > code"></button><code><span class="n">accuracy</span> <span class="o">=</span> <span class="n">train</span><span class="p">(</span><span class="n">model</span><span class="p">,</span> <span class="n">inputs</span><span class="o">=</span><span class="n">batches</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
    <span class="k">assert</span> <span class="n">accuracy</span> <span class="o">==</span> <span class="n">pytest</span><span class="o">.</span><span class="n">approx</span><span class="p">(</span><span class="mf">0.95</span><span class="p">,</span> <span class="nb">abs</span><span class="o">=</span><span class="mf">0.05</span><span class="p">)</span> <span class="c1"># 0.95 ± 0.05</span>
    </code></pre></div></td></tr></tbody></table>
    
-   训练完成（测试提前停止、保存等）
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_62"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_62 > code"></button><code><span class="n">train</span><span class="p">(</span><span class="n">model</span><span class="p">)</span>
    <span class="k">assert</span> <span class="n">learning_rate</span> <span class="o">&gt;=</span> <span class="n">min_learning_rate</span>
    <span class="k">assert</span> <span class="n">artifacts</span>
    </code></pre></div></td></tr></tbody></table>
    
-   在不同的设备上
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_63"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_63 > code"></button><code><span class="k">assert</span> <span class="n">train</span><span class="p">(</span><span class="n">model</span><span class="p">,</span> <span class="n">device</span><span class="o">=</span><span class="n">torch</span><span class="o">.</span><span class="n">device</span><span class="p">(</span><span class="s2">"cpu"</span><span class="p">))</span>
    <span class="k">assert</span> <span class="n">train</span><span class="p">(</span><span class="n">model</span><span class="p">,</span> <span class="n">device</span><span class="o">=</span><span class="n">torch</span><span class="o">.</span><span class="n">device</span><span class="p">(</span><span class="s2">"cuda"</span><span class="p">))</span>
    </code></pre></div></td></tr></tbody></table>
    

note

您可以使用 pytest 标记标记计算密集型测试，并且仅在对影响模型的系统进行更改时才执行它们。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_64"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_64 > code"></button><code><span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">training</span>
<span class="k">def</span> <span class="nf">test_train_model</span><span class="p">():</span>
    <span class="o">...</span>
</code></pre></div></td></tr></tbody></table>

### 行为测试

行为测试是测试输入数据和预期输出的过程，同时将模型视为黑盒（与模型无关的评估）。它们不一定在本质上是对抗性的，但更多的是在部署模型后可能期望在现实世界中看到的扰动类型。关于这个主题的具有里程碑意义的论文是[Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://arxiv.org/abs/2005.04118)，它将行为测试分为三种类型的测试：

-   `invariance`：更改不应影响输出。
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_65"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_65 > code"></button><code tabindex="0"><span class="c1"># INVariance via verb injection (changes should not affect outputs)</span>
    <span class="n">tokens</span> <span class="o">=</span> <span class="p">[</span><span class="s2">"revolutionized"</span><span class="p">,</span> <span class="s2">"disrupted"</span><span class="p">]</span>
    <span class="n">texts</span> <span class="o">=</span> <span class="p">[</span><span class="sa">f</span><span class="s2">"Transformers applied to NLP have </span><span class="si">{</span><span class="n">token</span><span class="si">}</span><span class="s2"> the ML field."</span> <span class="k">for</span> <span class="n">token</span> <span class="ow">in</span> <span class="n">tokens</span><span class="p">]</span>
    <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="n">texts</span><span class="p">,</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)</span>
    </code></pre></div></td></tr></tbody></table>
    

```
['自然语言处理'，'自然语言处理']

```

-   `directional`：变化应该会影响产出。
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_66"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_66 > code"></button><code><span class="c1"># DIRectional expectations (changes with known outputs)</span>
    <span class="n">tokens</span> <span class="o">=</span> <span class="p">[</span><span class="s2">"text classification"</span><span class="p">,</span> <span class="s2">"image classification"</span><span class="p">]</span>
    <span class="n">texts</span> <span class="o">=</span> <span class="p">[</span><span class="sa">f</span><span class="s2">"ML applied to </span><span class="si">{</span><span class="n">token</span><span class="si">}</span><span class="s2">."</span> <span class="k">for</span> <span class="n">token</span> <span class="ow">in</span> <span class="n">tokens</span><span class="p">]</span>
    <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="n">texts</span><span class="p">,</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)</span>
    </code></pre></div></td></tr></tbody></table>
    

```
['自然语言处理'，'计算机视觉']

```

-   `minimum functionality`：输入和预期输出的简单组合。
    
    <table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
    <span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_67"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_67 > code"></button><code tabindex="0"><span class="c1"># Minimum Functionality Tests (simple input/output pairs)</span>
    <span class="n">tokens</span> <span class="o">=</span> <span class="p">[</span><span class="s2">"natural language processing"</span><span class="p">,</span> <span class="s2">"mlops"</span><span class="p">]</span>
    <span class="n">texts</span> <span class="o">=</span> <span class="p">[</span><span class="sa">f</span><span class="s2">"</span><span class="si">{</span><span class="n">token</span><span class="si">}</span><span class="s2"> is the next big wave in machine learning."</span> <span class="k">for</span> <span class="n">token</span> <span class="ow">in</span> <span class="n">tokens</span><span class="p">]</span>
    <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="n">texts</span><span class="p">,</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)</span>
    </code></pre></div></td></tr></tbody></table>
    

```
['自然语言处理'，'mlops']

```

对抗性测试

这些类型的测试中的每一种还可以包括对抗性测试，例如使用常见的有偏见的令牌或嘈杂的令牌进行测试等。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_68"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_68 > code"></button><code><span class="n">texts</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s2">"CNNs for text classification."</span><span class="p">,</span>  <span class="c1"># CNNs are typically seen in computer-vision projects</span>
    <span class="s2">"This should not produce any relevant topics."</span>  <span class="c1"># should predict `other` label</span>
<span class="p">]</span>
<span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="n">texts</span><span class="p">,</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)</span>
</code></pre></div></td></tr></tbody></table>

```
    ['自然语言处理'，'其他']

```

可以将这些测试转换为系统的参数化测试：

```
mkdir tests/model
touch tests/model/test_behavioral.py

```

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">13 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">14 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">15 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">16 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">17 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">18 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">19 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">20 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">21 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">22 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">23 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">24 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">25 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">26 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">27</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_70"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_70 > code"></button><code tabindex="0"><span class="c1"># tests/model/test_behavioral.py</span>
<span class="kn">from</span> <span class="nn">pathlib</span> <span class="kn">import</span> <span class="n">Path</span>
<span class="kn">import</span> <span class="nn">pytest</span>
<span class="kn">from</span> <span class="nn">config</span> <span class="kn">import</span> <span class="n">config</span>
<span class="kn">from</span> <span class="nn">tagifai</span> <span class="kn">import</span> <span class="n">main</span><span class="p">,</span> <span class="n">predict</span><font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">fixture</span><span class="p">(</span><span class="n">scope</span><span class="o">=</span><span class="s2">"module"</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">artifacts</span><span class="p">():</span>
    <span class="n">run_id</span> <span class="o">=</span> <span class="nb">open</span><span class="p">(</span><span class="n">Path</span><span class="p">(</span><span class="n">config</span><span class="o">.</span><span class="n">CONFIG_DIR</span><span class="p">,</span> <span class="s2">"run_id.txt"</span><span class="p">))</span><span class="o">.</span><span class="n">read</span><span class="p">()</span>
    <span class="n">artifacts</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">load_artifacts</span><span class="p">(</span><span class="n">run_id</span><span class="o">=</span><span class="n">run_id</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">artifacts</span><font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"text_a, text_b, tag"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span>
            <span class="s2">"Transformers applied to NLP have revolutionized machine learning."</span><span class="p">,</span>
            <span class="s2">"Transformers applied to NLP have disrupted machine learning."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">),</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_inv</span><span class="p">(</span><span class="n">text_a</span><span class="p">,</span> <span class="n">text_b</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">artifacts</span><span class="p">):</span>
    <span class="sd">"""INVariance via verb injection (changes should not affect outputs)."""</span>
    <span class="n">tag_a</span> <span class="o">=</span> <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="p">[</span><span class="n">text_a</span><span class="p">],</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s2">"predicted_tag"</span><span class="p">]</span>
    <span class="n">tag_b</span> <span class="o">=</span> <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="p">[</span><span class="n">text_b</span><span class="p">],</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s2">"predicted_tag"</span><span class="p">]</span>
    <span class="k">assert</span> <span class="n">tag_a</span> <span class="o">==</span> <span class="n">tag_b</span> <span class="o">==</span> <span class="n">tag</span>
</code></pre></div></td></tr></tbody></table>

看法`tests/model/test_behavioral.py`

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"> 1</span>
<span class="normal"> 2</span>
<span class="normal"> 3</span>
<span class="normal"> 4</span>
<span class="normal"> 5</span>
<span class="normal"> 6</span>
<span class="normal"> 7</span>
<span class="normal"> 8</span>
<span class="normal"> 9</span>
<span class="normal">10</span>
<span class="normal">11</span>
<span class="normal">12</span>
<span class="normal">13</span>
<span class="normal">14</span>
<span class="normal">15</span>
<span class="normal">16</span>
<span class="normal">17</span>
<span class="normal">18</span>
<span class="normal">19</span>
<span class="normal">20</span>
<span class="normal">21</span>
<span class="normal">22</span>
<span class="normal">23</span>
<span class="normal">24</span>
<span class="normal">25</span>
<span class="normal">26</span>
<span class="normal">27</span>
<span class="normal">28</span>
<span class="normal">29</span>
<span class="normal">30</span>
<span class="normal">31</span>
<span class="normal">32</span>
<span class="normal">33</span>
<span class="normal">34</span>
<span class="normal">35</span>
<span class="normal">36</span>
<span class="normal">37</span>
<span class="normal">38</span>
<span class="normal">39</span>
<span class="normal">40</span>
<span class="normal">41</span>
<span class="normal">42</span>
<span class="normal">43</span>
<span class="normal">44</span>
<span class="normal">45</span>
<span class="normal">46</span>
<span class="normal">47</span>
<span class="normal">48</span>
<span class="normal">49</span>
<span class="normal">50</span>
<span class="normal">51</span>
<span class="normal">52</span>
<span class="normal">53</span>
<span class="normal">54</span>
<span class="normal">55</span>
<span class="normal">56</span>
<span class="normal">57</span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">58 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">59 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">60 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">61 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">62 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">63 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">64 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">65 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">66 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">67 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">68 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">69 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">70 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">71 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">72 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">73 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">74 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">75 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">76 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">77 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">78</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><code><span class="kn">from</span> <span class="nn">pathlib</span> <span class="kn">import</span> <span class="n">Path</span><font></font>
<font></font>
<span class="kn">import</span> <span class="nn">pytest</span><font></font>
<font></font>
<span class="kn">from</span> <span class="nn">config</span> <span class="kn">import</span> <span class="n">config</span>
<span class="kn">from</span> <span class="nn">tagifai</span> <span class="kn">import</span> <span class="n">main</span><span class="p">,</span> <span class="n">predict</span><font></font>
<font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">fixture</span><span class="p">(</span><span class="n">scope</span><span class="o">=</span><span class="s2">"module"</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">artifacts</span><span class="p">():</span>
    <span class="n">run_id</span> <span class="o">=</span> <span class="nb">open</span><span class="p">(</span><span class="n">Path</span><span class="p">(</span><span class="n">config</span><span class="o">.</span><span class="n">CONFIG_DIR</span><span class="p">,</span> <span class="s2">"run_id.txt"</span><span class="p">))</span><span class="o">.</span><span class="n">read</span><span class="p">()</span>
    <span class="n">artifacts</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">load_artifacts</span><span class="p">(</span><span class="n">run_id</span><span class="o">=</span><span class="n">run_id</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">artifacts</span><font></font>
<font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"text, tag"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span>
            <span class="s2">"Transformers applied to NLP have revolutionized machine learning."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">),</span>
        <span class="p">(</span>
            <span class="s2">"Transformers applied to NLP have disrupted machine learning."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">),</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_inv</span><span class="p">(</span><span class="n">text</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">artifacts</span><span class="p">):</span>
    <span class="sd">"""INVariance via verb injection (changes should not affect outputs)."""</span>
    <span class="n">predicted_tag</span> <span class="o">=</span> <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="p">[</span><span class="n">text</span><span class="p">],</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s2">"predicted_tag"</span><span class="p">]</span>
    <span class="k">assert</span> <span class="n">tag</span> <span class="o">==</span> <span class="n">predicted_tag</span><font></font>
<font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"text, tag"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span>
            <span class="s2">"ML applied to text classification."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">),</span>
        <span class="p">(</span>
            <span class="s2">"ML applied to image classification."</span><span class="p">,</span>
            <span class="s2">"computer-vision"</span><span class="p">,</span>
        <span class="p">),</span>
        <span class="p">(</span>
            <span class="s2">"CNNs for text classification."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">)</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_dir</span><span class="p">(</span><span class="n">text</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">artifacts</span><span class="p">):</span>
    <span class="sd">"""DIRectional expectations (changes with known outputs)."""</span>
    <span class="n">predicted_tag</span> <span class="o">=</span> <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="p">[</span><span class="n">text</span><span class="p">],</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s2">"predicted_tag"</span><span class="p">]</span>
    <span class="k">assert</span> <span class="n">tag</span> <span class="o">==</span> <span class="n">predicted_tag</span><font></font>
<font></font>
<font></font>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">parametrize</span><span class="p">(</span>
    <span class="s2">"text, tag"</span><span class="p">,</span>
    <span class="p">[</span>
        <span class="p">(</span>
            <span class="s2">"Natural language processing is the next big wave in machine learning."</span><span class="p">,</span>
            <span class="s2">"natural-language-processing"</span><span class="p">,</span>
        <span class="p">),</span>
        <span class="p">(</span>
            <span class="s2">"MLOps is the next big wave in machine learning."</span><span class="p">,</span>
            <span class="s2">"mlops"</span><span class="p">,</span>
        <span class="p">),</span>
        <span class="p">(</span>
            <span class="s2">"This should not produce any relevant topics."</span><span class="p">,</span>
            <span class="s2">"other"</span><span class="p">,</span>
        <span class="p">),</span>
    <span class="p">],</span>
<span class="p">)</span>
<span class="k">def</span> <span class="nf">test_mft</span><span class="p">(</span><span class="n">text</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">artifacts</span><span class="p">):</span>
    <span class="sd">"""Minimum Functionality Tests (simple input/output pairs)."""</span>
    <span class="n">predicted_tag</span> <span class="o">=</span> <span class="n">predict</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">texts</span><span class="o">=</span><span class="p">[</span><span class="n">text</span><span class="p">],</span> <span class="n">artifacts</span><span class="o">=</span><span class="n">artifacts</span><span class="p">)[</span><span class="mi">0</span><span class="p">][</span><span class="s2">"predicted_tag"</span><span class="p">]</span>
    <span class="k">assert</span> <span class="n">tag</span> <span class="o">==</span> <span class="n">predicted_tag</span>
</code></pre></div></td></tr></tbody></table>

### 推理

部署模型后，大多数用户将使用它进行推理（直接/间接），因此测试它的各个方面非常重要。

#### 加载工件

这是第一次不从内存中加载组件，因此希望确保所需的工件（模型权重、编码器、配置等）都能够被加载。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_71"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_71 > code"></button><code><span class="n">artifacts</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">load_artifacts</span><span class="p">(</span><span class="n">run_id</span><span class="o">=</span><span class="n">run_id</span><span class="p">)</span>
<span class="k">assert</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">artifacts</span><span class="p">[</span><span class="s2">"label_encoder"</span><span class="p">],</span> <span class="n">data</span><span class="o">.</span><span class="n">LabelEncoder</span><span class="p">)</span>
<span class="o">...</span>
</code></pre></div></td></tr></tbody></table>

#### 预言

一旦加载了工件，就准备好测试预测管道。应该只用一个输入和一批输入来测试样本（例如，填充有时会产生意想不到的后果）。

<table class="highlighttable"><tbody><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">1 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">2 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">3 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">4 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">5 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">6 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">7 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">8 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11 </font></font></span>
<span class="normal"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">12</font></font></span></pre></div></td><td class="code"><div class="highlight"><pre id="__code_72"><span></span><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_72 > code"></button><code tabindex="0"><span class="c1"># test our API call directly</span>
<span class="n">data</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">"texts"</span><span class="p">:</span> <span class="p">[</span>
        <span class="p">{</span><span class="s2">"text"</span><span class="p">:</span> <span class="s2">"Transfer learning with transformers for text classification."</span><span class="p">},</span>
        <span class="p">{</span><span class="s2">"text"</span><span class="p">:</span> <span class="s2">"Generative adversarial networks in both PyTorch and TensorFlow."</span><span class="p">},</span>
    <span class="p">]</span>
<span class="p">}</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s2">"/predict"</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">data</span><span class="p">)</span>
<span class="k">assert</span> <span class="n">response</span><span class="o">.</span><span class="n">status_code</span> <span class="o">==</span> <span class="n">HTTPStatus</span><span class="o">.</span><span class="n">OK</span>
<span class="k">assert</span> <span class="n">response</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s2">"POST"</span>
<span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">response</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s2">"data"</span><span class="p">][</span><span class="s2">"predictions"</span><span class="p">])</span> <span class="o">==</span> <span class="nb">len</span><span class="p">(</span><span class="n">data</span><span class="p">[</span><span class="s2">"texts"</span><span class="p">])</span>
<span class="o">...</span>
</code></pre></div></td></tr></tbody></table>

## 生成文件

让在其中创建一个目标，`Makefile`这将允许一次调用执行所有测试：

```
# Test
.PHONY: test
test:
    pytest -m "not training"
    cd tests && great_expectations checkpoint run projects
    cd tests && great_expectations checkpoint run tags
    cd tests && great_expectations checkpoint run labeled_projects

```

```
make test

```

## 测试与监控

最后，将讨论测试和[监控](https://madewithml.com/courses/mlops/testing//../monitoring/)之间的相似点和区别。它们都是 ML 开发管道的组成部分，并且相互依赖以进行迭代。测试可确保系统（代码、数据和模型）达到在离线时建立的预期。鉴于监控涉及这些期望继续在线传递实时生产数据，同时还通过以下方式确保其数据分布[与](https://madewithml.com/courses/mlops/testing//../monitoring/#measuring-drift)参考窗口（通常是训练数据的子集）具有可比性吨n. 当这些条件不再成立时，需要更仔细地检查（再培训可能并不总能解决根本问题）。

对于[监控](https://madewithml.com/courses/mlops/testing//../monitoring/)，在测试期间不必考虑很多不同的问题，因为它涉及尚未看到的（实时）数据。

-   特征和预测分布（漂移）、类型、模式不匹配等。
-   使用间接信号（因为标签可能不容易获得）确定模型性能（整体和数据切片的滚动和窗口度量）。
-   在大数据的情况下，需要知道要标记哪些数据点并进行上采样以进行训练。
-   识别异常和异常值。

> [将在监控](https://madewithml.com/courses/mlops/testing//../monitoring/)课程中更深入地（和代码）介绍所有这些概念。

## 资源

- [远大的期望](https://github.com/great-expectations/great_expectations)
- [ML 测试分数：ML 生产准备和技术债务减少量规](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf)
- [超越准确性：使用 CheckList 对 NLP 模型进行行为测试](https://arxiv.org/abs/2005.04118)
- [健壮性健身房：统一 NLP 评估领域](https://arxiv.org/abs/2101.04840)

本文主体源自以下链接：
```
@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}
```
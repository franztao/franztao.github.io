---
layout:     post
title:      模型服务 API
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - APIs for Model Serving

---


## 模型服务 API

## 直觉

[CLI 应用程序](https://madewithml.com/courses/mlops/cli/)使与模型交互变得更加容易，特别是对于可能不想深入研究代码库的团队成员。但是使用 CLI 为模型提供服务有几个限制：

-   用户需要访问终端、代码库、虚拟环境等。
-   终端上的 CLI 输出不可导出

为了解决这些问题，将开发一个应用程序编程接口 (API)，_任何人都_可以通过一个简单的请求与应用程序进行交互。

> 最终用户可能不会直接与 API 交互，但可能会使用向发送请求的 UI/UX 组件。

## 服务

API 允许不同的应用程序实时相互通信。但是在提供预测服务时，需要首先决定是批量还是实时进行，这完全基于特征空间（有限与无限制）。

### 批量服务

可以对一组有限的输入进行批量预测，然后将其写入数据库以进行低延迟推理。当用户或下游进程实时发送推理请求时，会返回数据库中的缓存结果。

![批量服务](https://madewithml.com/static/images/mlops/systems-design/batch_serving.png)

-   ✅ 生成和缓存预测，以便为用户提供非常快速的推理。
-   ✅ 该模型不需要作为它自己的服务进行旋转，因为它从未实时使用。
-   ❌ 如果用户开发了当前预测所基于的旧数据未捕获的新兴趣，则预测可能会变得陈旧。
-   ❌ 输入特征空间必须是有限的，因为需要在需要实时预测之前生成所有预测。

批量服务任务

哪些任务适合批量服务？

显示答案

_根据现有_用户的观看历史推荐他们喜欢的内容。然而，在第二天处理他们的历史记录之前，_新用户可能只会收到一些基于他们明确兴趣的通用推荐。_即使不进行批量服务，缓存非常流行的输入特征集（例如，明确兴趣的组合导致某些推荐内容）可能仍然有用，以便可以更快地提供这些预测。

### 实时服务

还可以提供实时预测，通常是通过使用适当的输入数据向 API 发出请求。

![实时服务](https://madewithml.com/static/images/mlops/systems-design/real_time_serving.png)

-   ✅ 可以产生更多最新的预测，从而产生更有意义的用户体验等。
-   ❌ 需要托管微服务来处理请求流量。
-   ❌ 需要实时监控，因为输入空间是无限的，这可能会产生错误的预测。

在本课中，将创建启用实时服务所需的 API。在情况下，交互涉及客户端（用户、其他应用程序等）向服务器发送带有适当输入的_请求_（例如预测请求）（应用程序具有经过训练的模型）并接收_响应_（例如预测）作为回报。

![客户端 API 交互](https://madewithml.com/static/images/mlops/api/interactions.png)

## 要求

用户将以请求的形式与 API 进行交互。让看一下请求的不同组成部分：

### URI

统一资源标识符 (URI) 是特定资源的标识符。

```
https:// localhost: 8000 /models/{modelId}/ ?filter=passed #details

```

### 方法

方法是对 URI 定义的特定资源执行的操作。有许多可能的[方法](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)可供选择，但以下四种是最受欢迎的，它们通常被称为**CRUD** [，](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)**因为**它们允许您创建、**读取**、更新和**删除**。

-   `GET`: 获取资源。
-   `POST`: 创建或更新资源。
-   `PUT/PATCH`: 创建或更新资源。
-   `DELETE`: 删除资源。

笔记

您可以使用`POST`or `PUT`request 方法来创建和修改资源，但主要区别在于`PUT`幂等性，这意味着您可以重复调用该方法，并且每次都会产生相同的状态。然而，`POST`多次调用可能会导致创建多个实例，因此每次都会更改整体状态。

```
POST /models/<new_model> -d {}       # error since we haven't created the `new_model` resource yet
POST /models -d {}                   # creates a new model based on information provided in data
POST /models/<existing_model> -d {}  # updates an existing model based on information provided in data

PUT /models/<new_model> -d {}        # creates a new model based on information provided in data
PUT /models/<existing_model> -d {}   # updates an existing model based on information provided in data

```

可以使用[cURL](https://linuxize.com/post/curl-rest-api/)通过以下选项执行 API 调用：

```
用法：curl [选项...]
-X, --request HTTP 方法（即 GET）
-H, --header 要发送到请求的标头（例如身份验证）
-d, --data 数据到 POST、PUT/PATCH、DELETE（通常是 JSON）
...

```

例如，如果想要 GET all `models`， cURL 命令将如下所示：

```
curl -X GET "http://localhost:8000/models"

```

标头包含有关特定事件的信息，通常在客户端的请求和服务器的响应中都可以找到。它的范围可以从他们将发送和接收的格式类型、身份验证和缓存信息等。

```
curl -X GET "http://localhost:8000/" \          # method and URI
    -H  "accept: application/json"  \           # client accepts JSON
    -H  "Content-Type: application/json" \      # client sends JSON

```

### 身体

正文包含处理请求可能需要的信息。它通常是在/请求方法期间发送`POST`的JSON 对象。`PUT``PATCH``DELETE`

```
curl -X POST "http://localhost:8000/models" \   # method and URI
    -H  "accept: application/json" \            # client accepts JSON
    -H  "Content-Type: application/json" \      # client sends JSON
    -d "{'name': 'RoBERTa', ...}"               # request body

```

## 回复

从服务器收到的响应是发送的请求的结果。响应还包括标题和正文，其中应包含正确的 HTTP 状态代码以及显式消息、数据等。

```
{
  "message": "OK",
  "method": "GET",
  "status-code": 200,
  "url": "http://localhost:8000/",
  "data": {}
}

```

> 可能还希望在响应中包含其他元数据，例如模型版本、使用的数据集等。下游消费者可能感兴趣的任何内容或可能对检查有用的元数据。

根据具体情况，有许多[HTTP 状态代码可供选择，但以下是最常见的选项：](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

## 最佳实践

在设计 API 时，需要遵循一些最佳实践：

-   URI 路径、消息等应尽可能明确。避免使用神秘的资源名称等。
-   使用名词而不是动词来命名资源。请求方法已经考虑了动词（✅  `GET /users`不是 ❌  `GET /get_users`）。
-   复数名词（✅  `GET /users/{userId}`不是 ❌  `GET /user/{userID}`）。
-   在 URI 中使用破折号表示资源和路径参数，但使用下划线表示查询参数 ( `GET /nlp-models/?find_desc=bert`)。
-   向用户返回适当的 HTTP 和信息性消息。

## 应用

将在一个单独的`app`目录中定义 API，因为将来可能会有额外的包，例如`tagifai`，不希望应用程序附加到任何一个包。在`app`目录中，将创建以下脚本：

```
mkdir app
cd app
touch api.py gunicorn.py schemas.py
cd ../

```

```
app/
├── api.py          - FastAPI app
├── gunicorn.py     - WSGI script
└── schemas.py      - API model schemas

```

-   [`api.py`](https://github.com/GokuMohandas/mlops-course/tree/main/app/api.py)：将包含 API 初始化和端点的主脚本。
-   [`gunicorn.py`](https://github.com/GokuMohandas/mlops-course/tree/main/app/gunicorn.py)：用于定义 API worker 配置的脚本。
-   [`schemas.py`](https://github.com/GokuMohandas/mlops-course/tree/main/app/schemas.py)：将在资源端点中使用的不同对象的定义。

## 快速API

将使用[FastAPI](https://fastapi.tiangolo.com/)作为框架来构建 API 服务。还有很多其他框架选项，例如[Flask](https://flask.palletsprojects.com/)、[Django](https://www.djangoproject.com/)，甚至是非基于 Python 的选项，例如[Node](https://nodejs.org/en/)、[Angular](https://angular.io/)等。FastAPI 结合了这些框架的许多优点，并且正在迅速成熟并被更广泛地采用。它的显着优势包括：

-   用 Python 开发
-   高性能[\_](https://fastapi.tiangolo.com/benchmarks/)
-   [通过pydantic](https://pydantic-docs.helpmanual.io/)进行数据验证[](https://pydantic-docs.helpmanual.io/)
-   自动生成的文档
-   依赖注入
-   通过 OAuth2 确保安全

```
pip install fastapi==0.78.0

```

```
# Add to requirements.txt
fastapi==0.78.0

```

> 您对框架的选择还取决于您团队的现有系统和流程。然而，随着微服务的广泛采用，可以将特定应用程序包装在选择的任何框架中并公开适当的资源，以便所有其他系统都可以轻松地与之通信。

### 初始化

第一步是`api.py`通过定义标题、描述和版本等元数据在脚本中初始化 API：

<table><tbody><tr><td></td><td><div><pre id="__code_29"><span></span><code><span># app/api.py</span>
<span>from</span> <span>fastapi</span> <span>import</span> <span>FastAPI</span><span></span>
<span></span>
<span># Define application</span>
<span>app</span> <span>=</span> <span>FastAPI</span><span>(</span>
    <span>title</span><span>=</span><span>"TagIfAI - Made With ML"</span><span>,</span>
    <span>description</span><span>=</span><span>"Classify machine learning projects."</span><span>,</span>
    <span>version</span><span>=</span><span>"0.1"</span><span>,</span>
<span>)</span>
</code></pre></div></td></tr></tbody></table>

第一个端点将是一个简单的端点，希望显示一切都按预期工作。端点的路径将只是`/`（当用户访问基本 URI 时），它将是一个`GET`请求。这个简单的端点通常用作健康检查，以确保应用程序确实启动并正常运行。

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
<span><span><span>13</span></span></span></pre></div></td><td><div><pre id="__code_30"><span></span><code><span># app/api.py</span>
<span>from</span> <span>http</span> <span>import</span> <span>HTTPStatus</span>
<span>from</span> <span>typing</span> <span>import</span> <span>Dict</span>
<span>
</span><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/"</span><span>)</span>
<span>def</span> <span>_index</span><span>()</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
    <span>"""Health check."""</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

通过第 4 行中的路径操作装饰器让应用程序知道端点位于，`/`并且返回带有`200 OK`HTTP 状态代码的 JSON 响应。

> 在实际[`api.py`](https://github.com/GokuMohandas/mlops-course/tree/main/app/api.py)脚本中，您会注意到甚至索引函数看起来也不同。别担心，正在慢慢地将组件添加到端点并在此过程中证明它们的合理性。

### 发射

正在使用[Uvicorn](https://www.uvicorn.org/)，这是一个快速的[ASGI](https://en.wikipedia.org/wiki/Asynchronous_Server_Gateway_Interface)服务器，可以在单个进程中运行异步代码来启动应用程序。

```
pip install uvicorn==0.17.6

```

```
# Add to requirements.txt
uvicorn==0.17.6

```

可以使用以下命令启动应用程序：

```
uvicorn app.api:app \       # location of app (`app` directory > `api.py` script > `app` object)
    --host 0.0.0.0 \        # localhost
    --port 8000 \           # port 8000
    --reload \              # reload every time we update
    --reload-dir tagifai \  # only reload on updates to `tagifai` directory
    --reload-dir app        # and the `app` directory

```

```
信息：将观察这些目录中的变化：['/Users/goku/Documents/madewithml/mlops/app', '/Users/goku/Documents/madewithml/mlops/tagifai']
信息：Uvicorn 在 http://0.0.0.0:8000 上运行（按 CTRL+C 退出）
信息：使用 statreload 开始重新加载进程 [57609]
信息：已启动服务器进程 [57611]
INFO：等待应用程序启动。
信息：应用程序启动完成。

```

> 请注意，只重新加载对特定目录的更改，因为这是为了避免重新加载不会影响应用程序的文件，例如日志文件等。

如果想管理多个 uvicorn 工作者以在应用程序中启用并行性，可以将[Gunicorn](https://gunicorn.org/)与 Uvicorn 结合使用。这通常在将处理有意义的流量的生产环境中完成。已经包含了一个[`app/gunicorn.py`](https://github.com/GokuMohandas/mlops-course/tree/main/app/gunicorn.py)带有可定制配置的脚本，可以使用以下命令启动所有工作人员：

```
gunicorn -c config/gunicorn.py -k uvicorn.workers.UvicornWorker app.api:app

```

还将这两个命令添加到`README.md`文件中：

```
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload --reload-dir tagifai --reload-dir app  # dev
gunicorn -c app/gunicorn.py -k uvicorn.workers.UvicornWorker app.api:app  # prod

```

### 要求

现在应用程序正在运行，可以`GET`使用几种不同的方法提交请求：

-   在浏览器上访问端点[http://localhost:8000/](http://localhost:8000/)
-   卷曲
    
    ```
    curl -X GET http://localhost:8000/
    
    ```
    
-   通过代码访问端点。在这里，展示了如何使用 Python 中的[requests](https://requests.readthedocs.io/en/master/)库来完成它，但它可以使用大多数流行的语言来完成。您甚至可以使用[在线工具](https://curl.trillworks.com/)将您的 cURL 命令转换为代码！
    
    <table><tbody><tr><td></td><td><div><pre id="__code_7"><span></span><code><span>import</span> <span>json</span>
    <span>import</span> <span>requests</span><span></span>
    <span></span>
    <span>response</span> <span>=</span> <span>requests</span><span>.</span><span>get</span><span>(</span><span>"http://localhost:8000/"</span><span>)</span>
    <span>print</span> <span>(</span><span>json</span><span>.</span><span>loads</span><span>(</span><span>response</span><span>.</span><span>text</span><span>))</span>
    </code></pre></div></td></tr></tbody></table>
    
-   使用[Postman](https://www.postman.com/use-cases/application-development/)等外部工具，这对于托管测试非常有用，您可以保存并与其他人共享等。

对于所有这些，将从 API 中看到完全相同的响应：

```
{
  “消息”：“好的”，
  “状态码”：200，
  “数据”： {}
}

```

### 装饰器

在`GET \`上面的请求响应中，关于实际请求的信息并不多，但是有 URL、时间戳等详细信息很有用。但是不想为每个端点单独执行此操作，所以让使用[装饰器](https://madewithml.com/courses/foundations/python/#decorators)自动将相关元数据添加到响应中

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
<span><span><span>16 </span></span></span>
<span><span><span>17 </span></span></span>
<span><span><span>18 </span></span></span>
<span><span><span>19 </span></span></span>
<span><span><span>20 </span></span></span>
<span><span><span>21 </span></span></span>
<span><span><span>22 </span></span></span>
<span><span><span>23</span></span></span></pre></div></td><td><div><pre id="__code_8"><span></span><code><span># app/api.py</span>
<span>from</span> <span>datetime</span> <span>import</span> <span>datetime</span>
<span>from</span> <span>functools</span> <span>import</span> <span>wraps</span>
<span>from</span> <span>fastapi</span> <span>import</span> <span>FastAPI</span><span>,</span> <span>Request</span><span></span>
<span></span>
<span>def</span> <span>construct_response</span><span>(</span><span>f</span><span>):</span>
    <span>"""Construct a JSON response for an endpoint."""</span><span></span>
<span></span>
    <span>@wraps</span><span>(</span><span>f</span><span>)</span>
<span>    <span>def</span> <span>wrap</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>,</span> <span>*</span><span>args</span><span>,</span> <span>**</span><span>kwargs</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
</span>        <span>results</span> <span>=</span> <span>f</span><span>(</span><span>request</span><span>,</span> <span>*</span><span>args</span><span>,</span> <span>**</span><span>kwargs</span><span>)</span>
        <span>response</span> <span>=</span> <span>{</span>
            <span>"message"</span><span>:</span> <span>results</span><span>[</span><span>"message"</span><span>],</span>
            <span>"method"</span><span>:</span> <span>request</span><span>.</span><span>method</span><span>,</span>
            <span>"status-code"</span><span>:</span> <span>results</span><span>[</span><span>"status-code"</span><span>],</span>
            <span>"timestamp"</span><span>:</span> <span>datetime</span><span>.</span><span>now</span><span>()</span><span>.</span><span>isoformat</span><span>(),</span>
            <span>"url"</span><span>:</span> <span>request</span><span>.</span><span>url</span><span>.</span><span>_url</span><span>,</span>
        <span>}</span>
        <span>if</span> <span>"data"</span> <span>in</span> <span>results</span><span>:</span>
            <span>response</span><span>[</span><span>"data"</span><span>]</span> <span>=</span> <span>results</span><span>[</span><span>"data"</span><span>]</span>
        <span>return</span> <span>response</span><span></span>
<span></span>
    <span>return</span> <span>wrap</span>
</code></pre></div></td></tr></tbody></table>

在第 10 行传入了一个[Request](https://fastapi.tiangolo.com/advanced/using-request-directly/)实例，因此可以访问请求方法和 URL 等信息。因此，端点函数也需要将此 Request 对象作为输入参数。一旦从端点函数接收到结果`f`，就可以附加额外的细节并返回更多信息的响应。要使用这个装饰器，只需要相应地包装函数。

<table><tbody><tr><td></td><td><div><pre id="__code_9"><span></span><code><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/"</span><span>)</span>
<span><span>@construct_response</span>
</span><span>def</span> <span>_index</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
    <span>"""Health check."""</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

```
{
    消息：“好的”，
    方法：“获取”，
    状态码：200，
    时间戳：“2021-02-08T13:19:11.343801”，
    url: "http://localhost:8000/",
    数据： { }
}

```

还有一些应该注意的内置装饰器。已经看到了路径操作装饰器（例如`@app.get("/")`），它定义了端点的路径以及[其他属性](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)。还有[事件装饰器](https://fastapi.tiangolo.com/advanced/events/)( `@app.on_event()`)，可以使用它来启动和关闭应用程序。例如，使用 ( `@app.on_event("startup")`) 事件来加载模型以用于推理的工件。将其作为事件执行的好处是，服务在完成之前不会启动，因此不会过早处理任何请求并导致错误。类似地，可以用 ( ) 来执行关闭事件`@app.on_event("shutdown")`，例如保存日志、清理等。

<table><tbody><tr><td></td><td><div><pre id="__code_10"><span></span><code><span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
<span>from</span> <span>config</span> <span>import</span> <span>config</span>
<span>from</span> <span>config.config</span> <span>import</span> <span>logger</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>main</span><span></span>
<span></span>
<span><span>@app</span><span>.</span><span>on_event</span><span>(</span><span>"startup"</span><span>)</span>
</span><span>def</span> <span>load_artifacts</span><span>():</span>
    <span>global</span> <span>artifacts</span>
    <span>run_id</span> <span>=</span> <span>open</span><span>(</span><span>Path</span><span>(</span><span>config</span><span>.</span><span>CONFIG_DIR</span><span>,</span> <span>"run_id.txt"</span><span>))</span><span>.</span><span>read</span><span>()</span>
    <span>artifacts</span> <span>=</span> <span>main</span><span>.</span><span>load_artifacts</span><span>(</span><span>model_dir</span><span>=</span><span>config</span><span>.</span><span>MODEL_DIR</span><span>)</span>
    <span>logger</span><span>.</span><span>info</span><span>(</span><span>"Ready for inference!"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

### 文档

当定义一个端点时，FastAPI 会根据它的输入、输入、输出等自动生成一些文档（遵守[OpenAPI](https://swagger.io/specification/)标准）。可以通过在 api 运行时转到任何浏览器上的端点来访问[Swagger UI](https://swagger.io/tools/swagger-ui/)以获取文档`/docs`.

![API 文档](https://madewithml.com/static/images/mlops/api/documentation.png)

单击端点 > `Try it out`\>`Execute`以查看服务器的响应将是什么样子。由于这是一个`GET`没有任何输入的请求，请求正文是空的，但对于其他方法，需要提供一些信息（将在发出`POST`请求时说明这一点）。

![执行 API 调用](https://madewithml.com/static/images/mlops/api/execute.png)

请注意，端点是在 UI 中的部分下组织的。可以`tags`在脚本中定义端点时使用：

<table><tbody><tr><td></td><td><div><pre id="__code_11"><span></span><code><span><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/"</span><span>,</span> <span>tags</span><span>=</span><span>[</span><span>"General"</span><span>])</span>
</span><span>@construct_response</span>
<span>def</span> <span>_index</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
    <span>"""Health check."""</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

> 您还可以使用`/redoc`端点查看[ReDoc](https://redocly.github.io/redoc/)文档或使用[Postman](https://www.postman.com/use-cases/application-development/)来执行和管理您可以保存并与他人共享的测试。

## 资源

在为 API 设计资源时，需要考虑以下问题：

-   `[USERS]`: 谁是最终用户？这将定义需要公开哪些资源。
    
    -   想要与 API 交互的开发人员。
    -   想要测试和检查模型及其性能的产品团队。
    -   想要对传入项目进行分类的后端服务。
-   `[ACTIONS]`：用户希望能够执行哪些操作？
    
    -   给定输入集的预测
    -   性能检查
    -   检查训练参数

### 查询参数

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
<span><span><span>12</span></span></span></pre></div></td><td><div><pre id="__code_12"><span></span><code><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/performance"</span><span>,</span> <span>tags</span><span>=</span><span>[</span><span>"Performance"</span><span>])</span>
<span>@construct_response</span>
<span><span>def</span> <span>_performance</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>,</span> <span>filter</span><span>:</span> <span>str</span> <span>=</span> <span>None</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
</span>    <span>"""Get the performance metrics."""</span>
    <span>performance</span> <span>=</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>]</span>
    <span>data</span> <span>=</span> <span>{</span><span>"performance"</span><span>:</span><span>performance</span><span>.</span><span>get</span><span>(</span><span>filter</span><span>,</span> <span>performance</span><span>)}</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>data</span><span>,</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

请注意，在这里传递了一个可选的查询参数`filter`来指示关心的性能子集。可以`GET`像这样在请求中包含这个参数：

```
curl -X "GET" \
  "http://localhost:8000/performance?filter=overall" \
  -H "accept: application/json"

```

这只会产生通过查询参数指示的性能子集：

```
{
  "message": "OK",
  "method": "GET",
  "status-code": 200,
  "timestamp": "2021-03-21T13:12:01.297630",
  "url": "http://localhost:8000/performance?filter=overall",
  "data": {
    "performance": {
      "precision": 0.8941372402587212,
      "recall": 0.8333333333333334,
      "f1": 0.8491658224308651,
      "num_samples": 144
    }
  }
}

```

### 路径参数

下一个端点将是`GET`用于训练模型的参数。这一次，使用了一个路径参数`args`，它是 URI 中的**必填**字段。

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
<span><span><span>12</span></span></span></pre></div></td><td><div><pre id="__code_15"><span></span><code><span><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/args/</span><span>{arg}</span><span>"</span><span>,</span> <span>tags</span><span>=</span><span>[</span><span>"Arguments"</span><span>])</span>
</span><span>@construct_response</span>
<span><span>def</span> <span>_arg</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>,</span> <span>arg</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
</span>    <span>"""Get a specific parameter's value used for the run."""</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{</span>
            <span>arg</span><span>:</span> <span>vars</span><span>(</span><span>artifacts</span><span>[</span><span>"args"</span><span>])</span><span>.</span><span>get</span><span>(</span><span>arg</span><span>,</span> <span>""</span><span>),</span>
        <span>},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

可以`GET`像这样执行请求，其中`param`是请求 URI 路径的一部分，而不是它的查询字符串的一部分。

```
curl -X "GET" \
  "http://localhost:8000/args/learning_rate" \
  -H "accept: application/json"

```

会收到这样的回复：

```
{
  "message": "OK",
  "method": "GET",
  "status-code": 200,
  "timestamp": "2021-03-21T13:13:46.696429",
  "url": "http://localhost:8000/params/hidden_dim",
  "data": {
    "learning_rate": 0.14688087680118794
  }
}

```

还可以创建一个端点来生成所有使用的参数：

看法`GET /args`

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
<span><span><span>12</span></span></span></pre></div></td><td><div><pre><span></span><code><span>@app</span><span>.</span><span>get</span><span>(</span><span>"/args"</span><span>,</span> <span>tags</span><span>=</span><span>[</span><span>"Arguments"</span><span>])</span>
<span>@construct_response</span>
<span>def</span> <span>_args</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
    <span>"""Get all arguments used for the run."""</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{</span>
            <span>"args"</span><span>:</span> <span>vars</span><span>(</span><span>artifacts</span><span>[</span><span>"args"</span><span>]),</span>
        <span>},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

可以`GET`像这样执行请求，其中`param`是请求 URI 路径的一部分，而不是它的查询字符串的一部分。

```
curl -X "GET" \
"http://localhost:8000/args" \
-H "accept: application/json"

```

会收到这样的回复：

```
{
"message":"OK",
"method":"GET",
"status-code":200,
"timestamp":"2022-05-25T11:56:37.344762",
"url":"http://localhost:8001/args",
"data":{
    "args":{
    "shuffle":true,
    "subset":null,
    "min_freq":75,
    "lower":true,
    "stem":false,
    "analyzer":"char_wb",
    "ngram_max_range":8,
    "alpha":0.0001,
    "learning_rate":0.14688087680118794,
    "power_t":0.158985493618746
    }
  }
}

```

### 模式

现在是时候定义预测端点了。需要使用想要分类的输入，因此需要定义在定义这些输入时需要遵循的模式。

```
# app/schemas.py
from typing import List
from fastapi import Query
from pydantic import BaseModel

class Text(BaseModel):
    text: str = Query(None, min_length=1)

class PredictPayload(BaseModel):
    texts: List[Text]

```

在这里，将一个对象定义为一个名为`PredictPayload`的对象列表。每个对象都是一个默认的字符串，并且必须至少有 1 个字符。`Text``texts``Text``None`

笔记

可以`PredictPayload`这样定义：

<table><tbody><tr><td></td><td><div><pre id="__code_19"><span></span><code><span>class</span> <span>PredictPayload</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>texts</span><span>:</span> <span>List</span><span>[</span><span>str</span><span>]</span> <span>=</span> <span>Query</span><span>(</span><span>None</span><span>,</span> <span>min_length</span><span>=</span><span>1</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

但是想创建非常明确的模式，以防将来想要合并更多的[验证](https://madewithml.com/courses/mlops/api/#validation)或添加额外的参数。

现在可以在预测端点中使用这个有效载荷：

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
<span><span><span>15</span></span></span></pre></div></td><td><div><pre id="__code_20"><span></span><code><span>from</span> <span>app.schemas</span> <span>import</span> <span>PredictPayload</span>
<span>from</span> <span>tagifai</span> <span>import</span> <span>predict</span><span></span>
<span></span>
<span>@app</span><span>.</span><span>post</span><span>(</span><span>"/predict"</span><span>,</span> <span>tags</span><span>=</span><span>[</span><span>"Prediction"</span><span>])</span>
<span>@construct_response</span>
<span><span>def</span> <span>_predict</span><span>(</span><span>request</span><span>:</span> <span>Request</span><span>,</span> <span>payload</span><span>:</span> <span>PredictPayload</span><span>)</span> <span>-&gt;</span> <span>Dict</span><span>:</span>
</span>    <span>"""Predict tags for a list of texts."""</span>
    <span>texts</span> <span>=</span> <span>[</span><span>item</span><span>.</span><span>text</span> <span>for</span> <span>item</span> <span>in</span> <span>payload</span><span>.</span><span>texts</span><span>]</span>
    <span>predictions</span> <span>=</span> <span>predict</span><span>.</span><span>predict</span><span>(</span><span>texts</span><span>=</span><span>texts</span><span>,</span> <span>artifacts</span><span>=</span><span>artifacts</span><span>)</span>
    <span>response</span> <span>=</span> <span>{</span>
        <span>"message"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>.</span><span>phrase</span><span>,</span>
        <span>"status-code"</span><span>:</span> <span>HTTPStatus</span><span>.</span><span>OK</span><span>,</span>
        <span>"data"</span><span>:</span> <span>{</span><span>"predictions"</span><span>:</span> <span>predictions</span><span>},</span>
    <span>}</span>
    <span>return</span> <span>response</span>
</code></pre></div></td></tr></tbody></table>

`PredictPayload`当想要使用`/predict`端点时，需要遵守架构：

```
curl -X 'POST' 'http://0.0.0.0:8000/predict' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "texts": [
        {"text": "Transfer learning with transformers for text classification."},
        {"text": "Generative adversarial networks for image generation."}
      ]
    }'

```

```
{
  “消息”：“确定”，
  “方法”：“发布”，
  “状态码”：200，
  “时间戳”：“2022-05-25T12：23：34.381614”，
  "url":"http://0.0.0.0:8001/predict",
  “数据”：{
    “预测”：[
      {
        "input_text":"使用转换器进行迁移学习以进行文本分类。",
        “predicted_tag”：“自然语言处理”
      },
      {
        "input_text":"用于图像生成的生成对抗网络。",
        “predicted_tag”：“计算机视觉”
      }
    ]
  }
}

```

### 验证

#### 内置

在[`BaseModel`](https://pydantic-docs.helpmanual.io/usage/models/)这里使用 pydantic 的对象，因为它为所有的模式提供了内置的验证。在例子中，如果一个`Text`实例少于 1 个字符，那么服务将返回相应的错误消息和代码：

```
curl -X POST "http://localhost:8000/predict" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"texts\":[{\"text\":\"\"}]}"

```

```
{
  “细节”： [
    {
      “位置”：[
        “身体”，
        “文本”，
        0,
        “文本”
      ],
      "msg": "确保该值至少有 1 个字符",
      "type": "value_error.any_str.min_length",
      “ctx”：{
        “限制值”：1
      }
    }
  ]
}

```

#### 风俗

还可以使用装饰器在特定实体上添加自定义验证`@validator`，就像确保列表`texts`不为空一样。

<table><tbody><tr><td></td><td><div><pre id="__code_23"><span></span><code><span>class</span> <span>PredictPayload</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>texts</span><span>:</span> <span>List</span><span>[</span><span>Text</span><span>]</span><span></span>
<span></span>
<span>    <span>@validator</span><span>(</span><span>"texts"</span><span>)</span>
</span><span>    <span>def</span> <span>list_must_not_be_empty</span><span>(</span><span>cls</span><span>,</span> <span>value</span><span>):</span>
</span><span>        <span>if</span> <span>not</span> <span>len</span><span>(</span><span>value</span><span>):</span>
</span><span>            <span>raise</span> <span>ValueError</span><span>(</span><span>"List of texts to classify cannot be empty."</span><span>)</span>
</span><span>        <span>return</span> <span>value</span>
</span></code></pre></div></td></tr></tbody></table>

```
curl -X POST "http://localhost:8000/predict" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"texts\":[]}"

```

```
{
  “细节”：[
    {
      “位置”：[
        “身体”，
        “文本”
      ],
      "msg": "要分类的文本列表不能为空。",
      “类型”：“值错误”
    }
  ]
}

```

最后，可以在类[`schema_extra`](https://fastapi.tiangolo.com/tutorial/schema-extra-example/)下添加一个对象`Config`来描述示例的`PredictPayload`外观。当这样做时，它会自动出现在端点的文档中（单击`Try it out`）。

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
<span><span><span>16 </span></span></span>
<span><span><span>17 </span></span></span>
<span><span><span>18</span></span></span></pre></div></td><td><div><pre id="__code_25"><span></span><code tabindex="0"><span>class</span> <span>PredictPayload</span><span>(</span><span>BaseModel</span><span>):</span>
    <span>texts</span><span>:</span> <span>List</span><span>[</span><span>Text</span><span>]</span><span></span>
<span></span>
    <span>@validator</span><span>(</span><span>"texts"</span><span>)</span>
    <span>def</span> <span>list_must_not_be_empty</span><span>(</span><span>cls</span><span>,</span> <span>value</span><span>):</span>
        <span>if</span> <span>not</span> <span>len</span><span>(</span><span>value</span><span>):</span>
            <span>raise</span> <span>ValueError</span><span>(</span><span>"List of texts to classify cannot be empty."</span><span>)</span>
        <span>return</span> <span>value</span><span></span>
<span></span>
<span>    <span>class</span> <span>Config</span><span>:</span>
</span><span>        <span>schema_extra</span> <span>=</span> <span>{</span>
</span><span>            <span>"example"</span><span>:</span> <span>{</span>
</span><span>                <span>"texts"</span><span>:</span> <span>[</span>
</span><span>                    <span>{</span><span>"text"</span><span>:</span> <span>"Transfer learning with transformers for text classification."</span><span>},</span>
</span><span>                    <span>{</span><span>"text"</span><span>:</span> <span>"Generative adversarial networks in both PyTorch and TensorFlow."</span><span>},</span>
</span><span>                <span>]</span>
</span><span>            <span>}</span>
</span><span>        <span>}</span>
</span></code></pre></div></td></tr></tbody></table>

![使用 API 进行推理](https://madewithml.com/static/images/mlops/api/predict.png)

## 产品

为了使 API 成为一个独立的产品，需要为用户和资源创建和管理一个数据库。这些用户将拥有用于身份验证的凭据，并使用他们的权限与服务进行通信。当然，可以显示一个渲染的前端，以使所有这些与 HTML 表单、按钮等无缝连接。这正是[旧 MWML 平台](https://twitter.com/madewithml/status/1284503478685978625)的构建方式，利用 FastAPI 为每天 500K+ 的服务请求提供高性能。

如果您正在构建产品，那么我强烈建议您使用这个[生成模板](https://fastapi.tiangolo.com/project-generation/)来开始。它包括您的产品所需的主干架构：

-   数据库（模型、迁移等）
-   通过 JWT 进行身份验证
-   带有 Celery 的异步任务队列
-   通过 Vue JS 可定制的前端
-   Docker 集成
-   那么多！

但是，对于大多数 ML 开发人员来说，由于微服务的广泛采用，不需要做所有这些。设计良好的 API 服务可以与所有其他服务（与框架无关）无缝通信，将适合任何流程并为整个产品增加价值。主要重点应该是确保服务正常工作并不断改进，这正是下一组课程将关注的内容（[测试](https://madewithml.com/courses/mlops/testing/)和[监控](https://madewithml.com/courses/mlops/monitoring/)）

## 模型服务器

除了将模型包装为单独的、可扩展的微服务之外，还可以使用专门构建的模型服务器来托管模型。模型服务器提供具有 API 层的注册表，以无缝检查、更新、服务、回滚等多个版本的模型。它们还提供自动扩展以满足吞吐量和延迟需求。流行的选项包括[BentoML](https://www.bentoml.com/)、[MLFlow](https://docs.databricks.com/applications/mlflow/model-serving.html)、[TorchServe](https://pytorch.org/serve/)、[RedisAI](https://oss.redislabs.com/redisai/)、[Nvidia Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server)等。

> 模型服务器因其在整个团队中标准化模型部署和服务流程的能力而被广泛采用——实现无缝升级、验证和集成。

___

要引用此内容，请使用：

<table><tbody><tr><td></td><td><div><pre id="__code_26"><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ RESTful API - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
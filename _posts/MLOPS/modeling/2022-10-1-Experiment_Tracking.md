---
layout:     post
title:      实验跟踪
subtitle:   2022年10月
date:       2022-10-1
author:     franztao
header-img: post-bg-re-vs-ng2.jpg
catalog: true
tags:
    - Experiment Tracking

---

管理和跟踪机器学习实验。

## 直觉

到目前为止，我们一直在训练和评估我们不同的基线，但还没有真正跟踪这些实验。我们将解决这个问题，但定义一个适当的实验跟踪过程，我们将用于所有未来的实验（包括超参数优化）。实验跟踪是管理所有不同实验及其组件（例如参数、指标、模型和其他工件）的过程，它使我们能够：

-   **组织**特定实验的所有必要组件。重要的是把所有东西都放在一个地方并且知道它在哪里，这样你以后可以使用它们。
-   使用保存的实验（轻松）**重现过去的结果。**
-   **记录**跨时间、数据、想法、团队等的迭代改进。

实验跟踪有很多选项，但我们将使用[MLFlow](https://mlflow.org/)（100% 免费和[开源](https://github.com/mlflow/mlflow)），因为它具有我们需要的所有功能（以及[不断增长的集成支持](https://medium.com/pytorch/mlflow-and-pytorch-where-cutting-edge-ai-meets-mlops-1985cf8aa789)）。我们可以在我们自己的服务器和数据库上运行 MLFlow，因此没有存储成本/限制，使其成为最受欢迎的选项之一，并被 Microsoft、Facebook、Databricks 和其他公司使用。您还可以设置自己的跟踪服务器，以在多个团队成员之间同步运行同一任务。

There are also several popular options such as a [Comet ML](https://www.comet.ml/site/) (used by Google AI, HuggingFace, etc.), [Neptune](https://neptune.ai/) (used by Roche, NewYorker, etc.), [Weights and Biases](https://www.wandb.com/) (used by Open AI, Toyota Research, etc.). These are fantastic tools that provide features like dashboards, seamless integration, hyperparameter search, reports and even [debugging](https://wandb.ai/latentspace/published-work/The-Science-of-Debugging-with-W-B-Reports--Vmlldzo4OTI3Ng)!

> Many platforms are leveraging their position as the source for experiment data to provide features that extend into other parts of the ML development pipeline such as versioning, debugging, monitoring, etc.

## Application

We'll start by initializing all the required arguments for our experiment.

```
pip install mlflow==1.23.1 -q

```

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>from</span> <span>argparse</span> <span>import</span> <span>Namespace</span>
<span>import</span> <span>mlflow</span>
<span>from</span> <span>pathlib</span> <span>import</span> <span>Path</span>
</code></pre></div></td></tr></tbody></table>

输入参数`args`包含所有需要的参数，很高兴将它们全部组织在一个变量下，这样我们就可以轻松地记录它并为不同的实验调整它（我们会在进行[超参数优化](https://madewithml.com/courses/mlops/optimization/)时看到这一点）。

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Specify arguments</span>
<span>args</span> <span>=</span> <span>Namespace</span><span>(</span>
    <span>lower</span><span>=</span><span>True</span><span>,</span>
    <span>stem</span><span>=</span><span>False</span><span>,</span>
    <span>analyzer</span><span>=</span><span>"char"</span><span>,</span>
    <span>ngram_max_range</span><span>=</span><span>7</span><span>,</span>
    <span>alpha</span><span>=</span><span>1e-4</span><span>,</span>
    <span>learning_rate</span><span>=</span><span>1e-1</span><span>,</span>
    <span>power_t</span><span>=</span><span>0.1</span><span>,</span>
    <span>num_epochs</span><span>=</span><span>100</span>
<span>)</span>
</code></pre></div></td></tr></tbody></table>

接下来，我们将设置我们的模型注册表，其中将存储所有实验及其各自的运行。我们还将使用特定的运行 ID 从此注册表中加载经过训练的模型。

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Set tracking URI</span>
<span>MODEL_REGISTRY</span> <span>=</span> <span>Path</span><span>(</span><span>"experiments"</span><span>)</span>
<span>Path</span><span>(</span><span>MODEL_REGISTRY</span><span>)</span><span>.</span><span>mkdir</span><span>(</span><span>exist_ok</span><span>=</span><span>True</span><span>)</span> <span># create experiments dir</span>
<span>mlflow</span><span>.</span><span>set_tracking_uri</span><span>(</span><span>"file://"</span> <span>+</span> <span>str</span><span>(</span><span>MODEL_REGISTRY</span><span>.</span><span>absolute</span><span>()))</span>
</code></pre></div></td></tr></tbody></table>

小费

在 Windows 上，我们设置跟踪 URI 的最后一行应该有三个正斜杠：

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>mlflow</span><span>.</span><span>set_tracking_uri</span><span>(</span><span>"file:///"</span> <span>+</span> <span>str</span><span>(</span><span>MODEL_REGISTRY</span><span>.</span><span>absolute</span><span>()))</span>
</code></pre></div></td></tr></tbody></table>

```
实验labeled_projects.csv sample_data

```

> When we're collaborating with other team members, this model registry will live on the cloud. Members from our team can connect to it (with authentication) to save and load trained models. If you don't want to set up and maintain a model registry, this is where platforms like [Comet ML](https://www.comet.ml/site/), [Weights and Biases](https://www.wandb.com/) and others offload a lot of technical setup.

## Training

And to make things simple, we'll encapsulate all the components for training into one function which returns all the artifacts we want to be able to track from our experiment.

> Ignore the `trial` argument for now (default is `None`) as it will be used during the [hyperparameter optimization](https://madewithml.com/courses/mlops/optimization/) lesson for pruning unpromising trials.

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
<span>71</span></pre></div></td><td><div><pre><span></span><code><span>def</span> <span>train</span><span>(</span><span>args</span><span>,</span> <span>df</span><span>,</span> <span>trial</span><span>=</span><span>None</span><span>):</span>
    <span>"""Train model on data."""</span><span></span>
<span></span>
    <span># Setup</span>
    <span>set_seeds</span><span>()</span>
    <span>df</span> <span>=</span> <span>pd</span><span>.</span><span>read_csv</span><span>(</span><span>"labeled_projects.csv"</span><span>)</span>
    <span>df</span> <span>=</span> <span>df</span><span>.</span><span>sample</span><span>(</span><span>frac</span><span>=</span><span>1</span><span>)</span><span>.</span><span>reset_index</span><span>(</span><span>drop</span><span>=</span><span>True</span><span>)</span>
    <span>df</span> <span>=</span> <span>preprocess</span><span>(</span><span>df</span><span>,</span> <span>lower</span><span>=</span><span>True</span><span>,</span> <span>stem</span><span>=</span><span>False</span><span>,</span> <span>min_freq</span><span>=</span><span>min_freq</span><span>)</span>
    <span>label_encoder</span> <span>=</span> <span>LabelEncoder</span><span>()</span><span>.</span><span>fit</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>)</span>
    <span>X_train</span><span>,</span> <span>X_val</span><span>,</span> <span>X_test</span><span>,</span> <span>y_train</span><span>,</span> <span>y_val</span><span>,</span> <span>y_test</span> <span>=</span> \
        <span>get_data_splits</span><span>(</span><span>X</span><span>=</span><span>df</span><span>.</span><span>text</span><span>.</span><span>to_numpy</span><span>(),</span> <span>y</span><span>=</span><span>label_encoder</span><span>.</span><span>encode</span><span>(</span><span>df</span><span>.</span><span>tag</span><span>))</span><span></span>
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
        <span># Log</span>
        <span>if</span> <span>not</span> <span>trial</span><span>:</span>
            <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"train_loss"</span><span>:</span> <span>train_loss</span><span>,</span> <span>"val_loss"</span><span>:</span> <span>val_loss</span><span>},</span> <span>step</span><span>=</span><span>epoch</span><span>)</span><span></span>
<span></span>
        <span># Pruning (for optimization in next section)</span>
        <span>if</span> <span>trial</span><span>:</span>
            <span>trial</span><span>.</span><span>report</span><span>(</span><span>val_loss</span><span>,</span> <span>epoch</span><span>)</span>
            <span>if</span> <span>trial</span><span>.</span><span>should_prune</span><span>():</span>
                <span>raise</span> <span>optuna</span><span>.</span><span>TrialPruned</span><span>()</span><span></span>
<span></span>
    <span># Threshold</span>
    <span>y_pred</span> <span>=</span> <span>model</span><span>.</span><span>predict</span><span>(</span><span>X_val</span><span>)</span>
    <span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_val</span><span>)</span>
    <span>args</span><span>.</span><span>threshold</span> <span>=</span> <span>np</span><span>.</span><span>quantile</span><span>(</span>
        <span>[</span><span>y_prob</span><span>[</span><span>i</span><span>][</span><span>j</span><span>]</span> <span>for</span> <span>i</span><span>,</span> <span>j</span> <span>in</span> <span>enumerate</span><span>(</span><span>y_pred</span><span>)],</span> <span>q</span><span>=</span><span>0.25</span><span>)</span>  <span># Q1</span><span></span>
<span></span>
    <span># Evaluation</span>
    <span>other_index</span> <span>=</span> <span>label_encoder</span><span>.</span><span>class_to_index</span><span>[</span><span>"other"</span><span>]</span>
    <span>y_prob</span> <span>=</span> <span>model</span><span>.</span><span>predict_proba</span><span>(</span><span>X_test</span><span>)</span>
    <span>y_pred</span> <span>=</span> <span>custom_predict</span><span>(</span><span>y_prob</span><span>=</span><span>y_prob</span><span>,</span> <span>threshold</span><span>=</span><span>args</span><span>.</span><span>threshold</span><span>,</span> <span>index</span><span>=</span><span>other_index</span><span>)</span>
    <span>metrics</span> <span>=</span> <span>precision_recall_fscore_support</span><span>(</span><span>y_test</span><span>,</span> <span>y_pred</span><span>,</span> <span>average</span><span>=</span><span>"weighted"</span><span>)</span>
    <span>performance</span> <span>=</span> <span>{</span><span>"precision"</span><span>:</span> <span>metrics</span><span>[</span><span>0</span><span>],</span> <span>"recall"</span><span>:</span> <span>metrics</span><span>[</span><span>1</span><span>],</span> <span>"f1"</span><span>:</span> <span>metrics</span><span>[</span><span>2</span><span>]}</span>
    <span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span><span></span>
<span></span>
    <span>return</span> <span>{</span>
        <span>"args"</span><span>:</span> <span>args</span><span>,</span>
        <span>"label_encoder"</span><span>:</span> <span>label_encoder</span><span>,</span>
        <span>"vectorizer"</span><span>:</span> <span>vectorizer</span><span>,</span>
        <span>"model"</span><span>:</span> <span>model</span><span>,</span>
        <span>"performance"</span><span>:</span> <span>performance</span>
    <span>}</span>
</code></pre></div></td></tr></tbody></table>

With MLFlow we need to first initialize an experiment and then you can do runs under that experiment.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>import</span> <span>joblib</span>
<span>import</span> <span>tempfile</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Set experiment</span>
<span>mlflow</span><span>.</span><span>set_experiment</span><span>(</span><span>experiment_name</span><span>=</span><span>"baselines"</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
INFO: 'baselines' does not exist. Creating a new experiment

```

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>def</span> <span>save_dict</span><span>(</span><span>d</span><span>,</span> <span>filepath</span><span>):</span>
    <span>"""Save dict to a json file."""</span>
    <span>with</span> <span>open</span><span>(</span><span>filepath</span><span>,</span> <span>"w"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
        <span>json</span><span>.</span><span>dump</span><span>(</span><span>d</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>,</span> <span>sort_keys</span><span>=</span><span>False</span><span>,</span> <span>fp</span><span>=</span><span>fp</span><span>)</span>
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
<span>21</span></pre></div></td><td><div><pre><span></span><code><span># Tracking</span>
<span>with</span> <span>mlflow</span><span>.</span><span>start_run</span><span>(</span><span>run_name</span><span>=</span><span>"sgd"</span><span>):</span><span></span>
<span></span>
    <span># Train &amp; evaluate</span>
    <span>artifacts</span> <span>=</span> <span>train</span><span>(</span><span>args</span><span>=</span><span>args</span><span>,</span> <span>df</span><span>=</span><span>df</span><span>)</span><span></span>
<span></span>
    <span># Log key metrics</span>
    <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"precision"</span><span>:</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>][</span><span>"precision"</span><span>]})</span>
    <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"recall"</span><span>:</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>][</span><span>"recall"</span><span>]})</span>
    <span>mlflow</span><span>.</span><span>log_metrics</span><span>({</span><span>"f1"</span><span>:</span> <span>artifacts</span><span>[</span><span>"performance"</span><span>][</span><span>"f1"</span><span>]})</span><span></span>
<span></span>
    <span># Log artifacts</span>
    <span>with</span> <span>tempfile</span><span>.</span><span>TemporaryDirectory</span><span>()</span> <span>as</span> <span>dp</span><span>:</span>
        <span>artifacts</span><span>[</span><span>"label_encoder"</span><span>]</span><span>.</span><span>save</span><span>(</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"label_encoder.json"</span><span>))</span>
        <span>joblib</span><span>.</span><span>dump</span><span>(</span><span>artifacts</span><span>[</span><span>"vectorizer"</span><span>],</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"vectorizer.pkl"</span><span>))</span>
        <span>joblib</span><span>.</span><span>dump</span><span>(</span><span>artifacts</span><span>[</span><span>"model"</span><span>],</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"model.pkl"</span><span>))</span>
        <span>save_dict</span><span>(</span><span>artifacts</span><span>[</span><span>"performance"</span><span>],</span> <span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"performance.json"</span><span>))</span>
        <span>mlflow</span><span>.</span><span>log_artifacts</span><span>(</span><span>dp</span><span>)</span><span></span>
<span></span>
    <span># Log parameters</span>
    <span>mlflow</span><span>.</span><span>log_params</span><span>(</span><span>vars</span><span>(</span><span>artifacts</span><span>[</span><span>"args"</span><span>]))</span>
</code></pre></div></td></tr></tbody></table>

```
Epoch: 00 | train_loss: 1.16930, val_loss: 1.21451
Epoch: 10 | train_loss: 0.46116, val_loss: 0.65903
Epoch: 20 | train_loss: 0.31565, val_loss: 0.56018
Epoch: 30 | train_loss: 0.25207, val_loss: 0.51967
Epoch: 40 | train_loss: 0.21740, val_loss: 0.49822
Epoch: 50 | train_loss: 0.19615, val_loss: 0.48529
Epoch: 60 | train_loss: 0.18249, val_loss: 0.47708
Epoch: 70 | train_loss: 0.17330, val_loss: 0.47158
Epoch: 80 | train_loss: 0.16671, val_loss: 0.46765
Epoch: 90 | train_loss: 0.16197, val_loss: 0.46488
{
  "precision": 0.8929962902778195,
  "recall": 0.8333333333333334,
  "f1": 0.8485049088497365
}

```

## Viewing

Let's view what we've tracked from our experiment. MLFlow serves a dashboard for us to view and explore our experiments on a localhost port. If you're running this on your local computer, you can simply run the MLFlow server:

```
mlflow server -h 0.0.0.0 -p 8000 --backend-store-uri $PWD/experiments/

```

and open [http://localhost:8000/](http://localhost:8000/) to view the dashboard. But if you're on Google colab, we're going to use [localtunnel](https://github.com/localtunnel/localtunnel) to create a connection between this notebook and a public URL.

> If localtunnel is not installed, you may need to run `!npm install -g localtunnel` in a cell first.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Run MLFlow server and localtunnel</span>
<span>get_ipython</span><span>()</span><span>.</span><span>system_raw</span><span>(</span><span>"mlflow server -h 0.0.0.0 -p 8000 --backend-store-uri $PWD/experiments/ &amp;"</span><span>)</span>
<span>!</span><span>npx</span> <span>localtunnel</span> <span>--</span><span>port</span> <span>8000</span>
</code></pre></div></td></tr></tbody></table>

MLFlow creates a main dashboard with all your experiments and their respective runs. We can sort runs by clicking on the column headers.

![mlflow仪表板](https://madewithml.com/static/images/mlops/experiment_tracking/dashboard.png)

We can click on any of our experiments on the main dashboard to further explore it (click on the timestamp link for each run). Then click on metrics on the left side to view them in a plot:

![实验指标](https://madewithml.com/static/images/mlops/experiment_tracking/plots.png)

## Loading

We need to be able to load our saved experiment artifacts for inference, retraining, etc.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>def</span> <span>load_dict</span><span>(</span><span>filepath</span><span>):</span>
    <span>"""Load a dict from a json file."""</span>
    <span>with</span> <span>open</span><span>(</span><span>filepath</span><span>,</span> <span>"r"</span><span>)</span> <span>as</span> <span>fp</span><span>:</span>
        <span>d</span> <span>=</span> <span>json</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>)</span>
    <span>return</span> <span>d</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Load all runs from experiment</span>
<span>experiment_id</span> <span>=</span> <span>mlflow</span><span>.</span><span>get_experiment_by_name</span><span>(</span><span>"baselines"</span><span>)</span><span>.</span><span>experiment_id</span>
<span>all_runs</span> <span>=</span> <span>mlflow</span><span>.</span><span>search_runs</span><span>(</span><span>experiment_ids</span><span>=</span><span>experiment_id</span><span>,</span> <span>order_by</span><span>=</span><span>[</span><span>"metrics.val_loss ASC"</span><span>])</span>
<span>print</span> <span>(</span><span>all_runs</span><span>)</span>
</code></pre></div></td></tr></tbody></table>

```
                             run_id  ... tags.mlflow.runName
0  3e5327289e9c499cabfda4fe8b09c037  ...                 sgd

[1 rows x 22 columns]

```

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Best run</span>
<span>best_run_id</span> <span>=</span> <span>all_runs</span><span>.</span><span>iloc</span><span>[</span><span>0</span><span>]</span><span>.</span><span>run_id</span>
<span>best_run</span> <span>=</span> <span>mlflow</span><span>.</span><span>get_run</span><span>(</span><span>run_id</span><span>=</span><span>best_run_id</span><span>)</span>
<span>client</span> <span>=</span> <span>mlflow</span><span>.</span><span>tracking</span><span>.</span><span>MlflowClient</span><span>()</span>
<span>with</span> <span>tempfile</span><span>.</span><span>TemporaryDirectory</span><span>()</span> <span>as</span> <span>dp</span><span>:</span>
    <span>client</span><span>.</span><span>download_artifacts</span><span>(</span><span>run_id</span><span>=</span><span>best_run_id</span><span>,</span> <span>path</span><span>=</span><span>""</span><span>,</span> <span>dst_path</span><span>=</span><span>dp</span><span>)</span>
    <span>vectorizer</span> <span>=</span> <span>joblib</span><span>.</span><span>load</span><span>(</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"vectorizer.pkl"</span><span>))</span>
    <span>label_encoder</span> <span>=</span> <span>LabelEncoder</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>=</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"label_encoder.json"</span><span>))</span>
    <span>model</span> <span>=</span> <span>joblib</span><span>.</span><span>load</span><span>(</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"model.pkl"</span><span>))</span>
    <span>performance</span> <span>=</span> <span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>Path</span><span>(</span><span>dp</span><span>,</span> <span>"performance.json"</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>print</span> <span>(</span><span>json</span><span>.</span><span>dumps</span><span>(</span><span>performance</span><span>,</span> <span>indent</span><span>=</span><span>2</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

```
{
  "precision": 0.8929962902778195,
  "recall": 0.8333333333333334,
  "f1": 0.8485049088497365
}

```

<table><tbody><tr><td></td><td><div><pre><span></span><code><span># Inference</span>
<span>text</span> <span>=</span> <span>"Transfer learning with transformers for text classification."</span>
<span>predict_tag</span><span>(</span><span>texts</span><span>=</span><span>[</span><span>text</span><span>])</span>
</code></pre></div></td></tr></tbody></table>

```
['natural-language-processing']

```

Tip

We can also load a specific run's model artifacts, by using it's run ID, directly from the model registry without having to save them to a temporary directory.

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>artifact_uri</span> <span>=</span> <span>mlflow</span><span>.</span><span>get_run</span><span>(</span><span>run_id</span><span>=</span><span>run_id</span><span>)</span><span>.</span><span>info</span><span>.</span><span>artifact_uri</span><span>.</span><span>split</span><span>(</span><span>"file://"</span><span>)[</span><span>-</span><span>1</span><span>]</span>
<span>params</span> <span>=</span> <span>Namespace</span><span>(</span><span>**</span><span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>Path</span><span>(</span><span>artifact_uri</span><span>,</span> <span>"args.json"</span><span>)))</span>
<span>label_encoder</span> <span>=</span> <span>data</span><span>.</span><span>MultiLabelLabelEncoder</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>=</span><span>Path</span><span>(</span><span>artifact_uri</span><span>,</span> <span>"label_encoder.json"</span><span>))</span>
<span>tokenizer</span> <span>=</span> <span>data</span><span>.</span><span>Tokenizer</span><span>.</span><span>load</span><span>(</span><span>fp</span><span>=</span><span>Path</span><span>(</span><span>artifact_uri</span><span>,</span> <span>"tokenizer.json"</span><span>))</span>
<span>model_state</span> <span>=</span> <span>torch</span><span>.</span><span>load</span><span>(</span><span>Path</span><span>(</span><span>artifact_uri</span><span>,</span> <span>"model.pt"</span><span>),</span> <span>map_location</span><span>=</span><span>device</span><span>)</span>
<span>performance</span> <span>=</span> <span>utils</span><span>.</span><span>load_dict</span><span>(</span><span>filepath</span><span>=</span><span>Path</span><span>(</span><span>artifact_uri</span><span>,</span> <span>"performance.json"</span><span>))</span>
</code></pre></div></td></tr></tbody></table>

___

To cite this content, please use:

<table><tbody><tr><td></td><td><div><pre><span></span><code><span>@article</span><span>{</span><span>madewithml</span><span>,</span><span></span>
<span>    </span><span>author</span><span>       </span><span>=</span><span> </span><span>{Goku Mohandas}</span><span>,</span><span></span>
<span>    </span><span>title</span><span>        </span><span>=</span><span> </span><span>{ Experiment tracking - Made With ML }</span><span>,</span><span></span>
<span>    </span><span>howpublished</span><span> </span><span>=</span><span> </span><span>{\url{https://madewithml.com/}}</span><span>,</span><span></span>
<span>    </span><span>year</span><span>         </span><span>=</span><span> </span><span>{2022}</span><span></span>
<span>}</span><span></span>
</code></pre></div></td></tr></tbody></table>
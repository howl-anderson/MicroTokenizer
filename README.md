# 微型中文分词器

[![Build Status](https://travis-ci.org/howl-anderson/MicroTokenizer.svg?branch=master)](https://travis-ci.org/howl-anderson/MicroTokenizer)
[![PyPI Status](https://img.shields.io/pypi/v/MicroTokenizer.svg)](https://pypi.python.org/pypi/MicroTokenizer)

一个微型的中文分词器，目前提供了七种分词算法:

1. 按照词语的频率（概率）来利用构建 DAG（有向无环图）来分词，使用 `Trie Tree` 构建前缀字典树
2. 使用隐马尔可夫模型（Hidden Markov Model，HMM）来分词
3. 融合 DAG 和 HMM 两种分词模型的结果，按照分词粒度最大化的原则进行融合得到的模型
4. 正向最大匹配法
5. 反向最大匹配法
6. 双向最大匹配法
7. 基于 CRF (Conditional Random Field, 条件随机场) 的分词方法

# 特点 / 特色

* 面向教育：可以导出 `graphml` 格式的图结构文件，辅助学习者理解算法过程
* 良好的分词性能：由于使用类似 `结巴分词` 的算法，具有良好的分词性能
* 具有良好的扩展性：使用和 `结巴分词` 一样的字典文件，可以轻松添加自定义字典
* 自定义能力强
* 提供工具和脚本帮助用户训练自己的分词模型而不是使用内建的模型

# 演示

## 在线演示

### 在线的 Jupyter Notebook
点击右侧图标，即可访问 [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/howl-anderson/MicroTokenizer/master?filepath=.notebooks%2FMicroTokenizer.ipynb)

### Online web demo
@ [http://nlp_demo.xiaoquankong.ai/](http://nlp_demo.xiaoquankong.ai/)

## 离线演示
### DAG 分词
代码：
```python
import MicroTokenizer

tokens = MicroTokenizer.cut("知识就是力量")
print(tokens)

```
输出：
```python
['知识', '就是', '力量']
```

#### 加载用户字典
```python
import MicroTokenizer

tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)

# loading user's custom dictionary file
MicroTokenizer.load_userdict('user_dict.txt')

tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)

```

`user_dict.txt` 的内容为：
```text
杭研 10

```

输出:
```text
['「', '杭', '研', '」', '正确', '应该', '不会', '被', '切开']
['「', '杭研', '」', '正确', '应该', '不会', '被', '切开']

```

### 有向无环图效果演示
![DAG of 'knowledge is power'](.images/DAG_of_knowledge_is_power.png)

#### 备注
* `<s>` 和 `</s>` 是图的起始和结束节点，不是实际要分词的文本
* 图中 Edge 上标注的是 `log(下一个节点的概率的倒数)`
* 最短路径已经用 `深绿色` 作了标记

### 更多 DAG 分词的演示
#### "王小明在北京的清华大学读书"
![DAG of xiaomin](.images/DAG_of_xiaomin.png)

### HMM 分词
因 HMM 模型单独分词性能不佳, 一般情况下只用于和其他模型的融合, 故不在此提供示例, 需要演示者,可在 在线的 Jupyter Notebook 找到使用的例子.

### DAG+HMM 分词
将前两个模型的结果融合，融合了 DAG 稳定的构词能力和 HMM 的新词发现能力，缺点是速度较慢

### 正向最大匹配法

具体介绍，请阅读博文 [构建中文分词器 - 正向最大匹配法](http://blog.xiaoquankong.ai/%E6%9E%84%E5%BB%BA%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%99%A8-%E6%AD%A3%E5%90%91%E6%9C%80%E5%A4%A7%E5%8C%B9%E9%85%8D%E6%B3%95/)

### 反向最大匹配法

具体介绍，请阅读博文 [构建中文分词器 - 反向最大匹配法](http://blog.xiaoquankong.ai/%E6%9E%84%E5%BB%BA%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%99%A8-%E5%8F%8D%E5%90%91%E6%9C%80%E5%A4%A7%E5%8C%B9%E9%85%8D%E6%B3%95/)

### 双向最大匹配法

具体介绍，请阅读博文 [构建中文分词器 - 双向最大匹配法](http://blog.xiaoquankong.ai/%E6%9E%84%E5%BB%BA%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%99%A8-%E5%8F%8C%E5%90%91%E6%9C%80%E5%A4%A7%E5%8C%B9%E9%85%8D%E6%B3%95/)

### 基于 CRF 的分词

TODO

# 依赖
只在 python 3.5+ 环境测试过，其他环境不做兼容性保障。

# 安装
新版本的 MicroTokenizer 引入了和 [SpaCy](https://spacy.io/) 类似的代码和模型分离的理念。这一理念具有以下优点：

* 极大减小 MicroTokenizer 安装包的大小。未分离版本的 MicroTokenizer 大约 20 MB，分离后将减少到 10 KB 的规模，将大大减少下载安装的时间。
* 给予模型最大的灵活性，用户可以下载想要的模型，多种模型可以同时共存，极大的方便用户的使用。
* 让用户定制化模型变得简单，用户可以将自己定制的模型打包成 Python package, 用管理 package 的方式管理模型。

为了兼容以前的使用方式，MicroTokenizer 安装包依旧带有模型数据。但为了获得以上的优势，建议使用代码和模型分离的方式。

## 安装 MicroTokenizer
### pip (推荐，稳定版本)
```bash
pip install MicroTokenizer
```

### source (最新特性版本)
```bash
pip install git+https://github.com/howl-anderson/MicroTokenizer.git
```
## 安装模型
这里我们选择下载和安装默认的 model package
```bash
MicroTokenizer download
```

上述命令将会自动下载和安装默认的模型。

# 如何使用

## 分词

### 使用基于 Loader 的方式（推荐）
```python
import MicroTokenizer

tokenizer_loader = MicroTokenizer.load()
tokenizer = tokenizer_loader.get_tokenizer()

input_text = '王小明在北京的清华大学读书。'

# 取消下面代码的注释，就可以使用相关的算法来分词。
#
# result = tokenizer.cut_by_HMM(input_text)
#
# result = tokenizer.cut_by_CRF(input_text)
#
# result = tokenizer.cut_by_max_match_forward(input_text)
#
# result = tokenizer.cut_by_max_match_backward(input_text)
#
# result = tokenizer.cut_by_max_match_bidirectional(input_text)
#
result = tokenizer.cut_by_DAG(input_text)

print(result)

```

输出：

```python
['小', '明', '在', '北京', '的', '清华大学', '读书', '。']

```

### 使用基于 legacy 的方式
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()

input_text = '王小明在北京的清华大学读书。'

# 取消下面代码的注释，就可以使用相关的算法来分词。
#
# result = tokenizer.cut_by_HMM(input_text)
#
# result = tokenizer.cut_by_CRF(input_text)
#
# result = tokenizer.cut_by_max_match_forward(input_text)
#
# result = tokenizer.cut_by_max_match_backward(input_text)
#
# result = tokenizer.cut_by_max_match_bidirectional(input_text)
#
result = tokenizer.cut_by_DAG(input_text)

print(result)

```

输出：

```python
['小', '明', '在', '北京', '的', '清华大学', '读书', '。']

```


## 导出 GraphML 文件

针对基于 DAG 的算法，用户可以到处 GraphML 文件，研究其工作原理。

```python
from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()
tokenizer.init_dag_tokenizer()

dag_tokenizer = tokenizer.dag_tokenizer
dag_tokenizer.graph_builder.build_graph("知识就是力量")
dag_tokenizer.graph_builder.write_graphml("output.graphml")

```

NOTE: 导出后的 `graphml` 文件可以使用 [Cytoscape](http://www.cytoscape.org/) 进行浏览和渲染

## 如何训练自己的模型
MicroTokenizer 也提供了非常强大工具帮助你训练工具。
安装 MicroTokenizer 后，你可以使用如下命令来训练模型。

```bash
MicroTokenizer train output_model_dir input_data.txt
```

`output_model_dir` 指定了输出目录，`input_data.txt` 则指定了输入文件。
输入文件的格式为纯文本格式，每个词语之间用空格隔开即可。



### 基于 Loader 的模型
MicroTokenizer 提供了非常强大的包和模型分离的机制，用户可以训练自己的数据并打包成一个普通的 python package, 安装就可以使用，非常强大。
首先我们先安装 cookiecutter， 这是一个项目创建工具，帮助我们快速创建所需的 package 模板。
```bash
pip install cookiecutter
```

利用 cookiecutter 创建我们 MicroTokenizer 专属的 package 格式。

```bash
cokiecutter https://github.com/howl-anderson/cookiecutter-MicroTokenizer
```

回答几个相关的问题后，就将为你生成一个 python package 在  `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` 位置。`{{ cookiecutter.xx }}` 为变量，具体值在上一步填写问题中得到。

|                    源文件                    |                                                                                      拷贝至目录                                                                                      |
| :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `A.pickle`、`B.pickle`、`vocabulary.pickle`  | `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `{{ cookiecutter.project_slug }}` / `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `hmm_based`        |
| `feature_func_list.pickle`、`model.crfsuite` | `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `{{ cookiecutter.project_slug }}` / `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `crf_based`        |
| `dict.txt`                                   | `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `{{ cookiecutter.project_slug }}` / `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / `dictionary_based` |

然后在 `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` 执行：
```bash
make dist
```

就可以在 `{{ cookiecutter.project_slug }}-{{ cookiecutter.version }}` / dist 目录得到 python package



### 基于 legacy 的模型

TODO

## 如何安装和使用自定义模型

### 基于 Loader 的模型
#### 安装
安装模型
```bash
MicroTokenzier download xxxx
```

`xxx` 为你的 package name (如果他在 pypi 上) 或者 package file 都可以


在这完成以后，为了更加方便的使用，你还可以建立一个符号链接

```bash
MicroTokenizer link xxxx xy
```

也就是将 xy 符号链接到 xxxx package

##### 使用
直接使用 xxxx package
```python
import xxx

tokenizer_loader = xxx.load()
tokenizer = tokenizer_loader.get_tokenizer()

...
```

使用 MicroTokenizer 的方式

```python
import MicroTokenizer

tokenizer_loader = MicroTokenizer.load('xxxx')
tokenizer = tokenizer_loader.get_tokenizer()

...
```

如果你建立了符号链接，那么你还可以用

```python
import MicroTokenizer

tokenizer_loader = MicroTokenizer.load('xy')
tokenizer = tokenizer_loader.get_tokenizer()

...
```

这里的 xy 和 上面的链接符号对应

### 基于 legacy 的模型

TODO

# Roadmap
* [DONE] DAG 模型融合 HMM 模型 以处理 OOV 以及提高 Performance
* [DONE] 和主流分词模型做一个分词能力的测试 @ [中文分词软件基准测试 | Chinese tokenizer benchmark](https://github.com/howl-anderson/Chinese_tokenizer_benchmark)
* [DONE] 使用 `Trie Tree` 来压缩运行时内存和改善前缀查找速度
* [DONE] 允许添加自定义 DAG 词典
* [DONE] 开发自定义 DAG 字典构造 Feature, 允许用户构建自己的 DAG 字典
* [DONE] 开发自定义 HMM 参数构建 Feature, 允许用户训练自己的 HMM 模型
* [DONE] 引入 CRF 分词模型，使用 python-crfsuite
* [DOING] 模型系统分成代码和模型两个部分，用户可以选择性的下载和安装模型以及让用户训练和安装定制的模型
* [TODO] 引入 char-level word embedding + Bi-LSTM + CRF 分词模型，参考 [FoolNLTK](https://github.com/rockyzhengwu/FoolNLTK)
* [TODO] 将预测和训练代码分成不同的模块
* [DOING] 添加测试代码，确保功能正常和 Python 2/3 的兼容性
* [TODO] 增加并发处理的能力
* [TODO] 允许用户非常方便的训练自己的模型包
* [DONE] 使用人明日报字典替换 jieba 提供的字典
* [TODO] 添加 jieba 兼容的 banana peel 接口
* [TODO] 使用 scikit-crfsuite 替代 python-crfsuite


# Credits
* 代码和模型分离所使用的机制和代码全部修改自 [SpaCy](https://spacy.io/) 项目
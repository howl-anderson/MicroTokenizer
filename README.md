# 微型中文分词器

一个微型的中文分词器，能够按照词语的频率（概率）来利用构建 DAG（有向无环图）来分词。

# 特点 / 特色

* 微型：主要代码只有一个文件，不足 200 行
* 面向教育：可以导出 `graphml` 格式的图结构文件，辅助学习者理解算法过程
* 良好的分词性能：由于使用类似 `结巴分词` 的算法，具有良好的分词性能
* 具有良好的扩展性：使用和 `结巴分词` 一样的字典文件，可以轻松添加自定义字典

# 演示

## 在线演示
在线的 Jupyter Notebook 在 [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/howl-anderson/MicroTokenizer/master?filepath=.notebooks%2FMicroTokenizer.ipynb)

## 离线演示
### 分词
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
### 有向无环图效果演示
![DAG of 'knowledge is power'](.images/DAG_of_knowledge_is_power.png)

#### 备注
* `<s>` 和 `</s>` 是图的起始和结束节点，不是实际要分词的文本
* 图中 Edge 上标注的是 `log(下一个节点的概率的倒数)`
* 最短路径已经用 `深绿色` 作了标记

### 更多演示
#### "王小明在北京的清华大学读书"
![DAG of xiaomin](.images/DAG_of_xiaomin.png)


# 依赖
只在 python 3.5+ 环境测试过，其他环境不做兼容性保障。

# 安装
## pip
```bash
pip install MicroTokenizer
```

## source
```console
pip install git+https://github.com/howl-anderson/MicroTokenizer.git
```

# 如何使用
## 分词
见上文

## 导出 GraphML 文件
```python
from MicroTokenizer.MicroTokenizer import MicroTokenizer

micro_tokenizer = MicroTokenizer()
micro_tokenizer.build_graph("知识就是力量")
micro_tokenizer.write_graphml("output.graphml")
```

# Roadmap
* 融合 HMM 模型 以处理 OOV 以及提高 Performance
* 和主流分词模型做一个分词能力的测试

# Credits

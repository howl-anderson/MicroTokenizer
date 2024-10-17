# MicroTokenizer: A Lightweight Chinese Tokenizer for Education and Research

[![Python package](https://github.com/howl-anderson/MicroTokenizer/actions/workflows/python-package.yml/badge.svg)](https://github.com/howl-anderson/MicroTokenizer/actions/workflows/python-package.yml) [![PyPI Status](https://img.shields.io/pypi/v/MicroTokenizer.svg)](https://pypi.python.org/pypi/MicroTokenizer)

MicroTokenizer is a lightweight Chinese tokenizer designed primarily for educational purposes, offering a simplified yet powerful way to understand the intricacies of natural language processing (NLP). This project implements multiple tokenization algorithms that provide practical examples for understanding the foundational concepts behind text segmentation in Chinese.

## Key Features

- **Educational Focus**: Designed to help learners understand the internal mechanics of tokenization algorithms by exporting graph structures in `graphml` format, enabling step-by-step visualization of the tokenization process.
- **High-Performance Tokenization**: Utilizes algorithms similar to the widely adopted Jieba tokenizer, delivering efficient and accurate segmentation.
- **Flexible Extensibility**: Compatible with Jieba's dictionary format, allowing easy integration of custom dictionaries.
- **Customizable Models**: Provides tools and scripts to train user-specific tokenization models, rather than relying solely on built-in models.

## Tokenization Algorithms Implemented

1. **DAG-Based Tokenization**: Uses word frequency (probability) to construct a Directed Acyclic Graph (DAG) for tokenization, using a `Trie Tree` to build a prefix dictionary.
2. **Hidden Markov Model (HMM)**: Implements a statistical approach to tokenization using the Hidden Markov Model.
3. **Hybrid DAG & HMM**: Combines the results of DAG and HMM to maximize segmentation granularity.
4. **Forward Maximum Matching (FMM)**
5. **Backward Maximum Matching (BMM)**
6. **Bidirectional Maximum Matching (BMM)**
7. **CRF-Based Tokenization**: Uses Conditional Random Fields (CRF) for context-sensitive segmentation.
8. **UnicodeScriptTokenizer**: Splits tokens when Unicode scripts change.
9. **EnsembleTokenizer**: Segments text using different tokenizers based on Unicode script, allowing for tailored tokenization approaches.

## Demonstrations

### Online Demo

- **Jupyter Notebook**: Experience an interactive walkthrough using [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/howl-anderson/MicroTokenizer/master?filepath=.notebooks%2FMicroTokenizer.ipynb)
- **Web Demo**: Access a live demo at [http://nlp_demo.xiaoquankong.ai/](http://nlp_demo.xiaoquankong.ai/)

### Offline Example
#### DAG Tokenization Example
```python
import MicroTokenizer

tokens = MicroTokenizer.cut("知识就是力量")
print(tokens)
```
Output:
```
['知识', '就是', '力量']
```

#### Loading Custom Dictionary
```python
import MicroTokenizer

# Without user-defined dictionary
tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)

# Loading user's custom dictionary
MicroTokenizer.load_userdict('user_dict.txt')

tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)
```
Content of `user_dict.txt`:
```
杭研 10
```
Output:
```
['「', '杭', '研', '」', '正确', '应该', '不会', '被', '切开']
['「', '杭研', '」', '正确', '应该', '不会', '被', '切开']
```
## Educational Features

This section demonstrates the internal weights and logic of the Directed Acyclic Graph (DAG) tokenization. The following image showcases the built-in visualization of the tokenizer, which aids learners in understanding the internal workings of the tokenization process.
![DAG of 'knowledge is power'](.images/DAG_of_knowledge_is_power.png)

**Notes**:

* `<s>` and `</s>` represent the start and end nodes of the graph, not the actual text to be tokenized.
* The labels on the edges indicate `log(reciprocal of the next node's probability)`.
* The shortest path is highlighted in `dark green`.

This visualization tool is a powerful educational resource, providing a clear and intuitive way to grasp the complexities of tokenization algorithms. This feature is done by using the `graphml` format, which can be exported by the tokenizer for further analysis and visualization.

### Exporting GraphML Files

For the DAG-based algorithm, users can export GraphML files to study its working principles.

```python
from MicroTokenizer import dag_tokenizer

dag_tokenizer.graph_builder.build_graph("Knowledge is power")
dag_tokenizer.graph_builder.write_graphml("output.graphml")
```

**NOTE**: The exported `graphml` file can be viewed and rendered using software like [Cytoscape](http://www.cytoscape.org/). The previous image was rendered using Cytoscape.

This feature allows users to delve deeper into the mechanics of the tokenization process, providing a hands-on approach to understanding and visualizing the algorithm's structure and behavior.

## Usage of tokenization methods

### Installation

```bash
pip install MicroTokenizer
```

### Basic Tokenization Methods

```python
from MicroTokenizer import (
    hmm_tokenizer,
    crf_tokenizer,
    dag_tokenizer,
    max_match_forward_tokenizer,
    max_match_backward_tokenizer,
    max_match_bidirectional_tokenizer,
)

input_text = "王小明在北京的清华大学读书。"

# Use different algorithms for tokenization.

result = hmm_tokenizer.segment(input_text)
print("HMM Tokenizer:", result)

result = crf_tokenizer.segment(input_text)
print("CRF Tokenizer:", result)

result = max_match_forward_tokenizer.segment(input_text)
print("Max Match Forward Tokenizer:", result)

result = max_match_backward_tokenizer.segment(input_text)
print("Max Match Backward Tokenizer:", result)

result = max_match_bidirectional_tokenizer.segment(input_text)
print("Max Match Bidirectional Tokenizer:", result)

result = dag_tokenizer.segment(input_text)
print("DAG Tokenizer:", result)
```

Output:
```python
HMM Tokenizer: ['小', '明', '在', '北京', '的', '清华大学', '读书', '。']
```

### Unicode Script Tokenization

```python
from MicroTokenizer.tokenizers.unicode_script.tokenizer import UnicodeScriptTokenizer

tokenizer = UnicodeScriptTokenizer()
tokens = tokenizer.segment("2021年时我在Korea的汉城听了이효리的にほんご这首歌。")
print([(token.text, token.script) for token in tokens])
```

Output:
```python
[('2021', 'Common'), ('年时我在', 'Han'), ('Korea', 'Latin'), ('的汉城听了', 'Han'), ('이효리', 'Hangul'), ('的', 'Han'), ('にほんご', 'Hiragana'), ('这首歌', 'Han'), ('。', 'Common')]
```

### Ensemble Tokenization

#### Multi-Language Segmentation

```python
from MicroTokenizer.tokenizers.ensemble.tokenizer import EnsembleTokenizer
from MicroTokenizer import dag_tokenizer

# Use EnsembleTokenizer to segment text based on different scripts.
tokenizer = EnsembleTokenizer({"Han": dag_tokenizer})
tokens = tokenizer.segment("2021年时我在Korea的汉城听了이효리的にほんご这首歌。")
print(tokens)
```

Output:
```python
['2021', '年', '时', '我', '在', 'Korea', '的', '汉城', '听', '了', '이효리', '的', 'にほんご', '这', '首', '歌', '。']
```

#### [Experimental] Pipeline-Based Tokenization Scheme

Provides stable extraction of numbers and email addresses. Differentiates between Chinese and English using different tokenization methods (defaults to whitespace segmentation for English).

```python
from MicroTokenizer.experimental import dag_tokenizer

tokens = dag_tokenizer.segment("我的电话是15555555555，邮箱是xxx@yy.com,工作单位是 Tokyo University。")
print(tokens)
```

Output:
```python
['我', '的', '电话', '是', '15555555555', '，', '邮箱', '是', 'xxx@yy.com', ',', '工作', '单位', '是', 'Tokyo', 'University', '。']
```


## Algorithm Explanation

You can find detailed exmaples and explanations of the tokenization algorithms in the following blog posts:

Forward Maximum Matching (FMM): [Building a Chinese Tokenizer - Forward Maximum Matching](http://blog.xiaoquankong.ai/building-chinese-tokenizer-forward-maximum-matching/)

Backward Maximum Matching (BMM): [Building a Chinese Tokenizer - Backward Maximum Matching](http://blog.xiaoquankong.ai/building-chinese-tokenizer-backward-maximum-matching/)

Bidirectional Maximum Matching (BMM): [Building a Chinese Tokenizer - Bidirectional Maximum Matching](http://blog.xiaoquankong.ai/building-chinese-tokenizer-bidirectional-maximum-matching/)

## Impact and Applications

MicroTokenizer aims to bridge the gap between theoretical understanding and practical application of NLP techniques, making it an ideal tool for:

- **Educational Institutions**: Suitable for courses on NLP, computational linguistics, and data science, providing students with a hands-on experience.
- **Research and Prototyping**: A lightweight toolkit for researchers to quickly test new tokenization ideas without the overhead of large frameworks.
- **Customization and Experimentation**: Ideal for those who want to experiment with customized models or tokenization techniques that cater to specific use-cases, such as specialized domains or new languages.

The hybrid and ensemble approaches implemented in MicroTokenizer provide unique perspectives on how multiple tokenization strategies can be integrated to enhance accuracy and robustness. This flexibility makes it not just an educational tool, but also a valuable component for developing innovative solutions in various NLP projects.

## Roadmap
- **[DONE]** Integrate DAG and HMM models to handle OOV (Out-of-Vocabulary) words and improve performance.
- **[DONE]** Benchmark against mainstream tokenization models ([Chinese tokenizer benchmark](https://github.com/howl-anderson/Chinese_tokenizer_benchmark)).
- **[DOING]** Split the model into code and model parts for optional downloads and user-specific customization.
- **[TODO]** Introduce char-level word embedding + Bi-LSTM + CRF model for tokenization.
- **[TODO]** Improve concurrency support and add compatibility with multiple Python versions.
- **[DONE]** Replace Jieba dictionary with an updated dictionary from Renmin Ribao.

## Get Involved
MicroTokenizer is an open-source project, and we welcome contributions from the community. Whether it's reporting bugs, proposing new features, or adding to the documentation, your input is valuable. Let's make Chinese NLP more accessible and insightful for everyone.

Feel free to check out the source code, run the demos, or experiment with your own models to see how tokenization can be tailored to your needs. Together, we can drive innovation in natural language processing.
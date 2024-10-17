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
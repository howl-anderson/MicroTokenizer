# Additional Documentation for MicroTokenizer

This document provides supplementary information that was mentioned in the original README but not covered in the enhanced version. It includes specific details about certain tokenization approaches, usage instructions, and other technical features that may be useful for advanced users or contributors.

## Detailed Tokenization Methods

### UnicodeScriptTokenizer
The **UnicodeScriptTokenizer** is used to split text when there is a change in Unicode scripts. This is particularly useful for handling texts that contain mixed languages or character sets. For example, when processing a string that contains both Latin and Chinese characters, this tokenizer helps in separating the segments based on script type.

### EnsembleTokenizer
The **EnsembleTokenizer** leverages different tokenizers depending on the Unicode script of the text segments. It first segments the text based on Unicode script changes and then applies an appropriate tokenizer to each segment. This method is particularly effective when dealing with multilingual texts, ensuring that each language is processed with a tokenizer optimized for it.

## Advanced Usage

### CRF Tokenizer
The **CRF-Based Tokenizer** uses Conditional Random Fields (CRF) for tokenization, allowing context-sensitive segmentation. The CRF model used in MicroTokenizer can be trained with user-specific data, which makes it adaptable for specialized domains or languages. Training your CRF model involves preparing a labeled dataset and using the provided training scripts to build a model that suits your needs.

### Training Custom Models
MicroTokenizer provides tools to train your own models instead of using built-in models. You can train:
- **DAG Dictionary**: Construct a custom Directed Acyclic Graph (DAG) dictionary to control the segmentation process.
- **HMM Parameters**: Train a Hidden Markov Model (HMM) using your dataset, allowing the tokenizer to better handle domain-specific vocabulary.
- **CRF Models**: Train your own CRF model to improve tokenization accuracy for specific contexts.

The training scripts and instructions are available within the project, allowing for full customization of the tokenization process.

## Loading User Dictionaries
MicroTokenizer supports loading custom user dictionaries to influence the segmentation process. To add a custom dictionary:
1. Create a text file (e.g., `user_dict.txt`) containing your custom words, each followed by an optional frequency weight.
2. Load the dictionary using the following code:

```python
import MicroTokenizer

# Load user-defined dictionary
MicroTokenizer.load_userdict('user_dict.txt')
```

This feature is especially useful when dealing with named entities or specialized vocabulary that are not present in the default dictionary.

## DAG Visualization
MicroTokenizer can export the structure of its DAG-based tokenization process in `graphml` format, which can then be visualized using tools such as yEd or Gephi. This feature allows learners to see the internal decision-making process of the tokenizer, making it an effective educational tool.

To generate a `graphml` representation of the DAG for a given input:

```python
import MicroTokenizer

# Generate a graphml representation
MicroTokenizer.export_dag_to_graphml("input_text", "output_file.graphml")
```

This visualization feature helps to understand how different paths are evaluated and selected during the tokenization process.

## Compatibility and Extensibility

- **Jieba Dictionary Compatibility**: MicroTokenizer is compatible with the Jieba dictionary format, making it easy to switch between the two or use existing resources.
- **Python Version Compatibility**: The tokenizer is being updated to ensure compatibility with both Python 2 and Python 3, though Python 3 is recommended for all new developments.

## Planned Features

- **Concurrent Processing**: Enhancing concurrency support to improve tokenization speed, especially when processing large datasets.
- **Banana Peel Interface**: Adding a Jieba-compatible banana peel interface to allow seamless integration for users familiar with Jieba's API.
- **Scikit-CRFsuite Integration**: Switching from `python-crfsuite` to `scikit-crfsuite` for improved performance and better support.
- **Char-Level Word Embedding + Bi-LSTM + CRF**: Introducing an advanced tokenization model that utilizes character-level embeddings combined with Bi-LSTM and CRF, inspired by the FoolNLTK project.

## Testing and Validation
MicroTokenizer includes testing scripts to ensure that its various tokenizers work as expected and are compatible across different Python versions. Users are encouraged to run these tests when contributing to the project or modifying its core features.

To run the tests:
```bash
python -m unittest discover tests/
```
This helps maintain stability and ensures the accuracy of tokenization across updates and different environments.


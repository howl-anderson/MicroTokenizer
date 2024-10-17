#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

long_description = """
MicroTokenizer: A Lightweight and Educational Chinese Tokenizer

MicroTokenizer is a lightweight, flexible, and powerful Chinese tokenizer designed for educational and research purposes. Its core objective is to simplify the understanding of natural language processing (NLP) techniques, offering a hands-on approach to text segmentation. This package not only delivers practical solutions for tokenizing Chinese text but also provides insight into how various tokenization methods work, making it an excellent resource for students, researchers, and NLP practitioners.

### Key Features and Impact

- **Educational Focus**: MicroTokenizer is crafted with an educational purpose in mind. It enables learners to understand the inner workings of tokenization algorithms by providing visual representations of their processes. Users can export graph structures in `graphml` format to visualize the tokenization pathways, facilitating a deeper comprehension of text processing.

- **High Performance and Customization**: The package implements several state-of-the-art tokenization techniques, including DAG-based segmentation, HMM, CRF, and hybrid methods. Its performance is on par with mainstream tokenizers like Jieba, but with greater flexibility, allowing users to easily integrate custom dictionaries or train their models to suit specific needs.

- **Extensive Tokenization Algorithms**: MicroTokenizer includes multiple tokenization approaches, such as:
  - Directed Acyclic Graph (DAG)-based segmentation.
  - Hidden Markov Model (HMM) for statistical tokenization.
  - CRF (Conditional Random Fields) for context-sensitive tokenization.
  - Maximum Matching methods (Forward, Backward, and Bidirectional).
  - Unicode Script-based segmentation for handling multilingual text.
  - Ensemble approaches to combine the strengths of multiple tokenizers.

- **Research and Prototyping Tool**: Its lightweight nature makes MicroTokenizer ideal for prototyping and experimentation. Researchers can quickly test and refine tokenization techniques without the overhead of large-scale frameworks. The CRF-based tokenizer, for example, can be trained using user-specific data, providing customization for unique domains.

- **Community-Centric and Open Source**: MicroTokenizer is an open-source project, inviting collaboration and contributions from developers, educators, and researchers. Its development roadmap includes features aimed at enhancing user experience, expanding tokenization capabilities, and ensuring compatibility across diverse Python environments.

### Applications

- **Academic Use**: MicroTokenizer is perfect for use in NLP, linguistics, and data science courses. It helps students grasp the fundamentals of Chinese text segmentation and explore advanced models like CRF and hybrid tokenization.
- **Custom NLP Solutions**: Users can create their dictionaries and models, tailoring tokenization to specialized contexts, such as legal documents, medical records, or technical manuals, thereby enhancing accuracy and utility.
- **Educational and Research Projects**: The unique ability to visualize tokenization processes and train custom models makes MicroTokenizer a valuable resource for those conducting research or building educational tools in NLP.

### Get Involved
MicroTokenizer is more than just a tokenizer; it’s a community-driven effort to make NLP accessible. We welcome contributions and feedback from the community to improve and expand its capabilities.

Explore, contribute, or simply learn—MicroTokenizer aims to empower the next generation of NLP enthusiasts and experts.
"""

requirements = [
    'networkx', 'MicroHMM', 'python-crfsuite', 'pyyaml'
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest']

setup(
    author="Xiaoquan Kong",
    author_email='u1mail2me@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A micro tokenizer for Chinese",
    entry_points={
        'console_scripts': [
            'MicroTokenizer=MicroTokenizer.cli.main:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    include_package_data=True,
    keywords='MicroTokenizer',
    name='MicroTokenizer',
    packages=find_packages(include=['MicroTokenizer', 'MicroTokenizer.*']),
    data_files=[(
        '',
        [
            'MicroTokenizer/model_data/dict.txt',

            'MicroTokenizer/model_data/A.pickle',
            'MicroTokenizer/model_data/B.pickle',
            'MicroTokenizer/model_data/vocabulary.pickle',
            'MicroTokenizer/model_data/feature_func_list.pickle',
            'MicroTokenizer/model_data/model.crfsuite'
        ]
    )],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/howl-anderson/MicroTokenizer',
    version="0.21.3",
    zip_safe=False,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

long_description = """
微型中文分词器
==============

一个微型的中文分词器，目前提供了七种分词算法:


#. 按照词语的频率（概率）来利用构建 DAG（有向无环图）来分词，使用 ``Trie Tree`` 构建前缀字典树
#. 使用隐马尔可夫模型（Hidden Markov Model，HMM）来分词
#. 融合 DAG 和 HMM 两种分词模型的结果，按照分词粒度最大化的原则进行融合得到的模型
#. 正向最大匹配法
#. 反向最大匹配法
#. 双向最大匹配法
#. 基于 CRF (Conditional Random Field, 条件随机场) 的分词方法

特点 / 特色
===========


* 面向教育：可以导出 ``graphml`` 格式的图结构文件，辅助学习者理解算法过程
* 良好的分词性能：由于使用类似 ``结巴分词`` 的算法，具有良好的分词性能
* 具有良好的扩展性：使用和 ``结巴分词`` 一样的字典文件，可以轻松添加自定义字典
* 自定义能力强
* 提供工具和脚本帮助用户训练自己的分词模型而不是使用内建的模型

----

更多内容见仓库 https://github.com/howl-anderson/MicroTokenizer
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
    version="0.21.2",
    zip_safe=False,
)

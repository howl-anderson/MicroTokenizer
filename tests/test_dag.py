#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from MicroTokenizer.dag import DAGTokenizer


def test_train():
    tokenizer = DAGTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()
    result = tokenizer.segment("你打人")

    pytest.helpers.assert_token_equals(result, "你打人")


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = DAGTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()
    tokenizer.persist_to_dir(temp_path_str)

    assert len(temp_path.listdir()) == 1


def test_segment():
    tokenizer = DAGTokenizer()
    tokenizer.load_model()
    result = tokenizer.segment("你打人")

    pytest.helpers.assert_token_equals(result, "你打人")

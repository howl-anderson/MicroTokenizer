#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `MicroTokenizer` package."""
import pytest

from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer


def test_train():
    tokenizer = MaxMatchForwardTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()

    input_text = "你打人"

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = MaxMatchForwardTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()
    tokenizer.persist_to_dir(temp_path_str)

    assert len(temp_path.listdir()) == 1


def test_segment():
    tokenizer = MaxMatchForwardTokenizer()
    tokenizer.load_model()

    input_text = "你打人"

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

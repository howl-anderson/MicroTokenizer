#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Tests for `MicroTokenizer` package."""
import pytest

from MicroTokenizer.hmm import HMMTokenizer


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("hmm")
    temp_path_str = str(temp_path)

    tokenizer = HMMTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()
    tokenizer.persist_to_dir(temp_path_str)

    assert len(temp_path.listdir()) == 3


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = HMMTokenizer()
    tokenizer.load_model()

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

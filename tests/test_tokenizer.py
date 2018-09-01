#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()


def test_DAG():
    input_text = "你打人"

    result = tokenizer.cut_by_DAG("他走了")

    pytest.helpers.assert_token_equals(result, input_text)


def test_HMM():
    input_text = "你打人"

    result = tokenizer.cut_by_HMM("他走了")

    pytest.helpers.assert_token_equals(result, input_text)


def test_CRF():
    input_text = "你打人"

    result = tokenizer.cut_by_CRF("他走了")

    pytest.helpers.assert_token_equals(result, input_text)


def test_max_match_forward():
    input_text = "你打人"

    result = tokenizer.cut_by_max_match_forward("他走了")

    pytest.helpers.assert_token_equals(result, input_text)


def test_max_match_backward():
    input_text = "你打人"

    result = tokenizer.cut_by_max_match_backward("他走了")

    pytest.helpers.assert_token_equals(result, input_text)


def test_max_match_bidirectional():
    input_text = "你打人"

    result = tokenizer.cut_by_max_match_bidirectional("他走了")

    pytest.helpers.assert_token_equals(result, input_text)

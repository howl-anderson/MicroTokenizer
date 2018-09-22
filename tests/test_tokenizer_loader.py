#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from MicroTokenizer import load

tokenizer_loader = load('pd')
tokenizer = tokenizer_loader.get_tokenizer()


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_DAG(input_text):
    result = tokenizer.cut_by_DAG(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_HMM(input_text):
    result = tokenizer.cut_by_HMM(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_CRF(input_text):
    result = tokenizer.cut_by_CRF(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_max_match_forward(input_text):
    result = tokenizer.cut_by_max_match_forward(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_max_match_backward(input_text):
    result = tokenizer.cut_by_max_match_backward(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_max_match_bidirectional(input_text):
    result = tokenizer.cut_by_max_match_bidirectional(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

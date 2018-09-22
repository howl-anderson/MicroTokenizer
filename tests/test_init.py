#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

import MicroTokenizer


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_DAG(input_text):
    result = MicroTokenizer.cut_by_DAG(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_HMM(input_text):
    result = MicroTokenizer.cut_by_HMM(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_CRF(input_text):
    result = MicroTokenizer.cut_by_CRF(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_joint_model(input_text):
    result = MicroTokenizer.cut_by_joint_model(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

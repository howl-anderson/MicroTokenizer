#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import MicroTokenizer


def test_DAG():
    input_text = "你打人"
    result = MicroTokenizer.cut_by_DAG(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


def test_HMM():
    input_text = "你打人"
    result = MicroTokenizer.cut_by_HMM(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


def test_CRF():
    input_text = "你打人"
    result = MicroTokenizer.cut_by_CRF(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


def test_joint_model():
    input_text = "你打人"
    result = MicroTokenizer.cut_by_joint_model(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

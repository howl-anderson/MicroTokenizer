# -*- coding: utf-8 -*-
from __future__ import unicode_literals

pytest_plugins = ['helpers_namespace']

import pytest


@pytest.helpers.register
def assert_token_equals(left_value, right_vlue):
    assert type(left_value) == list

    assert "".join(left_value) == right_vlue


@pytest.helpers.register
def tokenizer_test_cases():
    test_cases = [
        '.',
        '人',
        '人们',
        '盖浇饭'
    ]

    # return as list of list
    return test_cases

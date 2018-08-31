pytest_plugins = ['helpers_namespace']

import pytest


@pytest.helpers.register
def assert_token_equals(left_value, right_vlue):
    assert type(left_value) == list

    assert "".join(left_value) == right_vlue

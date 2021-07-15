import pytest

from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer import default_model_dir


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_train(input_text):
    tokenizer = MaxMatchBackwardTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = MaxMatchBackwardTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])
    tokenizer.save(temp_path_str)

    assert len(temp_path.listdir()) == 1


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = MaxMatchBackwardTokenizer.load(default_model_dir)

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

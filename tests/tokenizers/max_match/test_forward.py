import pytest

from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer import default_model_dir


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_train(input_text):
    tokenizer = MaxMatchForwardTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_persist(tmpdir, input_text):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = MaxMatchForwardTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])
    tokenizer.save(temp_path_str)

    assert len(temp_path.listdir()) == 1

    roundtrip_tokenizer = MaxMatchForwardTokenizer.load(temp_path)
    result = roundtrip_tokenizer.segment(input_text)
    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = MaxMatchForwardTokenizer.load(default_model_dir)

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

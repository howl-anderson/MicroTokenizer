import pytest

from MicroTokenizer import default_model_dir
from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_persist(tmpdir, input_text):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = CRFTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])
    tokenizer.save(temp_path_str)

    assert len(temp_path.listdir()) == 2

    roundtrip_tokenizer = CRFTokenizer.load(temp_path)
    result = roundtrip_tokenizer.segment(input_text)
    pytest.helpers.assert_token_equals(result, input_text)


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = CRFTokenizer.load(default_model_dir)

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

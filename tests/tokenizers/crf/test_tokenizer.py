import pytest

from MicroTokenizer import default_model_dir
from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("dag")
    temp_path_str = str(temp_path)

    tokenizer = CRFTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])
    tokenizer.save(temp_path_str)

    assert len(temp_path.listdir()) == 2


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = CRFTokenizer.load(default_model_dir)

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)

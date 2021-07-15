import pytest

from MicroTokenizer.tokenizers.hmm_tokenizer import HMMTokenizer
from MicroTokenizer import default_model_dir


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("hmm")
    temp_path_str = str(temp_path)

    tokenizer = HMMTokenizer()
    tokenizer.train([["我", "是", "中国人"], ["你", "打", "人"]])
    tokenizer.save(temp_path_str)

    assert len(temp_path.listdir()) == 3


@pytest.mark.parametrize("input_text", pytest.helpers.tokenizer_test_cases())
def test_segment(input_text):
    tokenizer = HMMTokenizer.load(default_model_dir)

    result = tokenizer.segment(input_text)

    pytest.helpers.assert_token_equals(result, input_text)
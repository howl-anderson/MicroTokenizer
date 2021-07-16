import pytest

from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer
from MicroTokenizer.tokenizers.dag_tokenizer import DAGTokenizer
from MicroTokenizer.tokenizers.hmm_tokenizer import HMMTokenizer
from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.tokenizers.max_match.bidirectional import (
    MaxMatchBidirectionalTokenizer,
)
from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.training.train import train


# @pytest.mark.skip("It will takes 670s to complete, too slow")
def test_main(tmpdir, datadir):
    input_file_list = [datadir / "data.txt"]
    output_dir = str(tmpdir)

    train(input_file_list, output_dir)

    # asserts start at here
    input_text = "王小明在北京的清华大学读书。"

    # asserts start from here

    hmm_tokenizer_v2 = HMMTokenizer.load(output_dir)
    result = hmm_tokenizer_v2.segment(input_text)
    print(result)

    crf_tokenizer_v2 = CRFTokenizer.load(output_dir)
    result = crf_tokenizer_v2.segment(input_text)
    print(result)

    max_match_forward_tokenizer_v2 = MaxMatchForwardTokenizer.load(output_dir)
    result = max_match_forward_tokenizer_v2.segment(input_text)
    print(result)

    max_match_backward_tokenizer_v2 = MaxMatchBackwardTokenizer.load(output_dir)
    result = max_match_backward_tokenizer_v2.segment(input_text)
    print(result)

    max_match_bidirectional_tokenizer_v2 = MaxMatchBidirectionalTokenizer.load(
        output_dir
    )
    result = max_match_bidirectional_tokenizer_v2.segment(input_text)
    print(result)

    dag_tokenizer_v2 = DAGTokenizer.load(output_dir)
    result = dag_tokenizer_v2.segment(input_text)
    print(result)

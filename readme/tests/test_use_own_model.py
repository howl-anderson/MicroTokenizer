from MicroTokenizer import MaxMatchBackwardTokenizer
from MicroTokenizer import MaxMatchForwardTokenizer
from MicroTokenizer import MaxMatchBidirectionalTokenizer
from MicroTokenizer import DAGTokenizer
from MicroTokenizer import HMMTokenizer
from MicroTokenizer import CRFTokenizer

def test_main(datadir):
    model_dir = str(datadir)
    input_text = "你的待分词文本"

    max_match_backward_tokenizer = MaxMatchBackwardTokenizer.load(model_dir)
    tokens = max_match_backward_tokenizer.segment(input_text)

    max_match_forward_tokenizer = MaxMatchForwardTokenizer.load(model_dir)
    tokens = max_match_forward_tokenizer.segment(input_text)

    max_match_bidirectional_tokenizer = MaxMatchBidirectionalTokenizer.load(model_dir)
    tokens = max_match_bidirectional_tokenizer.segment(input_text)

    dag_tokenizer = DAGTokenizer.load(model_dir)
    tokens = dag_tokenizer.segment(input_text)

    hmm_tokenizer = HMMTokenizer.load(model_dir)
    tokens = hmm_tokenizer.segment(input_text)

    crf_tokenizer = CRFTokenizer.load(model_dir)
    tokens = crf_tokenizer.segment(input_text)

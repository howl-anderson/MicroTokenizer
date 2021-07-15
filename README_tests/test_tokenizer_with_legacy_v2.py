def test_main():
    from MicroTokenizer import (
        hmm_tokenizer_v2,
        crf_tokenizer_v2,
        dag_tokenizer_v2,
        max_match_forward_tokenizer_v2,
        max_match_backward_tokenizer_v2,
        max_match_bidirectional_tokenizer_v2,
    )

    input_text = "王小明在北京的清华大学读书。"

    # 使用相关的算法来分词。

    result = hmm_tokenizer_v2.segment(input_text)
    print(result)

    result = crf_tokenizer_v2.segment(input_text)
    print(result)

    result = max_match_forward_tokenizer_v2.segment(input_text)
    print(result)

    result = max_match_backward_tokenizer_v2.segment(input_text)
    print(result)

    result = max_match_bidirectional_tokenizer_v2.segment(input_text)
    print(result)

    result = dag_tokenizer_v2.segment(input_text)
    print(result)

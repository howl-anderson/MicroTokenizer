def test_main():
    from MicroTokenizer import (
        hmm_tokenizer,
        crf_tokenizer,
        dag_tokenizer,
        max_match_forward_tokenizer,
        max_match_backward_tokenizer,
        max_match_bidirectional_tokenizer,
    )

    input_text = "王小明在北京的清华大学读书。"

    # 使用相关的算法来分词。

    result = hmm_tokenizer.segment(input_text)
    print(result)

    result = crf_tokenizer.segment(input_text)
    print(result)

    result = max_match_forward_tokenizer.segment(input_text)
    print(result)

    result = max_match_backward_tokenizer.segment(input_text)
    print(result)

    result = max_match_bidirectional_tokenizer.segment(input_text)
    print(result)

    result = dag_tokenizer.segment(input_text)
    print(result)

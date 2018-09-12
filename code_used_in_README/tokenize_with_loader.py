import MicroTokenizer

tokenizer_loader = MicroTokenizer.load()
tokenizer = tokenizer_loader.get_tokenizer()

input_text = '王小明在北京的清华大学读书。'

# 取消下面代码的注释，就可以使用相关的算法来分词。
#
# result = tokenizer.cut_by_HMM(input_text)
#
# result = tokenizer.cut_by_CRF(input_text)
#
# result = tokenizer.cut_by_max_match_forward(input_text)
#
# result = tokenizer.cut_by_max_match_backward(input_text)
#
# result = tokenizer.cut_by_max_match_bidirectional(input_text)
#
result = tokenizer.cut_by_DAG(input_text)

print(result)

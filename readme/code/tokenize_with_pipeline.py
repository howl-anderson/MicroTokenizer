from MicroTokenizer.experimental import dag_tokenizer

tokens = dag_tokenizer.segment("我的电话是15555555555，邮箱是xxx@yy.com,工作单位是 Tokyo University。")
print(tokens)
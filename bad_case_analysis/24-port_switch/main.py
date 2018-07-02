from MicroTokenizer.MicroTokenizer import MicroTokenizer

micro_tokenizer = MicroTokenizer()
micro_tokenizer.build_graph("二十四口交换机")
micro_tokenizer.write_graphml("output.graphml")

from MicroTokenizer import dag_tokenizer

dag_tokenizer.graph_builder.build_graph("知识就是力量")
dag_tokenizer.graph_builder.write_graphml("output.graphml")

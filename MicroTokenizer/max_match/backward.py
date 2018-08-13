

from MicroTokenizer.DAG.graph_builder.graph_builder import GraphBuilder


class MaxMatchBackwardTokenizer(GraphBuilder):
    def process(self, message):
        reversed_token_result = []

        current_message = message
        while True:
            token_weight_pair = list(
                self.dict_data.get_token_and_weight_at_text_head(
                    current_message)
            )

            max_match = None

            if token_weight_pair:
                sorted_token_weight_pair = sorted(token_weight_pair,
                                                  key=lambda x: len(x[0]),
                                                  reverse=True)

                max_match = sorted_token_weight_pair[0][0]

            else:  # OOV now
                max_match = current_message[-1]

            reversed_token_result.append(max_match)

            current_message = current_message[: - len(max_match)]

            if not current_message:
                # no more message
                break

        return list(reversed(reversed_token_result))


if __name__ == "__main__":
    from MicroTokenizer import default_model_dir, get_dict_file
    from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm

    dag_dict_file = get_dict_file(default_model_dir)

    dict_data = TrieAlgorithm(dag_dict_file, reverse=True)

    tokenizer = MaxMatchBackwardTokenizer(dict_data)

    result = tokenizer.process("中国的首都是北京")
    print(result)

    result = tokenizer.process("我们在野生动物园玩")
    print(result)

    result = tokenizer.process("王小明在北京的清华大学读书。")
    print(result)


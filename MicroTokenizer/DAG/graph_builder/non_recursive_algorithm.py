# -*- coding: utf-8 -*-

from MicroTokenizer.DAG.graph_builder.graph_builder import GraphBuilder
from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData


class NonRecursiveAlgorithm(GraphBuilder):
    def __init__(self, dict_data):
        # type: (DictionaryData) -> None
        super(NonRecursiveAlgorithm, self).__init__(dict_data)

    def build_graph(self, message):
        cached_process_result = {}  # dictionary: message => list of head node

        # previous_node, text_message, char_offset, weight_for_previous_node
        previous_node_and_message_pair = [(self.start_node_id, message, 0, 0)]

        while True:
            new_previous_node_and_message_pair = []
            for previous_node, current_message, offset, previous_node_weight in previous_node_and_message_pair:
                work_list = []

                if not current_message:  # end of a message
                    self.add_edge(previous_node, self.end_node_id,
                                  previous_node_weight)
                    continue

                # try find a cache
                if current_message in cached_process_result:
                    for head_node in cached_process_result.get(current_message):
                        self.add_edge(previous_node, head_node,
                                      previous_node_weight)
                    continue

                token_weight_pair = list(
                    self.dict_data.get_token_and_weight_at_text_head(
                    current_message)
                )

                for token, current_weight in token_weight_pair:
                    work_list.append(
                        self.build_raw_node(token, previous_node,
                                            current_message, offset,
                                            previous_node_weight,
                                            current_weight)
                    )

                if not token_weight_pair:  # it's OOV
                    # to deal with OOV, any single char will treat as a token
                    token = current_message[0]

                    # FIXME: need deal with OOV, current very basic strategy
                    default_node_weight = 0.001

                    work_list.append(
                        self.build_raw_node(token, previous_node,
                                            current_message, offset,
                                            previous_node_weight,
                                            default_node_weight)
                    )

                cached_process_result[current_message] = list(
                    map(lambda x: x[0], work_list))

                new_previous_node_and_message_pair.extend(work_list)

            previous_node_and_message_pair = new_previous_node_and_message_pair

            if not previous_node_and_message_pair:
                # no more working need to do
                break

    def build_raw_node(self, token, previous_node, current_message, offset,
                       previous_node_weight, current_weight):
        token_weight = current_weight

        len_token = len(token)
        token_offset = offset + len_token

        node_id = "{}-{}".format(offset, token_offset)

        # ensure node exists
        if node_id not in self.G.nodes:
            self.G.add_node(node_id, label=token)

        self.add_edge(previous_node, node_id, previous_node_weight)

        remain_message = current_message[len_token:]

        return node_id, remain_message, token_offset, token_weight

    def add_edge(self, prev_node_id, node_id, prev_node_weight):
        # prev_node_round_weight used to better display of long digital value
        # e.g. 2.12343234234234324 to 2.13
        prev_node_round_weight = round(prev_node_weight, 2)

        self.G.add_edge(prev_node_id, node_id,
                        weight=prev_node_weight,
                        round_weight=prev_node_round_weight,
                        shortest_path=False)


if __name__ == "__main__":
    from timer_cm import Timer

    graph_builder = NonRecursiveAlgorithm()

    with Timer('Building DAG graph'):
        for _ in range(1):
            graph_builder.init_graph()
            graph_builder.build_graph("王小明在北京的清华大学读书。")

    graph_builder.compute_shortest_path()

    result = graph_builder.get_tokens()
    print(result)

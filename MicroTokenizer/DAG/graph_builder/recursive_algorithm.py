# -*- coding: utf-8 -*-


from MicroTokenizer.DAG.graph_builder.graph_builder import GraphBuilder


class RecursiveAlgorithm(GraphBuilder):
    def __init__(self, dict_data):
        super(RecursiveAlgorithm, self).__init__(dict_data)

        self.processed_working_str = dict()

    def build_graph(self, message):
        # FIXME: if the message is very long (about 500), it will raise
        # RecursionError: maximum recursion depth exceeded while calling a Python object
        self.create_node_from_string(
            message,
            self.start_node_id,
            0,
            0.0  # using 0.0 than 0, used to fix bug that graphml file have two weight attributes
        )

        self.compute_shortest_path()

        # set edge's attribute: `shortest_path` in shortest path to be True
        i = self.shortest_path[0]  # get initial start_node_id
        for j in self.shortest_path[1:]:
            self.G.edges[i, j]['shortest_path'] = True

            # update start_node_id
            i = j

    def create_node_from_string(self, working_str, previous_node_id, offset, previous_node_weight):
        # previous_node_round_weight used to better display of long digital value (e.g. 2.12343234234234324 to 2.13)
        previous_node_round_weight = round(previous_node_weight, 2)

        if working_str in self.processed_working_str:  # this working str have been processed already
            for next_node_id in self.processed_working_str[working_str]:  # get all next_node_id
                self.G.add_edge(previous_node_id, next_node_id,
                                weight=previous_node_weight,
                                round_weight=previous_node_round_weight,
                                shortest_path=False)

            return  # end of the execution

        if working_str == "":  # if no more working str, add current node to the end node.
            self.G.add_edge(previous_node_id, self.end_node_id,
                            weight=previous_node_weight,
                            round_weight=previous_node_round_weight,
                            shortest_path=False)
            return  # end of the execution

        used_token = set()  # used to trace what token used for this working str
        head_token_id_set = set()  # used to trace what token id used for this working str as a head
        token_weight_pair = self.dict_data.get_token_and_weight_at_text_head(working_str)

        for token, current_weight in token_weight_pair:
            used_token.add(token)

            next_node_id = self.setup_node_edge_relationship(working_str, previous_node_id, offset, previous_node_weight, token, current_weight)
            head_token_id_set.add(next_node_id)

        single_symbol_token = working_str[0]

        if single_symbol_token not in used_token:
            token = single_symbol_token

            # FIXME: need deal with OOV, current very basic strategy
            default_node_weight = 0.001

            next_node_id = self.setup_node_edge_relationship(working_str, previous_node_id, offset, previous_node_weight, token, default_node_weight)
            head_token_id_set.add(next_node_id)

        self.processed_working_str[working_str] = head_token_id_set

    def setup_node_edge_relationship(self, working_str, previous_node_id, offset, previous_node_weight, token, current_weight):
        # previous_node_round_weight used to better display of long digital value (e.g. 2.12343234234234324 to 2.13)
        previous_node_round_weight = round(previous_node_weight, 2)

        len_of_token = len(token)

        next_offset = offset + len_of_token
        next_working_str = working_str[len_of_token:]

        # always treat single char as symbol
        current_node_id = "{}-{}".format(offset, next_offset)


        current_node_weight = current_weight

        self.G.add_node(current_node_id, label=token)

        self.G.add_edge(previous_node_id, current_node_id,
                        weight=previous_node_weight,
                        round_weight=previous_node_round_weight,
                        shortest_path=False)

        # continue process remained string
        self.create_node_from_string(next_working_str, current_node_id, next_offset, current_node_weight)
        return current_node_id


if __name__ == "__main__":
    from timer_cm import Timer

    graph_builder = RecursiveAlgorithm()

    with Timer('Building DAG graph'):
        for _ in range(100):
            graph_builder.init_graph()
            graph_builder.processed_working_str = dict()
            graph_builder.build_graph("王小明在北京的清华大学读书。")

    graph_builder.compute_shortest_path()

    result = graph_builder.get_tokens()
    print(result)

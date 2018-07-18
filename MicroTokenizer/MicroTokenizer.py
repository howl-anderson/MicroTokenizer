# -*- coding: utf-8 -*-

"""Main module."""
import math
import os

import matplotlib.pyplot as plt
import networkx as nx

current_dir = os.path.dirname(os.path.abspath(__file__))

default_dict_file = os.path.join(current_dir, 'dictionary', 'dict.txt')


class MicroTokenizer(object):
    def __init__(self, dict_data=None):
        if dict_data is None:
            self.dict_data = self.read_dict(default_dict_file)
            self.compute_edge_weight(self.dict_data)
        else:
            self.dict_data = dict_data

        self.G = nx.DiGraph()

        self.node_labels = dict()

        self.start_node_id = '<s>'
        self.end_node_id = '</s>'

        self.setup_start_end_nodes()

        self.processed_working_str = dict()
        self.shortest_path = None

    def setup_start_end_nodes(self):
        # setup node instance
        self.G.add_node(self.start_node_id, label=self.start_node_id)
        self.node_labels[self.start_node_id] = self.start_node_id

        self.G.add_node(self.end_node_id, label=self.end_node_id)
        self.node_labels[self.end_node_id] = self.end_node_id

    @staticmethod
    def read_dict(dict_file):
        dict_data = {}

        with open(dict_file, encoding='utf_8') as fd:
            for line in fd:
                splited_line = line.split(' ')
                data = dict(enumerate(splited_line))

                token = data[0]
                frequency = data[1].strip()  # using strip to clean tailing newline symbol
                part_of_speech = data.get(2, '').strip()  # using strip to clean tailing newline symbol

                # print(token, frequency)

                dict_data[token] = int(frequency)

        return dict_data

    @staticmethod
    def compute_edge_weight(dict_data):
        # get total weight count for compute possibility
        total_weight = sum(dict_data.values())

        # recompute the weight
        for k, v in dict_data.items():
            # possibility = count / total_count
            # reciprocal of possibility can turn max value to min value, which can be
            # used for search max value path by search shortest path
            # log function can turn multiplication to addition: log(A * B) = log(A) + log(B)
            dict_data[k] = math.log(total_weight / v)

    def build_graph(self, message):
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

    def compute_shortest_path(self):
        if self.shortest_path is None:
            self.shortest_path = nx.shortest_path(self.G, source=self.start_node_id, target=self.end_node_id)

    def draw(self):
        nx.draw_kamada_kawai(self.G, with_labels=True, labels=self.node_labels)

        plt.show()

    def get_tokens(self):
        # get the labels of shortest path
        return [self.node_labels[i] for i in self.shortest_path]

    def write_graphml(self, graphml_file):
        nx.write_graphml(
            self.G,
            graphml_file,

            # Determine if numeric types should be generalized. For example,
            # if edges have both int and float 'weight' attributes,
            # we infer in GraphML that both are floats.
            infer_numeric_types=True
        )

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
        for token in self.dict_data.keys():
            if working_str.startswith(token):  # find a symbol starts with this char
                used_token.add(token)

                next_node_id = self.setup_node_edge_relationship(working_str, previous_node_id, offset, previous_node_weight, token)
                head_token_id_set.add(next_node_id)

        single_symbol_token = working_str[0]

        if single_symbol_token not in used_token:
            token = single_symbol_token
            next_node_id = self.setup_node_edge_relationship(working_str, previous_node_id, offset, previous_node_weight, token)
            head_token_id_set.add(next_node_id)

        self.processed_working_str[working_str] = head_token_id_set

    def setup_node_edge_relationship(self, working_str, previous_node_id, offset, previous_node_weight, token):
        # previous_node_round_weight used to better display of long digital value (e.g. 2.12343234234234324 to 2.13)
        previous_node_round_weight = round(previous_node_weight, 2)

        len_of_token = len(token)

        next_offset = offset + len_of_token
        next_working_str = working_str[len_of_token:]

        # always treat single char as symbol
        current_node_id = "{}-{}".format(offset, next_offset)

        # FIXME: need deal with OOV, current very basic strategy
        default_node_weight = 0.001
        current_node_weight = self.dict_data.get(token, default_node_weight)

        self.G.add_node(current_node_id, label=token)

        # add lables info, this method is wired in networkx
        self.node_labels[current_node_id] = token

        self.G.add_edge(previous_node_id, current_node_id,
                        weight=previous_node_weight,
                        round_weight=previous_node_round_weight,
                        shortest_path=False)

        # continue process remained string
        self.create_node_from_string(next_working_str, current_node_id, next_offset, current_node_weight)
        return current_node_id

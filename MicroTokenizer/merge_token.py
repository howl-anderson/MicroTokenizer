# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import networkx as nx


class MergeSolutions(object):
    def __init__(self):
        self.G = nx.DiGraph()
        self.start_node = '<start>'
        self.G.add_node(self.start_node, label=self.start_node)
        self.end_node = '<end>'
        self.G.add_node(self.end_node, label=self.end_node)

        self.existing_nodes = {self.start_node, self.end_node}
        self.existing_checkpoint_notes = set()

    def merge(self, candidate_token_list):
        for token_list in candidate_token_list:
            index = 0
            # default previous node is start node
            previous_node = self.start_node
            current_node = None
            current_checkpoint_node = None

            for token in token_list:
                current_node = "{}_{}".format(index, token)

                # update immediately
                index += len(token)

                current_checkpoint_node = "ck_{}".format(index)

                if current_node not in self.existing_nodes:
                    self.G.add_node(current_node, token=token, label=token)
                    self.existing_nodes.add(current_node)

                if current_checkpoint_node not in self.existing_checkpoint_notes:
                    self.G.add_node(current_checkpoint_node, token="", label=current_checkpoint_node)
                    self.existing_checkpoint_notes.add(current_checkpoint_node)

                self.G.add_edge(previous_node, current_node, weight=1)
                self.G.add_edge(current_node, current_checkpoint_node, weight=0)

                # update variable
                previous_node = current_checkpoint_node

            # link last token to end node
            self.G.add_edge(current_checkpoint_node, self.end_node, weight=1)

        raw_shortest_path_nodes = nx.shortest_path(
            self.G, source=self.start_node, target=self.end_node
        )

        # remove start and end nodes
        shortest_path_nodes = raw_shortest_path_nodes[1:-1]

        # remove all the checkpoint node
        cleaned_shortest_path_nodes = filter(
            lambda x: self.G.nodes.get(x).get('token'),
            shortest_path_nodes
        )

        # extract tokens
        best_solution_tokens = list(map(
            lambda x: self.G.nodes.get(x)['token'],
            cleaned_shortest_path_nodes
        ))

        return best_solution_tokens

    def write_graph(self, graph_path):
        nx.write_graphml(self.G, graph_path)


if __name__ == "__main__":
    solutions = [
        ['王小明', '来到', '了', '网易', '杭', '研', '大厦'],
        ['王', '小明', '来到', '了', '网易', '杭研', '大', '厦']
    ]
    merge_solutions = MergeSolutions()
    best_solution = merge_solutions.merge(solutions)

    print(best_solution)

    merge_solutions.write_graph("./test.graphml")

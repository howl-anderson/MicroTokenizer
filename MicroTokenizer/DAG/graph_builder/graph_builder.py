import networkx as nx

from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData


class GraphBuilder(object):
    def __init__(self, dict_data):
        # type: (DictionaryData) -> None

        self.dict_data = dict_data  # type: DictionaryData

        # define those value
        self.G = None
        self.start_node_id = None
        self.end_node_id = None

        self.init_graph()

        self.shortest_path = None

    def setup_start_end_nodes(self):
        # setup node instance
        self.G.add_node(self.start_node_id, label=self.start_node_id)

        self.G.add_node(self.end_node_id, label=self.end_node_id)

    def init_graph(self):
        self.G = nx.DiGraph()

        self.start_node_id = '<s>'
        self.end_node_id = '</s>'

        self.setup_start_end_nodes()

        self.shortest_path = None

    def compute_shortest_path(self):
        if self.shortest_path is None:
            self.shortest_path = nx.shortest_path(self.G, source=self.start_node_id, target=self.end_node_id)

    def get_tokens(self):
        # get the labels of shortest path
        return [self.G.nodes[i]['label'] for i in self.shortest_path]

    def write_graphml(self, graphml_file):
        nx.write_graphml(
            self.G,
            graphml_file,

            # Determine if numeric types should be generalized. For example,
            # if edges have both int and float 'weight' attributes,
            # we infer in GraphML that both are floats.
            infer_numeric_types=True
        )

    def build_graph(self, message):
        raise NotImplemented

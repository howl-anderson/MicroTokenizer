from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData


class TreeNode(dict):
    def __init__(self, *args, **kwargs):
        super(TreeNode, self).__init__(*args, **kwargs)

        self.is_leaf = False
        self.weight = None

    def set_as_leaf(self, weight):
        self.is_leaf = True
        self.weight = weight


class TrieAlgorithm(DictionaryData):
    def __init__(self, *args, **kwargs):
        reverse = kwargs.pop('reverse', False)

        super(TrieAlgorithm, self).__init__(*args, **kwargs)

        # reverse the char order from head to tail
        self.reverse = reverse

        self.tree_root = TreeNode()
        self.build_trie_tree()

    def build_trie_tree(self):
        for token, weight in self.dict_data.items():
            current_node = self.tree_root

            char_list = list(reversed(token)) if self.reverse else token

            for i in char_list:
                if i not in current_node:
                    current_node[i] = TreeNode()

                current_node = current_node[i]

            current_node.set_as_leaf(weight)

    def get_token_and_weight_at_text_head(self, text):
        char_list = list(reversed(text)) if self.reverse else text

        current_node = self.tree_root
        for index, char in enumerate(char_list):
            if char in current_node:
                char_node = current_node[char]

                if char_node.is_leaf:
                    token = char_list[:index+1]

                    token_weight_pair = (
                        "".join(reversed(token)) if self.reverse else token,
                        char_node.weight
                    )

                    yield token_weight_pair

                current_node = char_node

            else:
                break

    def add_token_and_weight(self, token, weight):
        if self.reverse:
            token = reversed(token)

        current_node = self.tree_root
        for i in token:
            if i not in current_node:
                current_node[i] = TreeNode()

            current_node = current_node[i]

        current_node.set_as_leaf(weight)

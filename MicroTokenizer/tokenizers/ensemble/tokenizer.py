from MicroTokenizer.tokenizers.unicode_script.tokenizer import UnicodeScriptTokenizer
from typing import Dict


class EnsembleTokenizer:
    def __init__(self, conf: Dict[str, object]):
        self.tokenizer_conf = conf
        self.unicode_script_tokenizer = UnicodeScriptTokenizer()

    def segment(self, text):
        tokens = []
        script_tokens = self.unicode_script_tokenizer.segment(text)
        for token in script_tokens:
            tokenizer = self.tokenizer_conf.get(token.script)
            if tokenizer is None:
                tokens.append(token.text)
            else:
                sub_tokens = tokenizer.segment(token.text)
                tokens.extend(sub_tokens)

        return tokens

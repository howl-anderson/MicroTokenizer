from typing import List
from MicroTokenizer.tokenizers.base_tokenizer import BaseTokenizer


class WhitespaceSplitTokenizer(BaseTokenizer):
    def segment(self, message):
        # type: (str) -> List[str]

        return message.strip().split()
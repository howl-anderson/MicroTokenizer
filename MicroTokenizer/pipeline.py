from typing import Any, Dict, List
import re

from MicroTokenizer.tokenizers.unicode_script.tokenizer import UnicodeScriptTokenizer


class Token:
    def __init__(self, text=None, unicode_script=None):
        self.text = text
        self.unicode_script = unicode_script

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"Token('{self.text}', '{self.unicode_script}')"


class BaseComponent:
    def process(self, message: Any) -> List[Any]:
        raise NotImplementedError


class UnicodeScriptComponent(BaseComponent):
    def __init__(self) -> None:
        super().__init__()

        self.tokenizer = UnicodeScriptTokenizer()

    def process(self, message: str) -> List[Any]:
        raw_tokens = self.tokenizer.segment(message)
        tokens = [
            Token(text=token.text, unicode_script=token.script) for token in raw_tokens
        ]

        return tokens


class RegularExpressComponent(BaseComponent):
    def __init__(self) -> None:
        super().__init__()

        self.re_number = re.compile(r"([0-9]+)")
        self.re_email = re.compile(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})")
        self.re_puncuation = re.compile(
            "([{}]+)".format("|".join(re.escape(",，.。?？!！:：")))
        )

    def process(self, message: List[Token]) -> List[Any]:
        # message = self._process_merge_common_latin(message)
        message = self._process_split_number(message)
        message = self._process_split_email(message)
        message = self._process_split_puncuation(message)
        return message

    def _process_split_email(self, message: List[Token]) -> List[Any]:
        result = []
        tokens_to_merge = []
        for token in message:
            if token.unicode_script in ["Common", "Latin"]:
                tokens_to_merge.append(token)
            else:
                # not target scipt, start to merge tokens
                if tokens_to_merge:
                    if len(tokens_to_merge) == 1:
                        result.append(tokens_to_merge[0])
                    else:
                        text = "".join(t.text for t in tokens_to_merge)
                        blocks = self.re_email.split(text)

                        for blk in blocks:
                            if not blk:
                                continue
                            if self.re_email.match(blk):
                                result.append(Token(text=blk, unicode_script="_Email"))
                            else:
                                result.append(
                                    Token(text=blk, unicode_script=token.unicode_script)
                                )

                    # reset
                    tokens_to_merge = []

                result.append(token)

        if tokens_to_merge:
            if len(tokens_to_merge) == 1:
                result.append(tokens_to_merge[0])
            else:
                text = "".join(t.text for t in tokens_to_merge)
                blocks = self.re_email.split(text)

                for blk in blocks:
                    if not blk:
                        continue
                    if self.re_email.match(blk):
                        result.append(Token(text=blk, unicode_script="_Email"))
                    else:
                        result.append(
                            Token(text=blk, unicode_script=token.unicode_script)
                        )

        return result

    def _process_merge_common_latin(self, message: List[Token]) -> List[Any]:
        result = []
        tokens_to_merge = []
        for token in message:
            if token.unicode_script in ["Common", "Latin"]:
                tokens_to_merge.append(token)
            else:
                # not target scipt, start to merge tokens
                if tokens_to_merge:
                    if len(tokens_to_merge) == 1:
                        result.append(tokens_to_merge[0])
                    else:
                        result.append(
                            Token(
                                text="".join(t.text for t in tokens_to_merge),
                                unicode_script="_MergedCommonLatin",
                            )
                        )

                    # reset
                    tokens_to_merge = []

                result.append(token)

        if tokens_to_merge:
            if len(tokens_to_merge) == 1:
                result.append(tokens_to_merge[0])
            else:
                result.append(
                    Token(
                        text="".join(t.text for t in tokens_to_merge),
                        unicode_script="_MergedCommonLatin",
                    )
                )

        return result

    def _process_split_puncuation(self, message: List[Token]) -> List[Any]:
        result = []
        for token in message:
            if token.unicode_script in ["Common", "_MergedCommonLatin"]:
                blocks = self.re_puncuation.split(token.text)

                for blk in blocks:
                    if not blk:
                        continue
                    if self.re_puncuation.match(blk):
                        for word in blk:
                            result.append(
                                Token(text=word, unicode_script="_Puncuation")
                            )
                    else:
                        result.append(
                            Token(text=blk, unicode_script=token.unicode_script)
                        )
            else:
                result.append(token)

        return result

    def _process_split_number(self, message: List[Token]) -> List[Any]:
        result = []
        for token in message:
            if token.unicode_script in ["Common", "_MergedCommonLatin"]:
                blocks = self.re_number.split(token.text)

                for blk in blocks:
                    if not blk:
                        continue
                    if self.re_number.match(blk):
                        result.append(Token(text=blk, unicode_script="_Number"))
                    else:
                        result.append(
                            Token(text=blk, unicode_script=token.unicode_script)
                        )
            else:
                result.append(token)

        return result


class Pipeline:
    def __init__(self, components):
        self.components = components

    def segment(self, message: str) -> List[Any]:
        outputs = message
        for component in self.components:
            outputs = component.process(outputs)

        return outputs


pipeline = Pipeline([UnicodeScriptComponent(), RegularExpressComponent()])


class PipelineUnicodeScriptTokenizer:
    def __init__(self, conf: Dict[str, object]):
        self.tokenizer_conf = conf
        self.pipeline = pipeline

    def segment(self, text):
        tokens = []
        script_tokens = self.pipeline.segment(text)
        # print(script_tokens)
        for token in script_tokens:
            tokenizer = self.tokenizer_conf.get(token.unicode_script)
            if tokenizer is None:
                tokens.append(token.text)
            else:
                sub_tokens = tokenizer.segment(token.text)
                tokens.extend(sub_tokens)

        return tokens

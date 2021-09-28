from MicroTokenizer.tokenizers.unicode_script.script_data import script_data
from MicroTokenizer.tokenizers.unicode_script.token import Token


class UnicodeScriptTokenizer:
    def segment(self, text):
        tokens = []

        current_script = None
        current_token_cache = []
        for char in text:
            script = self.script(char)
            if script != current_script:  # find script changes
                if current_script is None:
                    # skip it.
                    # becasue it changes from script None to a real script,
                    # there is no validate current_token_cache value
                    pass
                else:
                    # produce token
                    token = "".join(current_token_cache)
                    tokens.append(Token(token, current_script))

                # update for next iteration
                current_script = script
                current_token_cache = [char]
            else:
                current_token_cache.append(char)

        # turn tail chars to token
        token = "".join(current_token_cache)
        tokens.append(Token(token, current_script))

        return tokens

    @staticmethod
    def script_cat(chr):
        """For the unicode character chr return a tuple (Scriptname, Category)."""
        l = 0
        r = len(script_data["idx"]) - 1
        c = ord(chr)
        while r >= l:
            m = (l + r) >> 1
            if c < script_data["idx"][m][0]:
                r = m - 1
            elif c > script_data["idx"][m][1]:
                l = m + 1
            else:
                return (
                    script_data["names"][script_data["idx"][m][2]],
                    script_data["cats"][script_data["idx"][m][3]],
                )
        return "Unknown", "Zzzz"

    @classmethod
    def script(cls, chr):
        a, _ = cls.script_cat(chr)
        return a

    @classmethod
    def category(cls, chr):
        _, a = cls.script_cat(chr)
        return a

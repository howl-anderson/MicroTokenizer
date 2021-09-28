class Token:
    def __init__(self, text, script=None):
        self.text = text
        self.script = script

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"'{self.text}'"

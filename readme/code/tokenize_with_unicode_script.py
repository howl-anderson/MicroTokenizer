from MicroTokenizer.tokenizers.unicode_script.tokenizer import UnicodeScriptTokenizer


tokenizer = UnicodeScriptTokenizer()
tokens = tokenizer.segment("2021年时我在Korea的汉城听了이효리的にほんご这首歌。")
print([(token.text, token.script) for token in tokens])

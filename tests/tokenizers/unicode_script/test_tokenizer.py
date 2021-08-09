from MicroTokenizer.tokenizers.unicode_script.tokenizer import UnicodeScriptTokenizer

def test_tokenizer():
    result = UnicodeScriptTokenizer.script("汉")
    assert result

    tokenizer = UnicodeScriptTokenizer()
    result = tokenizer.segment("王小明在2021年的时候参加了TsingHua University的活动，并听了이효리的にほんご。")
    print(result)
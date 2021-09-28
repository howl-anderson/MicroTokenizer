from MicroTokenizer.pipeline import pipeline, PipelineUnicodeScriptTokenizer


def test_pipeline():
    result = pipeline.segment("我的电话是15555555555，邮箱是xxx@yy.com")

    print(result)


def test_tokenizer():
    from MicroTokenizer import dag_tokenizer

    tokenizer = PipelineUnicodeScriptTokenizer({"Han": dag_tokenizer})

    tokens = tokenizer.segment("2021年时我在Korea的汉城听了이효리的にほんご这首歌。")
    print(tokens)

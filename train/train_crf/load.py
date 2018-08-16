#!/usr/bin/env python

from MicroTokenizer.hmm import HMMTokenizer

hmm_tokenizer = HMMTokenizer.load_model()

result = hmm_tokenizer.predict("王小明在北京的清华大学读书。")
print(result)

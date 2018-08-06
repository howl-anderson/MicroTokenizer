#!/usr/bin/env python

from . import tool
from MicroTokenizer.hmm import HMMTokenizer

hmm_tokenizer = HMMTokenizer()

# tool.driver(19000, 100, hmm_tagger.train_one_line, hmm_tagger.predict)
tool.driver(290000, 1, hmm_tokenizer.train_one_line, hmm_tokenizer.predict)
hmm_tokenizer.hmm_model.do_train()
hmm_tokenizer.hmm_model.save_model()
result = hmm_tokenizer.predict("王小明在北京的清华大学读书。")
print(result)

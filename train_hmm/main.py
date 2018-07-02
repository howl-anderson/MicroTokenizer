#!/usr/bin/env python

from train_hmm import tool
from train_hmm.train import HMMTagger

hmm_tagger = HMMTagger()

# tool.driver(19000, 100, hmm_tagger.train_one_line, hmm_tagger.predict)
tool.driver(290000, 1, hmm_tagger.train_one_line, hmm_tagger.predict)
hmm_tagger.hmm_model.do_train()
hmm_tagger.hmm_model.save_model()
result = hmm_tagger.predict("王小明在北京的清华大学读书。")
print(result)

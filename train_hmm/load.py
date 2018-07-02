#!/usr/bin/env python

from train_hmm.train import HMMTagger

hmm_tagger = HMMTagger.load_model()

result = hmm_tagger.predict("王小明在北京的清华大学读书。")
print(result)

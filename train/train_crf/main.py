#!/usr/bin/env python

from . import tool
from MicroTokenizer.CRF.crf_trainer import CRFTrainer

crf_trainer = CRFTrainer()

# tool.driver(19000, 100, hmm_tagger.train_one_line, hmm_tagger.predict)
tool.driver(290000, 1, crf_trainer.train_one_line, crf_trainer.cut)

crf_trainer.crf_tagger.train('conll2002-esp.crfsuite')

result = crf_trainer.predict("王小明在北京的清华大学读书。")
print(result)

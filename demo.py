#!/usr/bin/env python

import MicroTokenizer

tokens = MicroTokenizer.cut_by_DAG("王小明来到了网易杭研大厦")
print(tokens)

tokens = MicroTokenizer.cut_by_HMM("王小明来到了网易杭研大厦")
print(tokens)

tokens = MicroTokenizer.cut_by_joint_model("王小明来到了网易杭研大厦")
print(tokens)

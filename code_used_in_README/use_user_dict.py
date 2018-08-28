import MicroTokenizer

tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)

# loading user's custom dictionary file
MicroTokenizer.load_userdict('user_dict.txt')

tokens = MicroTokenizer.cut("「杭研」正确应该不会被切开", HMM=False)
print(tokens)

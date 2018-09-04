from MicroHMM.hmm import HMMModel

from MicroTokenizer.base_loader import BaseLoader


class HMMLoader(BaseLoader):
    name = 'hmm_based'

    def __init__(self, *args, **kwargs):
        super(HMMLoader, self).__init__(*args, **kwargs)

    def from_disk(self, model_path, tokenizer_list, *args, **kwargs):
        hmm_model = HMMModel.load_model(model_path)

        for tokenizer in tokenizer_list:
            tokenizer.assign_from_loader(hmm_model=hmm_model)

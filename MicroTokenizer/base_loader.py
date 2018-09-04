from MicroTokenizer.singleton import SingletonMixin


class BaseLoader(SingletonMixin):
    name = None

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_name(cls):
        return cls.name

    def from_disk(self, path, tokenizer_list):
        raise NotImplemented

    def get_model_dir(self):
        return False

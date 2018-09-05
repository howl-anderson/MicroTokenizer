from collections import OrderedDict, defaultdict

from MicroTokenizer import util
from MicroTokenizer.CRF.crf_tokenizer import CRFTokenizer
from MicroTokenizer.dag import DAGTokenizer
from MicroTokenizer.compat import basestring_
from MicroTokenizer.errors import Errors
from MicroTokenizer.hmm import HMMTokenizer
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.max_match.bidirectional import \
    MaxMatchBidirectionalTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.base_tokenizer import BaseTokenizer
from MicroTokenizer.tokenizer import Tokenizer


class BaseDefaults(object):
    tokenizers = [
        'max_match_forward_tokenizer',
        'max_match_backward_tokenizer',
        'max_match_bidirectional_tokenizer',
        'dag_tokenizer',
        'hmm_tokenizer',
        'crf_tokenizer'
    ]


class TokenizerLoader(object):
    Defaults = BaseDefaults

    factories = {
        'max_match_forward_tokenizer': lambda nlp, **cfg: MaxMatchForwardTokenizer(**cfg),
        'max_match_backward_tokenizer': lambda nlp, **cfg: MaxMatchBackwardTokenizer(**cfg),
        'max_match_bidirectional_tokenizer': lambda nlp, **cfg: MaxMatchBidirectionalTokenizer(**cfg),
        'dag_tokenizer': lambda nlp, **cfg: DAGTokenizer(**cfg),
        'hmm_tokenizer': lambda nlp, **cfg: HMMTokenizer(**cfg),
        'crf_tokenizer': lambda nlp, **cfg: CRFTokenizer(**cfg)
    }

    def __init__(self, meta=None, **kwargs):
        self.meta = {} if meta is None else meta
        self.tokenizers = {}

    def create_tokenizer(self, name, config=dict()):
        """Create a pipeline component from a factory.

        name (unicode): Factory name to look up in `Language.factories`.
        config (dict): Configuration parameters to initialise component.
        RETURNS (callable): Pipeline component.
        """
        if name not in self.factories:
            raise KeyError(Errors.E002.format(name=name))
        factory = self.factories[name]
        return factory(self, **config)

    def add_tokenizer(self, component, name=None):
        if issubclass(BaseTokenizer, component.__class__):
            msg = Errors.E003.format(component=repr(component), name=name)
            if isinstance(component, basestring_) and component in self.factories:
                msg += Errors.E004.format(component=component)
            raise ValueError(msg)
        if name is None:
            if hasattr(component, 'name'):
                name = component.name
            elif hasattr(component, '__name__'):
                name = component.__name__
            elif (hasattr(component, '__class__') and
                  hasattr(component.__class__, '__name__')):
                name = component.__class__.__name__
            else:
                name = repr(component)
        if name in self.tokenizers:
            raise ValueError(Errors.E007.format(name=name, opts=self.tokenizers.keys()))

        self.tokenizers[name] = component

    def from_disk(self, path, disable=tuple()):
        path = util.ensure_path(path)
        deserializers = OrderedDict()
        loader_name_to_tokenizer = defaultdict(list)
        loader_name_to_class = dict()
        loader_name_to_instance = dict()
        for name, tokenizer in self.tokenizers.items():
            if name in disable:
                continue

            # TODO: why using this in spacy
            # if not hasattr(tokenizer, 'to_disk'):
            #     continue

            loader_class = tokenizer.get_loader()
            loader_name = loader_class.get_name()
            loader_name_to_tokenizer[loader_name].append(tokenizer)

            if name not in loader_name_to_class:
                loader_name_to_class[loader_name] = loader_class

        for loader_name, loader_class in loader_name_to_class.items():
            loader_config = self.meta.get('loader_config', {}).get(loader_name, {})
            loader_name_to_instance[loader_name] = loader_class.instance(**loader_config)

        for loader_name, tokenizer in loader_name_to_tokenizer.items():
            loader_instance = loader_name_to_instance[loader_name]

            # if hasattr(loader_instance, 'skip_load_from_disk'):
            #     continue

            deserializers[loader_name] = lambda p, loader_instance=loader_instance, tokenizer=tokenizer: loader_instance.from_disk(p, tokenizer), loader_instance.get_model_dir()

        exclude = {p: False for p in disable}
        util.from_disk(path, deserializers, exclude)
        return self

    def get_tokenizer(self):
        def assemble_max_match_bidirectional_tokenizer(forward_tokenizer, backward_tokenizer):
            if forward_tokenizer and backward_tokenizer:
                max_match_bidirectional_tokenizer = MaxMatchBidirectionalTokenizer()
                max_match_bidirectional_tokenizer.forward_tokenizer = forward_tokenizer
                max_match_bidirectional_tokenizer.backward_tokenizer = backward_tokenizer

                return max_match_bidirectional_tokenizer

            return None

        forward_tokenizer = self.tokenizers.get('max_match_forward_tokenizer')
        backward_tokenizer = self.tokenizers.get('max_match_backward_tokenizer')

        tokenizer = Tokenizer()
        tokenizer.max_match_forward_tokenizer = forward_tokenizer
        tokenizer.max_match_backward_tokenizer = backward_tokenizer
        tokenizer.max_match_bidirectional_tokenizer = assemble_max_match_bidirectional_tokenizer(forward_tokenizer, backward_tokenizer)
        tokenizer.hmm_tokenizer = self.tokenizers.get('hmm_tokenizer')
        tokenizer.dag_tokenizer = self.tokenizers.get('dag_tokenizer')
        tokenizer.crf_tokenizer = self.tokenizers.get('crf_tokenizer')

        return tokenizer

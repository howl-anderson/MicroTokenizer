# copied from https://gist.github.com/werediver/4396488

import threading


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls(*args, **kwargs)
        return cls.__singleton_instance


if __name__ == '__main__':
    class A(SingletonMixin):
        pass


    class B(SingletonMixin):
        pass


    a, a2 = A.instance(), A.instance()
    b, b2 = B.instance(), B.instance()

    assert a is a2
    assert b is b2
    assert a is not b

    print('a:  %s\na2: %s' % (a, a2))
    print('b:  %s\nb2: %s' % (b, b2))

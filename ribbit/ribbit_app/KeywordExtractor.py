from abc import ABCMeta, abstractmethod

class KeywordExtractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, file):
        pass

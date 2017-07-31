from abc import ABCMeta, abstractmethod

class Recommender(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self,keywords):
        pass

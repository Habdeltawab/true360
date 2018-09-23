from abc import ABCMeta, abstractmethod


class ConnectionInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_registered(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def close(self):
        pass

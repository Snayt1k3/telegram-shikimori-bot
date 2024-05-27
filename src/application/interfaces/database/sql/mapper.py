from abc import ABC, abstractmethod


class AbstractMapper(ABC):
    @staticmethod
    @abstractmethod
    def model_to_entity(model):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def entity_to_model(model):
        raise NotImplementedError

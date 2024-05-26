from abc import ABC, abstractmethod
from typing import TypeVar, Generic


Entity = TypeVar("Entity")
Model = TypeVar("Model")


class AbstractMapper(ABC, Generic[Entity, Model]):
    @staticmethod
    @abstractmethod
    def model_to_entity(model: Model) -> Entity:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def entity_to_model(model: Entity) -> Model:
        raise NotImplementedError

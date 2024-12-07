from src.application.interfaces.factory import UseCaseFactoryAbstract
from src.application.interfaces.usecase import UseCase


class UseCaseFactory(UseCaseFactoryAbstract):
    def __init__(self):
        self._handlers = {
            "update_anime": "",
            "get_anime": "",
            "delete_anime": "",
            "add_anime": "",
        }

    def create(self, type: str) -> UseCase | None:
        if type not in self._handlers:
            return None
        # todo implementation

    def _inject_dependencies(self, usecase: type[UseCase]) -> UseCase:
        dependencies = {}
        # todo implementation

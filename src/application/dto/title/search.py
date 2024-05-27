import dataclasses
import uuid


@dataclasses.dataclass
class SearchResult:
    id: int
    ru: str
    en: str
    img: str
    status: str

    additional_data: dict


@dataclasses.dataclass
class SearchResults:
    uuid = uuid.uuid4()
    query: str
    results: list

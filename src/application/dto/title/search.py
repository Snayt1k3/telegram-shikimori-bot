import dataclasses


@dataclasses.dataclass
class SearchResultDTO:
    id: int
    ru: str
    en: str
    img: str
    status: str

    additional_data: dict


@dataclasses.dataclass
class SearchResultsDTO:
    query: str
    results: list

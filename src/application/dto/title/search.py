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
    results: list[SearchResultDTO]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            query=data.get("query"),
            results=[SearchResultDTO(**i) for i in data.get("results")],
        )

from dataclasses import asdict, dataclass
from typing import Any, TypeVar

from src.models._util import dict_factory

_Document = TypeVar("_Document", bound="Document")


@dataclass
class Document:
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Document - a model defined in OpenAPI

        text: The text of this Document.
        id: The id of this Document [Optional].
    """

    text: str
    id: str | None = None

    @classmethod
    def from_dict(cls: type[_Document], input: dict[str, Any]) -> _Document:
        return cls(
            text=input["text"],
            id=input.get(
                "id",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self, dict_factory=dict_factory)

from dataclasses import asdict, dataclass
from typing import Any, TypeVar

from src.models._util import dict_factory
from src.models.color import Color
from src.models.document import Document

_Input = TypeVar("_Input", bound="Input")


@dataclass
class Input:
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Input - a model defined in OpenAPI

        api_name: API name.
        name: name.
        documents: The documents of this Input. [Optional]
        color: The color of this Input. [Optional]
    """

    api_name: str
    name: str
    documents: list[Document] | None = None
    color: Color | None = None

    @classmethod
    def from_dict(cls: type[_Input], input: dict[str, Any]) -> _Input:
        return cls(
            api_name=input["api_name"],
            name=input["name"],
            documents=[Document.from_dict(v) for v in input["documents"]] if "documents" in input else None,
            color=Color(_value) if (_value := input.get("color")) is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self, dict_factory=dict_factory)

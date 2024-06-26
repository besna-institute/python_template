from dataclasses import asdict, dataclass
from typing import Any, TypeVar

from src.models._util import dict_factory

_Output = TypeVar("_Output", bound="Output")


@dataclass
class Output:
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Output - a model defined in OpenAPI

        api_name: API name.
        api_version: API version.
        text: text.
    """

    api_name: str
    api_version: str
    text: str

    @classmethod
    def from_dict(cls: type[_Output], input: dict[str, Any]) -> _Output:
        return cls(
            api_name=input["api_name"],
            api_version=input["api_version"],
            text=input["text"],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self, dict_factory=dict_factory)

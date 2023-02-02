# pylint: disable=duplicate-code
import unittest

from src.models import Color, Document, Input


class InputTest(unittest.TestCase):
    def test_from_dict(self) -> None:
        tests = [
            (Input.from_dict({"api_name": "api_name", "name": "name"}), Input(api_name="api_name", name="name")),
            (
                Input.from_dict({"api_name": "api_name", "name": "name", "color": "RED"}),
                Input(api_name="api_name", name="name", color=Color("RED")),
            ),
            (
                Input.from_dict(
                    {
                        "api_name": "api_name",
                        "name": "name",
                        "documents": [{"text": "text", "id": "id"}, {"text": "text"}],
                    }
                ),
                Input(
                    api_name="api_name", name="name", documents=[Document(text="text", id="id"), Document(text="text")]
                ),
            ),
        ]
        for actual, expected in tests:
            with self.subTest(name=expected):
                self.assertEqual(actual, expected)

    def test_to_dict(self) -> None:
        tests = [
            (
                Input(api_name="api_name", name="name").to_dict(),
                {"api_name": "api_name", "name": "name", "color": None, "documents": None},
            ),
            (
                Input(api_name="api_name", name="name", color=Color("RED")).to_dict(),
                {"api_name": "api_name", "name": "name", "color": "RED", "documents": None},
            ),
            (
                Input(
                    api_name="api_name", name="name", documents=[Document(text="text", id="id"), Document(text="text")]
                ).to_dict(),
                {
                    "api_name": "api_name",
                    "name": "name",
                    "documents": [{"text": "text", "id": "id"}, {"text": "text", "id": None}],
                    "color": None,
                },
            ),
        ]
        for actual, expected in tests:
            with self.subTest(name=expected):
                self.assertEqual(actual, expected)

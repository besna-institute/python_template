# pylint: disable=duplicate-code
import unittest

from src.models import Document


class DocumentTest(unittest.TestCase):
    def test_from_dict(self) -> None:
        tests = [
            (Document.from_dict({"text": "text", "id": "id"}), Document(text="text", id="id")),
            (Document.from_dict({"text": "text"}), Document(text="text")),
            (Document.from_dict({"text": "text", "id": None}), Document(text="text")),
        ]
        for actual, expected in tests:
            with self.subTest(name=expected):
                self.assertEqual(actual, expected)

    def test_to_dict(self) -> None:
        tests = [
            (Document(text="text", id="id").to_dict(), {"text": "text", "id": "id"}),
            (Document(text="text").to_dict(), {"text": "text", "id": None}),
        ]
        for actual, expected in tests:
            with self.subTest(name=expected):
                self.assertEqual(actual, expected)

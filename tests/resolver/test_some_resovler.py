import unittest

from src.resolver import some_resovler


class SomeResovlerTest(unittest.TestCase):
    def test_extract_referrer(self):
        tests = [
            ("Taro", "Hello, Taro"),
            ("Jiro", "Hello, Jiro"),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(some_resovler.analyze(name), expected)

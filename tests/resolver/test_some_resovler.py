import unittest

from src.resolver import some_resovler


class SomeResovlerTest(unittest.TestCase):
    def test_extract_referrer(self):
        tests = [
            ("Taro", some_resovler.Result(text="Hello, Taro")),
            ("Jiro", some_resovler.Result(text="Hello, Jiro")),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(some_resovler.analyze(name), expected)

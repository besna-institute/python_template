import unittest

from src.solver import some_sovler


class SomeResovlerTest(unittest.TestCase):
    def test_extract_referrer(self):
        tests = [
            ("Taro", some_sovler.Result(text="Hello, Taro")),
            ("Jiro", some_sovler.Result(text="Hello, Jiro")),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(some_sovler.analyze(name), expected)

import unittest

from src.solver import some_solver


class SomeResovlerTest(unittest.TestCase):
    def test_extract_referrer(self):
        tests = [
            ("Taro", some_solver.Result(text="Hello, Taro")),
            ("Jiro", some_solver.Result(text="Hello, Jiro")),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(some_solver.analyze(name), expected)

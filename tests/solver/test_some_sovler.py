import unittest

from src.solver import some_solver


class SomeSolverTest(unittest.TestCase):
    def test_analyze(self):
        tests = [
            ("Taro", some_solver.Result(text="Hello, Taro")),
            ("Jiro", some_solver.Result(text="Hello, Jiro")),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(some_solver.analyze(name), expected)

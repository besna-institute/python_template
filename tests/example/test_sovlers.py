import unittest

from src.example.solvers import Result, SomeSolver


class SomeSolverTest(unittest.TestCase):
    def test_analyze(self):
        tests = [
            ("Taro", Result(text="Hello, Taro")),
            ("Jiro", Result(text="Hello, Jiro")),
        ]
        for name, expected in tests:
            with self.subTest(name=name):
                self.assertEqual(SomeSolver().analyze(name), expected)

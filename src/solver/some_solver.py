from src.api import BaseSolverAPI, Result


class SomeSolver(BaseSolverAPI):
    def __init__(self):
        super().__init__("Solver", "1.0.0")

    def analyze(self, name: str) -> Result:
        text = f"Hello, {name}"
        return Result(text=text)

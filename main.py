from src.another_example.entrypoint import another_example
from src.example.entrypoint import example
from src.save_result.entrypoint import save_result

__all__: list[str] = ["example", "another_example", "save_result"]

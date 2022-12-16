import json
import unittest
from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient

from src.example.entrypoint import APP

client = TestClient(APP)
path_to_dir = Path(__file__).parent
path_to_data = path_to_dir / "data"


class MainTest(unittest.TestCase):
    def test_input1(self) -> None:
        with open(path_to_data / "input1.json", encoding="utf-8") as fp:
            json_input1 = json.load(fp)

        response = client.post("/", json=json_input1)
        status_code = response.status_code

        with open(path_to_data / "output1.json", encoding="utf-8") as fp:
            json_output1 = json.load(fp)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_output1)

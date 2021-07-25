import json
import unittest
from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient

from src.main import app


class MainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path_to_dir = Path(__file__).parent
        cls.path_to_data = path_to_dir / "api" / "data"
        cls.client = TestClient(app)

    def test_input1(self):
        with open(self.path_to_data / "input1.json") as fp:
            json_input1 = json.load(fp)

        correct_response = self.client.post("/", json=json_input1)
        correct_status_code = correct_response.status_code

        with open(self.path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        self.maxDiff = None
        self.assertEqual(correct_status_code, status.HTTP_200_OK)
        self.assertEqual(correct_response.json(), json_output1)

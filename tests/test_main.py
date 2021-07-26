import json
import unittest
from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)
path_to_dir = Path(__file__).parent
path_to_data = path_to_dir / "data"


class MainTest(unittest.TestCase):
    def test_input1(self):
        with open(path_to_data / "input1.json") as fp:
            json_input1 = json.load(fp)

        response = client.post("/", json=json_input1)
        status_code = response.status_code

        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        self.maxDiff = None
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_output1)

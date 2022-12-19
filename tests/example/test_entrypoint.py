import json
import subprocess  # nosec B404
import unittest
from pathlib import Path

from requests import Session  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from urllib3.util.retry import Retry  # type: ignore

path_to_dir = Path(__file__).parent
path_to_data = path_to_dir / "data"
path_to_function_source = Path(__file__).parent.parent.parent


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        """ref: https://cloud.google.com/functions/docs/testing/test-http?hl=ja#integration_tests"""
        port = 8080  # Each functions framework instance needs a unique port
        self.process = subprocess.Popen(  # pylint: disable=consider-using-with  # nosec B603 B607
            ["functions-framework", "--target", "example", "--port", str(port)],
            cwd=path_to_function_source,
            stdout=subprocess.PIPE,
        )
        self.base_url = f"http://localhost:{port}"

        retry_policy = Retry(total=6, backoff_factor=1)
        retry_adapter = HTTPAdapter(max_retries=retry_policy)

        self.session = Session()
        self.session.mount(self.base_url, retry_adapter)

    def test_input1(self) -> None:
        with open(path_to_data / "input1.json", encoding="utf-8") as fp:
            json_input1 = json.load(fp)

        with open(path_to_data / "output1.json", encoding="utf-8") as fp:
            json_output1 = json.load(fp)

        res = self.session.post(self.base_url, json=json_input1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.text), json_output1)

    def tearDown(self) -> None:
        self.process.kill()
        self.process.wait()

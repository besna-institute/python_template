import json
import subprocess  # nosec B404
import unittest
from pathlib import Path

from requests import Response, Session  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from urllib3.util.retry import Retry  # type: ignore

path_to_dir: Path = Path(__file__).parent
path_to_data: Path = path_to_dir / "data"
path_to_function_source: Path = Path(__file__).parent.parent.parent


class EntrypointTest(unittest.TestCase):
    _process: subprocess.Popen[bytes]
    base_url: str
    session: Session

    @classmethod
    def setUpClass(cls) -> None:
        """ref: https://cloud.google.com/functions/docs/testing/test-http?hl=ja#integration_tests"""
        port: str = "8080"  # Each functions framework instance needs a unique port
        cls._process = subprocess.Popen(  # pylint: disable=consider-using-with  # nosec B603 B607
            ["functions-framework", "--target", "example", "--port", port],
            cwd=path_to_function_source,
            stdout=subprocess.PIPE,
        )
        cls.base_url = f"http://localhost:{port}"

        retry_policy: Retry = Retry(total=6, backoff_factor=1)
        retry_adapter: HTTPAdapter = HTTPAdapter(max_retries=retry_policy)

        cls.session = Session()
        cls.session.mount(cls.base_url, retry_adapter)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._process.kill()
        cls._process.wait()

    def test_json_input(self) -> None:
        """JSONを使ったテスト
        test_with_jsonlと選択。
        """
        with open(path_to_data / "input1.json", encoding="utf-8") as fp:
            json_input1 = json.load(fp)

        with open(path_to_data / "output1.json", encoding="utf-8") as fp:
            json_output1 = json.load(fp)

        res: Response = self.session.post(self.base_url, json=json_input1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.text), json_output1)

    def test_json_input_with_jsonl(self) -> None:
        """JSON Linesを使ったテスト
        test_json_inputと選択。
        """
        with open(path_to_data / "input.jsonl", encoding="utf-8") as input_jsonl, open(
            path_to_data / "output.jsonl", encoding="utf-8"
        ) as output_jsonl:
            for input_json, output_json in zip(input_jsonl, output_jsonl):
                input = json.loads(input_json)
                output = json.loads(output_json)
                res: Response = self.session.post(self.base_url, json=input)
                self.assertEqual(res.status_code, 200)
                self.assertEqual(json.loads(res.text), output)

    def test_jsonlines_input(self) -> None:
        """JSON Linesを入力とするテスト"""
        with open(path_to_data / "input.jsonl", encoding="utf-8") as input_jsonl, open(
            path_to_data / "output.jsonl", encoding="utf-8"
        ) as output_jsonl:
            input = input_jsonl.read()
            output = output_jsonl.read()
            res: Response = self.session.post(self.base_url, data=input, headers={"Content-Type": "application/jsonl"})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.text, output)

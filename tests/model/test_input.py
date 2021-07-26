import json
import unittest
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver

path_to_dir = Path(__file__).parent
path_to_schema = path_to_dir.parent.parent / "src" / "model" / "schema"
path_to_input = path_to_schema / "input.json"
path_to_metadata = path_to_schema / "metadata.json"
path_to_data = path_to_dir.parent / "data"


class InputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(path_to_input) as fp:
            cls.input_schema = json.load(fp)

        with open(path_to_metadata) as fp:
            metadata_schema = json.load(fp)

        schema_store = {
            cls.input_schema["$id"]: cls.input_schema,
            metadata_schema["$id"]: metadata_schema,
        }

        cls.resolver = RefResolver.from_schema(cls.input_schema, store=schema_store)

    def test_input_json(self):
        json_name_list = ["input1.json"]

        for json_name in json_name_list:
            with open(path_to_data / json_name) as fp:
                json_data = json.load(fp)
            with self.subTest(name=json_name):
                Draft7Validator(self.input_schema, resolver=self.resolver).validate(json_data)

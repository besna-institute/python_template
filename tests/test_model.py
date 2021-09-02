import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, RefResolver

path_to_root = Path(__file__).parent
path_to_schema = path_to_root.parent / "src" / "schema.yaml"
path_to_data = path_to_root / "data"


class ModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(path_to_schema, "r") as fp:
            spec_dict = yaml.full_load(fp)
        cls.schemas = spec_dict["components"]["schemas"]
        cls.resolver = RefResolver.from_schema(spec_dict)

    def test_error_json(self):
        json_name_list = ["error1.json"]

        for json_name in json_name_list:
            with open(path_to_data / json_name) as fp:
                json_data = json.load(fp)
            with self.subTest(name=json_name):
                Draft7Validator(self.schemas["Error"], resolver=self.resolver).validate(json_data)

    def test_input_json(self):
        json_name_list = ["input1.json"]

        for json_name in json_name_list:
            with open(path_to_data / json_name) as fp:
                json_data = json.load(fp)
            with self.subTest(name=json_name):
                Draft7Validator(self.schemas["Input"], resolver=self.resolver).validate(json_data)

    def test_output_json(self):
        json_name_list = ["output1.json"]

        for json_name in json_name_list:
            with open(path_to_data / json_name) as fp:
                json_data = json.load(fp)
            with self.subTest(name=json_name):
                Draft7Validator(self.schemas["Output"], resolver=self.resolver).validate(json_data)

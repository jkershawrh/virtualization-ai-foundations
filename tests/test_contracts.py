import json
import unittest
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


class ContractTests(unittest.TestCase):
    def load_json(self, name):
        return json.loads((CONTRACTS / name).read_text())

    def validator(self, name):
        schema = self.load_json(name)
        registry = jsonschema.validators.validator_for(schema)
        registry.check_schema(schema)
        return registry(schema, format_checker=jsonschema.FormatChecker())

    def test_request_example_matches_schema(self):
        self.validator("analysis-request.schema.json").validate(
            self.load_json("examples/healthy-request.json")
        )

    def test_response_examples_match_schema(self):
        validator = self.validator("analysis-response.schema.json")
        validator.validate(self.load_json("examples/healthy-response.json"))
        validator.validate(self.load_json("examples/unavailable-response.json"))

    def test_unavailable_response_cannot_claim_ai_participation(self):
        response = self.load_json("examples/unavailable-response.json")
        response["ai_participated"] = True
        with self.assertRaises(jsonschema.ValidationError):
            self.validator("analysis-response.schema.json").validate(response)

    def test_openapi_declares_versioned_paths(self):
        document = yaml.safe_load((CONTRACTS / "openapi.yaml").read_text())
        self.assertEqual(document["openapi"], "3.1.0")
        self.assertIn("/api/v1/analyze", document["paths"])
        self.assertIn("/api/v1/evidence/{request_id}", document["paths"])


if __name__ == "__main__":
    unittest.main()

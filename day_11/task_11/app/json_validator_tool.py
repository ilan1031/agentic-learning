import json
import jsonschema
from jsonschema import validate
import logging
from typing import Dict, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONValidatorTool:
    def __init__(self, schema: Dict = None):
        # Add a default schema for testing
        self.schema = schema or {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "city": {"type": "string"}
            },
            "required": ["name", "age"]
        }

    def validate_json(self, json_str: str) -> Dict:
        """
        Validate JSON syntax and optional schema
        Returns a dictionary with validation results
        """
        result = {
            "valid": False,
            "errors": [],
            "message": ""
        }
        
        # Step 1: Syntax validation
        try:
            json_data = json.loads(json_str)
            result["valid"] = True
            result["message"] = "JSON syntax is valid"
        except json.JSONDecodeError as e:
            error_info = {
                "type": "syntax",
                "message": str(e),
                "line": e.lineno,
                "column": e.colno,
                "path": "$"
            }
            result["errors"].append(error_info)
            result["message"] = "Syntax error in JSON"
            return result
        
        # Step 2: Schema validation if schema is provided
        if self.schema:
            try:
                validate(instance=json_data, schema=self.schema)
                result["message"] += " and matches schema"
            except jsonschema.ValidationError as e:
                error_info = {
                    "type": "schema",
                    "message": e.message,
                    "path": "->".join([str(p) for p in e.path]),
                    "context": e.context if e.context else None
                }
                result["errors"].append(error_info)
                result["valid"] = False
                result["message"] += " but schema validation failed"
        
        return result
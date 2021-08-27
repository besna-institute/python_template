#!/bin/bash
~/.local/bin/datamodel-codegen --input "src/schema.yaml" --input-file-type openapi --field-constraints --output "src/model.py"
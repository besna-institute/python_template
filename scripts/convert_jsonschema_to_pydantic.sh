#!/bin/bash
schemas=$(ls -1 src/api/model/schema/)
for schema in $schemas; do
  ~/.local/bin/datamodel-codegen --input "src/api/model/schema/$schema" --input-file-type jsonschema --field-constraints --output "src/api/model/$(basename "$schema" .json).py"
done

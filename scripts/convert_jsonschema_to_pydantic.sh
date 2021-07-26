#!/bin/bash
schemas=$(ls -1 src/model/schema/)
for schema in $schemas; do
  ~/.local/bin/datamodel-codegen --input "src/model/schema/$schema" --input-file-type jsonschema --field-constraints --output "src/model/$(basename "$schema" .json).py"
done

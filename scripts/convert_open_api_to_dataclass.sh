#!/bin/bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT/openapi-generator" || exit
npm exec -y -- @openapitools/openapi-generator-cli generate -c openapi_generator.yaml
rm generated/src/models/base_model_.py
rm -fr "$PROJECT_ROOT/src/models/"*
cp -r generated/src/models/* "$PROJECT_ROOT/src/models/"
rm -fr generated
cd "$PROJECT_ROOT" || exit
python -m pyupgrade --py310-plus src/models/*.py
python -m autoflake -i -r --remove-all-unused-imports src/models
python -m black src/models

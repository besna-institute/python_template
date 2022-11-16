#!/bin/bash
npm exec -y -- @openapitools/openapi-generator-cli generate -c openapi_generator.yaml
rm openapi-generator-tmp/src/models/base_model_.py
rm -fr src/models/*
cp -r openapi-generator-tmp/src/models/* src/models
rm -fr openapi-generator-tmp
python -m autoflake -i -r --remove-all-unused-imports src/models
python -m black src/models

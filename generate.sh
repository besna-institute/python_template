/usr/src/app/.local/bin/datamodel-codegen  --input src/api/model/schema/metadata.json --input-file-type jsonschema --output src/api/model/metadata.py
/usr/src/app/.local/bin/datamodel-codegen  --input src/api/model/schema/error.json --input-file-type jsonschema --output src/api/model/error.py
/usr/src/app/.local/bin/datamodel-codegen  --input src/api/model/schema/input.json --input-file-type jsonschema --output src/api/model/input.py
/usr/src/app/.local/bin/datamodel-codegen  --input src/api/model/schema/output.json --input-file-type jsonschema --output src/api/model/output.py
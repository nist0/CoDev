#!/usr/bin/env python3
"""
Validate OpenAPI YAML contract for required fields.
"""
import sys
import yaml

if len(sys.argv) != 2:
    print("Usage: validate-openapi.py <openapi-file>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    doc = yaml.safe_load(f)

if 'openapi' not in doc or 'paths' not in doc:
    print("Invalid OpenAPI: missing 'openapi' or 'paths'.")
else:
    print("OpenAPI contract is valid.")

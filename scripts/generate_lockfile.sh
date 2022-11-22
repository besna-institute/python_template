#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
pip install -q --user pip-tools
pip-compile -qo requirements.lock requirements.txt
echo "$(tput setaf 2)✓ Generate requirements.lock"

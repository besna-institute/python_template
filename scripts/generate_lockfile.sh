#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
pip install -q --user pip-tools
pip-compile --resolver=backtracking -qo requirements.txt requirements.in
echo "$(tput setaf 2)✓ Generate requirements.txt"

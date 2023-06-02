#!/bin/bash
set -euo pipefail

if [[ $(git diff --stat) != '' ]]; then
  echo "$(tput setaf 1)✘ Working directory is dirty"
  echo "$(tput setaf 0)  Commit or stash your changes"
  exit 1
fi
echo "$(tput setaf 2)✓ Working directory is clean$(tput setaf 7)"

cd "$(git rev-parse --show-toplevel)"
git remote add template https://github.com/besna-institute/python_template.git
set +e
git fetch --no-tags template refs/tags/v*:refs/tags/template-v*
TEMPLATE_VERSION=$(git tag --sort=-v:refname -l 'template-v*' | head -1)
BASE_BRANCH=$(git rev-parse --abbrev-ref @)
git diff --output=update.patch "$BASE_BRANCH" "$TEMPLATE_VERSION"
echo "$(tput setaf 2)✓ Create patch from $TEMPLATE_VERSION"
git remote rm template
git tag | grep template-v | xargs git tag -d
git apply update.patch
rm update.patch
set -e
echo "$(tput setaf 2)✓ Apply patch"
echo "$(tput setaf 3)🚨 Check changes before commit!"

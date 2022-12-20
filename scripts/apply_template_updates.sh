#!/bin/bash
set -euo pipefail

if [[ $(git diff --stat) != '' ]]; then
  echo "$(tput setaf 1)✘ Working directry is dirty"
  echo "$(tput setaf 0)  Commit or stash your changes"
  exit 1
fi
echo "$(tput setaf 2)✓ Working directry is clean$(tput setaf 7)"

cd "$(git rev-parse --show-toplevel)"
git remote add template https://github.com/besna-institute/python_template.git
git fetch --no-tags template refs/tags/v*:refs/tags/template-v*
TEMPALTE_VERSION=$(git tag --sort=-v:refname -l 'template-v*' | head -1)
git diff --output=update.patch main "$TEMPALTE_VERSION" -- \
  .devcontainer \
  .editorconfig \
  .flake8 \
  .gcloudignore \
  .gitignore \
  .github/workflows \
  .pylintrc \
  .vscode \
  Dockerfile \
  cloudbuild.yaml \
  openapi_generator.yaml \
  openapitools.json \
  pyproject.toml \
  requirements.in \
  scripts \
  src/__init.py \
  template

echo "$(tput setaf 2)✓ Create patch from $TEMPALTE_VERSION"
git remote rm template
git tag | grep template-v | xargs git tag -d
git apply update.patch
rm update.patch
echo "$(tput setaf 2)✓ Apply patch"
echo "$(tput setaf 3)🚨 Check changes before commit!"

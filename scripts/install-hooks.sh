#!/usr/bin/env bash

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
ln -sf scripts/pre-commit $GIT_DIR/hooks/pre-commit
ln -sf scripts/pre-push $GIT_DIR/hooks/pre-push
echo "Done!"
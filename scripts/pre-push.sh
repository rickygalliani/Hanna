#!/usr/bin/env bash

echo "Running pre-push unit tests..."
./scripts/unittest.sh

# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo "Tests must pass before pushing to repository..."
 exit 1
fi
#!/usr/bin/bash
# Run all unittests in tests when using FileStorage engine.

python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1

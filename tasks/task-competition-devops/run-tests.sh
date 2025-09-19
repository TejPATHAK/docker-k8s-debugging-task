#!/bin/bash
set -e
python3 tests/test_outputs.py
if [ $? -ne 0 ]; then
  echo "Some tests failed"
  exit 1
fi
echo "All tests passed!"
exit 0

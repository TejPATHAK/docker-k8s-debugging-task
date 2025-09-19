#!/bin/bash
set -e
pytest -q --tb=short tests/test_outputs.py

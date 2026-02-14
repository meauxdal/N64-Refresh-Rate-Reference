#!/usr/bin/env python3
# build.py

from pathlib import Path
from tools.generate_docs_core import generate_all_docs

PROJECT_ROOT = Path(__file__).parent.resolve()

def build_docs():
    generate_all_docs(PROJECT_ROOT)

if __name__ == "__main__":
    build_docs()
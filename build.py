#!/usr/bin/env python3
# build.py

from tools.generate_docs_core import generate_all_docs

if __name__ == "__main__":
    markdown = generate_all_docs()
    print("N64 refresh rate markdown generated successfully.")
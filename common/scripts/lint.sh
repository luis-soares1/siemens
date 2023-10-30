#!/bin/bash

# Loop over all tracked files
git ls-files | while read -r file; do
    # Check if the file is a Python file
    if [[ "$file" == *.py ]]; then
        autopep8 --in-place --aggressive --aggressive "$file"
    fi
done
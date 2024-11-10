#!/bin/bash

# Check for Pip 24.x
if command -v python >/dev/null 2>&1; then
    pip_version=$(python -m pip --version | awk '{print $2}')
elif command -v python3 >/dev/null 2>&1; then
    pip_version=$(python3 -m pip --version | awk '{print $2}')
elif command -v python3.12 >/dev/null 2>&1; then
    pip_version=$(python3 -m pip --version | awk '{print $2}')
else
    (echo "Pip: NOT FOUND, please install pip version 24.x and ensure 'python', 'python3' or 'python3.12' is in your PATH" && exit 1)
fi

# Check pip version if found
if [[ -n "$pip_version" ]]; then
    if [[ "$pip_version" =~ ^24\..* ]]; then
        echo "Pip: $pip_version -> OK"
    else
        (echo "Pip: $pip_version -> INCOMPATIBLE, version 24.x required" && exit 1)
    fi
fi

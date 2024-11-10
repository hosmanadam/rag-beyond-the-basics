#!/bin/bash

# Check for Python 3.12.x
if command -v python >/dev/null 2>&1; then
    python_version=$(python --version | awk '{print $2}')
elif command -v python3 >/dev/null 2>&1; then
    python_version=$(python3 --version | awk '{print $2}')
    echo "WARNING: 'python3' was found, but 'python' wasn't. To make the README commands work, you have to either add 'python' to your PATH, or change the commands to use 'python3' instead."
elif command -v python3.12 >/dev/null 2>&1; then
    python_version=$(python3 --version | awk '{print $2}')
    echo "WARNING: 'python3.12' was found, but 'python' wasn't. To make the README commands work, you have to either add 'python' to your PATH, or change the commands to use 'python3.12' instead."
else
    (echo "Python: NOT FOUND, please install version 3.12.x (preferably 3.12.7) and ensure 'python', 'python3' or 'python3.12' is in your PATH" && exit 1)
fi

# Only proceed with version checks if a version was found
if [[ -n "$python_version" ]]; then
    if [[ "$python_version" == "3.12.7" ]]; then
        echo "Python: $python_version -> PERFECT"
    elif [[ "$python_version" =~ ^3\.12\.[0-9]+$ ]]; then
        echo "Python: $python_version -> PROBABLY COMPATIBLE, but consider upgrading to 3.12.7"
    else
        (echo "Python: $python_version -> INCOMPATIBLE, version 3.12.x required" && exit 1)
    fi
fi

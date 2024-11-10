#!/bin/bash

# Check for Git 2.20 or higher
if command -v git >/dev/null 2>&1; then
    git_version=$(git --version | awk '{print $3}')
    if [[ "$git_version" =~ ^2\.[2-9][0-9]\.|^[3-9]\.|^[1-9][0-9] ]]; then
        echo "Git: $git_version -> OK"
    else
        (echo "Git: $git_version -> OUTDATED, version 2.20 or higher required" && exit 1)
    fi
else
    (echo "Git: NOT INSTALLED, version 2.20 or higher required" && exit 1)
fi

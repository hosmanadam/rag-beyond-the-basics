#!/bin/bash

# Check for Bash 4.0+ or Zsh
if command -v zsh >/dev/null 2>&1; then
    zsh_version=$(zsh --version | awk '{print $2}')
    echo "Shell (Zsh): $zsh_version -> OK"
elif command -v bash >/dev/null 2>&1; then
    bash_version=$(bash --version | head -n1 | awk '{print $4}')
    if [[ "$bash_version" =~ ^[4-9]\.[0-9]+ ]]; then
        echo "Shell (Bash): $bash_version -> OK"
    else
        (echo "Shell (Bash): $bash_version -> OUTDATED, version 4.0 or higher required" && exit 1)
    fi
else
    (echo "Shell: NOT INSTALLED, Bash 4.0 or higher or any Zsh version required" && exit 1)
fi

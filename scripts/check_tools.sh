#!/bin/bash

echo "Checking all system tools..."
echo

chmod +x scripts/check_shell.sh && ./scripts/check_shell.sh &&
chmod +x scripts/check_git.sh && ./scripts/check_git.sh &&
chmod +x scripts/check_python.sh && ./scripts/check_python.sh &&
chmod +x scripts/check_pip.sh && ./scripts/check_pip.sh &&
chmod +x scripts/check_venv.sh && ./scripts/check_venv.sh ||
exit 1

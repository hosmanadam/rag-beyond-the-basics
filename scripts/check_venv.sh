#!/bin/bash

if [[ -n "$VIRTUAL_ENV" && "$VIRTUAL_ENV" == "$(pwd)/.venv" ]]; then
    echo "Virtual environment -> OK, active"
else
    (echo "Virtual environment -> NOK, inactive or wrong venv" && exit 1)
fi

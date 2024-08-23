#!/bin/bash

# This script is used to run a command at a specific directory using Poetry.
# Example: ./runpoetry.sh database-setup python script.py arg1 arg2

if [[ -z "$1" ]]; then
    echo "Usage: $0 <directory> <command> [args...]"
    exit 1
fi

dir_abspath=$(realpath "$1")
shift  # Remove the first argument (directory)

if ! cd "$dir_abspath"; then
    echo "Error: Failed to change directory to '$dir_abspath'"
    exit 1
fi

# Construct and run the command with remaining arguments
COMMAND="${*@Q}" # Oneliner without COMMAND variable didn't work
poetry run bash -c "$COMMAND"

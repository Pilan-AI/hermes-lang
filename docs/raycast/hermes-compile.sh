#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🐍
# @raycast.packageName Hermes
# @raycast.title Hermes: Compile
# @raycast.description Compile Hermes file to Python
# @raycast.author Hermes
# @raycast.authorURL https://github.com/Pilan-AI/hermes-lang

# Documentation:
# @raycast.argument1 { "type": "text", "placeholder": "Enter .herm file path" }

FILE="$1"

if [ -n "$FILE" ]; then
    echo "Usage: hermes-compile <file.herm>"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

# Compile Hermes to Python
/opt/homebrew/bin/hermes compile "$FILE" 2>&1

exit 0

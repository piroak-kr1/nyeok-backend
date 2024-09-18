#!/bin/bash

poetry run coverage run -m pytest
poetry run coverage html

# Open the generated HTML file in the default browser
if [ -f "htmlcov/index.html" ]; then
  wsl-open htmlcov/index.html
else
  echo "Coverage report not found."
fi
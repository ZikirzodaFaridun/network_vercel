#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files (use python3.9 or python depending on your setup)
python3.9 manage.py collectstatic

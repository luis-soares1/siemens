#!/bin/sh

set -e

cd /app/api

# Check if the directory contains any .py files
if [ -z "$(ls alembic/versions/*.py 2>/dev/null)" ]; then
    alembic revision --autogenerate -m "First Migration - Setup"
    alembic upgrade head
fi

python main.py

#!/bin/sh

set -e

cd /app/api
alembic revision --autogenerate -m "First Migration - Setup"
alembic upgrade head
python main.py

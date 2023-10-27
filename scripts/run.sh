#!/bin/sh

set -e

alembic revision --autogenerate -m "First Migration - Setup"
alembic upgrade head
uvicorn main:app --reload --port=8000 --host=0.0.0.0
#!/bin/sh

set -e

alembic revision --autogenerate -m "First Migration - Setup"
alembic upgrade head
uvicorn app.main:app
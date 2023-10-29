#!/bin/sh

# check dynamic message
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <DYNAMIC_MESSAGE>"
    exit 1
fi

DYNAMIC_MESSAGE=$1

cd api
rm *.db

# delete alembic migrations
cd alembic/versions
rm -rf *

# Return to api dir
cd ../..

# Run alembic with dynamic message
alembic revision --autogenerate -m "$DYNAMIC_MESSAGE"
alembic upgrade head
uvicorn main:app --reload

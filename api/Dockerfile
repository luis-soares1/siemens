FROM python:3.11.5-alpine
LABEL maintainer="github.com/luis-soares1"
ENV PYTHONUNBUFFERED=1

COPY ./api /app/api
COPY ./common/scripts /app/common/scripts
COPY ./common/settings/config.py /app/common/settings/config.py
COPY ./common/utils /app/common/utils

WORKDIR /app
EXPOSE 8000

USER root

RUN python -m venv /app/py && \
    /app/py/bin/pip install --upgrade pip && \
    /app/py/bin/pip install --upgrade cython && \
    /app/py/bin/pip install --no-cache-dir -r /app/api/requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    chown -R app:app /app && \
    chmod -R 755 /app && \
    chmod -R +x /app/common/scripts

ENV PATH="/app/py/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

USER app

CMD ["common/scripts/run.sh"]

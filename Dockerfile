FROM python:3.11.5-alpine
LABEL maintainer="github.com/luis-soares1"
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

USER root

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # apk add --update --no-cache postgresql-client && \
    # apk add --update --no-cache --virtual .tmp-deps \
    #     build-base postgresql-dev musl-dev linux-headers gfortran musl-dev g++ gcc libffi-dev openssl-dev libxml2 libxml2-dev libxslt libxslt-dev libjpeg-turbo-dev zlib-dev && \
    /py/bin/pip install --upgrade cython && \
    /py/bin/pip install --no-cache-dir -r /requirements.txt && \
    # apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    # mkdir -p /vol/web/static && \
    # mkdir -p /vol/web/media && \
    chown -R app:app /app && \
    chmod -R 755 /app && \
    chmod -R +x /app/scripts

ENV PATH="/app/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]

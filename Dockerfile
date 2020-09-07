FROM python:3-alpine

LABEL maintainer="nathan@frcv.net"

COPY . /tiddlysaver

RUN pip install /tiddlysaver && \
    mkdir /tiddlywiki

WORKDIR /tiddlywiki

VOLUME /tiddlywiki

EXPOSE 8000

CMD ["gunicorn", "tiddlysaver:create_app()"]

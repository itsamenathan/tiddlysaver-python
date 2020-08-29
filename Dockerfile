FROM python:3-alpine

MAINTAINER Nathan W. <nathan@frcv.net>

COPY tiddlysaver /tiddlysaver

RUN pip install /tiddlysaver && \
    mkdir /tiddlywiki

WORKDIR /tiddlywiki

VOLUME /tiddlywiki

EXPOSE 8000

CMD ["tiddlysaver"]

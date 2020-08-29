FROM python:3-alpine

MAINTAINER Nathan W. <nathan@frcv.net>

COPY tiddlysaver /tiddlysaver

RUN pip install -r /tiddlysaver/requirements.txt && \
    mkdir /tiddlywiki

WORKDIR /tiddlywiki

VOLUME /tiddlywiki

EXPOSE 8000

CMD ["python3", "/tiddlysaver/tiddlysaver.py"]

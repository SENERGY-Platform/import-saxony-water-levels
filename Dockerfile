FROM python:3.7-alpine
RUN apk add git gcc librdkafka-dev musl-dev proj proj-dev proj-util libxml2 libxml2-dev libxslt libxslt-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
LABEL org.opencontainers.image.source https://github.com/SENERGY-Platform/import-saxony-water-levels
CMD [ "python", "./main.py" ]

FROM python:3.7-alpine

WORKDIR /opt/dblpWebBackend
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
COPY . .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi
RUN apk del .tmp
CMD ["uwsgi","./uwsgi.ini"]
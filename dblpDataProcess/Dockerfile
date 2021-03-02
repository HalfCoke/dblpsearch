FROM python:3.7-alpine

WORKDIR /opt/dblpDataProcess
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp

COPY ./resources ./resources
COPY ./conf ./conf
COPY ./utils ./utils
COPY ./Dockerfile .
COPY ./main.py .

CMD ["python","main.py"]
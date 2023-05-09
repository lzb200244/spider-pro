FROM alpine:latest
MAINTAINER codeminer "2632141215@qq.com"


RUN apk add --update \
    python3 \
    py3-pip \
    firefox-esr \
    firefox-esr-libs \
    geckodriver \
    && rm -rf /var/cache/apk/*

#firefox驱动环境变量
ENV PATH="/usr/bin/geckodriver:${PATH}"
#更换阿里pip代理
RUN mkdir -p /root/.pip
COPY ./pip.conf /root/.pip
#切换工作目录
WORKDIR /www
COPY ./requirements.txt /www
#下载依赖
RUN pip install -r requirements.txt




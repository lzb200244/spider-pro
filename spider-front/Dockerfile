FROM alpine:latest
MAINTAINER codeminer "2632141215@qq.com"
#下载git和nginx与ssh
RUN apk update && \
    apk add  openssh-client nginx && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan gitee.com >> /root/.ssh/known_hosts
#复制本地.ssh密钥加入容器
COPY .ssh /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa

RUN git config --global user.email "2632141215@qq.com" && \
    git config --global user.name "codeminer"
#切换工作目录
#每次构建时都克隆一次项目来维护版本
COPY ./html/* /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx","-g","daemon off;"]

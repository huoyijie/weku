# @author: huoyijie
# @file: Dockerfile
# @time: 2018/08/29
#
# @copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
# @license: GPL v3, see LICENSE for more details.

FROM python:3.6

MAINTAINER yijie.huo@foxmail.com

RUN mkdir -p /root/workspace/weku

WORKDIR /root/workspace/weku

ADD . .

RUN cp docker/sources.list /etc/apt/sources.list && apt-get update

RUN apt-get install -y --allow-unauthenticated --no-install-recommends openssh-server vim ffmpeg

RUN mkdir -p /var/run/sshd /root/.ssh

RUN cat docker/id_rsa.pub > /root/.ssh/authorized_keys
RUN sed -ri 's#session    required     pam_loginuid.so#session    required     pam_loginuid.so#g' /etc/pam.d/sshd
RUN sed -i "s/#Port 22/Port 58422/g" /etc/ssh/sshd_config
RUN chmod 755 docker/run.sh

RUN pip config set global.index-url 'https://pypi.tuna.tsinghua.edu.cn/simple'

RUN pip install -r requirements.txt

RUN mkdir -p /data/weku/media

RUN mkdir -p /data/applogs/weku/uwsgi

RUN echo 'from .docker import *' > weku/settings/__init__.py
RUN python docker/gen_secret_key.py > weku/settings/secret_key.txt
RUN cat weku/settings/secret_key.txt

RUN cp docker/uwsgi.ini uwsgi.ini

RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py collectstatic \
    && python manage.py createsuperuser

EXPOSE 58422
EXPOSE 9090

CMD ["docker/run.sh"]
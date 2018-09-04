#!/bin/bash
/usr/sbin/sshd -D &
uwsgi --ini uwsgi.ini \
      --static-map /static=/root/workspace/weku/weku/collectstatic \
      --static-map /media=/data/weku/media
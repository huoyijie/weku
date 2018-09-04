#1.Prepare

* ubuntu
* python 3(3.6)
* virtualenv
* docker (optional)
* git (optional)
`git clone {url}`

#2.Install

* virtual env
`mkdir ~/py3env-weku; cd ~/py3env-weku; virtualenv -p /usr/bin/python3 .;`

* install dependencies
`cd {project.dir}; pip install -r requirements.txt;`

#3.Migrations

* database
`python manage.py makemigrations`
`python manage.py migrate`

* create super user
`python manage.py createsuperuser`

* static
`python manage.py collectstatic`

#3.Manage
* switch virtualenv to py3env-weku
`source ~/py3env-weku/bin/activate`

* run uwsgi server 
`cd {project.dir}; uwsgi --ini uwsgi.ini;`

* reload uwsgi server
`uwsgi --reload /tmp/weku-master.pid`

* stop uwsgi server
`uwsgi --stop /tmp/weku-master.pid`

* auto run on reboot
run `crontab -e;`
add `@reboot cd {project.dir}; uwsgi --ini uwsgi.ini  &`

#4.Configuration

* {project.dir}/uwsgi.ini

* uwsgi log file
`/var/log/webapps/weku/uwsgi/weku-uwsgi.log`

* nginx log file
`/var/log/webapps/weku/nginx`

* django log file
`/var/log/webapps/weku/weku-django.log`

* make sure have enough permissions
`sudo chmod -R  a+w  /var/log/webapps`

# docker

* build image
`cd {project.dir}; docker build -t weku:1.0 .`
`cp ~/.ssh/id_rsa.pub docker/ && docker build -t weku:1.0 .`

* docker run(containerPort=9090 by default)
`docker run -d -p{hostPort}:{containerPort} --name weku -v wekudata:/data weku:1.0`
`docker run -d --net=host --name weku1.6 -v wekudata:/data weku:1.6`
`docker run -d -p9090:9090 -p58422:22 --name weku -v wekudata:/data weku:1.0`

* create super user
`docker exec -it  5de240de1ece python manage.py createsuperuser`

* ps
`docker ps -l`

* stop
`docker stop {containerID}`

* start
`docker start {containerID}`

* ssh
`ssh root@192.168.31.53 -p 58422`

# docker 创建WEKU APP步骤

* git clone {project.url} or download zip package(unpack), cd {project.dir}

* build image
`cp ~/.ssh/id_rsa.pub docker/ && docker build -t weku:1.0 .` for UNIX...
`cp {user.home}/.ssh/id_rsa.pub docker/ && docker build -t weku:1.0 .` for Windows

* run
`docker run -d -p9090:9090 -p58422:22 --name weku -v wekudata:/data weku:1.0`

* create super user
docker exec -it `docker ps -l | grep weku | awk '{print $1}'` python manage.py createsuperuser

* open browser
访问`http://ip:9090`
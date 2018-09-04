# WEKU(Alpha Stage)
WEKU is a personal video&amp;photo manager written by python and based on Django/Bootstrap/videojs/FFMpeg. It helps you manage your family's photos and videos and could run on all kind of devices. 

# Current Features
* create album
* upload photos&videos
* play videos(also support playlist)
* photo gallery
* DLNA cast, play photo&video on TV
* support multi language(en/zh-Hans)

# Requirements(e.g. in CentOS)
* docker
`yum -y install docker`

`service docker start`

* git
`yum -y install git`

* ~/.ssh/id_rsa.pub
`ssh-keygen -t rsa`

# Getting Started（Recommend docker）
* download project

`git clone git@github.com:huoyijie/weku.git`

* build docker image

`cd $PWD/weku && cp ~/.ssh/id_rsa.pub docker/ && docker build -t weku:1.0 .`

* run

`docker run -d --net=host --name weku -v wekudata:/data weku:1.0`

* create super user(input admin username/email/password)

docker exec -it `docker ps -l | grep weku | awk '{print $1}'` python manage.py createsuperuser

* open browser

type url `http://ip:9090`

# Special Thanks
* Python/Django
* [video.js](https://github.com/videojs/video.js), [videojs-playlist](https://github.com/brightcove/videojs-playlist)
* [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)
* [Gallery](https://github.com/blueimp/Gallery)
* [FFmpeg](https://github.com/FFmpeg/FFmpeg)

# Minute Commute Project Notes

## Test Run on AWS Instance


### after ssh to a new AWS instance
or use docker?
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx
sudo apt-get -y install mysql-server postfix supervisor git
sudo pip3 install virtualenv
```

### make a parent directory
```
mkdir ~/myproject
cd ~/myproject

virtualenv myprojectenv
source myprojectenv/bin/activate
```

### in the (env):
```
pip install gunicorn flask
pip install pymysql

nano ~/myproject/myproject.py

nano ~/myproject/wsgi.py

gunicorn --bind 0.0.0.0:5000 wsgi:app


```




### supervisor
set a conf for supervisor to control the gunicorn
```
sudo nano /etc/supervisor/conf.d/gunicorn.conf
```

Care about the `wsgi` is the name of `wsgi.py`, `app` is the module in `wsgi.py`
IP and Port `127.0.0.1:8000` is the same as in nginx config `http://127.0.0.1:8000`
`user = ubuntu`, `command = /home/ubuntu/...`, `directory = /home/ubuntu/...` how to automatically adjust it?
```
[program:gunicorn]
command = /home/ubuntu/myproject/myprojectenv/bin/gunicorn -w 4 -b 127.0.0.1:8000 -k gevent wsgi:app
directory = /home/ubuntu/myproject
autorestart = true
autostart = true
startsecs = 5
startretries = 3
user = ubuntu
nodaemon = false
```
After set the conf: reload and check the supervisor:

```
sudo supervisorctl reload
sudo supervisorctl status

```

### nginx
```
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/myproject
```

```
server {
    # listen on port 80 (http)
    listen 80;
    server_name <******>;
    
    # write access and error logs to /var/log
    access_log /var/log/myproject_access.log;
    error_log /var/log/myproject_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://127.0.0.1:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }    
    
    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/ubuntu/myproject/app/static;
        expires 30d;
    }

}
```

### If index.html changed, restart supervisor, check status.:
```
sudo supervisorctl reload
sudo supervisorctl status
```
Stop all the process in Supervisor:
```
sudo supervisorctl stop all
```

### If want to start/stop/restart Nginx:

```
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
```


## Using Docker on AWS Instance

Launch a new Amazon Linux VM, then install Docker and git
```
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```
log out and log in to pickup the added group

then install git
```
sudo yum install -y git
```

git clone this repo
```
git clone https://github.com/pzeng123/Insight2018DO.git
```
cd into Insight2018DO and build docker
```
docker build -t mc1 .
```


run docker image just built
```
docker run -p 80:80 mc1
```







## install docker on ubuntu 18.04

https://unix.stackexchange.com/questions/363048/unable-to-locate-package-docker-ce-on-a-64bit-ubuntu
You can install docker-ce on Ubuntu 16.04 as follows:
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
sudo apt-get update
```
Run the following

apt-cache search docker-ce
sample output:

docker-ce - Docker: the open-source application container engine
Install docker-ce:
```
sudo apt-get install docker-ce
```
Update Jan 03 2018

installing docker-ce on Ubuntu 17.10 :

docker-ce package is available on the official docker (Ubutu Artful) repository , to install it use the following commands :

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu artful stable"
sudo apt update
sudo apt install docker-ce
Update Apr 29 2018 : Installing docker-ce on Ubuntu 18.04 (bionic)

A testing (note the test instead of stable) release is available for Ubuntu 18.04 it can installed as follows:

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic test"
sudo apt update
sudo apt install docker-ce
The above command will install the testing release available on the pool/test/amd64/

$ docker --version
Docker version 18.05.0-ce-rc1, build 33f00ce













## ports vs expose in Dockerfile
https://stackoverflow.com/questions/40801772/what-is-the-difference-between-docker-compose-ports-vs-expose



## reference
http://www.ameyalokare.com/docker/2017/09/20/nginx-flask-postgres-docker-compose.html
https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example

http://www.patricksoftwareblog.com/how-to-use-docker-and-docker-compose-to-create-a-flask-application/
https://gitlab.com/patkennedy79/flask_recipe_app




## github
git clone only the branch:

git clone -b feature_bg --single-branch https://github.com/pzeng123/Insight2018DO.git


push to a new branch:

Create a new branch:
```
git checkout -b feature_branch_name
```
Edit, add and commit your files.
Push your branch to the remote repository:
```
git push -u origin feature_branch_name

```










## postgresql

install
```
sudo apt-get install postgresql-client

sudo apt-get install postgresql
```

add <new user> and <new database>
```
sudo su - postgres

psql

set a password for postgres

\password postgres

CREATE USER <dbuser> WITH PASSWORD 'password';

CREATE DATABASE <exampledb> OWNER <dbuser>;

GRANT ALL PRIVILEGES ON DATABASE <exampledb> to <dbuser>;

\q




# others

in `__init__.py`
`db.drop_all()` before `db.create_all()`
or will be `sqlalchemy.exc.IntegrityError: (psycopg2.IntegrityError) duplicate key value violates unique constraint "pg_type_typname_nsp_index"
` error because database was there.






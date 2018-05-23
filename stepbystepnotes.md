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

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
sudo apt-get update
Run the following

apt-cache search docker-ce
sample output:

docker-ce - Docker: the open-source application container engine
Install docker-ce:

sudo apt-get install docker-ce
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


















## github
git clone only the branch:

git clone -b feature_bg --single-branch https://github.com/pzeng123/Insight2018DO.git
















## postgresql

一、安装

首先，安装PostgreSQL客户端。

sudo apt-get install postgresql-client

然后，安装PostgreSQL服务器。

sudo apt-get install postgresql

正常情况下，安装完成后，PostgreSQL服务器会自动在本机的5432端口开启。

如果还想安装图形管理界面，可以运行下面命令，但是本文不涉及这方面内容。

sudo apt-get install pgadmin3

二、添加新用户和新数据库

初次安装后，默认生成一个名为postgres的数据库和一个名为postgres的数据库用户。这里需要注意的是，同时还生成了一个名为postgres的Linux系统用户。

下面，我们使用postgres用户，来生成其他用户和新数据库。好几种方法可以达到这个目的，这里介绍两种。

第一种方法，使用PostgreSQL控制台。

首先，新建一个Linux新用户，可以取你想要的名字，这里为dbuser。

sudo adduser dbuser

然后，切换到postgres用户。

sudo su - postgres

下一步，使用psql命令登录PostgreSQL控制台。

psql

这时相当于系统用户postgres以同名数据库用户的身份，登录数据库，这是不用输入密码的。如果一切正常，系统提示符会变为"postgres=#"，表示这时已经进入了数据库控制台。以下的命令都在控制台内完成。

第一件事是使用\password命令，为postgres用户设置一个密码。

\password postgres

第二件事是创建数据库用户dbuser（刚才创建的是Linux系统用户），并设置密码。

CREATE USER dbuser WITH PASSWORD 'password';

第三件事是创建用户数据库，这里为exampledb，并指定所有者为dbuser。

CREATE DATABASE exampledb OWNER dbuser;

第四件事是将exampledb数据库的所有权限都赋予dbuser，否则dbuser只能登录控制台，没有任何数据库操作权限。

GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser;

最后，使用\q命令退出控制台（也可以直接按ctrl+D）。

\q

第二种方法，使用shell命令行。

添加新用户和新数据库，除了在PostgreSQL控制台内，还可以在shell命令行下完成。这是因为PostgreSQL提供了命令行程序createuser和createdb。还是以新建用户dbuser和数据库exampledb为例。

首先，创建数据库用户dbuser，并指定其为超级用户。

sudo -u postgres createuser --superuser dbuser

然后，登录数据库控制台，设置dbuser用户的密码，完成后退出控制台。

sudo -u postgres psql

\password dbuser

\q

接着，在shell命令行下，创建数据库exampledb，并指定所有者为dbuser。

sudo -u postgres createdb -O dbuser exampledb

三、登录数据库

添加新用户和新数据库以后，就要以新用户的名义登录数据库，这时使用的是psql命令。

psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432

上面命令的参数含义如下：-U指定用户，-d指定数据库，-h指定服务器，-p指定端口。

输入上面命令以后，系统会提示输入dbuser用户的密码。输入正确，就可以登录控制台了。

psql命令存在简写形式。如果当前Linux系统用户，同时也是PostgreSQL用户，则可以省略用户名（-U参数的部分）。举例来说，我的Linux系统用户名为ruanyf，且PostgreSQL数据库存在同名用户，则我以ruanyf身份登录Linux系统后，可以直接使用下面的命令登录数据库，且不需要密码。

psql exampledb

此时，如果PostgreSQL内部还存在与当前系统用户同名的数据库，则连数据库名都可以省略。比如，假定存在一个叫做ruanyf的数据库，则直接键入psql就可以登录该数据库。

psql

另外，如果要恢复外部数据，可以使用下面的命令。

psql exampledb < exampledb.sql

四、控制台命令

除了前面已经用到的\password命令（设置密码）和\q命令（退出）以外，控制台还提供一系列其他命令。

\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
\e：打开文本编辑器。
\conninfo：列出当前数据库和连接的信息。
五、数据库操作

基本的数据库操作，就是使用一般的SQL语言。

# 创建新表 
CREATE TABLE user_tbl(name VARCHAR(20), signup_date DATE);

# 插入数据 
INSERT INTO user_tbl(name, signup_date) VALUES('张三', '2013-12-22');

# 选择记录 
SELECT * FROM user_tbl;

# 更新数据 
UPDATE user_tbl set name = '李四' WHERE name = '张三';

# 删除记录 
DELETE FROM user_tbl WHERE name = '李四' ;

# 添加栏位 
ALTER TABLE user_tbl ADD email VARCHAR(40);

# 更新结构 
ALTER TABLE user_tbl ALTER COLUMN signup_date SET NOT NULL;

# 更名栏位 
ALTER TABLE user_tbl RENAME COLUMN signup_date TO signup;

# 删除栏位 
ALTER TABLE user_tbl DROP COLUMN email;

# 表格更名 
ALTER TABLE user_tbl RENAME TO backup_tbl;

# 删除表格 
DROP TABLE IF EXISTS backup_tbl;











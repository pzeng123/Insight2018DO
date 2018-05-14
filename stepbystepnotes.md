## Install steps

### ssh to aws instance

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

### If index.html changed, restart supervisor:
```
sudo supervisorctl reload
sudo supervisorctl status
```

### If want to start/stop/restart Nginx:

```
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
```

#


FROM ubuntu:16.04
LABEL author="Peng"

# install python3 nginx supervisor gunicorn
RUN apt-get update && apt-get install -y python3 python3-dev python3-pip \
        nginx supervisor
RUN pip3 install gunicorn setuptools


# Build Folder
RUN mkdir -p /deploy/MinuteCommute
WORKDIR /deploy/MinuteCommute
#at first copy requirements.txt.
COPY requirements.txt /deploy/MinuteCommute
RUN pip3 install -r /deploy/MinuteCommute/requirements.txt


COPY . /deploy/MinuteCommute

# Setup nginx
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
COPY nginx-app.conf /etc/nginx/conf.d/

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

EXPOSE 80

CMD ["/usr/bin/supervisord"]

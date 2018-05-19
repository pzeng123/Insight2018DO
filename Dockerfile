# nginx-gunicorn-flask with python3


FROM ubuntu:16.04
LABEL author="Peng"

# 安装git、python、nginx、supervisor
RUN apt-get update
RUN apt-get install -y git python python-dev python-setuptools python-pip \
        nginx supervisor libmysqlclient-dev
RUN pip install gunicorn
RUN pip install setuptools

# 环境变量
ENV MYSQL_DATABASE_NAME MCdatabase
ENV EMAIL_HOST_USER my-email@email.com
ENV EMAIL_HOST_PASSWORD my-secret-email-password

# Build Folder
RUN mkdir -p /deploy/MC
COPY . /deploy/MC
# Install requirements
RUN pip install -r /deploy/MC/Docker/Main/requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx-app.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisor-app.conf /etc/supervisor/conf.d/
COPY gunicorn.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["/usr/bin/supervisord"]

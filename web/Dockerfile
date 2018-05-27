# Dockerfile for web application
FROM python:3.6.1
LABEL author="Peng"

# Build Folder
RUN mkdir -p /usr/src/app/web
WORKDIR /usr/src/app/web

#first copy requirements.txt, separated from copying all the source code.
COPY requirements.txt /usr/src/app/web
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /usr/src/app/web


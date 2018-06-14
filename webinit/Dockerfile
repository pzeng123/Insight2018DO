# Dockerfile for web application
FROM python:3.6.1
LABEL author="Peng"

# Build Folder
RUN mkdir -p /usr/src/app/webinit
WORKDIR /usr/src/app/webinit

#first copy requirements.txt, separated from copying all the source code.
COPY requirements.txt /usr/src/app/webinit
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /usr/src/app/webinit

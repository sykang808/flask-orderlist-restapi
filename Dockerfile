FROM 566034038752.dkr.ecr.us-west-2.amazonaws.com/python:latest
LABEL maintainer "sykang@amazon.com>" 
LABEL "enviroment"="dev"
RUN apt-get update
ADD . /www
WORKDIR /www
EXPOSE 80
RUN pip3 install -r requirements.txt
CMD uwsgi uwsgi.ini

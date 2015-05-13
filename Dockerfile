FROM python:3-wheezy
RUN apt-get update
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

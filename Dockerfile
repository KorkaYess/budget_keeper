# pull official base image
FROM python:3

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy project
COPY . /app/

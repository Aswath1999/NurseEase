FROM mcr.microsoft.com/devcontainers/python:0-3.11
WORKDIR /app
RUN apk update
RUN apk add --no-cache git
RUN apk add --no-cache docker-engine
RUN apk add --no-cache docker-cli
RUN apk add --no-cache docker-compose
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000


FROM mcr.microsoft.com/devcontainers/python:0-3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000


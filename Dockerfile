FROM mcr.microsoft.com/devcontainers/python:0-3.11
WORKDIR /app
COPY requirements.txt .
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

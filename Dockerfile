#Dockerfile when setting up locally
# FROM mcr.microsoft.com/devcontainers/python:0-3.11
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#Dockerfile when setting up in codespaces with codespaces secretts
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Install necessary dependencies
RUN apt-get update && apt-get install -y git curl

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh



# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Set the environment variables with the secret values
ARG DATABASE
ARG DATABASE_URL
ARG MAIL_FROM
ARG MAIL_PASSWORD
ARG MAIL_SERVER
ARG MAIL_USERNAME
ARG SECRET_KEY
ARG USER
ARG MAIL_PORT
ENV DATABASE=${DATABASE}
ENV DATABASE_URL=${DATABASE_URL}
ENV MAIL_FROM=${MAIL_FROM}
ENV MAIL_PASSWORD=${MAIL_PASSWORD}
ENV MAIL_SERVER=${MAIL_SERVER}
ENV MAIL_USERNAME=${MAIL_USERNAME}
ENV SECRET_KEY=${SECRET_KEY}
ENV USER=${USER}
ENV MAIL_PORT=${MAIL_PORT}

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Expose the necessary port
EXPOSE 8000

# Start the FastAPI server with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


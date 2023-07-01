FROM mcr.microsoft.com/devcontainers/python:0-3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# FROM mcr.microsoft.com/devcontainers/python:0-3.11

# # Install necessary dependencies
# RUN apt-get update && apt-get install -y git curl

# # Install GitHub CLI
# RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
#     && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
#     && apt-get update \
#     && apt-get install -y gh

# # Install Docker
# RUN curl -fsSL https://get.docker.com -o get-docker.sh
# RUN sh get-docker.sh

# # Install Docker Compose
# RUN apt-get install -y docker-compose
# # Set the working directory
# WORKDIR /app

# # Copy the requirements file
# COPY requirements.txt .


# # Install project dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the project files to the working directory
# COPY . .

# # Retrieve the encrypted secrets from GitHub Codespaces
# ARG MY_TOKEN
# RUN export DATABASE=$(gh secret repo get NurseEase DATABASE --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export DATABASE_URL=$(gh secret repo get NurseEase DATABASE_URL --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export MAIL_FROM=$(gh secret repo get NurseEase MAIL_FROM --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export MAIL_PASSWORD=$(gh secret repo get NurseEase MAIL_PASSWORD --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export MAIL_SERVER=$(gh secret repo get NurseEase MAIL_SERVER --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export MAIL_USERNAME=$(gh secret repo get NurseEase MAIL_USERNAME --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export SECRET_KEY=$(gh secret repo get NurseEase SECRET_KEY --json token=${MY_TOKEN} --jq .value --unwrap) \
#     && export USER=$(gh secret repo get NurseEase USER --json token=${MY_TOKEN} --jq .value --unwrap)

# # Set the environment variables with the secret values
# ENV DATABASE=${DATABASE}
# ENV DATABASE_URL=${DATABASE_URL}
# ENV MAIL_FROM=${MAIL_FROM}
# ENV MAIL_PASSWORD=${MAIL_PASSWORD}
# ENV MAIL_SERVER=${MAIL_SERVER}
# ENV MAIL_USERNAME=${MAIL_USERNAME}
# ENV SECRET_KEY=${SECRET_KEY}
# ENV USER=${USER}

# # Expose the necessary port
# EXPOSE 8000

# # Start the FastAPI server with uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


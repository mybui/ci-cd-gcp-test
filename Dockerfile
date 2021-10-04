# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# set the working directory in the container
WORKDIR /app

# copy the content of the local src directory to the working directory
COPY src /app

# Bitbucket app password for to pull from private IDBBN repo
ARG BIT_USER
ENV BIT_USER ${BIT_USER}

ARG BIT_APP_PASS
ENV BIT_APP_PASS ${BIT_APP_PASS}

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define $PORT environment variable.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 app:app
# Use an official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Firefox
RUN apt-get update && \
    apt-get install -y firefox-esr

# Install Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz && \
    tar -xvzf geckodriver-v0.33.0-linux-aarch64.tar.gz && \
    rm geckodriver-v0.33.0-linux-aarch64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/6

# Make port 5000 available to the world outside this container
EXPOSE 5000

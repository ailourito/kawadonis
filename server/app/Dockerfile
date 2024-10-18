# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Need cmake to build dlib etc
# This could take up to 20 minutes,because the build for g++ and cmake is slow AF
RUN apt-get update && \
    apt-get install -y cmake g++ libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# # Expose the port your app runs on
# EXPOSE 5000

# # Set the environment variable for Flask
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0


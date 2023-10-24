# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Node.js and PM2. 
# We need Node.js as PM2 is a Node.js application.
RUN apt-get update && apt-get install -y nodejs npm && \
    npm install -g pm2

# Copy the rest of the application code into the container.
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an environment variable
# Use -e flag with docker run to override
ENV TELEGRAM_TOKEN undefined

# Command to run PM2 using the configuration file.
CMD ["pm2-runtime", "start", "pm2.json"]
# Use an official Python 3.12 runtime as a parent image with the correct platform
FROM --platform=linux/amd64 python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Run Chainlit when the container launches
CMD ["chainlit", "run", "main.py", "--port", "8080"]
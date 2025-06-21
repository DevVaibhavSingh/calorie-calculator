# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the .env file into the container (if it's in the same directory as your Dockerfile)
COPY /app/.env /app/.env

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the start.sh script into the container
COPY start.sh /app/start.sh

# Give the script execution permissions
RUN chmod +x /app/start.sh

# Expose port 8000 to access the app from outside the container
EXPOSE 8000

# Use the start.sh script as the entrypoint to run migrations and then start FastAPI
CMD ["/app/start.sh"]

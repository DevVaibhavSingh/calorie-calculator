# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to access the app from outside the container
EXPOSE 8000

# Run the FastAPI app using Uvicorn (with a host of 0.0.0.0 to make it publicly accessible)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

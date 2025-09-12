# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code
COPY . .

# Expose the port your application will listen on
EXPOSE 8080

# This will look for a module named 'main_v2' inside the 'app' directory.
CMD ["uvicorn", "app.main_v2:app", "--host", "0.0.0.0", "--port", "8080"]

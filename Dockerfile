# Use the official Python 3.11 image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and CSV files into the container
COPY src /app/src
COPY src/*.csv /app/

# Install  libraries
RUN pip install --no-cache-dir -r requirements.txt

# Start the application
CMD ["python", "src/main.py"]

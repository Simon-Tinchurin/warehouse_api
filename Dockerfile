# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy all the other project files into the working directory
COPY . .

# Specify the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use a slim Python image
FROM python:3.9-slim

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest for testing
RUN pip install --no-cache-dir pytest

# Copy the application code into the container
COPY . /app/

# Expose the correct port (Cloud Run expects your container to listen on port 8080)
EXPOSE 8080

# Run the app using Flask's built-in server (main.py is the entry point now)
CMD ["python", "main.py"]
# Dockerfile
# Use a slim Python image
FROM python:3.9-slim

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set environment variables for secret keys during the build
ARG API_KEY
ENV API_KEY=$API_KEY

# Install dependencies
RUN pip install --no-cache-dir google-cloud-secret-manager

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Run tests with pytest before starting the app
RUN pytest --maxfail=1 --disable-warnings -q

# Expose the correct port (Cloud Run expects your container to listen on port 8080)
EXPOSE 8080


# Run the app using Flask's built-in server (main.py is the entry point now)
CMD ["python", "main.py"]
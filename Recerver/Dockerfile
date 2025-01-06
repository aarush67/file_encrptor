# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY server.py /app/

# Create a directory for storing keys
RUN mkdir -p /app/keys

# Set environment variables for Flask
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Install dependencies
RUN pip install --no-cache-dir flask flask-cors

# Expose the port the Flask app will run on
EXPOSE 4998

# Set the command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=4998"]

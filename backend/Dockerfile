# Use the official Python image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend code to the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the port the container will listen on
EXPOSE 3030

# Set the command to run your app
CMD ["python", "app.py"]

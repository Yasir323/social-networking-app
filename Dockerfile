# Use the official Python image.
FROM python:3.10-slim-buster

# Set the working directory.
WORKDIR /app

# Install the dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the project files.
COPY . .

# Expose the port the app runs on.
EXPOSE 8000

# Default command to run when container starts.
CMD ["python3", "./soccial_networking/manage.py", "runserver", "0.0.0.0:8000"]

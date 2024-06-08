# Use the official Python image.
FROM python:3.10-slim-buster

# Set the working directory.
WORKDIR /app

# Install the dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the project files.
COPY . .

# Run database migrations and collect static files.
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port the app runs on.
EXPOSE 8000

# Start the application.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

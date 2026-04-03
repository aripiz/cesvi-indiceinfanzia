FROM python:3.11-slim

# Set envionment variables
# ENV PYTHONUNBUFFERED 1

# Run this before copying requirements for cache efficiency
RUN pip install --upgrade pip

# Adding requirements file to current directory
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install -r /requirements.txt

# Copy code itself from context to image
COPY ./app /app

WORKDIR /app

EXPOSE 8080

# Run from working directory, and separate args in the json syntax
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:server"]

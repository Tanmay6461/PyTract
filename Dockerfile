# Use the official Python 3.10-slim image
FROM --platform=linux/amd64 python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies separately to leverage Docker cache
COPY requirements.txt /app/
RUN pip install  -r requirements.txt 

# Copy the rest of the application code
COPY . /app/

ENV PORT=8080
# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]


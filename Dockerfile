# Use an official lightweight Python image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to start FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

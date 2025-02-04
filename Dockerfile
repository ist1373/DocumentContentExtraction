FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update 

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy the entire application code into the container
COPY . /app

# Expose the application port
EXPOSE 8001

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8004"]

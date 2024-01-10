# System software for execute 
FROM python:3.8-slim-buster

WORKDIR /app

# Installing dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install necessary software
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Envioronment variables
ARG data_clickgreen
ENV data_clickgreen=$data_clickgreen

# Copy the app information to the Image
COPY . .

# Execute the app in API format
CMD ["python", "app.py"]



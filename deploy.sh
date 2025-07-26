#!/bin/bash

# Build and deploy script for Render

echo "Building Docker image..."
docker build -t book-reader-spacy-api .

echo "Testing image locally..."
docker run -p 8000:8000 book-reader-spacy-api &
sleep 5

echo "Testing API..."
curl http://localhost:8000/health

echo "Stopping local container..."
docker stop $(docker ps -q --filter ancestor=book-reader-spacy-api)

echo "Deploy to Render:"
echo "1. Go to https://render.com"
echo "2. Create new Web Service"
echo "3. Choose 'Deploy an existing image from a registry'"
echo "4. Use image: your-dockerhub-username/book-reader-spacy-api"
echo "5. Set port to 8000"
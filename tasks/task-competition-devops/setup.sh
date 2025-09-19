#!/bin/bash
set -e
echo "Building Docker image (fixed-node-app)..."
docker build -t fixed-node-app .
echo "Running container to test..."
docker run -d --name fixed-node-app -p 3000:3000 --env-file .env fixed-node-app
sleep 2
echo "App response:"
curl -s http://localhost:3000 || true
docker stop fixed-node-app && docker rm fixed-node-app
echo "Kubernetes deploy (requires kubectl & cluster):"
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
echo "Done"

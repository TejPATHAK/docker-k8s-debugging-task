#!/bin/bash
set -e

cat > Dockerfile <<'EOF'
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY . .
EXPOSE 3000
ENV MESSAGE="Hello from container"
CMD ["node", "app.js"]
EOF

docker build -t simple-docker-k8s-task:latest .

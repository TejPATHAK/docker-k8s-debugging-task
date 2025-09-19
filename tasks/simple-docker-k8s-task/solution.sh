#!/bin/bash
set -e

cat > Dockerfile <<'EOF'
FROM node:18-alpine

WORKDIR /app
COPY package.json .
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
EOF

docker build -t simple-docker-k8s-task:latest .

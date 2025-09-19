        # Oracle solution (fixed Dockerfile and steps)
        # This script shows the expected fixes and is NOT executed by tests.
        cat > Dockerfile.fixed <<'EOF'
FROM node:18-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
# pre-bundled node_modules included in task; no npm install required
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
EOF

echo "Fixed Dockerfile written to Dockerfile.fixed"

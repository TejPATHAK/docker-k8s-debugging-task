# Broken Dockerfile (intentional bugs for candidate to fix)
FROM node:18-alpine
WORKDIR /usr/src/app
# Note: node_modules are pre-bundled to avoid network installs during grading
COPY package.json package-lock.json ./
# Intentionally not running npm install in broken version
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]  # wrong entrypoint (should be app.js)

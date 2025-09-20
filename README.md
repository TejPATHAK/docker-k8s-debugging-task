# Simple Docker + Kubernetes Task

Task Summary

- This project demonstrates the creation, deployment, and testing of a Dockerized Node.js application using Kubernetes. It includes:

- Building a Docker image

- Running the container locally and verifying with automated tests

- Deploying the application on Kubernetes using Deployment and Service manifests

- CI/CD integration using automated test scripts

---
## Domain Chosen

Containerization and Orchestration (Docker + Kubernetes) with DevOps practices.

---
## Features
- Simple Node.js app serving a message (`Hello from container!` by default).
- Configurable via `MESSAGE` environment variable.
- Dockerized and tested with **pytest**.
- Deployable on Kubernetes with **Deployment** + **Service** manifests.

---

## Prerequisites
Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Kubernetes](https://kubernetes.io/docs/tasks/tools/) (e.g. Minikube)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [pytest](https://docs.pytest.org/en/stable/) (for running tests)

---

## Run Locally with Docker

### Build the image
```bash
docker build -t simple-docker-k8s-task:latest .
```

### Run the container
```bash
docker run -d -p 3000:3000 simple-docker-k8s-task:latest
```

### Test the output
```bash
curl http://localhost:3000
# Expected output: Hello from container!
```

### Override with environment variable
```bash
docker run -d -p 3000:3000 -e MESSAGE="Custom message" simple-docker-k8s-task:latest
curl http://localhost:3000
# Expected output: Custom message
```

---

## Run Tests
Tests automatically validate Docker build, default message, and env override.

```bash
bash run-tests.sh
```

Expected: All tests should pass 

---

## Deploy on Kubernetes

### Apply manifests
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Check pod status
```bash
kubectl get pods
```

### Port-forward the service
```bash
kubectl port-forward service/simple-docker-k8s-task-service 8080:3000
```

### Test the app via service
```bash
curl http://localhost:8080
# Expected output: Hello from kubernetes!
```

---

## Project Structure
```
.
├── app.js               # Node.js app
├── Dockerfile           # Docker build instructions
├── .env
├── requirements.txt
├── package.json
├── tests/
│   └── test_outputs.py  # Pytest cases
├── run-tests.sh         # Script to run tests
├── solution.sh
└── k8s/
    ├── deployment.yaml  # K8s Deployment
    └── service.yaml     # K8s Service
```

---

## Notes

- Application runs internally on port 4000. The service maps it to 3000 externally.

- If curl fails, ensure no other process is occupying port 3000.

- CI/CD scripts include automated tests using requests and dynamic free port allocation.

- Ensure Docker and Kubernetes (Minikube or cluster) are running and configured correctly.

For any issues, verify container logs:
```
kubectl logs <pod_name>
```
---

## Author
Tejaswi Pathak  
*Cloud & DevOps Enthusiast | Docker | Kubernetes | CI/CD*

        Competition-level DevOps task (Domain: Docker + Kubernetes)

        Summary:
        - Fix the broken Dockerfile so the Node.js app builds and runs (app reads APP_NAME from env).
        - Deploy to Kubernetes using provided manifests and verify behavior with tests.

        Quickstart:

        1) Build & test locally (Docker required):
   ./setup.sh

2) Run automated tests (requires docker + kubectl + access to K8s cluster):
   ./run-tests.sh

Caveats:
- Node modules are bundled in node_modules/ to avoid network installs.
- Docker base image still needs to be pulled (node:18-alpine). If grading system disallows network, use cached base image.

Checklist included in task.yaml

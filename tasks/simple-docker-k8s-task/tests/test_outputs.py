import os
import subprocess
import time
import requests
import socket

APP_IMAGE = "simple-docker-k8s-task:latest"

def run_cmd(cmd):
    """Run a shell command and raise error if it fails."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def get_free_port():
    """Get a free port from the OS for mapping."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def wait_for_container(port, timeout=15):
    """Wait until the container responds on HTTP port."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"http://localhost:{port}")
            return r
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    raise TimeoutError(f"Container on port {port} did not start in {timeout} seconds")

# ---------------- TESTS ---------------- #

def test_1_docker_build():
    """Build the Docker image."""
    run_cmd(f"docker build -t {APP_IMAGE} .")

def test_2_docker_run_default():
    """Run container with default message and check output."""
    port = get_free_port()
    cid = run_cmd(f"docker run -d -p {port}:3000 {APP_IMAGE}")
    try:
        r = wait_for_container(port)
        assert r.text.strip() == "Hello from container!", f"Expected default message, got {r.text}"
    finally:
        run_cmd(f"docker rm -f {cid}")

def test_3_docker_run_env():
    """Run container with MESSAGE env variable and check output."""
    port = get_free_port()
    cid = run_cmd(f"docker run -d -p {port}:3000 -e MESSAGE='EnvTest' {APP_IMAGE}")
    try:
        r = wait_for_container(port)
        assert r.text.strip() == "EnvTest", f"Expected env override, got {r.text}"
    finally:
        run_cmd(f"docker rm -f {cid}")


def test_4_port_exposed():
    dockerfile_content = open("Dockerfile").read()
    assert "3000" in dockerfile_content, "Dockerfile must expose port 3000"

def test_5_k8s_apply():
    run_cmd("kubectl apply -f k8s/deployment.yaml")
    run_cmd("kubectl apply -f k8s/service.yaml")

def test_6_k8s_pod_running():
    for _ in range(10):
        pods = run_cmd("kubectl get pods -l app=simple-docker-k8s-task --no-headers")
        if pods and "Running" in pods:
            return
        time.sleep(5)
    raise AssertionError("Kubernetes pod did not reach Running state")

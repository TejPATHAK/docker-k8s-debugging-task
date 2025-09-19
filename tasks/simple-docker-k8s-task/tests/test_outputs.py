import os
import subprocess
import time
import requests

APP_IMAGE = "simple-docker-k8s-task:latest"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def test_1_docker_build():
    run_cmd(f"docker build -t {APP_IMAGE} .")

def test_2_docker_run_default():
    cid = run_cmd(f"docker run -d -p 3000:3000 {APP_IMAGE}")
    time.sleep(3)
    r = requests.get("http://localhost:3000")
    assert r.text.strip() == "Hello from container!", f"Expected default message, got {r.text}"
    run_cmd(f"docker rm -f {cid}")

def test_3_docker_run_env():
    cid = run_cmd(f"docker run -d -p 3000:3000 -e MESSAGE='EnvTest' {APP_IMAGE}")
    time.sleep(3)
    r = requests.get("http://localhost:3000")
    assert r.text.strip() == "EnvTest", f"Expected env override, got {r.text}"
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

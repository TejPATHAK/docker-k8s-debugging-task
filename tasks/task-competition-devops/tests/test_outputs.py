#!/usr/bin/env python3
import subprocess, sys, time, os

def run(cmd, check=True, capture=True):
    res = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}")
    return res.stdout.strip()

def test_docker_build():
    print('1) Docker build...')
    run('docker build -t fixed-node-app .')
    print('  Docker build OK')

def test_docker_run():
    print('2) Docker run...')
    run('docker run -d --name fixed-node-app -p 3000:3000 --env-file .env fixed-node-app')
    time.sleep(1)
    out = run('curl -s http://localhost:3000')
    run('docker stop fixed-node-app && docker rm fixed-node-app')
    if 'TerminalBench-Competition' not in out:
        raise AssertionError(f"App response mismatch: got '{out}'")
    print('  Docker run OK')

def test_k8s_deployment_replicas():
    print('3) K8s deployment replicas...')
    out = run("kubectl get deployment competition-node-app -o jsonpath='{.spec.replicas}'")
    if out != '2':
        raise AssertionError(f"Expected 2 replicas, got {out}")
    print('  Deployment replicas OK')

def test_k8s_service():
    print('4) K8s service port...')
    out = run("kubectl get svc competition-node-app-service -o jsonpath='{.spec.ports[0].port}'")
    if out != '3000':
        raise AssertionError(f"Expected service port 3000, got {out}")
    print('  Service OK')

def test_hpa_values():
    print('5) HPA values...')
    mn = run("kubectl get hpa competition-node-app-hpa -o jsonpath='{.spec.minReplicas}'")
    mx = run("kubectl get hpa competition-node-app-hpa -o jsonpath='{.spec.maxReplicas}'")
    if mn != '2' or mx != '5':
        raise AssertionError(f"HPA min/max mismatch: {mn}/{mx}")
    print('  HPA OK')

def test_env_vars():
    print('6) Env vars in pod...')
    pod = run("kubectl get pods -l app=competition-node-app -o jsonpath='{.items[0].metadata.name}'")
    app_name = run(f"kubectl exec {pod} -- printenv APP_NAME")
    secret = run(f"kubectl exec {pod} -- printenv DUMMY_SECRET")
    if app_name != 'TerminalBench-Competition':
        raise AssertionError(f"APP_NAME mismatch: {app_name}")
    if secret != 'topsecret':
        raise AssertionError(f"DUMMY_SECRET mismatch: {secret}")
    print('  Env vars OK')

def test_determinism():
    print('7) Determinism of builds...')
    out1 = run('docker build -t fixed-node-app .')
    out2 = run('docker build -t fixed-node-app .')
    if out1 != out2:
        raise AssertionError('Docker builds differ between runs')
    print('  Determinism OK')

if __name__ == '__main__':
    tests = [
        test_docker_build,
        test_docker_run,
        test_k8s_deployment_replicas,
        test_k8s_service,
        test_hpa_values,
        test_env_vars,
        test_determinism
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print('\nFAIL:', e)
            failed += 1
    if failed:
        print(f"\n{failed} tests failed")
        sys.exit(1)
    print('\nALL TESTS PASSED')

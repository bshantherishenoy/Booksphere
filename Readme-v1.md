# Booksphere — End-to-End DevOps & Kubernetes Project

## Overview

Booksphere is a cloud-native DevOps project built to demonstrate:

* CI/CD automation
* Containerization
* Kubernetes orchestration
* Cloud deployment
* Load balancing
* Self-healing infrastructure
* Performance testing with k6

The project starts as a simple Flask application and evolves into a production-style Kubernetes deployment running on AWS EC2 using K3s.

---

# Tech Stack

| Category           | Technology        |
| ------------------ | ----------------- |
| Backend            | Python Flask      |
| Containerization   | Docker            |
| CI/CD              | GitHub Actions    |
| Container Registry | DockerHub         |
| Orchestration      | Kubernetes (K3s)  |
| Cloud              | AWS EC2           |
| Load Testing       | k6                |
| Monitoring         | Grafana (planned) |
| Infrastructure     | Linux / Debian    |

---

# Project Architecture

```text
Developer Push
      ↓
GitHub Actions CI/CD
      ↓
Docker Image Build
      ↓
DockerHub Push
      ↓
AWS EC2 (Debian)
      ↓
K3s Kubernetes Cluster
      ↓
Kubernetes Service Load Balancer
      ↓
Booksphere Flask Application
```

---

# Features Implemented

## 1. Flask Application

Created a lightweight Flask API application.

### Endpoints

| Endpoint  | Purpose              |
| --------- | -------------------- |
| /         | Health check         |
| /books    | Returns sample books |
| /hostname | Returns pod hostname |

---

## 2. Dockerization

Containerized the Flask application using Docker.

### Docker Features

* Lightweight Python base image
* Port exposure
* Dependency installation
* Container startup command

### Commands

Build image:

```bash
docker build -t booksphere-app .
```

Run container:

```bash
docker run -p 5000:5000 booksphere-app
```

---

## 3. Docker Compose

Added Docker Compose support for simplified local development.

### Run

```bash
docker compose up
```

---

# 4. Testing

Implemented automated testing using pytest.

### Run Tests

```bash
pytest
```

---

# 5. GitHub Actions CI/CD Pipeline

Implemented CI pipeline using GitHub Actions.

## Pipeline Stages

```text
Lint → Test → Docker Build → Docker Push
```

### Features

* Automatic pipeline trigger on push
* Python dependency installation
* Flake8 linting
* Pytest execution
* Docker image build
* DockerHub image push

---

# 6. DockerHub Integration

Configured DockerHub integration using GitHub Secrets.

## Secrets Used

| Secret          | Purpose                |
| --------------- | ---------------------- |
| DOCKER_USERNAME | DockerHub username     |
| DOCKER_PASSWORD | DockerHub access token |

### Docker Pull Example

```bash
docker pull <dockerhub-username>/booksphere-app:latest
```

---

# 7. Kubernetes Deployment

Deployed the application on Kubernetes using K3s.

## Kubernetes Resources

| Resource   | Purpose            |
| ---------- | ------------------ |
| Namespace  | Isolation          |
| Deployment | Replica management |
| Service    | Traffic routing    |

---

# 8. Kubernetes High Availability

Configured multiple replicas for high availability.

### Deployment Features

* Multiple pod replicas
* Self-healing deployments
* Rolling updates
* Automatic pod recreation

### Verify Pods

```bash
kubectl get pods -n booksphere
```

---

# 9. Kubernetes Service Load Balancing

Used Kubernetes Service for internal load balancing.

## Service Type

```yaml
NodePort
```

### Traffic Flow

```text
Client Request
      ↓
Kubernetes Service
      ↓
Replica Pods
```

---

# 10. AWS Cloud Deployment

Deployed Kubernetes cluster on AWS EC2.

## EC2 Configuration

| Setting       | Value     |
| ------------- | --------- |
| OS            | Debian 12 |
| Instance Type | t3.small  |
| Kubernetes    | K3s       |

---

# 11. K3s Kubernetes Cluster

Installed lightweight Kubernetes using K3s.

### Installation

```bash
curl -sfL https://get.k3s.io | sh -
```

### Verify Cluster

```bash
sudo kubectl get nodes
```

---

# 12. Public Application Access

Exposed Kubernetes application publicly using NodePort.

### Access URL

```text
http://EC2_PUBLIC_IP:NODEPORT
```

---

# 13. Self-Healing Demonstration

Simulated pod failure and validated Kubernetes self-healing.

### Pod Deletion

```bash
kubectl delete pod POD_NAME -n booksphere
```

### Observed Behavior

* Kubernetes automatically recreated failed pod
* Application remained available
* Traffic routed to healthy replicas

---

# 14. Load Testing Using k6

Implemented load testing using k6.

## Objectives

* Validate Kubernetes load balancing
* Verify traffic distribution
* Test replica failover
* Simulate concurrent traffic

### Example k6 Configuration

```javascript
export const options = {
    vus: 10,
    duration: '20s',
};
```

---

# 15. Replica Traffic Verification

Added hostname endpoint to verify request distribution.

### Example Response

```text
booksphere-app-abc123
```

This confirmed:

* Requests were distributed across replicas
* Kubernetes service load balancing worked correctly
* Failover traffic routing worked during pod deletion

---

# Project Folder Structure

```text
Booksphere/
├── app/
│   ├── __init__.py
│   └── app.py
│
├── tests/
│   └── test_app.py
│
├── k8s/
│   ├── namespace.yml
│   ├── deployment.yml
│   └── service.yml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Kubernetes Deployment Commands

Apply manifests:

```bash
kubectl apply -f k8s/
```

Verify pods:

```bash
kubectl get pods -n booksphere
```

Verify services:

```bash
kubectl get svc -n booksphere
```

Restart deployment:

```bash
kubectl rollout restart deployment booksphere-app -n booksphere
```

---

# Future Enhancements

## Planned Improvements

* Horizontal Pod Autoscaler (HPA)
* Prometheus integration
* Grafana dashboards
* Ingress controller
* Terraform infrastructure automation
* Helm charts
* Blue/Green deployments
* Canary deployments
* ArgoCD GitOps
* Centralized logging

---

# Key DevOps Concepts Demonstrated

## CI/CD

* Automated testing
* Automated image builds
* Automated deployments

## Containers

* Docker image lifecycle
* Container portability
* Registry integration

## Kubernetes

* Deployments
* Services
* Namespaces
* Replicas
* Load balancing
* Self-healing
* Rolling updates

## Cloud

* AWS EC2 provisioning
* Public networking
* Security groups
* NodePort exposure

## Performance Engineering

* Concurrent request simulation
* Replica traffic validation
* Failover testing
* Load distribution analysis

---

# Resume Highlights

* Built end-to-end CI/CD pipeline using GitHub Actions and DockerHub.
* Deployed containerized Flask application on Kubernetes using K3s.
* Implemented high availability using Kubernetes replicas and service load balancing.
* Simulated pod failures and validated Kubernetes self-healing behavior.
* Performed load testing and traffic distribution validation using k6.
* Deployed cloud-native infrastructure on AWS EC2.

---

# Conclusion

This project demonstrates practical DevOps engineering concepts including:

* CI/CD automation
* Kubernetes orchestration
* Cloud deployment
* Observability foundations
* Resiliency testing
* Performance validation

The goal of the project was to simulate a production-style deployment pipeline and demonstrate real-world infrastructure behavior using lightweight cloud-native tooling.

### Full Stack Blogging Application

Job Scenario:
Sometime ago, I was tasked with setting up a CI/CD pipeline for a full-stack blogging app hosted on GitHub.

This project involves integrating Jenkins for build and deployment, using SonarQube for code quality checks,
Nexus for artifact management, and Docker for containerizing the application.

Once deployed, we will monitor the application using Prometheus, Blackbox Exporter, and visualize it with Grafana.

I integrated Email notification script using Groovy to send alerts when the pipeline fails or succeeds. 


![1_9CvhrnA6Fg1LTmMjr3n3Kg](https://github.com/user-attachments/assets/837ea1ca-f69e-40a1-b4ee-15ace4dc3892)

---

### Project Structure.

``` 
/full-stack-blogging-app
├── /ci-scripts
│   ├── install_jenkins.sh
│   ├── install_docker.sh
│   ├── install_blackbox.sh
│   ├── prometheus.yml
│   └── grafana_dashboard.json
├── /kubernetes
│   ├── deployment.yml
│   ├── service.yml
│   ├── role.yaml
│   ├── rolebinding.yaml
│   └── serviceaccount.yaml
├── /terraform
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
├── /src
│   ├── app.js
│   ├── Dockerfile
│   └── ...
├── README.md
```

---

####
---

```markdown
# Full-Stack Blogging App CI/CD Project 🚀

## Project Overview
This project demonstrates a complete **CI/CD pipeline** setup for deploying a full-stack blogging application, integrating modern tools like Jenkins, SonarQube, Nexus, Docker, Kubernetes (EKS), and Prometheus for monitoring. This repository showcases the **automation of code quality checks, artifact management, application deployment, and monitoring** in a production-like environment.

## Key Technologies & Tools
- Jenkins: Continuous Integration and Continuous Deployment.
- SonarQube: Static code analysis for quality and security checks.
- Nexus: Artifact repository manager.
- Docker: Containerization of the application.
- Kubernetes (EKS): Orchestration of containerized applications.
- Prometheus & Grafana: Monitoring and visualization of application performance.
- Blackbox Exporter: Probing application availability and uptime monitoring.

## Objectives
1. Automate the CI/CD pipeline: Automate building, testing, and deploying the blogging app.
2. Enhance code quality and security: Use SonarQube for static code analysis and Trivy for vulnerability scans.
3. Deploy to Kubernetes (EKS): Use Terraform to deploy and manage Kubernetes infrastructure on AWS.
4. Monitor the application: Use Prometheus, Blackbox Exporter, and Grafana for real-time monitoring and alerting.

## Repository Structure
- `/ci-scripts`: Shell scripts for installing Jenkins, Docker, Prometheus, Grafana, and Blackbox Exporter.
- `/kubernetes`: Kubernetes manifests for deploying the app and setting up roles and access.
- `/terraform`: Infrastructure as Code (IaC) files to provision an EKS cluster.
- `/src`: The source code and Dockerfile for the blogging application.

## CI/CD Pipeline Overview

1. **GitHub Integration**: Jenkins pulls the latest changes from the GitHub repository and triggers the pipeline.
2. **Build & Test**:
   - The code is compiled and built using Maven.
   - Code analysis is done using SonarQube.
   - Trivy scans for vulnerabilities.
3. **Docker & Nexus**:
   - Jenkins builds a Docker image for the application.
   - The image is tagged and pushed to DockerHub.
   - Artifacts are pushed to Nexus.
4. **Kubernetes Deployment**:
   - The app is deployed to an EKS cluster.
   - Kubernetes handles scaling and service management.
5. **Monitoring**:
   - Prometheus scrapes metrics from the Blackbox Exporter.
   - Grafana visualizes application uptime, health, and other critical metrics.

## Steps to Reproduce the Project

### 1. Clone the Repository
```bash
git clone https://github.com/devcloudninjas/full-stack-blogging-app.git
cd full-stack-blogging-app
```

### 2. Setup CI/CD Pipeline with Jenkins
- Install Jenkins using the provided script:
```bash
./ci-scripts/install_jenkins.sh 
```
- Configure Jenkins with plugins for Docker, SonarQube, Maven, and Kubernetes.

### 3. Set up Kubernetes (EKS)
- Deploy the EKS cluster using Terraform:
```bash
cd terraform
terraform init
terraform apply --auto-approve
```
- Apply Kubernetes manifests to deploy the application:
```bash
kubectl apply -f kubernetes/deployment.yml
```

### 4. Setup Monitoring with Prometheus and Grafana
- Install Prometheus and Grafana using the provided scripts:
```bash
./ci-scripts/install_blackbox.sh
./ci-scripts/install_prometheus.sh
```
- Access Grafana and Prometheus through the browser:
  - Grafana: `http://<your-server-ip>:3000`
  - Prometheus: `http://<your-server-ip>:9090`

## Key Pipeline Stages
1. Git Checkout: Pulls the latest code from GitHub.
2. Build & Analysis: Maven builds the app, SonarQube analyzes the code.
3. Vulnerability Scan: Trivy scans the Docker image for vulnerabilities.
4. Docker Build & Push: Builds a Docker image and pushes it to DockerHub.
5. Deploy to EKS: Deploys the app to the Kubernetes cluster.
6. Monitor: Monitors uptime and performance using Prometheus and Grafana.

## Project Highlights
- Full CI/CD Automation: Automates the entire software development lifecycle, from code commit to deployment.
- Real-Time Monitoring: Integrates a comprehensive monitoring system using Prometheus and Grafana to ensure the app's health.
- Security-Focused: Static code analysis via SonarQube and vulnerability scans via Trivy ensure high code quality and security.


---

## Contact
**Join Our** [Telegram Community](https://t.me/devcloudninjas) // [Follow me](https://github.com/devcloudninjas) **for more DevOps & Cloud content.**

```

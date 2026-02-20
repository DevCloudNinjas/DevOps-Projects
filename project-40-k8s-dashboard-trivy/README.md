# Kubernetes-Dashboard

![Kubernetes](https://imgur.com/yCAVAsK.png)

### A kubernetes dashboard integrated with health checks, trivy scanning and health checks for pods


Kubernetes Dashboard Web Application
Welcome to the Kubernetes Dashboard Web Application repository! This web application is designed to provide users with insights and information about their Kubernetes clusters, along with the ability to scan Docker images using Trivy.

### **Overview** :-

The Kubernetes Dashboard Web Application is built with a combination of HTML, CSS, JavaScript, and Python. It offers a user-friendly interface to monitor system metrics, Kubernetes resources, and perform image scans.

### **Features** :-

**System Metrics**: The upper section of the dashboard displays the current usage of storage, memory, and CPU resources, giving users a quick overview of the system's health.

**Kubernetes Status**: In the lower section of the dashboard, users can select a Kubernetes namespace from a dropdown. The dashboard then provides information about the number of deployments, services, and pods within the selected namespace.

**Trivy Image Scanning**: The application also integrates the Trivy scanning feature. Users can input an image ID, initiate a scan, and view the generated scan report. This helps identify vulnerabilities and potential security risks in Docker images.

**How to Use
Clone the Repository**: Start by cloning this repository to your local machine using the following command:

```
git clone https://github.com/NotHarshhaa/kubernetes-dashboard.git
```

**Frontend and Backend Setup**: The frontend of the application is built with HTML, CSS, and JavaScript, while the backend is developed using Flask (Python). Ensure that you have the required dependencies installed.

**Running the Application**: Start the Flask server to serve the backend of the application. Access the dashboard through your browser by navigating to `http://localhost:5000` or the appropriate address based on your setup.

**Monitoring System Metrics**: The top section of the dashboard displays the current storage, memory, and CPU utilization. These metrics provide insights into the system's performance.

**Kubernetes Status**: Select a namespace from the dropdown in the lower section to view the number of deployments, services, and pods associated with that namespace.

**Image Scanning with Trivy**: Use the image scanning feature to input an image ID and trigger a scan. The scan report will highlight vulnerabilities detected in the image.

**Technologies Used Frontend**: HTML, CSS, JavaScript

**Backend**: Python Flask

**Kubernetes API**: Python Kubernetes Client

**Security Scanning**: Trivy


# Hit the Star! ⭐
***If you are planning to use this repo for learning, please hit the star. Thanks!***

#### Author by [DevCloud Ninjas](https://github.com/DevCloudNinjas)

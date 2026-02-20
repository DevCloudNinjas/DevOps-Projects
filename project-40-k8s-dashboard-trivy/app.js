
document.addEventListener('DOMContentLoaded', () => {
  const scanForm = document.getElementById('scanForm');
  let defaultNamespace = '';

  if (scanForm) {
    scanForm.addEventListener('submit', (event) => {
      event.preventDefault();
      console.log('Form submitted');
      const imageInput = document.getElementById('imageInput').value;
      console.log('Image input:', imageInput);
      scanImage(imageInput);
    });
  }


  const healthCheckButton = document.getElementById('healthCheckButton');
  const healthCheckResult = document.getElementById('healthCheckResult');

  if (healthCheckButton) {
    healthCheckButton.addEventListener('click', () => {
      healthCheckResult.textContent = 'Checking...';

      fetch('http://127.0.0.1:5000/kubernetes_info?namespace=' + defaultNamespace)
        .then(response => response.json())
        .then(data => {
          const numPods = data.num_pods;
          const numPodsRunning = numPods; // You can adjust this based on your actual logic
          const allPodsRunning = numPods === numPodsRunning;

          if (allPodsRunning) {
            healthCheckResult.textContent = 'Good';
            healthCheckResult.style.color = 'green';
          } else {
            healthCheckResult.textContent = 'Bad';
            healthCheckResult.style.color = 'red';
          }
        })
        .catch(error => {
          healthCheckResult.textContent = 'Error checking health';
          healthCheckResult.style.color = 'red';
          console.error('Error checking health:', error);
        });
    });
  }

function updateDashboard() {
  // Fetch system info from your Python backend's API endpoint
  fetch('http://127.0.0.1:5000/system_info')
    .then(response => response.json())
    .then(data => {
      const memoryUtilizationElement = document.querySelector('.memory-utilization .percentage');
      memoryUtilizationElement.textContent = data.memory_usage.percent + '%';

      const cpuUtilizationElement = document.querySelector('.cpu-utilization .percentage');
      cpuUtilizationElement.textContent = data.cpu_percent + '%';

      const storageUtilizationElement = document.querySelector('.storage-used .percentage');
      storageUtilizationElement.textContent = data.disk_usage.percent + '%';
    });

  // Fetch Kubernetes namespaces from your Python backend's API endpoint
  fetch('http://127.0.0.1:5000/kubernetes_namespaces')
    .then(response => response.json())
    .then(namespaces => {
      const namespaceDropdown = document.getElementById('namespace-dropdown');

      // Clear existing options
      namespaceDropdown.innerHTML = '';

      // Add available namespaces to the dropdown
      namespaces.forEach(namespace => {
        const option = document.createElement('option');
        option.value = namespace;
        option.textContent = namespace;
        namespaceDropdown.appendChild(option);
      });

      // Attach event handler to the namespace dropdown
      namespaceDropdown.addEventListener('change', () => {
        const selectedNamespace = namespaceDropdown.value;
        fetchKubernetesInfo(selectedNamespace);
      });

      // Fetch Kubernetes info for the first namespace by default
      const defaultNamespace = namespaces[0];
      fetchKubernetesInfo(defaultNamespace);
    });
  }





 // Attach event handler to the scan form



function fetchKubernetesInfo(namespace) {
  // Fetch Kubernetes info from your Python backend's API endpoint for the selected namespace
  fetch(`http://127.0.0.1:5000/kubernetes_info?namespace=${namespace}`)
    .then(response => response.json())
    .then(data => {
      const numDeploymentsElement = document.querySelector('.deployments .count');
      numDeploymentsElement.textContent = data.num_deployments;

      const numPodsElement = document.querySelector('.pods-running .count');
      numPodsElement.textContent = data.num_pods;

      const numServicesElement = document.querySelector('.services-running .count');
      numServicesElement.textContent = data.num_services;
    });
}


function scanImage(imageName) {
  // Fetch Trivy scan results from your Python backend's API endpoint
  console.log('scanImage function called');
  fetch('http://127.0.0.1:5000/scan_image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ container_id: imageName }),
  })
    .then(response => response.json())
    .then(data => {
      const scanResultsElement = document.getElementById('scanResults');
      scanResultsElement.textContent = JSON.stringify(data.scan_results, null, 2);
    })
    .catch(error => {
      console.error('Error scanning image:', error);
    });
}




updateDashboard();
});
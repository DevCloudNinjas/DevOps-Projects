import psutil
from flask import Flask, jsonify, request
from flask_cors import CORS
from kubernetes import client, config
import subprocess

app = Flask(__name__)
CORS(app)

# Load Kubernetes configuration from default location
config.load_kube_config()

@app.route('/system_info', methods=['GET'])
def get_system_info():
    # CPU utilization as a percentage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Memory usage in bytes
    mem = psutil.virtual_memory()
    memory_usage = {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent
    }

    # Disk usage in bytes
    disk = psutil.disk_usage('/')
    disk_usage = {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent
    }

    # Combine all information into a dictionary
    system_info = {
        'cpu_percent': cpu_percent,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage
    }

    return jsonify(system_info)

@app.route('/kubernetes_info', methods=['GET'])
def get_kubernetes_info():
    namespace = request.args.get('namespace', 'default')

    # Fetch Kubernetes deployments
    deployments_api = client.AppsV1Api()
    deployments = deployments_api.list_namespaced_deployment(namespace).items
    num_deployments = len(deployments)

    # Fetch Kubernetes services
    services_api = client.CoreV1Api()
    services = services_api.list_namespaced_service(namespace).items
    num_services = len(services)

    # Fetch Kubernetes pods
    pods_api = client.CoreV1Api()
    pods = pods_api.list_namespaced_pod(namespace).items
    num_pods = len(pods)

    kubernetes_info = {
        'num_deployments': num_deployments,
        'num_services': num_services,
        'num_pods': num_pods
    }

    return jsonify(kubernetes_info)

@app.route('/kubernetes_namespaces', methods=['GET'])
def get_kubernetes_namespaces():
    namespaces_api = client.CoreV1Api()
    namespaces = namespaces_api.list_namespace().items
    namespace_list = [ns.metadata.name for ns in namespaces]
    return jsonify(namespace_list)

@app.route('/scan_image', methods=['POST'])
def scan_image():
    data = request.json
    print("scan_image function called")
    if 'container_id' not in data:
        return jsonify({'error': 'Container ID is required'}), 400

    container_id = data['container_id']
    try:
        output_path = '/home/avinash/sample'
        command = ['trivy', 'image', '--format', 'json', container_id]
        
        # Capture the subprocess output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        scan_output = result.stdout

        # Write scan output to a file (optional)
        with open(output_path, 'w') as file:
            file.write(scan_output)

        return jsonify({'scan_results': scan_output})
    except subprocess.CalledProcessError as e:
        error_message = f"Trivy scan failed. Error: {str(e)}"
        return jsonify({'error': error_message}), 500
    except Exception as e:
        error_message = f"An error occurred. Error: {str(e)}"
        return jsonify({'error': error_message}), 500




if __name__ == '__main__':
    app.run(debug=True)

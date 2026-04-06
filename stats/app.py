import os
import docker
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to the Docker socket
try:
    client = docker.from_env()
except Exception as e:
    print(f"Error connecting to Docker: {e}")
    client = None

def calculate_cpu_percent(stats):
    """
    Standard Docker CPU calculation:
    (cpu_delta / system_delta) * number_of_cpus * 100.0
    """
    cpu_stats = stats.get('cpu_stats', {})
    precpu_stats = stats.get('precpu_stats', {})
    
    cpu_usage = cpu_stats.get('cpu_usage', {}).get('total_usage', 0)
    precpu_usage = precpu_stats.get('cpu_usage', {}).get('total_usage', 0)
    
    system_cpu_usage = cpu_stats.get('system_cpu_usage', 0)
    presystem_cpu_usage = precpu_stats.get('system_cpu_usage', 0)
    
    cpu_delta = cpu_usage - precpu_usage
    system_delta = system_cpu_usage - presystem_cpu_usage
    
    # Get total number of CPUs
    num_cpus = cpu_stats.get('online_cpus', len(cpu_stats.get('cpu_usage', {}).get('percpu_usage', [1])))
    
    if system_delta > 0.0 and cpu_delta > 0.0:
        return (cpu_delta / system_delta) * num_cpus * 100.0
    return 0.0

@app.route('/stats')
def get_stats():
    if not client:
        return jsonify({"error": "Docker not reachable"}), 500
    
    try:
        # Get all containers and filter for our project prefix
        all_containers = client.containers.list()
        containers = [c for c in all_containers if 'hexstrike' in c.name.lower()]
        
        results = []
        total_cpu = 0
        total_mem_usage = 0
        total_mem_limit = 0
        total_net_in = 0
        total_net_out = 0
        
        for container in containers:
            # We use stream=False to get a single snapshot
            stats = container.stats(stream=False)
            
            # CPU
            cpu_percent = calculate_cpu_percent(stats)
            total_cpu += cpu_percent
            
            # MEMORY
            mem_stats = stats.get('memory_stats', {})
            mem_usage = mem_stats.get('usage', 0)
            mem_limit = mem_stats.get('limit', 0)
            total_mem_usage += mem_usage
            total_mem_limit = max(total_mem_limit, mem_limit) # Use host limit
            
            # NETWORKS
            networks = stats.get('networks', {})
            net_in = sum(n.get('rx_bytes', 0) for n in networks.values())
            net_out = sum(n.get('tx_bytes', 0) for n in networks.values())
            total_net_in += net_in
            total_net_out += net_out
            
            results.append({
                "id": container.id[:12],
                "name": container.name.replace('hexstrike_', '').replace('_', ' ').upper(),
                "cpu": round(cpu_percent, 1),
                "mem": round((mem_usage / mem_limit) * 100, 1) if mem_limit > 0 else 0,
                "mem_mb": round(mem_usage / (1024**2), 1),
                "status": container.status
            })
            
        # Overall totals for the "Main Cards"
        return jsonify({
            "individual": results,
            "aggregate": {
                "cpu": round(total_cpu, 1),
                "mem_usage": round(total_mem_usage / (1024**3), 2), # GB
                "mem_limit": round(total_mem_limit / (1024**3), 2), # GB
                "mem_percent": round((total_mem_usage / total_mem_limit) * 100, 1) if total_mem_limit > 0 else 0,
                "net_in_mb": round(total_net_in / (1024**2), 1),
                "net_out_mb": round(total_net_out / (1024**2), 1)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)

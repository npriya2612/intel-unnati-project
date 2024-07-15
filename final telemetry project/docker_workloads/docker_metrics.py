import docker

def collect_docker_metrics():
    try:
        client = docker.from_env()
        containers = client.containers.list()

        metrics = []
        for container in containers:
            if 'cpu_workload_image' in container.image.tags:
                metrics.append({
                    'container_id': container.short_id,
                    'image': container.image.tags[0],
                    'status': container.status,
                    'created': container.attrs['Created'],
                    'cpu_percentage': container.attrs['HostConfig']['NanoCpus'] / 1e9,  # Convert NanoCpus to percentage
                })
        
        return metrics

    except docker.errors.APIError as e:
        print(f"Error accessing Docker API: {e}")
        return None

if __name__ == "__main__":
    docker_metrics = collect_docker_metrics()
    if docker_metrics:
        for metric in docker_metrics:
            print(metric)

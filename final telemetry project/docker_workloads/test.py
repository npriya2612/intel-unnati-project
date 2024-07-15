import docker

def test_docker_api_access():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        # If no exceptions are raised, Docker API access is successful
        print("Docker API access successful.")
        return True
    
    except docker.errors.DockerException as e:
        print(f"Error accessing Docker API: {e}")
        return False

# Run the function to test Docker API access
test_docker_api_access()

import httpx
from prefect import flow
from dotenv import load_dotenv
import paramiko

load_dotenv()


@flow(log_prints=True)
def get_repo_info(repo_name: str = "PrefectHQ/prefect"):
    url = f"https://api.github.com/repos/{repo_name}"
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()
    print(f"{repo_name} repository statistics 🤓:")
    print(f"Stars 🌠 : {repo['stargazers_count']}")
    print(f"Forks 🍴 : {repo['forks_count']}")

    push_file_to_remote_server()

    


def push_file_to_remote_server():

    # Establish the SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    username = "normal"
    host = "65.21.62.139"
    ssh.connect(hostname=host, 
        username=username)

    sftp = ssh.open_sftp()

    local_file_path = './test_paper.pdf'
    remote_file_path = '/tmp/received.pdf'
    sftp.put(local_file_path, remote_file_path)


    # Close the connections
    sftp.close()
    ssh.close()




if __name__ == "__main__":
    # get_repo_info.serve(name="prefect-docker-guide2")
    get_repo_info()

    push_file_to_remote_server()

# prefect deploy build ./flows/prefect-docker-guide-flow.py:get_repo_info -n logging-flow-docker -ib docker-container/docker-python-test -q docker-pool -o log-flow-docker-deployment.yaml

# prefect work-pool create docker-pool --type docker

# prefect worker start --pool docker-pool
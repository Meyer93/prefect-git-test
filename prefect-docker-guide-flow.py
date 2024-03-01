import httpx
from prefect import flow
from dotenv import load_dotenv

from myownmodule import myfunction

myfunction()
load_dotenv()


@flow(log_prints=True)
def get_repo_info2(repo_name: str = "PrefectHQ/prefect"):
    url = f"https://api.github.com/repos/{repo_name}"
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()
    print(f"{repo_name} repository statistics 🤓:")
    print(f"Stars 🌠 : {repo['stargazers_count']}")
    print(f"Forks 🍴 : {repo['forks_count']}")


if __name__ == "__main__":
    get_repo_info2()

# prefect deploy build ./flows/prefect-docker-guide-flow.py:get_repo_info -n logging-flow-docker -ib docker-container/docker-python-test -q docker-pool -o log-flow-docker-deployment.yaml

# prefect work-pool create docker-pool --type docker

# prefect worker start --pool docker-pool
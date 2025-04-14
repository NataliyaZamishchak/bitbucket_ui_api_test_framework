import random
import string
import subprocess
import os
import shutil
from pathlib import Path


def clone_repo(repo_url: str, dest_folder: str = "cloned_repo") -> None:
    subprocess.run(["git", "clone", repo_url, dest_folder], check=True)

def create_test_file(repo_path: str, filename: str = "hello.py", content: str = 'print("Hello")') -> None:
    file_path = Path(repo_path) / filename
    with open(file_path, "w") as f:
        f.write(content)

def git_status(repo_path: str) -> str:
    result = subprocess.run(["git", "status"], cwd=repo_path, capture_output=True, text=True)
    return result.stdout

def git_add_all(repo_path: str) -> None:
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

def git_commit(repo_path: str, message: str = "Add test file") -> None:
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)

def git_push(repo_path: str, branch: str = "main") -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "push"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def delete_cloned_repo(repo_path: Path):
    try:
        os.chmod(repo_path, 0o777)
        shutil.rmtree(repo_path)
        print(f"Repo at {repo_path} deleted successfully.")
    except Exception as e:
        print(f"Error while deleting the repo: {e}")


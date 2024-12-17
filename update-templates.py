import json
import os
from typing import List
import requests
import dotenv
from dataclasses import dataclass

REPO_API_URL = "https://api.github.com/repos/github/gitignore/contents/"

@dataclass
class File:
    name: str
    download_url: str

def get_gitignore_files(repo_api_url: str, auth_token: str) -> List[File]:
    """
    Recursively fetch all .gitignore files from a GitHub repository.

    :param repo_api_url: The API URL of the repository.
    :param auth_token: The GitHub API token.
    :return: A list of File objects for all .gitignore files.
    """
    gitignore_files = []

    try:
        # Fetch the current directory's contents
        response = requests.get(repo_api_url, headers={"Authorization": f"token {auth_token}"})
        response.raise_for_status()
        files = response.json()

        # Iterate through the contents
        for file in files:
            if file["type"] == "file" and file["name"].endswith(".gitignore"):
                # Add .gitignore files to the list
                gitignore_files.append(File(parse_filename(file["path"]), file["download_url"]))
            elif file["type"] == "dir":
                # If it's a directory, recurse into it
                gitignore_files.extend(get_gitignore_files(file["url"], auth_token))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching files from {repo_api_url}: {e}")

    return gitignore_files

def parse_filename(filename: str):
    """
    Parse a filename to extract the language or framework name.

    :param filename: The name of the .gitignore file.
    :return: The language or framework name.
    """
    return filename.lower().replace(".gitignore", "").lower().replace("/", "-")

def dump_file_data(path: str, files: List[File]):
    """
    Dump the to a single JSON file.

    :param path: The path to the output JSON file.
    :param files: A list of File objects.
    """
    
    with open(path, "w") as f:
        json_data = [{"name": file.name, "download_url": file.download_url} for file in files]
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    dotenv.load_dotenv()
    auth_token = os.getenv("GITHUB_TOKEN")
    
    if not auth_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    
    gitignore_files = get_gitignore_files(REPO_API_URL, auth_token)
    dump_file_data("./templates.json", gitignore_files)
    

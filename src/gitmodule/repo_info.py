import os
import git
from github import Github
default_path = "tmp"
class repo_info:
    def __init__(self, remote: str):
        self.remote = remote
        self.repo_path = self.get_repo_path(remote)
        self.remote_repo_info : Github.Repository = None
    def get_repo_path(self, name) -> str:
        if name is not None:
            short_name = name.split("/")[-1]
            tmp_path = os.path.join("/tmp", short_name)
            if os.path.exists(tmp_path):
                print("Repo path already exists. Using existing path:", tmp_path)
            else:
                print("Repo path does not exist. Creating new path:", tmp_path)
                clone_url = f"https://github.com/{name}.git"
                repo = git.Repo.clone_from(clone_url, tmp_path)
        return tmp_path
    def set_remote_info(self, github_instance: Github):
        try:
            self.remote_repo_info = github_instance.get_repo(self.remote)
        except Exception as e:
            print(f"Error fetching remote repo info for {self.remote}: {e}")
class repo_info_list:
    def __init__(self):
        self.repo_infos = []
    def __init__(self, repo_raw_info_list: str):
        self.repo_infos = []
        self.add_repo_info(repo_raw_info_list)
    def add_repo_info(self, repo_raw_info_list: str):
        for item in repo_raw_info_list.split(","):
            self.repo_infos.append(repo_info(item))
    def get_repo_infos(self) -> list:
        return self.repo_infos
    def __iter__(self):
        return iter(self.repo_infos)
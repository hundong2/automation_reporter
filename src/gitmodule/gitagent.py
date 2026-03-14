from dotenv import load_dotenv
from github import Github
from agent.agent import Agent, AgentList, InitializeAgentList
from gitmodule.repo_info import repo_info, repo_info_list
from prompt.make_prompt import make_prompt
import os 

class GitEnvironment:
    def __init__(self):
        load_dotenv()
        self.git_token = os.getenv("GIT_TOKEN")
        self.git_repo_list = os.getenv("GIT_REPO_LIST").split(",")
    def get_git_token(self) -> str:
        return self.git_token
    def get_git_repo_list(self) -> list:
        return self.git_repo_list
    def get_git_repo_origin_str(self) -> str:
        return os.getenv("GIT_REPO_LIST")
    
class GitEnvironmentFactory:
    @staticmethod
    def create_git_environment() -> GitEnvironment:
        return GitEnvironment()

class GitAgent:
    def __init__(self, git_env: GitEnvironment):
        self.git_env = git_env
    def get_git_token(self) -> str:
        return self.git_env.get_git_token()
    def get_git_repo_list(self) -> list:
        return self.git_env.get_git_repo_list()
    def get_github_instance(self) -> Github:
        return Github(self.get_git_token())
    def get_github_repos(self):
        github = self.get_github_instance()
        repos = repo_info_list(self.git_env.get_git_repo_origin_str())
        for repo in repos:
            repo.set_remote_info(github)
        return repos
    def get_issue_list(self, assignee: str = None):
        repos = self.get_github_repos()
        issues = []
        for repo in repos:
            try:
                repo_issues = repo.remote_repo_info.get_issues(state="open")
                for repo_issue in repo_issues:
                    if assignee:
                        body = repo_issue.body or ""  # None 방지
                        if f"@{assignee}" in body:    # @ 포함 정확히 검색
                            issues.append(repo_issue)
                    else:
                        issues.append(repo_issue)     # assignee 없으면 전체 반환
            except Exception as e:
                print(f"Error fetching issues for repo {repo.name}: {e}")
        return issues
    def make_prompt_for_issue(self, assignee: str) -> list:
        repos = self.get_github_repos()
        prompt = []
        for repo in repos:
            try:
                repo_issues = repo.remote_repo_info.get_issues(state="open")
                for repo_issue in repo_issues:
                    if assignee:
                        body = repo_issue.body or ""  # None 방지
                        if f"@{assignee}" in body:    # @ 포함 정확히 검색
                            temp_prompt = make_prompt(assignee, repo_issue.number, repo_issue.title, repo_issue.body, repo.repo_path)
                            prompt.append(temp_prompt)
            except Exception as e:
                print(f"Error fetching issues for repo {repo.name}: {e}")
        return prompt
    def run_assignee_issue(self) -> list:
        agentList = InitializeAgentList()
        promptList = []
        for agent in agentList:
            issue_list = self.make_prompt_for_issue(agent.name)
            if issue_list:
                promptList.extend(issue_list)
        return promptList
                
    
class GitAgentFactory:
    @staticmethod
    def create_git_agent() -> GitAgent:
        git_env = GitEnvironmentFactory.create_git_environment()
        return GitAgent(git_env)
from gitmodule.gitagent import GitAgentFactory
def main():
    git_agent = GitAgentFactory.create_git_agent()
    print("Git Token:", git_agent.get_git_token())
    print("Git Repo List:", git_agent.get_git_repo_list())
    git_agent.get_issue_list("claude")
if __name__ == "__main__":
    main()
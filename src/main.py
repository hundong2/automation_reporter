from gitmodule.gitagent import GitAgentFactory
import asyncio
from command.run import run_agents_parallel
def main():
    git_agent = GitAgentFactory.create_git_agent()
    print("Git Token:", git_agent.get_git_token())
    print("Git Repo List:", git_agent.get_git_repo_list())
    command_set = git_agent.run_assignee_issue()
    results = asyncio.run(run_agents_parallel(command_set))
    print("Results:", results)
if __name__ == "__main__":
    main()
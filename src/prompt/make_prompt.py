def make_prompt(agent_name: str, issue_number : int, issue_title: str, issue_body: str ) -> dict:
    return {
        "agent": agent_name,
        "prompt": f"issue title(#{issue_number}): {issue_title}, issue_body: {issue_body}, please solve this issue and auto create branch and pull request to master or main branch."
    }
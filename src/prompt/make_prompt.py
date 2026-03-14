def make_prompt(agent_name: str, issue_number : int, issue_title: str, issue_body: str , path: str) -> dict:
    path_prompt = f"해당 경로 내에서만 작업을 해야 되고 다른 경로는 참고 하면 안된다. {path}"
    return {
        "agent": agent_name,
        "prompt": f"issue title(#{issue_number}): {issue_title}, issue_body: {issue_body}, please solve this issue and auto create branch and pull request to master or main branch.",
        "cwd": path
    }
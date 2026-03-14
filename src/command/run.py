import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
async def run_agent(agent: str, prompt: str, cwd: str):
    options = "--dangerously-skip-permissions"
    if 'gemini' in agent:
        options = "--yolo"
    command = f"{agent} -p \"{prompt}\" {options}"
    if 'codex' in agent:
        options = "--full-auto"
        command = f"{agent} exec {options} \"{prompt}\""

    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)

    # gh 설정 디렉토리 명시적 상속 (HOME이 다를 경우 대비)
    env["HOME"] = os.path.expanduser("~")
    env["XDG_CONFIG_HOME"] = os.path.expanduser("~/.config")
    proc = await asyncio.create_subprocess_shell(command, 
                                                 stdout=asyncio.subprocess.PIPE, 
                                                 stderr=asyncio.subprocess.PIPE,
                                                 cwd=cwd,
                                                 env=env)
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        print(f"{agent} output: {stdout.decode()}")
    else:
        print(f"{agent} error: {stderr.decode()}")
    return {
        "agent": agent,
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
        "returncode": proc.returncode
    }

async def run_agents_parallel(tasks: list[dict]) -> list[dict]:
    """여러 에이전트 병렬 실행"""
    coroutines = [
        run_agent(task["agent"], task["prompt"], task["cwd"])
        for task in tasks
    ]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    return results
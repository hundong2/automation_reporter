import json
class Agent:
    def __init__(self, name: str, command: str, path: str, description: str):
        self.name = name
        self.command = command
        self.path = path
        self.description = description

class AgentList:
    def __init__(self):
        self.agents = []
    def add_agent(self, agent: Agent):
        self.agents.append(agent)
    def get_agents(self, name: str) -> list:
        return [agent for agent in self.agents if agent.name == name]
    def __iter__(self):
        return iter(self.agents)
    
def InitializeAgentList() -> AgentList:
    agent_list = AgentList()
    # GitAgent 추가
    with open("src/environment/agents.json", "r") as f:
        agents_data = json.load(f)
        for agent_data in agents_data:
            agent = Agent(
                name=agent_data["name"],
                command=agent_data["command"],
                path=agent_data["path"],
                description=agent_data["description"]
            )
            agent_list.add_agent(agent)
    return agent_list
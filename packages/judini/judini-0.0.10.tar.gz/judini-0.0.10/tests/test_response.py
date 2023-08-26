from judini.codegpt.agent import Agent
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()


codegpt_api_key= os.getenv("CODEGPT_API_KEY")
codegpt_agent_id= os.getenv("CODEGPT_AGENT_ID")

agent_instance = Agent(api_key=codegpt_api_key, agent_id=codegpt_agent_id)

prompt = "tell me a short story about a blue turtle"

response = asyncio.run(agent_instance.completion(prompt, stream=False))

print(response)


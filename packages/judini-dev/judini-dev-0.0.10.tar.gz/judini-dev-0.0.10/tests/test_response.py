from judini.agent import Agent
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()


judini_api_key= os.getenv("JUDINI_API_KEY")
judini_agent_id= os.getenv("JUDINI_AGENT_ID")

agent_instance = Agent(api_key=judini_api_key, agent_id=judini_agent_id)

prompt = 'Escribeme un parrafo de un cuento sobre una tortuga azul'
response = asyncio.run(agent_instance.completion(prompt, stream=True))

print(response)


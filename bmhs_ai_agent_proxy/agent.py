import os
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from dotenv import load_dotenv

load_dotenv()

remote_url = os.getenv("REMOTE_AGENT_URL", "http://localhost:8001")

root_agent = RemoteA2aAgent(
    name='root_agent',
    description='Agen ini berfungsi sebagai remote proxy untuk server A2A.',
    agent_card=f"{remote_url}{AGENT_CARD_WELL_KNOWN_PATH}",
)

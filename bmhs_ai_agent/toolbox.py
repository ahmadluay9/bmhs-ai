import os
import asyncio
from toolbox_core import ToolboxClient
from dotenv import load_dotenv
from google.auth.transport.requests import Request
import google.oauth2.id_token
import subprocess
load_dotenv()

server_url = os.getenv("TOOLBOX_URL","http://localhost:5000")

def get_bearer_token() -> str:
    credentials, project_id = google.auth.default()

    if hasattr(credentials, "id_token_info"):
         req = Request()
         credentials.refresh(req)
         token = credentials.token
    else:
         from google.oauth2 import id_token
         req = Request()
         
         try:
             token = id_token.fetch_id_token(req, server_url)
         except google.auth.exceptions.DefaultCredentialsError:
             
             result = subprocess.run(
                 ["gcloud", "auth", "print-identity-token"], 
                 capture_output=True, 
                 text=True, 
                 check=True,
                 shell=True
             )
             token = result.stdout.strip()
             
    return f"Bearer {token}"

headers = {
    "Authorization": get_bearer_token()
}

async def main():
    async with ToolboxClient(server_url,client_headers=headers) as toolbox:
        tool = await toolbox.load_tool("search-pasien-by-name")
        result = await tool(nama="Bagas Dwi")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
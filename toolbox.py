import asyncio
from toolbox_core import ToolboxClient

async def main():
    # Replace with the actual URL where your Toolbox service is running
    async with ToolboxClient("https://bmhs-mcp-server-739118104730.asia-southeast2.run.app") as toolbox:
        tool = await toolbox.load_tool("search-pasien-by-name")
        result = await tool(nama="Bagas Dwi")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
from agents.mcp import MCPServerStdio
import asyncio
from datetime import datetime
from agents import Agent, Runner, function_tool


@function_tool
async def get_time()->str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

mcp_fetch = MCPServerStdio(
    params={
        "command":"uvx", 
        "args": ['mcp-server-fetch']
    })


async def async_main():
    async with mcp_fetch:
        agent = Agent(
            name="Clark", 
            model="gpt-4.1-mini", 
            instructions="You are a helpful assistant.",
            mcp_server=mcp_fetch,
            tools=[get_time])
        result= await Runner.run(
            agent, """
            Please introduce yourself as David Benjamin Clark, but explain you 
            go by Clark, so you're not mistaken as Superman.
            """)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(async_main())   
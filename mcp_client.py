# pip install google-generativeai mcp
import asyncio
import os
# Add json import for formatting output
import json
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Re-add StdioServerParameters, setting args for stdio
server_params = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp-everest", "mcp-everest"],
    env={
        "EVEREST_HOST": os.getenv("EVEREST_HOST", "http://localhost:8080"),
        "EVEREST_API_KEY": os.getenv("EVEREST_API_KEY"),
        "EVEREST_VERIFY_SSL": os.getenv("EVEREST_VERIFY_SSL", "true"),
    }
)

async def run():
    # Remove debug prints
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # prompt = f"How many database clusters are there in the namespace 'default'?"
            prompt = f"Create pxc cluster in namespace everest with 1 node and 10 GB storage, name it mcp-test"
            await session.initialize()

            mcp_tools = await session.list_tools()
            # Remove debug prints
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]
            # Remove debug prints

            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            # Remove raw response print
            print(response)
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call

                result = await session.call_tool(
                    function_call.name, arguments=dict(function_call.args)
                )
                print(function_call.args)
                print(result)

                # Parse and print formatted JSON result
                print("--- Formatted Result ---") # Add header for clarity
                try:
                    everest_data = json.loads(result.content[0].text)
                    print(json.dumps(everest_data, indent=2))
                except json.JSONDecodeError:
                    print("MCP server returned non-JSON response:")
                    print(result.content[0].text)
                except (IndexError, AttributeError):
                     print("Unexpected result structure from MCP server:")
                     print(result)
            else:
                print("No function call was generated by the model.")
                if response.text:
                     print("Model response:")
                     print(response.text)

# Revert main block
asyncio.run(run())

import asyncio
import google.generativeai as genai
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# The command to run your MCP server
MCP_SERVER_COMMAND = ["uv", "run", "--with", "mcp-everest", "mcp-everest"]

# Replace with your actual Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def handle_server_response(server_output: str) -> str:
    """Processes the raw server output using Gemini."""
    if server_output:
        prompt = f"The MCP server outputted the following: {server_output}. Please analyze and provide insights."
        response = await model.generate_content_async(prompt)  # Use async version
        return response.text
    else:
        return "No output received from the MCP server."

async def run_client(user_query: str):
    """Runs the MCP client and interacts with Gemini."""
    server_params = StdioServerParameters(
        command=MCP_SERVER_COMMAND[0],
        args=MCP_SERVER_COMMAND[1:],
        env=None,
    )

    async def sampling_callback(
        message: types.CreateMessageRequestParams,
    ) -> types.CreateMessageResult:
        # You can customize how the client responds here if the server requests sampling.
        # For a basic interaction, we might just return an empty or default response.
        return types.CreateMessageResult(
            role="assistant",
            content=types.TextContent(
                type="text",
                text="Processing...",
            ),
            model="gemini-pro",
            stopReason="intermediate",
        )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read, write, sampling_callback=sampling_callback
            ) as session:
                await session.initialize()

                tools = await session.list_tools()
                print(tools)

                """
                # Send a CreateMessageRequest to the server
                response = await session.create_message(
                    prompt="user_query",  # You might need to adjust this based on your server's expectations
                    messages=[
                        types.ChatMessage(
                            role="user",
                            content=[types.TextContent(type="text", text=user_query)],
                        )
                    ],
                )

                if response and response.choices:
                    server_output = response.choices[0].message.content[0].text
                    print(f"\nResponse from MCP server: {server_output}")
                    gemini_analysis = await handle_server_response(server_output)
                    print(f"\nGemini's analysis: {gemini_analysis}")
                else:
                    print("\nNo meaningful response received from the MCP server.")
                """

    except FileNotFoundError:
        print(f"Error: Command not found: {MCP_SERVER_COMMAND[0]}. Make sure it's in your PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_query = input("Enter your query for the MCP server: ")
    asyncio.run(run_client(user_query))
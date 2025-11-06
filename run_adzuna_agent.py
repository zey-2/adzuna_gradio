import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import StructuredTool
from fastmcp import Client
import json
from pydantic import BaseModel, Field, create_model
from typing import Optional, Any, Dict

os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")


def json_schema_to_pydantic(schema: Dict[str, Any], model_name: str) -> type[BaseModel]:
    """
    Convert a JSON schema to a Pydantic model.
    
    Parameters:
    schema (Dict[str, Any]): The JSON schema dictionary.
    model_name (str): The name for the generated Pydantic model.
    
    Returns:
    type[BaseModel]: A dynamically created Pydantic model class.
    """
    if not schema or 'properties' not in schema:
        return None
    
    fields = {}
    properties = schema.get('properties', {})
    required = schema.get('required', [])
    
    for prop_name, prop_info in properties.items():
        field_type = Any
        field_default = ...
        
        # Map JSON schema types to Python types
        prop_type = prop_info.get('type')
        if prop_type == 'string':
            field_type = str
        elif prop_type == 'integer':
            field_type = int
        elif prop_type == 'number':
            field_type = float
        elif prop_type == 'boolean':
            field_type = bool
        elif prop_type == 'array':
            field_type = list
        elif prop_type == 'object':
            field_type = dict
        
        # Handle optional fields
        if prop_name not in required:
            field_type = Optional[field_type]
            field_default = None
        
        # Add field with description
        description = prop_info.get('description', '')
        fields[prop_name] = (field_type, Field(default=field_default, description=description))
    
    return create_model(model_name, **fields)


def create_tool_from_mcp(tool_info, client):
    """
    Convert MCP tool to LangChain tool with proper schema.
    
    Parameters:
    tool_info: The MCP tool information object.
    client: The FastMCP client instance.
    
    Returns:
    StructuredTool: A LangChain StructuredTool instance.
    """
    async def tool_func(**kwargs):
        result = await client.call_tool(tool_info.name, kwargs)
        # Extract text content from result
        if result.content and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
        return str(result)
    
    # Convert the input schema to a Pydantic model
    args_schema = None
    if hasattr(tool_info, 'inputSchema') and tool_info.inputSchema:
        model_name = f"{tool_info.name.replace('-', '_').title()}Input"
        args_schema = json_schema_to_pydantic(tool_info.inputSchema, model_name)
    
    return StructuredTool.from_function(
        coroutine=tool_func,
        name=tool_info.name.replace("-", "_"),  # LangChain requires valid Python identifiers
        description=tool_info.description or "No description",
        args_schema=args_schema
    )


async def main():
    # Connect to the Adzuna MCP server using FastMCP Client
    server_url = "https://adzuna-mcp-server-236255620233.us-central1.run.app/mcp"
    
    print(f"Connecting to Adzuna MCP server at {server_url}...")
    
    async with Client(server_url) as client:
        print("✓ Connected!")
        
        # List available tools
        tools = await client.list_tools()
        print(f"✓ Found {len(tools)} tools\n")
        
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}")
        print()
        
        # Convert MCP tools to LangChain-compatible format
        langchain_tools = [create_tool_from_mcp(tool, client) for tool in tools]
        
        # Initialize the language model and agent
        model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        agent = create_react_agent(model, langchain_tools)

        print("Agent ready!\n")

        # Example 1: Search for data science jobs
        print("=== Example 1: Searching for data science jobs ===")
        resp1 = await agent.ainvoke({
            "messages": "Search for data science jobs in Singapore. Show me the top 3 results."
        })
        print("Response:", resp1["messages"][-1].content)

        print("\n" + "="*60 + "\n")

        # Example 2: Get top hiring companies
        print("=== Example 2: Top companies hiring ===")
        resp2 = await agent.ainvoke({
            "messages": "What are the top companies hiring in Singapore?"
        })
        print("Response:", resp2["messages"][-1].content)


# Run the async function
asyncio.run(main())

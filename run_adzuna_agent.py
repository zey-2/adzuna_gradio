import asyncio
import os
import warnings
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Suppress all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import gradio as gr
from fastmcp import Client
from langchain.tools import StructuredTool
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field, create_model
 
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def json_schema_to_pydantic(schema: Dict[str, Any], model_name: str) -> Optional[type[BaseModel]]:
    """
    Convert a JSON schema dictionary to a Pydantic model.

    Parameters:
        schema: JSON schema describing expected arguments.
        model_name: Name for the generated Pydantic model.

    Returns:
        A dynamically created Pydantic model class or None if schema is invalid.
    """
    if not schema or "properties" not in schema:
        return None

    fields: Dict[str, Tuple[Any, Any]] = {}
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    for prop_name, prop_info in properties.items():
        field_type: Any = Any
        field_default = ...

        prop_type = prop_info.get("type")
        if prop_type == "string":
            field_type = str
        elif prop_type == "integer":
            field_type = int
        elif prop_type == "number":
            field_type = float
        elif prop_type == "boolean":
            field_type = bool
        elif prop_type == "array":
            field_type = list
        elif prop_type == "object":
            field_type = dict

        if prop_name not in required:
            field_type = Optional[field_type]  # type: ignore[valid-type]
            field_default = None

        description = prop_info.get("description", "")
        fields[prop_name] = (field_type, Field(default=field_default, description=description))

    return create_model(model_name, **fields)


def create_tool_from_mcp(tool_info, client) -> StructuredTool:
    """
    Convert an MCP tool description into a LangChain StructuredTool.
    """

    async def tool_func(**kwargs):
        result = await client.call_tool(tool_info.name, kwargs)
        if result.content:
            first_item = result.content[0]
            text = getattr(first_item, "text", None)
            if text:
                return text
        return str(result)

    args_schema = None
    if getattr(tool_info, "inputSchema", None):
        model_name = f"{tool_info.name.replace('-', '_').title()}Input"
        args_schema = json_schema_to_pydantic(tool_info.inputSchema, model_name)

    return StructuredTool.from_function(
        coroutine=tool_func,
        name=tool_info.name.replace("-", "_"),
        description=(tool_info.description or "No description provided."),
        args_schema=args_schema,
    )


class AdzunaMCPAgent:
    """
    Maintain a single LangGraph agent that communicates with the Adzuna MCP server.
    """

    def __init__(self, server_url: str, model_name: str = "gemini-2.5-flash"):
        self.server_url = server_url
        self.model_name = model_name
        self._client_cm: Optional[Client] = None
        self._client: Optional[Any] = None
        self._agent = None
        self._lock = asyncio.Lock()
        self._tool_metadata: List[Tuple[str, str]] = []

    async def _ensure_agent(self):
        if self._agent is not None:
            return self._agent

        async with self._lock:
            if self._agent is not None:
                return self._agent

            if not os.environ.get("GOOGLE_API_KEY"):
                raise RuntimeError("GOOGLE_API_KEY environment variable is not set.")

            client_cm = Client(self.server_url)
            client = await client_cm.__aenter__()
            tools = await client.list_tools()

            self._tool_metadata = [
                (tool.name, tool.description or "No description available.") for tool in tools
            ]

            langchain_tools = [create_tool_from_mcp(tool, client) for tool in tools]
            model = ChatGoogleGenerativeAI(model=self.model_name)
            self._agent = create_react_agent(model, langchain_tools)

            self._client_cm = client_cm
            self._client = client

        return self._agent

    async def ainvoke(self, prompt: str, history: Optional[Sequence[Tuple[str, str]]] = None) -> str:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        agent = await self._ensure_agent()

        messages: List[Any] = []
        for user_message, assistant_message in history or []:
            if user_message:
                messages.append(HumanMessage(content=user_message))
            if assistant_message:
                messages.append(AIMessage(content=assistant_message))
        messages.append(HumanMessage(content=prompt))

        result = await agent.ainvoke({"messages": messages})

        messages_output = result.get("messages") if isinstance(result, dict) else None
        if not messages_output:
            return "The agent returned an empty response."

        final_message = messages_output[-1]
        content = getattr(final_message, "content", None)

        if isinstance(content, str):
            return content.strip() or "The agent returned an empty response."

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
            if text_parts:
                return "\n".join(text_parts)

        return str(final_message)

    async def describe_tools(self) -> str:
        try:
            await self._ensure_agent()
        except Exception as exc:
            return f"Warning: Unable to load MCP tools: {exc}"

        if not self._tool_metadata:
            return "Warning: No tools were returned by the Adzuna MCP server."

        lines = "\n".join(f"- **{name}**: {description}" for name, description in self._tool_metadata)
        return f"### MCP Tools from Adzuna\n{lines}"

    async def aclose(self):
        if self._client_cm is not None:
            await self._client_cm.__aexit__(None, None, None)
            self._client_cm = None
            self._client = None
            self._agent = None


def normalize_history(history: Optional[Sequence[Any]]) -> List[Tuple[str, str]]:
    """
    Convert Gradio chat history into a list of (user, assistant) tuples.
    """
    normalized: List[Tuple[str, str]] = []
    if not history:
        return normalized

    for turn in history:
        user_message = ""
        assistant_message = ""

        if isinstance(turn, dict):
            user_message = str(turn.get("user") or turn.get("input") or "")
            assistant_message = str(turn.get("assistant") or turn.get("output") or "")
        elif isinstance(turn, (list, tuple)) and len(turn) >= 2:
            user_message = str(turn[0] or "")
            assistant_message = str(turn[1] or "")
        else:
            continue

        normalized.append((user_message, assistant_message))

    return normalized


def launch_app():
    server_url = os.environ.get(
        "ADZUNA_MCP_SERVER_URL",
        "https://adzuna-mcp-server-236255620233.us-central1.run.app/mcp",
    )
    agent = AdzunaMCPAgent(server_url=server_url)

    async def respond(message: str | dict, history: Optional[Sequence[Any]]):
        # Handle both message formats
        if isinstance(message, dict):
            text = (message.get("text", "") or "").strip()
        else:
            text = (message or "").strip()
        
        if not text:
            return "Please enter a question about jobs."

        normalized = normalize_history(history)
        try:
            return await agent.ainvoke(text, normalized)
        except Exception as exc:
            print(f"[Gradio] Error while processing request: {exc}")
            return f"Warning: {exc}"

    async def load_tools():
        return await agent.describe_tools()

    with gr.Blocks(title="Adzuna MCP Job Assistant") as demo:
        gr.ChatInterface(
            fn=respond,
            type="messages",
            submit_btn="Ask",
            description=(
                "## Adzuna MCP Job Assistant\n"
                "Ask about current job openings or hiring trends. "
                "The assistant uses LangGraph with the Adzuna MCP tools.\n\n"
                "Try prompts like:\n"
                "- Search for data science jobs in Singapore\n"
                "- Which companies are hiring in Singapore?\n"
                "- Summarize the top job categories in Singapore"
            ),
        )

    demo.queue()
    demo.launch()


if __name__ == "__main__":
    launch_app()

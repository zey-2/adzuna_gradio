# Adzuna MCP Job Assistant

Interactive Gradio application that wraps a LangGraph agent connected to the Adzuna Model Context Protocol (MCP) server. It lets you search live job listings, summarize results, and explore hiring trends through a conversational interface backed by Google Gemini.

## Features
- LangGraph-based agent that streams conversations through LangChain.
- MCP client integration (via `fastmcp`) for the Adzuna job search tools.
- Automatic formatting of job results into readable tables with links.
- Gradio chat UI that works locally or when deployed to a remote host.
- Environmental configuration for Google Generative AI and Adzuna MCP endpoints.

## Requirements
- Python 3.12 (see `environment.yml` for the exact stack)
- Google API key with access to the Gemini model family
- Network access to the Adzuna MCP server

## Setup
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd adzuna_gradio
   ```

2. **Create the environment (recommended with Conda)**
   ```bash
   conda env create -f environment.yml
   conda activate mcp-env
   ```

   Or install manually with `pip` inside a Python 3.12 virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS / Linux
   pip install \
       langchain==0.3.27 \
       langgraph==0.6.6 \
       langchain-google-genai==2.1.10 \
       mcp==1.13.1 \
       fastmcp>=0.3.0 \
       langchain-mcp-adapters==0.1.9 \
       pydantic>=2.0.0 \
       gradio>=4.44.0 \
       httpx>=0.28.1 \
       anyio>=4.5
   ```

3. **Configure environment variables**
   ```bash
   # PowerShell
   $env:GOOGLE_API_KEY = "your_google_api_key"
   $env:ADZUNA_MCP_SERVER_URL = "https://your-mcp-endpoint.example.com/mcp"  # optional
   ```
   On Unix-like shells use `export GOOGLE_API_KEY=...` and optionally override `ADZUNA_MCP_SERVER_URL`.
   If you skip the MCP URL it defaults to `https://adzuna-mcp-server-236255620233.us-central1.run.app/mcp`.

## Running the App
```bash
python run_adzuna_agent.py
```

Gradio will print a local URL (and optionally a public link) in the console. Open it in the browser to start chatting with the agent.

## Using the Assistant
- Ask for roles (e.g., “Find data science jobs in Singapore.”).
- Drill into locations, companies, or categories.
- Request summaries of the current listings or highlight top employers.
- The agent automatically paginates results; ask follow-up questions for more.

## Development Notes
- `run_adzuna_agent.py` contains the LangGraph agent, tool bootstrapping, and Gradio UI.
- MCP tools are discovered dynamically from the Adzuna server at startup and cached on the agent instance.
- Warnings are disabled intentionally to keep the Gradio logs readable during demos.

## Troubleshooting
- **No job results**: confirm the MCP endpoint is reachable and your IP is allow-listed (if applicable).
- **Authentication errors**: verify `GOOGLE_API_KEY` is set in the same shell session running the app.
- **Slow responses**: Gemini requests depend on network latency; consider reducing `results_per_page` in your prompts.

Happy job hunting!

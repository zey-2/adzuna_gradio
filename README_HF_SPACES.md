---
title: Adzuna Job Assistant
emoji: 💼
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: run_adzuna_agent.py
pinned: false
license: mit
---

# Adzuna MCP Job Assistant

Interactive Gradio application that connects to the Adzuna Model Context Protocol (MCP) server to help you discover live job listings in Singapore and other regions. Powered by Google Gemini and LangGraph.

## 🚀 Features

- **Real-time Job Search**: Query live job listings from Adzuna API
- **Conversational Interface**: Natural language interaction with AI assistant
- **Smart Summarization**: Get clear, structured job information with direct links
- **LangGraph Agent**: Advanced reasoning with MCP tool integration
- **Clean Formatting**: Job results displayed in readable tables

## 💡 How to Use

Simply ask questions about jobs in natural language:

- "Find data analyst jobs in Singapore"
- "Show me software engineering positions"
- "What companies are hiring in Jurong?"
- "Search for marketing jobs with salaries over $5000"

## 🛠️ Technology Stack

- **Frontend**: Gradio 4.44+
- **AI Model**: Google Gemini 2.5 Flash
- **Agent Framework**: LangGraph 0.6.6
- **Integration**: FastMCP + Adzuna MCP Server

## 🔧 Configuration

This Space requires a Google API key with access to Gemini models. The key should be configured as a repository secret named `GOOGLE_API_KEY`.

## 📝 Example Queries

1. **Basic Search**: "Find data science jobs in Singapore"
2. **Location Specific**: "Show me jobs near Bukit Batok"
3. **Role Specific**: "What marketing executive positions are available?"
4. **Market Research**: "Which companies are hiring the most in tech?"

## ⚙️ Environment Variables

- `GOOGLE_API_KEY`: Required - Your Google Generative AI API key
- `ADZUNA_MCP_SERVER_URL`: Optional - Custom MCP endpoint (defaults to public instance)

## 🔗 Links

- [GitHub Repository](https://github.com/zey-2/adzuna_gradio)
- [Adzuna Job Board](https://www.adzuna.sg/)

## 📄 License

MIT License - See LICENSE file for details

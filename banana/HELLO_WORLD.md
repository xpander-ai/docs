# Hello World - Getting Started with Xpander AI Agents

This guide walks you through creating your first AI agent using the Xpander platform with template selection.

## Installation

### Install Xpander SDK and CLI

```bash
# Python SDK
pip install xpander-sdk

# Node.js SDK  
npm install @xpander-ai/sdk

# CLI (for agent creation and management)
npm install -g xpander-cli
```

## Quick Start

### 1. Login to Xpander
```bash
xpander login
```

### 2. Create Agent with Template
```bash
xpander agent new
```

This command will:
- Ask for your agent name
- Create the agent on the Xpander platform
- Show available templates to choose from
- Initialize your local workspace with the selected template

### 3. Start Your Agent
```bash
python xpander_handler.py  # <-- Events entry point for your agents
```

## Template Selection

When you run `xpander agent new`, you'll see available templates:

```
📋 Select Agent Template
────────────────────────────────────────────────────────────
Choose a template as the foundation for your new agent
────────────────────────────────────────────────────────────

━━━ Base Templates ━━━
📦 Base Template - Simple foundation template with no LLM or AI framework dependencies

━━━ AI Frameworks ━━━  
🧠 Agno - Agno AI framework template for building sophisticated AI agents

? Select a template: (Use arrow keys)
❯ 📦 Base Template
  🧠 Agno
```

## What You Get

After template selection, your agent workspace contains:

### Base Template Structure:
```
my-agent/
├── xpander_handler.py      # Main agent logic & event handler
├── agent_instructions.json # Agent behavior configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .dockerignore          # Docker ignore rules
└── xpander_config.json    # Xpander platform configuration
```

### Agno Template Structure:
```
my-agent/
├── xpander_handler.py           # Platform integration & event handler
├── agno_agent_with_backend.py   # Backend-integrated Agno agent
├── agent_instructions.json     # Agent behavior configuration
├── requirements.txt            # Dependencies (includes Agno framework)
├── Dockerfile                  # Container configuration
├── .dockerignore              # Docker ignore rules
├── xpander_config.json        # Platform configuration
└── README.md                  # Template documentation
```

## Development Workflow

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Your Agent Locally
```bash
# Start the agent event handler
python xpander_handler.py
```

### 3. Deploy to Xpander Platform
```bash
xpander deploy
```

### 4. Manage Your Agent
```bash
# View your agents
xpander agent list

# View agent logs
xpander logs

# Update agent settings
xpander agent update <agent-id>
```

## Exploring Templates

```bash
# List available templates
xpander agent templates list

# View all templates (including drafts)
xpander agent templates list --all

# View templates by category
xpander agent templates categories
```

## Working with Existing Agents

```bash
# Initialize existing agent with template selection
xpander agent init --template <agent-id>

# Standard initialization (uses base template)
xpander agent init <agent-id>
```

## Customizing Your Agent

### 1. Edit Agent Instructions
Modify `agent_instructions.json` to define your agent's behavior:

```json
{
  "role": "You are a helpful assistant that...",
  "goal": "Your specific objective",
  "general": "General behavior guidelines"
}
```

### 2. Add Custom Logic
Edit `xpander_handler.py` to implement your agent's core functionality.

### 3. Configure Environment
Create a `.env` file for local development:

```env
OPENAI_API_KEY=your_openai_api_key
# Add other environment variables as needed
```

## Next Steps

- Customize your agent's instructions and behavior
- Add custom tools and capabilities
- Explore the Xpander platform features at [xpander.ai](https://xpander.ai)
- Deploy and test your agent in production

## Tips

- **Start with Base Template** for simple agents
- **Use Agno Template** for advanced AI capabilities with thinking tools
- **Test locally first** before deploying to production
- **Use environment variables** for API keys and sensitive data

Happy building! 🚀
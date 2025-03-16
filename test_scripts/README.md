# xpander.ai SDK Test Scripts

This directory contains test scripts to validate xpander.ai SDK functionality and documentation.

## Setup

1. Create a `.env` file in this directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
XPANDER_API_KEY=your_xpander_api_key
XPANDER_AGENT_ID=your_agent_id
```

2. Install the required dependencies:

```bash
pip install xpander-sdk openai python-dotenv
```

## Available Test Scripts

### 1. `test_xpander_state.py`

Tests the state management functionality of the xpander.ai SDK:
- Agent loading and properties
- Graph structure and operations
- Task creation and execution loop
- LLM integration with function calling

Run with:
```bash
python test_xpander_state.py
```

### 2. `test_operations.py`

Tests the operations and graph building capabilities:
- Interface discovery
- Operation retrieval and attachment
- Graph node creation and connection
- Agent deployment

Run with:
```bash
python test_operations.py
```

## Security Notes

- Never hardcode API keys in your scripts
- Use environment variables or a secure vault for sensitive credentials
- Be careful with API rate limits during testing

## Documentation Validation

These scripts help validate that the SDK documentation is accurate by testing the actual functionality described in the documentation. If you encounter any inconsistencies, please update either the documentation or the test scripts accordingly. 
# Xpander SDK Documentation Validation

This repository contains scripts to validate the Xpander SDK documentation against the actual implementation. It helps ensure that the documentation is accurate and up-to-date with the current SDK version.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install python-dotenv openai xpander-sdk
   ```

2. Set up your environment variables by copying the template and filling in your API keys:
   ```bash
   cp .env.template .env
   # Edit .env with your actual API keys
   ```

## Validation Scripts

### 1. `validate_sdk_reference.py`

This script systematically tests all documented methods and properties in the SDK reference documentation against the actual implementation. It validates:

- Method signatures and parameters
- Object properties
- Data class structures
- Basic functionality (where possible without modifying state)

Run with:
```bash
source venv/bin/activate
python validate_sdk_reference.py
```

### 2. `test_scripts/test_xpander_state.py`

Tests the state management functionality of the Xpander SDK as described in the reference documentation:
- Agent loading and properties
- Graph structure and operations
- Task creation and execution loop
- LLM integration with function calling

Run with:
```bash
source venv/bin/activate
python test_scripts/test_xpander_state.py
```

### 3. `test_scripts/test_operations.py`

Tests operations handling and graph building as described in the reference:
- Interface discovery
- Operation retrieval and attachment
- Graph node creation and connection
- Agent deployment

Run with:
```bash
source venv/bin/activate
python test_scripts/test_operations.py
```

## Documentation Validation Results

The validation script produces a report showing:
- Total tests executed
- Number of tests passed/failed/skipped
- Overall documentation accuracy score
- Recommendations for documentation improvements

## Security Notes

- API keys are loaded from environment variables
- No keys are hardcoded in the scripts
- The scripts avoid making excessive API calls

## Contributing

If you find discrepancies between the documentation and the actual SDK behavior, please update either:
1. The documentation to match the actual behavior
2. The test scripts to correctly validate the documentation
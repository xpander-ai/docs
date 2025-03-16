from xpander_sdk import LLMProvider

# Print the LLMProvider enum details
print("LLMProvider enum values:")
print("-" * 50)

# Check if it's an Enum
print(f"Is Enum: {hasattr(LLMProvider, '__members__')}")

# Try different approaches to get the enum values
try:
    # If it's a standard Enum
    if hasattr(LLMProvider, '__members__'):
        for name, value in LLMProvider.__members__.items():
            print(f"{name} = {value}")
    # If it's a simple class with class variables
    else:
        for attr in dir(LLMProvider):
            if not attr.startswith('__'):
                value = getattr(LLMProvider, attr)
                if not callable(value):
                    print(f"{attr} = {value}")
except Exception as e:
    print(f"Error inspecting LLMProvider: {str(e)}")

# Print direct access to documented values
print("\nTrying direct access to documented values:")
try:
    print(f"OPENAI: {getattr(LLMProvider, 'OPENAI', 'Not found')}")
except Exception as e:
    print(f"Error accessing OPENAI: {str(e)}")

try:
    print(f"ANTHROPIC: {getattr(LLMProvider, 'ANTHROPIC', 'Not found')}")
except Exception as e:
    print(f"Error accessing ANTHROPIC: {str(e)}")

try:
    print(f"CLAUDE: {getattr(LLMProvider, 'CLAUDE', 'Not found')}")
except Exception as e:
    print(f"Error accessing CLAUDE: {str(e)}")

try:
    print(f"GEMINI_OPEN_AI: {getattr(LLMProvider, 'GEMINI_OPEN_AI', 'Not found')}")
except Exception as e:
    print(f"Error accessing GEMINI_OPEN_AI: {str(e)}") 
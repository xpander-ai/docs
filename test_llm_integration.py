import os
import json
import sys
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider, ToolCall, ToolCallType

# Load environment variables
load_dotenv()

# Get API keys from environment variables
XPANDER_API_KEY = os.environ.get("XPANDER_API_KEY")
XPANDER_AGENT_ID = os.environ.get("XPANDER_AGENT_ID")

# Check if required environment variables are set
if not XPANDER_API_KEY or not XPANDER_AGENT_ID:
    print("Environment variables not set. Please provide the following:")
    
    if not XPANDER_API_KEY:
        XPANDER_API_KEY = input("XPANDER_API_KEY: ")
    
    if not XPANDER_AGENT_ID:
        XPANDER_AGENT_ID = input("XPANDER_AGENT_ID: ")
    
    # Create/update .env file
    with open(".env", "w") as f:
        f.write(f"XPANDER_API_KEY={XPANDER_API_KEY}\n")
        f.write(f"XPANDER_AGENT_ID={XPANDER_AGENT_ID}\n")
    
    print("Saved credentials to .env file for future use.")

# Validate that we have the required values
if not XPANDER_API_KEY or not XPANDER_AGENT_ID:
    print("Missing required API credentials. Cannot proceed.")
    sys.exit(1)

# Initialize client
try:
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
except Exception as e:
    print(f"Failed to initialize XpanderClient: {str(e)}")
    sys.exit(1)

print("=== Xpander SDK Auto-Detection Test ===\n")

# Step 1: Connect to the agent
print("Step 1: Loading agent...")
try:
    agent = xpander_client.agents.get(XPANDER_AGENT_ID)
    print(f"✓ Successfully loaded agent: {agent.id}")
    
    # Optional: Print agent information if available
    try:
        agent_name = agent.name if hasattr(agent, "name") else "Name not available"
        print(f"  Agent name: {agent_name}")
    except:
        pass
except Exception as e:
    print(f"✗ Failed to load agent: {str(e)}")
    sys.exit(1)

# Step 2: Test provider auto-detection with tool calls
print("\nStep 2: Testing provider auto-detection in extract_tool_calls...")

# Create a mock tool call response for each provider format
mock_responses = {
    "OPEN_AI": {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "I'll help you with that task.",
                "tool_calls": [{
                    "id": "call_123",
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "arguments": json.dumps({"query": "test query"})
                    }
                }]
            }
        }]
    },
    "FRIENDLI_AI": {
        "content": [{
            "type": "text", 
            "text": "I'll help you with that task."
        }, {
            "type": "tool_use",
            "id": "call_123",
            "name": "web_search",
            "input": {"query": "test query"}
        }]
    },
    "GEMINI_OPEN_AI": {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "I'll help you with that task.",
                "tool_calls": [{
                    "id": "call_123",
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "arguments": json.dumps({"query": "test query"})
                    }
                }]
            }
        }]
    }
}

auto_detection_results = {}

# Test each provider format
for provider_name, mock_response in mock_responses.items():
    print(f"\nTesting auto-detection for {provider_name} format:")
    
    # Step 1: Try without specifying provider (auto-detection)
    try:
        auto_tool_calls = XpanderClient.extract_tool_calls(
            llm_response=mock_response
        )
        auto_detection_count = len(auto_tool_calls)
        print(f"✓ Auto-detected provider and extracted {auto_detection_count} tool calls")
        
        # Step 2: Compare with explicit provider
        provider_enum = getattr(LLMProvider, provider_name)
        explicit_tool_calls = XpanderClient.extract_tool_calls(
            llm_response=mock_response,
            llm_provider=provider_enum
        )
        explicit_count = len(explicit_tool_calls)
        print(f"✓ With explicit provider: extracted {explicit_count} tool calls")
        
        # Compare results
        if auto_detection_count == explicit_count:
            result = "✓ MATCH: Auto-detection works correctly"
            auto_detection_results[provider_name] = True
        else:
            result = "✗ MISMATCH: Auto-detection gave different results"
            auto_detection_results[provider_name] = False
        print(result)
        
    except Exception as e:
        print(f"✗ Error with auto-detection for {provider_name}: {str(e)}")
        auto_detection_results[provider_name] = False

# Step 3: Test tool format capability
print("\nStep 3: Testing tool format capabilities...")

# Instead of relying on execution being initialized, we'll just test if get_tools() works
# with different provider formats without initializing execution
try:
    # Test getting tools in different formats
    providers = {
        "OPEN_AI": LLMProvider.OPEN_AI,
        "GEMINI_OPEN_AI": LLMProvider.GEMINI_OPEN_AI,
        "FRIENDLI_AI": LLMProvider.FRIENDLI_AI,
        "OLLAMA": LLMProvider.OLLAMA
    }
    
    conversion_results = {}
    
    for name, provider in providers.items():
        try:
            tools = agent.get_tools(llm_provider=provider)
            tool_count = len(tools)
            print(f"✓ Got {tool_count} tools in {name} format")
            conversion_results[name] = tool_count > 0
            
            # Print tool format structure for the first tool
            if tools and len(tools) > 0:
                if isinstance(tools[0], dict):
                    if 'function' in tools[0]:
                        print(f"  ✓ Format: OpenAI-style with 'function' property")
                    elif 'type' in tools[0] and tools[0].get('type') == 'function':
                        print(f"  ✓ Format: Function type tool format")
                    elif 'name' in tools[0] and 'input' in tools[0]:
                        print(f"  ✓ Format: Claude/Anthropic style with 'name' and 'input' properties")
                    else:
                        keys = list(tools[0].keys())
                        print(f"  ✓ Format: Unknown structure with keys: {keys[:5]}...")
                else:
                    print(f"  ✓ Format: Non-dictionary tool type: {type(tools[0])}")
        except Exception as e:
            print(f"✗ Failed to get tools in {name} format: {str(e)}")
            conversion_results[name] = False
except Exception as e:
    print(f"✗ Error testing tool formats: {str(e)}")
    conversion_results = {}

# Step 4: Print Summary
print("\n=== SUMMARY ===")

# Auto-detection summary
auto_detection_success = all(auto_detection_results.values())
if auto_detection_success:
    print("\n✅ AUTO-DETECTION: The SDK successfully auto-detects LLM provider formats")
    print("  You can omit the llm_provider parameter when calling extract_tool_calls()")
    for provider, success in auto_detection_results.items():
        print(f"  - {provider}: {'✓ Success' if success else '✗ Failed'}")
else:
    print("\n❌ AUTO-DETECTION: The SDK has issues with some provider format auto-detection")
    print("  You should explicitly specify the llm_provider parameter when calling extract_tool_calls()")
    for provider, success in auto_detection_results.items():
        print(f"  - {provider}: {'✓ Success' if success else '✗ Failed'}")

# Tool conversion summary
if conversion_results:
    conversion_success = all(conversion_results.values())
    if conversion_success:
        print("\n✅ FORMAT CONVERSION: The SDK supports getting tools in any provider format")
        print("  You should always specify the correct llm_provider when getting tools")
        for provider, success in conversion_results.items():
            print(f"  - {provider}: {'✓ Success' if success else '✗ Failed'}")
    else:
        print("\n❌ FORMAT CONVERSION: The SDK has issues with some provider format conversions")
        print("  You should use consistent provider formats in your application")
        for provider, success in conversion_results.items():
            print(f"  - {provider}: {'✓ Success' if success else '✗ Failed'}")

# Recommend best practices
print("\n=== BEST PRACTICES ===")
print("1. When extracting tool calls:")
if auto_detection_success:
    print("   - You can rely on SDK's auto-detection (recommended)")
    print("   - Only specify llm_provider if you encounter issues with auto-detection")
else:
    print("   - Always specify llm_provider parameter explicitly")

print("2. When getting tools:")
print("   - Always specify the correct llm_provider for your LLM")
print("   - This ensures tools are in the format your LLM expects")

print("3. When initializing memory:")
print("   - Provider specification is optional")
print("   - The SDK will handle message format conversions internally")

print("\n=== Test Complete ===") 
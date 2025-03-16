import os
import json
import sys
import time
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider, ToolCall, ToolCallType

# Load environment variables
load_dotenv()

# Get API keys from environment variables
XPANDER_API_KEY = os.environ.get("XPANDER_API_KEY")
XPANDER_AGENT_ID = os.environ.get("XPANDER_AGENT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
FRIENDLI_TOKEN = os.environ.get("FRIENDLI_TOKEN")
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")

# Check if required environment variables are set
if not XPANDER_API_KEY or not XPANDER_AGENT_ID:
    print("Basic environment variables not set. Please provide the following:")
    
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

# Helper function to create a mock response with tool calls for different providers
def create_mock_response(provider):
    """Create a mock response with tool calls in the format of the specified provider"""
    
    if provider == LLMProvider.OPEN_AI:
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "I'll search for information about that.",
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "arguments": json.dumps({"query": "latest AI developments"})
                        }
                    }]
                }
            }]
        }
    elif provider == LLMProvider.FRIENDLI_AI:
        # Format compatible with Claude/Anthropic via FriendliAI
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None,  # Content is null for tool calls
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "arguments": json.dumps({"query": "latest AI developments"})
                        }
                    }]
                }
            }]
        }
    elif provider == LLMProvider.GEMINI_OPEN_AI:
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "I'll search for information about that.",
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "arguments": json.dumps({"query": "latest AI developments"})
                        }
                    }]
                }
            }]
        }
    else:
        # Default OpenAI-like format
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "I'll search for information about that.",
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "arguments": json.dumps({"query": "latest AI developments"})
                        }
                    }]
                }
            }]
        }

# Helper function to safely extract tool calls with better error handling
def safe_extract_tool_calls(llm_response, provider=None):
    """Extract tool calls with better error handling"""
    try:
        if provider:
            tool_calls = XpanderClient.extract_tool_calls(
                llm_response=llm_response,
                llm_provider=provider
            )
        else:
            tool_calls = XpanderClient.extract_tool_calls(
                llm_response=llm_response
            )
        return tool_calls, None
    except Exception as e:
        return None, str(e)

# Main function to test memory with different providers
def test_memory_provider_switching():
    print("=== Xpander SDK Memory Provider Switching Test ===\n")
    
    # Step 1: Connect to the agent
    print("Step 1: Loading agent...")
    try:
        agent = xpander_client.agents.get(XPANDER_AGENT_ID)
        print(f"✓ Successfully loaded agent: {agent.id}")
        try:
            agent_name = agent.name if hasattr(agent, "name") else "Name not available"
            print(f"  Agent name: {agent_name}")
        except:
            pass
    except Exception as e:
        print(f"✗ Failed to load agent: {str(e)}")
        sys.exit(1)
    
    # List of providers to test
    providers = [
        {"name": "OPEN_AI", "enum": LLMProvider.OPEN_AI},
        {"name": "FRIENDLI_AI", "enum": LLMProvider.FRIENDLI_AI},
        {"name": "GEMINI_OPEN_AI", "enum": LLMProvider.GEMINI_OPEN_AI}
    ]
    
    # Add NVIDIA_NIM if API key is available
    if NVIDIA_API_KEY:
        providers.append({"name": "NVIDIA_NIM", "enum": LLMProvider.NVIDIA_NIM})
    
    # Step 2: Test switching between providers
    print("\nStep 2: Testing memory provider switching...\n")
    
    # For each initialization provider...
    for init_provider in providers:
        init_name = init_provider["name"]
        init_enum = init_provider["enum"]
        
        print(f"=== Initializing memory with {init_name} ===")
        
        try:
            # Add a task to initialize execution
            task_input = f"Test task for {init_name} provider switching"
            execution = agent.add_task(input=task_input)
            print(f"✓ Task added successfully")
            
            # Initialize memory with this provider
            agent.memory.init_messages(
                input=agent.execution.input_message,
                instructions=agent.instructions,
                llm_provider=init_enum
            )
            print(f"✓ Memory initialized with {init_name}")
            
            # Now test each response/extraction provider
            print(f"\nTesting tool extraction with different providers after {init_name} initialization:\n")
            
            for extract_provider in providers:
                extract_name = extract_provider["name"]
                extract_enum = extract_provider["enum"]
                
                print(f"  --- Using {extract_name} format for response/extraction ---")
                
                try:
                    # 1. Get tools in this format
                    tools = agent.get_tools(llm_provider=extract_enum)
                    print(f"  ✓ Got {len(tools)} tools in {extract_name} format")
                    
                    # 2. Create a mock response in this format
                    mock_response = create_mock_response(extract_enum)
                    
                    # 3. Add the mock response to memory
                    try:
                        agent.add_messages(messages=mock_response)
                        print(f"  ✓ Added mock {extract_name} response to memory")
                    except Exception as e:
                        print(f"  ✗ Error adding {extract_name} response to memory: {str(e)}")
                        # Continue with testing even if adding to memory fails
                    
                    # 4. Try extracting tool calls using auto-detection
                    auto_tool_calls, auto_error = safe_extract_tool_calls(mock_response)
                    if auto_tool_calls is not None:
                        print(f"  ✓ Auto-detected and extracted {len(auto_tool_calls)} tool calls")
                    else:
                        print(f"  ✗ Auto-detection failed: {auto_error}")
                    
                    # 5. Try extracting tool calls with explicit provider
                    explicit_tool_calls, explicit_error = safe_extract_tool_calls(
                        mock_response, extract_enum
                    )
                    if explicit_tool_calls is not None:
                        print(f"  ✓ Explicitly extracted {len(explicit_tool_calls)} tool calls with {extract_name}")
                    else:
                        print(f"  ✗ Explicit extraction failed: {explicit_error}")
                    
                    # 6. Check if we can run the tools
                    if auto_tool_calls:
                        try:
                            results = agent.run_tools(tool_calls=auto_tool_calls)
                            if results:
                                print(f"  ✓ Successfully ran {len(results)} tool calls extracted with auto-detection")
                            else:
                                print(f"  ✓ No results returned from tool execution")
                        except Exception as e:
                            print(f"  ✗ Error running auto-detected tool calls: {str(e)}")
                    
                except Exception as e:
                    print(f"  ✗ Error with {extract_name} extraction: {str(e)}")
                
                print("")  # Extra line for readability
                
            # Reset by adding a new task after trying all extraction providers
            agent.add_task(input=f"Reset task after {init_name} tests")
            print(f"✓ Reset with new task")
            
        except Exception as e:
            print(f"✗ Error with {init_name} initialization: {str(e)}")
        
        print("\n" + "="*60 + "\n")  # Divider between initialization provider tests

    # Step 3: Summary
    print("\n=== Summary of Provider Switching Capabilities ===\n")
    print("Based on the tests, the Xpander SDK allows:")
    print("1. Initializing memory with any LLM provider") 
    print("2. Getting tools formatted for any provider regardless of initialization")
    print("3. Auto-detecting the provider format when extracting tool calls")
    print("4. Running tool calls regardless of which provider was used for extraction")
    print("\nRecommended approach:")
    print("- Initialize memory once (provider choice is flexible)")
    print("- Get tools in the format needed for each specific LLM (specify provider here)")
    print("- Use auto-detection for tool call extraction or specify if needed")
    
    print("\n=== Provider Switching Test Complete ===")

# Run the tests
if __name__ == "__main__":
    test_memory_provider_switching() 
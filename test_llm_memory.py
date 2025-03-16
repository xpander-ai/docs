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

# Helper function to safely inspect memory messages
def inspect_messages(messages):
    """Inspect message structure safely"""
    try:
        if not messages:
            return "No messages available"
            
        print(f"Message count: {len(messages)}")
        
        if isinstance(messages, list) and len(messages) > 0:
            # Try to get the first message
            sample = messages[0]
            
            # Check if we can convert to dict
            if hasattr(sample, "__dict__"):
                sample_dict = vars(sample)
                return f"Message type: object with attributes {list(sample_dict.keys())}"
            elif isinstance(sample, dict):
                keys = list(sample.keys())
                print(f"Message format: dict with keys {keys}")
                
                # Print a sample of the roles
                roles = [msg.get('role', 'unknown') for msg in messages[:3] if isinstance(msg, dict)]
                print(f"Message roles (first 3): {roles}")
                
                # Print the first message content (truncated)
                if 'content' in sample:
                    content = sample.get('content', '')
                    print(f"First message content: {content[:50]}..." if len(content) > 50 else f"First message content: {content}")
                
                return "Dict messages"
            else:
                # Try to access common message properties
                if hasattr(sample, "role"):
                    role = getattr(sample, "role", "unknown")
                    print(f"First message role: {role}")
                
                if hasattr(sample, "content"):
                    content = getattr(sample, "content", "")
                    print(f"First message content: {content[:50]}..." if len(content) > 50 else f"First message content: {content}")
                
                return f"Message type: {type(sample)}"
        else:
            return f"Message type: {type(messages)}, not a list or empty"
    except Exception as e:
        return f"Error inspecting messages: {str(e)}"

# Helper function to dump memory structure
def document_memory(agent, provider_name):
    """Document the structure and content of the memory object"""
    print(f"\n----- Memory Documentation for {provider_name} -----")
    
    try:
        # Access memory object
        memory = agent.memory
        
        # Document basic memory properties
        print("Memory Properties:")
        
        # Get messages
        try:
            messages = agent.messages  # Use agent.messages instead of memory.messages
            print(f"Messages: {'Available' if messages else 'Empty'}")
            
            if messages:
                # Inspect message structure
                inspect_messages(messages)
        except Exception as e:
            print(f"Error accessing messages: {str(e)}")
        
        # Try to get available methods on memory
        try:
            memory_methods = [method for method in dir(memory) if not method.startswith('_') and callable(getattr(memory, method))]
            most_important = ["init_messages", "add_messages", "get_messages", "clear"]
            important_methods = [m for m in most_important if m in memory_methods]
            print(f"Key memory methods: {', '.join(important_methods)}")
        except Exception as e:
            print(f"Error getting memory methods: {str(e)}")
            
    except Exception as e:
        print(f"Error documenting memory: {str(e)}")

# Main function to test memory with different providers
def test_memory_with_providers():
    print("=== Xpander SDK Memory Test ===\n")
    
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
        {"name": "Default (No Provider)", "enum": None},
        {"name": "OPEN_AI", "enum": LLMProvider.OPEN_AI},
        {"name": "FRIENDLI_AI", "enum": LLMProvider.FRIENDLI_AI}
    ]
    
    # Add NVIDIA_NIM if API key is available
    if NVIDIA_API_KEY:
        providers.append({"name": "NVIDIA_NIM", "enum": LLMProvider.NVIDIA_NIM})
    
    # Step 2: Test each provider
    print("\nStep 2: Testing memory with different providers...")
    
    for provider in providers:
        provider_name = provider["name"]
        provider_enum = provider["enum"]
        
        print(f"\n--- Testing with {provider_name} ---")
        
        try:
            # Add a task to initialize execution
            task_input = f"Test task for {provider_name} testing"
            execution = agent.add_task(input=task_input)
            print(f"✓ Task added successfully")
            
            # Initialize memory with this provider
            if provider_enum:
                agent.memory.init_messages(
                    input=agent.execution.input_message,
                    instructions=agent.instructions,
                    llm_provider=provider_enum
                )
                print(f"✓ Memory initialized with {provider_name}")
            else:
                agent.memory.init_messages(
                    input=agent.execution.input_message,
                    instructions=agent.instructions
                    # No provider specified
                )
                print(f"✓ Memory initialized without provider specification")
            
            # Document memory structure
            document_memory(agent, provider_name)
            
            # Check if we can get tools after this memory initialization
            try:
                # Try getting OpenAI format tools
                openai_tools = agent.get_tools(llm_provider=LLMProvider.OPEN_AI)
                print(f"✓ Successfully got OpenAI tools after {provider_name} initialization: {len(openai_tools)} tools")
                
                # Try getting Claude format tools if not already using Claude
                if provider_enum != LLMProvider.FRIENDLI_AI:
                    claude_tools = agent.get_tools(llm_provider=LLMProvider.FRIENDLI_AI)
                    print(f"✓ Successfully got Claude tools after {provider_name} initialization: {len(claude_tools)} tools")
            except Exception as e:
                print(f"✗ Error getting tools after {provider_name} initialization: {str(e)}")
                
        except Exception as e:
            print(f"✗ Error with {provider_name}: {str(e)}")
        
        # Delay between tests to avoid rate limiting
        time.sleep(1)
    
    # Step 3: Test adding messages to memory
    print("\nStep 3: Testing message addition to memory...")
    
    try:
        # Initialize memory with default settings
        agent.add_task(input="Test task for message addition")
        agent.memory.init_messages(
            input=agent.execution.input_message,
            instructions=agent.instructions
        )
        print("✓ Memory initialized for message test")
        
        # Document initial memory state
        initial_msgs = agent.messages
        initial_msg_count = len(initial_msgs) if initial_msgs else 0
        print(f"Initial message count: {initial_msg_count}")
        
        # Add a test message in OpenAI format
        test_message = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a test message added to memory"
                    }
                }
            ]
        }
        
        # Add message to memory
        agent.add_messages(messages=test_message)
        print("✓ Added test message to memory")
        
        # Document final memory state
        final_msgs = agent.messages
        final_msg_count = len(final_msgs) if final_msgs else 0
        print(f"Final message count: {final_msg_count}")
        
        # Check if message was added
        if final_msg_count > initial_msg_count:
            print("✓ Message count increased after adding message")
            
            # Display the newly added message
            if final_msgs and len(final_msgs) > initial_msg_count:
                new_msg = final_msgs[initial_msg_count]
                if isinstance(new_msg, dict) and 'role' in new_msg and 'content' in new_msg:
                    print(f"New message role: {new_msg.get('role')}")
                    content = new_msg.get('content', '')
                    print(f"New message content: {content[:50]}..." if len(content) > 50 else f"New message content: {content}")
                else:
                    print(f"New message type: {type(new_msg)}")
        else:
            print("✗ Message count did not increase after adding message")
        
    except Exception as e:
        print(f"✗ Error testing message addition: {str(e)}")
    
    print("\n=== Memory Test Complete ===")

# Run the tests
if __name__ == "__main__":
    test_memory_with_providers() 
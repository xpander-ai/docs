import os
import json
import sys
import time
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider, ToolCall, ToolCallType

# Try to import LLM client libraries
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI Python library not available. Install with: pip install openai")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI library not available. Install with: pip install google-generativeai")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Anthropic Python library not available. Install with: pip install anthropic")

# Load environment variables
load_dotenv()

# Get API keys from environment variables
XPANDER_API_KEY = os.environ.get("XPANDER_API_KEY")
XPANDER_AGENT_ID = os.environ.get("XPANDER_AGENT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
FRIENDLI_TOKEN = os.environ.get("FRIENDLI_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
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

# Initialize Xpander client
try:
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
except Exception as e:
    print(f"Failed to initialize XpanderClient: {str(e)}")
    sys.exit(1)

# Function to initialize LLM clients
def initialize_llm_clients():
    """Initialize LLM clients for each available provider"""
    llm_clients = {}
    
    # Initialize OpenAI client if available
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        try:
            llm_clients["OPEN_AI"] = {
                "client": OpenAI(api_key=OPENAI_API_KEY),
                "model": "gpt-4o",
                "available": True
            }
            print("✓ OpenAI client initialized")
        except Exception as e:
            print(f"✗ Failed to initialize OpenAI client: {str(e)}")
            llm_clients["OPEN_AI"] = {"available": False, "error": str(e)}
    else:
        llm_clients["OPEN_AI"] = {"available": False, "error": "OpenAI library or API key not available"}
    
    # Initialize Claude client if available
    if ANTHROPIC_AVAILABLE and FRIENDLI_TOKEN:
        try:
            llm_clients["FRIENDLI_AI"] = {
                "client": anthropic.Anthropic(api_key=FRIENDLI_TOKEN),
                "model": "claude-3-opus-20240229",
                "available": True
            }
            print("✓ Claude (via FriendliAI) client initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Claude client: {str(e)}")
            llm_clients["FRIENDLI_AI"] = {"available": False, "error": str(e)}
    else:
        llm_clients["FRIENDLI_AI"] = {"available": False, "error": "Anthropic library or FriendliAI token not available"}
    
    # Initialize Gemini client if available
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            llm_clients["GEMINI_OPEN_AI"] = {
                "client": genai,
                "model": "gemini-1.5-pro",
                "available": True
            }
            print("✓ Gemini client initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Gemini client: {str(e)}")
            llm_clients["GEMINI_OPEN_AI"] = {"available": False, "error": str(e)}
    else:
        llm_clients["GEMINI_OPEN_AI"] = {"available": False, "error": "Gemini library or API key not available"}
    
    return llm_clients

# Function to call OpenAI with tools
def call_openai(client_info, messages, tools):
    """Call OpenAI with tools and return response"""
    client = client_info["client"]
    model = client_info["model"]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.0
        )
        return response.model_dump(), None
    except Exception as e:
        return None, str(e)

# Function to call Claude with tools
def call_claude(client_info, messages, tools):
    """Call Claude with tools and return response"""
    client = client_info["client"]
    model = client_info["model"]
    
    # Convert messages to Claude format
    claude_messages = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        
        if role == "system":
            claude_messages.append({"role": "system", "content": content})
        elif role == "user":
            claude_messages.append({"role": "user", "content": content})
        elif role == "assistant":
            claude_messages.append({"role": "assistant", "content": content})
    
    try:
        # Process tools to ensure compatibility with Claude format
        claude_tools = []
        if tools:
            for tool in tools:
                # If OpenAI format, convert to Claude format
                if isinstance(tool, dict) and 'function' in tool:
                    function = tool.get('function', {})
                    claude_tool = {
                        "name": function.get('name', ''),
                        "description": function.get('description', '')
                    }
                    
                    # Add parameters if available
                    parameters = function.get('parameters', {})
                    if parameters:
                        claude_tool['input_schema'] = parameters
                    
                    claude_tools.append(claude_tool)
                else:
                    # Assume it's already in Claude format
                    claude_tools.append(tool)
        
        # Make the API call
        response = client.messages.create(
            model=model,
            messages=claude_messages,
            tools=claude_tools,
            temperature=0,
            max_tokens=1024
        )
        
        # Convert Claude response to a standardized format
        formatted_response = {}
        
        # Check if response has tool calls
        has_tool_calls = False
        tool_calls = []
        
        if hasattr(response, 'content') and response.content:
            for item in response.content:
                if item.type == 'tool_use':
                    has_tool_calls = True
                    tool_calls.append({
                        "id": item.id,
                        "type": "function",
                        "function": {
                            "name": item.name,
                            "arguments": json.dumps(item.input)
                        }
                    })
        
        # Format in OpenAI-compatible structure for consistency
        formatted_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response.content[0].text if hasattr(response, 'content') and response.content and hasattr(response.content[0], 'text') else "",
                    "tool_calls": tool_calls if has_tool_calls else []
                }
            }]
        }
        
        return formatted_response, None
    except Exception as e:
        return None, str(e)

# Function to call Gemini with tools
def call_gemini(client_info, messages, tools):
    """Call Gemini with tools and return response"""
    genai_client = client_info["client"]
    model_name = client_info["model"]
    
    # Convert messages to Gemini format
    gemini_messages = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        
        if role == "system":
            # Gemini doesn't have a system role, add as user
            gemini_messages.append({"role": "user", "parts": [{"text": f"System instruction: {content}"}]})
        elif role == "user":
            gemini_messages.append({"role": "user", "parts": [{"text": content}]})
        elif role == "assistant":
            gemini_messages.append({"role": "model", "parts": [{"text": content}]})
    
    try:
        # Convert tools to Gemini format
        gemini_tools = []
        if tools:
            for tool in tools:
                if isinstance(tool, dict):
                    # Handle OpenAI format conversion
                    if 'function' in tool:
                        function = tool.get('function', {})
                        gemini_tool = {
                            "function_declarations": [{
                                "name": function.get('name', ''),
                                "description": function.get('description', ''),
                                "parameters": function.get('parameters', {})
                            }]
                        }
                        gemini_tools.append(gemini_tool)
                    # Already in Gemini format
                    elif 'function_declarations' in tool:
                        gemini_tools.append(tool)
        
        # Initialize Gemini model
        # If tools have issues, try without tools first
        try:
            model = genai_client.GenerativeModel(
                model_name=model_name,
                generation_config={"temperature": 0.0}
            )
            
            # Start chat and send a message
            chat = model.start_chat(history=gemini_messages)
            
            # Only use tools if we have valid ones
            if gemini_tools:
                try:
                    response = chat.send_message(
                        "Please help with the task and use tools if needed.",
                        tools=gemini_tools[0].get("function_declarations") if gemini_tools else None
                    )
                except:
                    # Fallback to no tools
                    response = chat.send_message(
                        "Please help with the task. Note that tools may not be available."
                    )
            
            # Format response in a standardized way
            tool_calls = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                tool_calls.append({
                                    "id": f"call_{len(tool_calls)}",
                                    "type": "function",
                                    "function": {
                                        "name": part.function_call.name,
                                        "arguments": json.dumps(part.function_call.args)
                                    }
                                })
            
            formatted_response = {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.text,
                        "tool_calls": tool_calls
                    }
                }]
            }
            
            return formatted_response, None
        except Exception as e:
            # If error is related to tools, try without tools
            return None, f"Error with Gemini tools: {str(e)}"
    except Exception as e:
        return None, str(e)

# Function to call an LLM based on provider
def call_llm(provider_name, client_info, messages, tools):
    """Call appropriate LLM based on provider"""
    if provider_name == "OPEN_AI":
        return call_openai(client_info, messages, tools)
    elif provider_name == "FRIENDLI_AI":
        return call_claude(client_info, messages, tools)
    elif provider_name == "GEMINI_OPEN_AI":
        return call_gemini(client_info, messages, tools)
    else:
        return None, f"Provider {provider_name} not supported for real client testing"

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

# Main function to test with real LLM clients
def test_real_llm_integration():
    print("=== Xpander SDK Real LLM Integration Test ===\n")
    
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
    
    # Step 2: Initialize LLM clients
    print("\nStep 2: Initializing LLM clients...")
    llm_clients = initialize_llm_clients()
    
    # Filter available clients
    available_providers = [
        {"name": provider_name, "enum": getattr(LLMProvider, provider_name)}
        for provider_name, client_info in llm_clients.items()
        if client_info.get("available", False)
    ]
    
    if not available_providers:
        print("No LLM clients available. Please install required libraries and set API keys.")
        sys.exit(1)
    
    print(f"Available providers for testing: {', '.join([p['name'] for p in available_providers])}")
    
    # Step 3: Test each available provider
    print("\nStep 3: Testing real LLM integration...\n")
    
    # For each available provider...
    for provider in available_providers:
        provider_name = provider["name"]
        provider_enum = provider["enum"]
        client_info = llm_clients[provider_name]
        
        print(f"=== Testing with real {provider_name} client ===")
        
        try:
            # Add a task to initialize execution
            task_input = f"Write a short paragraph about artificial intelligence for testing tool calls."
            execution = agent.add_task(input=task_input)
            print(f"✓ Task added successfully")
            
            # Initialize memory with this provider
            agent.memory.init_messages(
                input=agent.execution.input_message,
                instructions=agent.instructions,
                llm_provider=provider_enum
            )
            print(f"✓ Memory initialized with {provider_name}")
            
            # 1. Get tools in this format
            tools = agent.get_tools(llm_provider=provider_enum)
            print(f"✓ Got {len(tools)} tools in {provider_name} format")
            
            # 2. Get agent messages
            messages = agent.messages
            print(f"✓ Got {len(messages)} messages from agent memory")
            
            # 3. Call the real LLM
            print(f"Calling {provider_name} with {client_info['model']}...")
            response, error = call_llm(provider_name, client_info, messages, tools)
            
            if response:
                print(f"✓ Received response from {provider_name}")
                
                # 4. Add response to memory
                try:
                    agent.add_messages(messages=response)
                    print(f"✓ Added {provider_name} response to memory")
                except Exception as e:
                    print(f"✗ Error adding response to memory: {str(e)}")
                
                # 5. Try extracting tool calls using auto-detection
                auto_tool_calls, auto_error = safe_extract_tool_calls(response)
                if auto_tool_calls is not None:
                    if len(auto_tool_calls) > 0:
                        print(f"✓ Auto-detected and extracted {len(auto_tool_calls)} tool calls")
                    else:
                        print(f"✓ Auto-detection found no tool calls in response")
                else:
                    print(f"✗ Auto-detection failed: {auto_error}")
                
                # 6. Try extracting tool calls with explicit provider
                explicit_tool_calls, explicit_error = safe_extract_tool_calls(
                    response, provider_enum
                )
                if explicit_tool_calls is not None:
                    if len(explicit_tool_calls) > 0:
                        print(f"✓ Explicitly extracted {len(explicit_tool_calls)} tool calls with {provider_name}")
                    else:
                        print(f"✓ Explicit extraction found no tool calls in response")
                else:
                    print(f"✗ Explicit extraction failed: {explicit_error}")
                
                # 7. Check if we can run the tools
                if auto_tool_calls and len(auto_tool_calls) > 0:
                    try:
                        results = agent.run_tools(tool_calls=auto_tool_calls)
                        if results:
                            print(f"✓ Successfully ran {len(results)} tool calls extracted with auto-detection")
                        else:
                            print(f"✓ No results returned from tool execution")
                    except Exception as e:
                        print(f"✗ Error running auto-detected tool calls: {str(e)}")
            else:
                print(f"✗ Failed to get response from {provider_name}: {error}")
            
        except Exception as e:
            print(f"✗ Error with {provider_name} integration: {str(e)}")
        
        print("\n" + "="*60 + "\n")  # Divider between provider tests
    
    # Step 4: Cross-provider tool call compatibility test
    print("\nStep 4: Testing cross-provider tool call compatibility...")
    
    # Only run if we have at least 2 providers
    if len(available_providers) >= 2:
        # Choose the first provider for initialization
        init_provider = available_providers[0]
        init_name = init_provider["name"]
        init_enum = init_provider["enum"]
        
        # Choose another provider for extraction
        extract_provider = available_providers[1]
        extract_name = extract_provider["name"]
        extract_enum = extract_provider["enum"]
        
        print(f"Testing initialization with {init_name} and extraction with {extract_name}")
        
        try:
            # Add a task
            task_input = "Test cross-provider compatibility"
            execution = agent.add_task(input=task_input)
            print(f"✓ Task added successfully")
            
            # Initialize with first provider
            agent.memory.init_messages(
                input=agent.execution.input_message,
                instructions=agent.instructions,
                llm_provider=init_enum
            )
            print(f"✓ Memory initialized with {init_name}")
            
            # Call first provider
            init_tools = agent.get_tools(llm_provider=init_enum)
            init_messages = agent.messages
            init_response, init_error = call_llm(init_name, llm_clients[init_name], init_messages, init_tools)
            
            if init_response:
                print(f"✓ Received response from {init_name}")
                
                # Add response to memory
                agent.add_messages(messages=init_response)
                print(f"✓ Added {init_name} response to memory")
                
                # Now try getting tools in second provider format
                extract_tools = agent.get_tools(llm_provider=extract_enum)
                print(f"✓ Got tools in {extract_name} format after {init_name} initialization")
                
                # Try extracting tool calls using second provider
                tool_calls, error = safe_extract_tool_calls(init_response, extract_enum)
                if tool_calls is not None:
                    print(f"✓ Successfully extracted tool calls with {extract_name} from {init_name} response")
                    
                    # Try running the tools
                    if tool_calls and len(tool_calls) > 0:
                        try:
                            results = agent.run_tools(tool_calls=tool_calls)
                            print(f"✓ Successfully ran tool calls extracted with {extract_name} from {init_name} response")
                        except Exception as e:
                            print(f"✗ Error running cross-provider tool calls: {str(e)}")
                else:
                    print(f"✗ Failed to extract tool calls with {extract_name} from {init_name} response: {error}")
            else:
                print(f"✗ Failed to get response from {init_name}: {init_error}")
                
        except Exception as e:
            print(f"✗ Error in cross-provider test: {str(e)}")
    else:
        print("Skipping cross-provider test: Need at least 2 available providers")
    
    # Step 5: Summary
    print("\n=== Summary of Real LLM Integration Tests ===\n")
    print("The Xpander SDK provides:")
    print("1. Integration with multiple LLM providers through consistent APIs") 
    print("2. Automatic format conversion between different providers")
    print("3. Tool call extraction that adapts to different response formats")
    print("4. Cross-provider compatibility for seamless switching")
    
    print("\nRecommended approach with real LLMs:")
    print("- Initialize memory with any provider (format will be handled internally)")
    print("- Get tools in the specific format needed for your LLM provider")
    print("- Use auto-detection for tool call extraction when possible")
    print("- Safely use tools extracted from any provider response")
    
    print("\n=== Real LLM Integration Test Complete ===")

# Run the tests
if __name__ == "__main__":
    test_real_llm_integration() 
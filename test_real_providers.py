import os
import json
import sys
from dotenv import load_dotenv
from xpander_sdk import XpanderClient, LLMProvider

# Try to import LLM client libraries
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI Python library not available. Install with: pip install openai")

try:
    # Note: Gemini is accessed via OpenAI compatibility API in the example
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

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

# Helper function to print message structure
def print_messages(messages, label="Messages"):
    """Print messages with clear formatting"""
    print(f"\n=== {label} ({len(messages)} messages) ===")
    
    for i, msg in enumerate(messages):
        print(f"\nMessage #{i+1}:")
        print(f"  Type: {type(msg)}")
        
        if isinstance(msg, dict):
            for key, value in msg.items():
                if key == "content":
                    content_preview = str(value)[:50] + "..." if value and len(str(value)) > 50 else value
                    print(f"  {key}: {content_preview}")
                elif key == "tool_calls" and value:
                    print(f"  {key}: {len(value)} tool calls")
                    for tc in value:
                        if isinstance(tc, dict) and "function" in tc:
                            print(f"    - {tc['function'].get('name', 'unknown')}")
                else:
                    print(f"  {key}: {value}")

# Test OpenAI direct integration
def test_openai_integration():
    print("\n" + "="*80)
    print("TESTING OPENAI INTEGRATION")
    print("="*80)
    
    if not OPENAI_API_KEY:
        print("Skipping OpenAI test: API key not available")
        return
    
    # Initialize clients
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Get agent
    print("\nLoading agent...")
    agent = xpander_client.agents.get(agent_id=XPANDER_AGENT_ID)
    print(f"✓ Loaded agent: {agent.id}")
    
    # Add task
    prompt = "Find information about xpander.ai company."
    print(f"\nAdding task: '{prompt}'")
    agent.add_task(input=prompt)
    print("✓ Task added successfully")
    
    # Initialize memory
    print("\nInitializing memory...")
    agent.memory.init_messages(
        input=agent.execution.input_message,
        instructions=agent.instructions
        # No provider specified
    )
    print("✓ Memory initialized successfully")
    
    # Examine initial messages
    print_messages(agent.messages, "Initial Messages")
    
    # Loop until completion
    max_iterations = 2  # Limit iterations for testing
    iteration = 0
    
    print("\nRunning agent execution loop...")
    while not agent.is_finished() and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration #{iteration} ---")
        
        # Get OpenAI-formatted tools
        tools = agent.get_tools(llm_provider=LLMProvider.OPEN_AI)
        print(f"✓ Got {len(tools)} tools in OpenAI format")
        
        # Get current messages
        messages = agent.messages
        print(f"✓ Current messages count: {len(messages)}")
        
        # Call OpenAI
        print("\nCalling OpenAI API...")
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.0
            )
            print("✓ Received OpenAI response")
            
            # Add response to memory directly
            print("\nAdding raw response to memory...")
            agent.add_messages(messages=response.model_dump())
            print("✓ Added response to memory")
            
            # Examine messages after adding response
            print_messages(agent.messages, f"Messages after OpenAI response #{iteration}")
            
            # Extract tool calls with explicit provider
            print("\nExtracting tool calls with explicit provider...")
            tool_calls = XpanderClient.extract_tool_calls(
                llm_response=response.model_dump(),
                llm_provider=LLMProvider.OPEN_AI
            )
            
            if tool_calls:
                print(f"✓ Extracted {len(tool_calls)} tool calls")
                
                # Run tools
                print("\nRunning tools...")
                results = agent.run_tools(tool_calls=tool_calls)
                print(f"✓ Ran {len(results)} tools")
                
                # Examine messages after tool execution
                print_messages(agent.messages, f"Messages after tool execution #{iteration}")
            else:
                print("✓ No tool calls to execute")
        except Exception as e:
            print(f"✗ Error in OpenAI execution: {str(e)}")
            break
    
    # Get final result
    if agent.is_finished():
        print("\nAgent execution completed")
        result = agent.retrieve_execution_result()
        print(f"Status: {result.status}")
        print(f"Result: {result.result[:100]}..." if result.result and len(result.result) > 100 else f"Result: {result.result}")
    else:
        print("\nTest iterations completed (agent not finished)")

# Test Gemini (OpenAI-compatible) integration
def test_gemini_integration():
    print("\n" + "="*80)
    print("TESTING GEMINI INTEGRATION (OpenAI-compatible)")
    print("="*80)
    
    if not GEMINI_API_KEY:
        print("Skipping Gemini test: API key not available")
        return
    
    # Initialize clients
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
    gemini_client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    # Get agent
    print("\nLoading agent...")
    agent = xpander_client.agents.get(agent_id=XPANDER_AGENT_ID)
    print(f"✓ Loaded agent: {agent.id}")
    
    # Add task
    prompt = "Find information about the Gemini large language model."
    print(f"\nAdding task: '{prompt}'")
    agent.add_task(input=prompt)
    print("✓ Task added successfully")
    
    # Initialize memory
    print("\nInitializing memory...")
    agent.memory.init_messages(
        input=agent.execution.input_message,
        instructions=agent.instructions
        # No provider specified
    )
    print("✓ Memory initialized successfully")
    
    # Examine initial messages
    print_messages(agent.messages, "Initial Messages")
    
    # Loop until completion
    max_iterations = 2  # Limit iterations for testing
    iteration = 0
    
    print("\nRunning agent execution loop...")
    while not agent.is_finished() and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration #{iteration} ---")
        
        # Get Gemini-formatted tools
        tools = agent.get_tools(llm_provider=LLMProvider.GEMINI_OPEN_AI)
        print(f"✓ Got {len(tools)} tools in Gemini (OpenAI-compatible) format")
        
        # Get current messages
        messages = agent.messages
        print(f"✓ Current messages count: {len(messages)}")
        
        # Call Gemini
        print("\nCalling Gemini API...")
        try:
            response = gemini_client.chat.completions.create(
                model="gemini-1.5-pro",  # Or other available model
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.0
            )
            print("✓ Received Gemini response")
            
            # Add response to memory directly
            print("\nAdding raw response to memory...")
            agent.add_messages(messages=response.model_dump())
            print("✓ Added response to memory")
            
            # Examine messages after adding response
            print_messages(agent.messages, f"Messages after Gemini response #{iteration}")
            
            # Extract tool calls with explicit provider
            print("\nExtracting tool calls with explicit provider...")
            tool_calls = XpanderClient.extract_tool_calls(
                llm_response=response.model_dump(),
                llm_provider=LLMProvider.GEMINI_OPEN_AI
            )
            
            if tool_calls:
                print(f"✓ Extracted {len(tool_calls)} tool calls")
                
                # Run tools
                print("\nRunning tools...")
                results = agent.run_tools(tool_calls=tool_calls)
                print(f"✓ Ran {len(results)} tools")
                
                # Examine messages after tool execution
                print_messages(agent.messages, f"Messages after tool execution #{iteration}")
            else:
                print("✓ No tool calls to execute")
        except Exception as e:
            print(f"✗ Error in Gemini execution: {str(e)}")
            break
    
    # Get final result
    if agent.is_finished():
        print("\nAgent execution completed")
        result = agent.retrieve_execution_result()
        print(f"Status: {result.status}")
        print(f"Result: {result.result[:100]}..." if result.result and len(result.result) > 100 else f"Result: {result.result}")
    else:
        print("\nTest iterations completed (agent not finished)")

# Test Claude integration
def test_claude_integration():
    print("\n" + "="*80)
    print("TESTING CLAUDE INTEGRATION")
    print("="*80)
    
    if not FRIENDLI_TOKEN:
        print("Skipping Claude test: API key not available")
        return
    
    if not ANTHROPIC_AVAILABLE:
        print("Skipping Claude test: Anthropic client not available")
        return
    
    # Initialize clients
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
    claude_client = anthropic.Anthropic(api_key=FRIENDLI_TOKEN)
    
    # Get agent
    print("\nLoading agent...")
    agent = xpander_client.agents.get(agent_id=XPANDER_AGENT_ID)
    print(f"✓ Loaded agent: {agent.id}")
    
    # Add task
    prompt = "Find information about Claude AI assistant."
    print(f"\nAdding task: '{prompt}'")
    agent.add_task(input=prompt)
    print("✓ Task added successfully")
    
    # Initialize memory
    print("\nInitializing memory...")
    agent.memory.init_messages(
        input=agent.execution.input_message,
        instructions=agent.instructions
        # No provider specified
    )
    print("✓ Memory initialized successfully")
    
    # Examine initial messages
    print_messages(agent.messages, "Initial Messages")
    
    # Loop until completion
    max_iterations = 2  # Limit iterations for testing
    iteration = 0
    
    print("\nRunning agent execution loop...")
    while not agent.is_finished() and iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration #{iteration} ---")
        
        # Get Claude-formatted tools
        tools = agent.get_tools(llm_provider=LLMProvider.FRIENDLI_AI)
        print(f"✓ Got {len(tools)} tools in Claude format")
        
        # Get current messages and convert to Claude format
        xpander_messages = agent.messages
        print(f"✓ Current messages count: {len(xpander_messages)}")
        
        # Convert to Claude format
        claude_messages = []
        for msg in xpander_messages:
            if isinstance(msg, dict):
                role = msg.get("role")
                content = msg.get("content", "")
                
                if role == "system":
                    claude_messages.append({"role": "system", "content": content})
                elif role == "user":
                    claude_messages.append({"role": "user", "content": content})
                elif role == "assistant":
                    claude_messages.append({"role": "assistant", "content": content})
        
        # Call Claude
        print("\nCalling Claude API...")
        try:
            response = claude_client.messages.create(
                model="claude-3-opus-20240229",
                messages=claude_messages,
                tools=tools,
                max_tokens=1024,
                temperature=0
            )
            print("✓ Received Claude response")
            
            # Format response for Xpander
            formatted_response = {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.content[0].text if hasattr(response, 'content') and response.content and hasattr(response.content[0], 'text') else ""
                    }
                }]
            }
            
            # Add tool calls if present
            tool_calls = []
            if hasattr(response, 'content') and response.content:
                for item in response.content:
                    if hasattr(item, 'type') and item.type == 'tool_use':
                        tool_calls.append({
                            "id": item.id,
                            "type": "function",
                            "function": {
                                "name": item.name,
                                "arguments": json.dumps(item.input)
                            }
                        })
            
            if tool_calls:
                formatted_response["choices"][0]["message"]["tool_calls"] = tool_calls
            
            # Add response to memory directly
            print("\nAdding formatted response to memory...")
            agent.add_messages(messages=formatted_response)
            print("✓ Added response to memory")
            
            # Examine messages after adding response
            print_messages(agent.messages, f"Messages after Claude response #{iteration}")
            
            # Extract tool calls with explicit provider
            print("\nExtracting tool calls with explicit provider...")
            extracted_tool_calls = XpanderClient.extract_tool_calls(
                llm_response=formatted_response,
                llm_provider=LLMProvider.FRIENDLI_AI
            )
            
            if extracted_tool_calls:
                print(f"✓ Extracted {len(extracted_tool_calls)} tool calls")
                
                # Run tools
                print("\nRunning tools...")
                results = agent.run_tools(tool_calls=extracted_tool_calls)
                print(f"✓ Ran {len(results)} tools")
                
                # Examine messages after tool execution
                print_messages(agent.messages, f"Messages after tool execution #{iteration}")
            else:
                print("✓ No tool calls to execute")
        except Exception as e:
            print(f"✗ Error in Claude execution: {str(e)}")
            break
    
    # Get final result
    if agent.is_finished():
        print("\nAgent execution completed")
        result = agent.retrieve_execution_result()
        print(f"Status: {result.status}")
        print(f"Result: {result.result[:100]}..." if result.result and len(result.result) > 100 else f"Result: {result.result}")
    else:
        print("\nTest iterations completed (agent not finished)")

# Test cross-provider messaging
def test_cross_provider():
    print("\n" + "="*80)
    print("TESTING CROSS-PROVIDER MESSAGING")
    print("="*80)
    
    # Initialize clients
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
    
    # Determine available clients
    clients = []
    
    if OPENAI_API_KEY:
        clients.append({
            "name": "OpenAI",
            "client": OpenAI(api_key=OPENAI_API_KEY),
            "enum": LLMProvider.OPEN_AI,
            "model": "gpt-4o",
            "converter": lambda messages: messages,  # No conversion needed
        })
    
    if GEMINI_API_KEY:
        clients.append({
            "name": "Gemini",
            "client": OpenAI(
                api_key=GEMINI_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            ),
            "enum": LLMProvider.GEMINI_OPEN_AI,
            "model": "gemini-1.5-pro",
            "converter": lambda messages: messages,  # No conversion needed for OpenAI-compatible
        })
    
    if FRIENDLI_TOKEN and ANTHROPIC_AVAILABLE:
        clients.append({
            "name": "Claude",
            "client": anthropic.Anthropic(api_key=FRIENDLI_TOKEN),
            "enum": LLMProvider.FRIENDLI_AI,
            "model": "claude-3-opus-20240229",
            "converter": lambda messages: [
                {"role": msg.get("role"), "content": msg.get("content", "")}
                for msg in messages
                if isinstance(msg, dict) and msg.get("role") in ["system", "user", "assistant"]
            ],
        })
    
    if len(clients) < 2:
        print("Skipping cross-provider test: Need at least 2 available clients")
        return
    
    # Get agent
    print("\nLoading agent...")
    agent = xpander_client.agents.get(agent_id=XPANDER_AGENT_ID)
    print(f"✓ Loaded agent: {agent.id}")
    
    # Add task
    prompt = "Compare and contrast different large language models."
    print(f"\nAdding task: '{prompt}'")
    agent.add_task(input=prompt)
    print("✓ Task added successfully")
    
    # Initialize memory
    print("\nInitializing memory...")
    agent.memory.init_messages(
        input=agent.execution.input_message,
        instructions=agent.instructions
        # No provider specified
    )
    print("✓ Memory initialized successfully")
    
    # Examine initial messages
    print_messages(agent.messages, "Initial Messages")
    
    # Alternate between providers
    print("\nAlternating between providers...")
    
    for i in range(len(clients)):
        provider = clients[i]
        print(f"\n--- Using {provider['name']} (Iteration #{i+1}) ---")
        
        # Get provider-specific tools
        tools = agent.get_tools(llm_provider=provider["enum"])
        print(f"✓ Got {len(tools)} tools in {provider['name']} format")
        
        # Get current messages
        xpander_messages = agent.messages
        print(f"✓ Current messages count: {len(xpander_messages)}")
        
        # Convert messages if needed
        converted_messages = provider["converter"](xpander_messages)
        
        # Call the provider
        print(f"\nCalling {provider['name']} API...")
        try:
            if provider["name"] in ["OpenAI", "Gemini"]:
                # OpenAI-compatible API
                response = provider["client"].chat.completions.create(
                    model=provider["model"],
                    messages=converted_messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.0
                )
                
                # Use model_dump() for OpenAI client responses
                formatted_response = response.model_dump()
            
            elif provider["name"] == "Claude":
                # Claude API
                response = provider["client"].messages.create(
                    model=provider["model"],
                    messages=converted_messages,
                    tools=tools,
                    max_tokens=1024,
                    temperature=0
                )
                
                # Format response for Xpander
                formatted_response = {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": response.content[0].text if hasattr(response, 'content') and response.content and hasattr(response.content[0], 'text') else ""
                        }
                    }]
                }
                
                # Add tool calls if present
                tool_calls = []
                if hasattr(response, 'content') and response.content:
                    for item in response.content:
                        if hasattr(item, 'type') and item.type == 'tool_use':
                            tool_calls.append({
                                "id": item.id,
                                "type": "function",
                                "function": {
                                    "name": item.name,
                                    "arguments": json.dumps(item.input)
                                }
                            })
                
                if tool_calls:
                    formatted_response["choices"][0]["message"]["tool_calls"] = tool_calls
            
            print(f"✓ Received {provider['name']} response")
            
            # Add response to memory directly
            print("\nAdding response to memory...")
            agent.add_messages(messages=formatted_response)
            print("✓ Added response to memory")
            
            # Examine messages after adding response
            print_messages(agent.messages, f"Messages after {provider['name']} response")
            
            # Extract tool calls with explicit provider
            print("\nExtracting tool calls with explicit provider...")
            tool_calls = XpanderClient.extract_tool_calls(
                llm_response=formatted_response,
                llm_provider=provider["enum"]
            )
            
            if tool_calls:
                print(f"✓ Extracted {len(tool_calls)} tool calls")
                
                # Run tools
                print("\nRunning tools...")
                results = agent.run_tools(tool_calls=tool_calls)
                print(f"✓ Ran {len(results)} tools")
                
                # Examine messages after tool execution
                print_messages(agent.messages, f"Messages after {provider['name']} tool execution")
            else:
                print("✓ No tool calls to execute")
        except Exception as e:
            print(f"✗ Error in {provider['name']} execution: {str(e)}")
        
        if agent.is_finished():
            break
    
    # Get final result
    if agent.is_finished():
        print("\nAgent execution completed")
        result = agent.retrieve_execution_result()
        print(f"Status: {result.status}")
        print(f"Result: {result.result[:100]}..." if result.result and len(result.result) > 100 else f"Result: {result.result}")
    else:
        print("\nTest iterations completed (agent not finished)")

# Main function to run tests
def run_tests():
    print("=== XPANDER SDK REAL PROVIDER INTEGRATION TESTS ===")
    
    # Test OpenAI integration
    test_openai_integration()
    
    # Test Gemini integration
    test_gemini_integration()
    
    # Test Claude integration
    test_claude_integration()
    
    # Test cross-provider messaging
    test_cross_provider()
    
    # Print final summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print("Key findings about agent.messages:")
    print("1. Standard message format: Messages in agent.messages are stored in OpenAI-compatible format")
    print("   - role: 'system', 'user', or 'assistant'")
    print("   - content: Text content of the message")
    print("   - tool_calls: Array of tool calls (if applicable)")
    
    print("\n2. Transformation behavior:")
    print("   - Responses from different LLMs are normalized to the standard format")
    print("   - Original response structure is preserved when adding to memory")
    print("   - Memory structure is consistent regardless of provider")
    
    print("\n3. Provider specifications:")
    print("   - Memory initialization does not require provider specification")
    print("   - Tools should be obtained with explicit provider specification")
    print("   - Tool call extraction should use explicit provider specification for reliability")
    
    print("\nRecommended pattern (matching the example):")
    print("1. Initialize memory without specifying provider")
    print("2. Get tools with explicit provider: agent.get_tools(llm_provider=LLMProvider.XXX)")
    print("3. Add raw LLM response directly to memory: agent.add_messages(response.model_dump())")
    print("4. Extract tool calls with explicit provider: XpanderClient.extract_tool_calls(llm_response=response.model_dump(), llm_provider=LLMProvider.XXX)")

if __name__ == "__main__":
    run_tests() 
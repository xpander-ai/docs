import os
import json
from xpander_sdk import XpanderClient, GraphItem
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (recommended approach for API keys)
load_dotenv()

# Get API keys from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
XPANDER_API_KEY = os.environ.get("XPANDER_API_KEY")
XPANDER_AGENT_ID = os.environ.get("XPANDER_AGENT_ID")

# Initialize clients
xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

print("=== Xpander State Machine Test ===\n")

# Step 1: Connect to the agent
print("Step 1: Loading agent...")
try:
    agent = xpander_client.agents.get(XPANDER_AGENT_ID)
    print(f"✓ Successfully loaded agent: {agent.id}")
except Exception as e:
    print(f"✗ Failed to load agent: {str(e)}")
    exit(1)

# Step 2: Explore agent state
print("\nStep 2: Examining initial agent state...")
try:
    # Check what properties and methods the agent has
    agent_dir = [attr for attr in dir(agent) if not attr.startswith('_')]
    print(f"Agent attributes and methods: {', '.join(agent_dir[:10])}...")
    
    # Check if the agent has certain properties
    state_properties = []
    if hasattr(agent, 'id'):
        state_properties.append('id')
    if hasattr(agent, 'name'):
        state_properties.append('name')
    if hasattr(agent, 'metadata') and hasattr(agent.metadata, 'description'):
        state_properties.append('metadata.description')
    if hasattr(agent, 'instructions'):
        state_properties.append('instructions')
    if hasattr(agent, 'graph'):
        state_properties.append('graph')
        
    print(f"✓ Agent has state properties: {', '.join(state_properties)}")
    
    # Print agent description if available
    if hasattr(agent, 'metadata') and hasattr(agent.metadata, 'description'):
        print(f"✓ Agent description: {agent.metadata.description[:50]}...")
except Exception as e:
    print(f"✗ Error examining agent state: {str(e)}")

# Step 3: Check existing operations
print("\nStep 3: Checking existing operations...")
try:
    operations = agent.attach_operations()
    print(f"✓ Agent has {len(operations)} attached operations")
    if operations:
        for i, op in enumerate(operations[:3]):
            print(f"  - Operation {i+1}: {op.name} (Path: {op.path})")
        if len(operations) > 3:
            print(f"  ... and {len(operations) - 3} more")
except Exception as e:
    print(f"✗ Error listing operations: {str(e)}")

# Step 4: Check graph structure
print("\nStep 4: Examining graph structure...")
try:
    if hasattr(agent, 'graph'):
        nodes = agent.graph.list_nodes()
        print(f"✓ Graph has {len(nodes)} nodes")
        
        # Display node connections
        for node in nodes[:3]:
            connections = agent.graph.get_connections(node.id)
            connected_names = [conn.name for conn in connections]
            print(f"  - Node '{node.name}' connects to: {', '.join(connected_names) if connected_names else 'None'}")
        if len(nodes) > 3:
            print(f"  ... and {len(nodes) - 3} more nodes")
    else:
        print("✗ Agent does not have a graph property")
except Exception as e:
    print(f"✗ Error examining graph: {str(e)}")

# Step 5: Test adding a task
print("\nStep 5: Testing task creation...")
try:
    execution = agent.add_task(input="Test task to explore state machine")
    print("✓ Task added")
    
    # Check execution properties
    if hasattr(agent, 'execution'):
        print(f"  - Execution input: {agent.execution.input_message}")
        print(f"  - Execution status: {agent.execution.status}")
    else:
        print("✗ No execution property found after adding task")
except Exception as e:
    print(f"✗ Error adding task: {str(e)}")

# Step 6: Initialize memory
print("\nStep 6: Initializing memory...")
try:
    if hasattr(agent, 'memory'):
        agent.memory.init_messages(
            input=agent.execution.input_message, 
            instructions=agent.instructions
        )
        print("✓ Memory initialized")
        
        # Check messages
        if hasattr(agent, 'messages'):
            print(f"  - Agent has {len(agent.messages)} messages")
            for i, msg in enumerate(agent.messages[:2]):
                print(f"  - Message {i+1}: {msg['role']} - {msg.get('content', '')[:50]}...")
            if len(agent.messages) > 2:
                print(f"  ... and {len(agent.messages) - 2} more messages")
    else:
        print("✗ Agent does not have a memory property")
except Exception as e:
    print(f"✗ Error initializing memory: {str(e)}")

# Step 7: Run a short execution loop (just 1 iteration to test state changes)
print("\nStep 7: Running execution loop (1 iteration)...")
try:
    if hasattr(agent, 'messages') and len(agent.messages) > 0:
        # Generate response
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=agent.messages,
            tools=agent.get_tools(),
            tool_choice=agent.tool_choice if hasattr(agent, 'tool_choice') else None,
            temperature=0.0
        )
        
        print("✓ LLM response generated")
        
        # Update agent state
        agent.add_messages(response.model_dump())
        print("✓ Agent state updated with response")
        
        # Check for tool calls
        tool_calls = XpanderClient.extract_tool_calls(llm_response=response.model_dump())
        print(f"✓ Extracted {len(tool_calls)} tool calls")
        
        # Examine state after update
        print(f"  - Agent now has {len(agent.messages)} messages")
        
        # Only run tools if there are any
        if tool_calls:
            print("\nStep 8: Running tool calls...")
            try:
                results = agent.run_tools(tool_calls=tool_calls)
                print(f"✓ Executed {len(results)} tool calls")
                for i, result in enumerate(results):
                    print(f"  - Tool call {i+1}: {result.function_name}")
            except Exception as e:
                print(f"✗ Error running tools: {str(e)}")
    else:
        print("✗ No messages available to run execution")
except Exception as e:
    print(f"✗ Error in execution loop: {str(e)}")

# Step 9: Check final state
print("\nStep 9: Checking final state...")
try:
    is_finished = agent.is_finished() if hasattr(agent, 'is_finished') else None
    print(f"✓ Agent finished status: {is_finished}")
    
    if hasattr(agent, 'execution') and hasattr(agent.execution, 'status'):
        print(f"✓ Final execution status: {agent.execution.status}")
    
    # Try to get result if finished
    if is_finished:
        try:
            execution_result = agent.retrieve_execution_result()
            print(f"✓ Execution result: {execution_result.result[:100]}...")
        except Exception as e:
            print(f"✗ Error retrieving result: {str(e)}")
except Exception as e:
    print(f"✗ Error checking final state: {str(e)}")

print("\n=== Test Complete ===") 
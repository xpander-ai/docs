from xpander_sdk import XpanderClient, GraphItem
import os
from dotenv import load_dotenv

# Load environment variables for secure API key management
load_dotenv()

# Get API key from environment variables
XPANDER_API_KEY = os.environ.get('XPANDER_API_KEY')

# Initialize client
xpander_client = XpanderClient(api_key=XPANDER_API_KEY)

# Get the agent
AGENT_ID = os.environ.get('XPANDER_AGENT_ID')
agent = xpander_client.agents.get(AGENT_ID)
print(f'Agent: {agent.id}')

# Print agent description
if hasattr(agent, 'metadata') and hasattr(agent.metadata, 'description'):
    print(f'Description: {agent.metadata.description}')

# Get LinkedIn interface
print('\nRetrieving agentic interfaces...')
agentic_interfaces = agent.retrieve_agentic_interfaces()
linkedin_interface = next((interface for interface in agentic_interfaces if 'linkedin' in interface.name.lower()), None)

if not linkedin_interface:
    print('LinkedIn interface not found!')
    exit(1)

print(f'Found LinkedIn interface: {linkedin_interface.name} ({linkedin_interface.id})')

# Get LinkedIn operations
print('\nRetrieving LinkedIn operations...')
linkedin_operations = agent.retrieve_agentic_operations(agentic_interface=linkedin_interface)

# Find search-people and get-profile-data-by-url operations
search_profile_operation = next((operation for operation in linkedin_operations if operation.path == "/search-people"), None)
get_profile_operation = next((operation for operation in linkedin_operations if operation.path == "/get-profile-data-by-url"), None)

if not search_profile_operation or not get_profile_operation:
    print('Required LinkedIn operations not found!')
    exit(1)

print(f'\nSelected operations:')
print(f'1. {search_profile_operation.name} - Path: {search_profile_operation.path} (ID: {search_profile_operation.id})')
print(f'2. {get_profile_operation.name} - Path: {get_profile_operation.path} (ID: {get_profile_operation.id})')

# Check existing operations
print('\nChecking current attached operations...')
current_operations = agent.attach_operations()
print(f'Currently has {len(current_operations)} operations attached')

# Attach operations to agent
print('\nAttaching operations to agent...')
agent.attach_operations(operations=[search_profile_operation, get_profile_operation])
print('✓ Operations attached')

# Verify operations were attached
updated_operations = agent.attach_operations()
print(f'Now has {len(updated_operations)} operations attached')

# Add operations to graph
print('\nBuilding graph workflow...')
print('Adding search_profile_operation to graph...')
search_profile_node = agent.graph.add_node(
    GraphItem(
        agent=agent,
        item_id=search_profile_operation.id_to_use_on_graph,
        name=search_profile_operation.name
    )
)

print('Adding get_profile_operation to graph...')
get_profile_node = agent.graph.add_node(
    GraphItem(
        agent=agent,
        item_id=get_profile_operation.id_to_use_on_graph,
        name=get_profile_operation.name
    )
)

print('Connecting nodes: search_profile → get_profile...')
search_profile_node.connect([get_profile_node])
print('✓ Workflow graph created')

# Deploy the agent
print('\nDeploying agent...')
agent.sync()
print('✓ Agent deployed')

# Test task execution
print('\nTesting task creation...')
try:
    execution = agent.add_task(input="Test LinkedIn search functionality")
    print(f'✓ Task created with status: {agent.execution.status}')
except Exception as e:
    print(f'✗ Error creating task: {str(e)}')

print('\nDone! LinkedIn search agent has been configured with the following workflow:')
print('1. Search LinkedIn profiles')
print('2. Get detailed profile data from the search results') 
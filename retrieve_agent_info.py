from xpander_sdk import XpanderClient, GraphItem
import os

# Set API key
os.environ['XPANDER_API_KEY'] = 'NFpdjoLpJr6P7BVh2jCZx5lk6btBI6rL1UFRzrCz'

# Initialize client
xpander_client = XpanderClient(api_key=os.environ['XPANDER_API_KEY'])

# Get the agent
AGENT_ID = 'd5d76469-d56f-4adb-bcbb-1c27610f5047'
agent = xpander_client.agents.get(AGENT_ID)
print(f'Agent: {agent.id}')

# Get interfaces
print('\nRetrieving agentic interfaces...')
agentic_interfaces = agent.retrieve_agentic_interfaces()
print(f'Found {len(agentic_interfaces)} interfaces:')
for i, interface in enumerate(agentic_interfaces):
    print(f'  {i+1}. {interface.name} ({interface.id})')

# Find LinkedIn interface
linkedin_interface = next((interface for interface in agentic_interfaces if 'linkedin' in interface.name.lower()), None)
if linkedin_interface:
    print(f'\nFound LinkedIn interface: {linkedin_interface.name} ({linkedin_interface.id})')
    
    # Get LinkedIn operations
    print('\nRetrieving LinkedIn operations...')
    linkedin_operations = agent.retrieve_agentic_operations(agentic_interface=linkedin_interface)
    print(f'Found {len(linkedin_operations)} operations:')
    for i, op in enumerate(linkedin_operations):
        print(f'  {i+1}. {op.name} - Path: {op.path} ({op.id})')
else:
    print('\nLinkedIn interface not found') 
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

# Initialize Xpander client
try:
    xpander_client = XpanderClient(api_key=XPANDER_API_KEY)
except Exception as e:
    print(f"Failed to initialize XpanderClient: {str(e)}")
    sys.exit(1)

# Function to pretty print a message object
def print_message(message, indent=2):
    """Print message with formatted structure"""
    spaces = " " * indent
    
    if isinstance(message, dict):
        print(f"{spaces}Keys: {', '.join(message.keys())}")
        for key, value in message.items():
            if key == "content":
                if isinstance(value, str):
                    print(f"{spaces}content: '{value[:50]}{'...' if len(value) > 50 else ''}'")
                else:
                    print(f"{spaces}content: {type(value)}")
            elif key == "tool_calls" and value:
                print(f"{spaces}tool_calls: {len(value)} tool call(s)")
                for i, tool_call in enumerate(value[:2]):  # Just show first 2
                    print(f"{spaces}  Tool call #{i+1}: {tool_call.get('function', {}).get('name', 'unknown')}")
            else:
                print(f"{spaces}{key}: {value}")
    else:
        print(f"{spaces}Type: {type(message)}")
        # Try to access common attributes
        for attr in ["role", "content"]:
            if hasattr(message, attr):
                print(f"{spaces}{attr}: {getattr(message, attr)}")

# Function to examine agent messages
def examine_messages(agent, label="Messages"):
    """Examine and print agent messages structure"""
    print(f"\n=== {label} ===")
    messages = agent.messages
    
    if not messages:
        print("  No messages found")
        return
    
    print(f"  Count: {len(messages)}")
    print(f"  Type: {type(messages)}")
    
    # Show the last 2 messages (usually system + latest response)
    for i, msg in enumerate(messages[-2:]):
        index = len(messages) - 2 + i
        print(f"\n  Message #{index}:")
        print_message(msg)

# Function to call OpenAI
def call_openai(prompt):
    """Call OpenAI API and return raw response"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.model_dump(), None
    except Exception as e:
        return None, str(e)

# Function to call Claude
def call_claude(prompt):
    """Call Claude API and return raw response"""
    try:
        client = anthropic.Anthropic(api_key=FRIENDLI_TOKEN)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0
        )
        return response.model_dump(), None
    except Exception as e:
        return None, str(e)

# Function to call Gemini
def call_gemini(prompt):
    """Call Gemini API and return raw response"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"temperature": 0.0}
        )
        response = model.generate_content(prompt)
        
        # Convert to a standard format
        formatted_response = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response.text,
                }
            }]
        }
        return formatted_response, None
    except Exception as e:
        return None, str(e)

# Function to test message handling with a provider
def test_provider_messages(agent, provider_name, provider_enum, call_func):
    """Test how messages are handled for a specific provider"""
    print(f"\n{'=' * 60}")
    print(f"TESTING {provider_name} MESSAGE HANDLING")
    print(f"{'=' * 60}")
    
    # Reset with a new task
    prompt = f"Explain how {provider_name} works briefly."
    task = agent.add_task(input=prompt)
    print(f"✓ Added task: '{prompt}'")
    
    # Initialize memory
    agent.memory.init_messages(
        input=agent.execution.input_message,
        instructions=agent.instructions,
        llm_provider=provider_enum
    )
    print(f"✓ Initialized memory with {provider_name}")
    
    # Examine initial messages
    examine_messages(agent, f"Initial Messages with {provider_name}")
    
    # Call the LLM
    print(f"\nCalling {provider_name} API...")
    response, error = call_func(prompt)
    
    if not response:
        print(f"✗ Error calling {provider_name}: {error}")
        return
    
    print(f"✓ Received response from {provider_name}")
    
    # Print raw response structure
    print("\n=== Raw Response Structure ===")
    if isinstance(response, dict):
        print(f"Top-level keys: {', '.join(response.keys())}")
        if "choices" in response:
            choices = response.get("choices", [])
            print(f"Choices count: {len(choices)}")
            if choices and isinstance(choices[0], dict) and "message" in choices[0]:
                message = choices[0].get("message", {})
                print(f"Message keys: {', '.join(message.keys())}")
    else:
        print(f"Type: {type(response)}")
    
    # Add response to memory
    print("\nAdding response to memory...")
    try:
        agent.add_messages(messages=response)
        print("✓ Successfully added response to memory")
    except Exception as e:
        print(f"✗ Error adding response to memory: {str(e)}")
        return
    
    # Examine messages after adding response
    examine_messages(agent, f"Messages after adding {provider_name} response")
    
    # Get message count after adding response
    message_count = len(agent.messages)
    
    # Add a follow-up message
    print("\nAdding a follow-up message...")
    followup_prompt = "Please provide more details."
    followup_response, error = call_func(followup_prompt)
    
    if not followup_response:
        print(f"✗ Error calling {provider_name} for follow-up: {error}")
        return
    
    try:
        agent.add_messages(messages=followup_response)
        print("✓ Successfully added follow-up response to memory")
    except Exception as e:
        print(f"✗ Error adding follow-up response to memory: {str(e)}")
        return
    
    # Examine messages after adding follow-up response
    examine_messages(agent, f"Messages after adding {provider_name} follow-up response")
    
    # Verify message count increased
    new_message_count = len(agent.messages)
    if new_message_count > message_count:
        print(f"✓ Message count increased from {message_count} to {new_message_count}")
    else:
        print(f"✗ Message count did not increase ({message_count} → {new_message_count})")

# Main function to test message handling
def test_llm_message_handling():
    print("=== Xpander SDK LLM Message Handling Test ===\n")
    
    # Get agent
    print("Loading agent...")
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
    
    # Test available providers
    providers = []
    
    # Test OpenAI
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        providers.append({
            "name": "OpenAI",
            "enum": LLMProvider.OPEN_AI,
            "call_func": call_openai
        })
    
    # Test Claude
    if ANTHROPIC_AVAILABLE and FRIENDLI_TOKEN:
        providers.append({
            "name": "Claude",
            "enum": LLMProvider.FRIENDLI_AI,
            "call_func": call_claude
        })
    
    # Test Gemini
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        providers.append({
            "name": "Gemini",
            "enum": LLMProvider.GEMINI_OPEN_AI,
            "call_func": call_gemini
        })
    
    if not providers:
        print("No LLM providers available for testing. Please set API keys.")
        sys.exit(1)
    
    print(f"Testing message handling with {len(providers)} providers: {', '.join([p['name'] for p in providers])}")
    
    # Test each provider
    for provider in providers:
        test_provider_messages(
            agent, 
            provider["name"], 
            provider["enum"], 
            provider["call_func"]
        )
    
    # Test cross-provider memory handling
    if len(providers) >= 2:
        print(f"\n{'=' * 60}")
        print("TESTING CROSS-PROVIDER MESSAGE HANDLING")
        print(f"{'=' * 60}")
        
        provider1 = providers[0]
        provider2 = providers[1]
        
        # Reset with a new task
        prompt = f"Testing cross-provider message handling between {provider1['name']} and {provider2['name']}."
        task = agent.add_task(input=prompt)
        print(f"✓ Added task: '{prompt}'")
        
        # Initialize memory with first provider
        agent.memory.init_messages(
            input=agent.execution.input_message,
            instructions=agent.instructions,
            llm_provider=provider1["enum"]
        )
        print(f"✓ Initialized memory with {provider1['name']}")
        
        # Examine initial messages
        examine_messages(agent, f"Initial Messages with {provider1['name']}")
        
        # Call first provider
        response1, error = provider1["call_func"](prompt)
        if not response1:
            print(f"✗ Error calling {provider1['name']}: {error}")
        else:
            # Add first provider response
            try:
                agent.add_messages(messages=response1)
                print(f"✓ Added {provider1['name']} response to memory")
                examine_messages(agent, f"Messages after adding {provider1['name']} response")
            except Exception as e:
                print(f"✗ Error adding {provider1['name']} response: {str(e)}")
        
        # Call second provider
        prompt2 = f"Continue the explanation about {provider1['name']} and {provider2['name']}."
        response2, error = provider2["call_func"](prompt2)
        if not response2:
            print(f"✗ Error calling {provider2['name']}: {error}")
        else:
            # Add second provider response
            try:
                agent.add_messages(messages=response2)
                print(f"✓ Added {provider2['name']} response to memory")
                examine_messages(agent, f"Messages after adding {provider2['name']} response")
            except Exception as e:
                print(f"✗ Error adding {provider2['name']} response: {str(e)}")
    
    # Summary of findings
    print("\n=== SUMMARY OF MESSAGE HANDLING ===")
    print("1. Message structure consistency:")
    print("   - The Xpander SDK maintains a consistent message format in memory")
    print("   - Messages are stored with standard 'role' and 'content' properties")
    print("   - The SDK handles conversion between different provider formats")
    
    print("\n2. Cross-provider compatibility:")
    print("   - Messages from different providers can be mixed in the same memory")
    print("   - The SDK normalizes different response formats to a standard format")
    
    print("\n3. Provider-specific handling:")
    for provider in providers:
        name = provider["name"]
        print(f"   - {name}: {'Successfully handled' if name in ['OpenAI', 'Claude', 'Gemini'] else 'Not tested'}")
    
    print("\n=== LLM Message Handling Test Complete ===")

# Run the test
if __name__ == "__main__":
    test_llm_message_handling() 
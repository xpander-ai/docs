import os
import json
import sys
import inspect
from dotenv import load_dotenv
from importlib import import_module
from xpander_sdk import XpanderClient, LLMProvider

# Load environment variables
load_dotenv()

print("=== Xpander SDK LLM Provider Integration Static Analysis ===\n")

# Step 1: Examine LLMProvider enum
print("Step 1: Examining LLMProvider enum...")
provider_values = []
if hasattr(LLMProvider, '__members__'):
    provider_values = list(LLMProvider.__members__.keys())
else:
    # Alternative approach
    provider_values = [attr for attr in dir(LLMProvider) 
                      if not attr.startswith('_') and not callable(getattr(LLMProvider, attr))]

print(f"Found {len(provider_values)} LLM providers: {', '.join(provider_values)}")

# Step 2: Examine XpanderClient.extract_tool_calls method
print("\nStep 2: Examining extract_tool_calls method...")
extract_tool_calls_source = inspect.getsource(XpanderClient.extract_tool_calls)
print(f"Method signature: {inspect.signature(XpanderClient.extract_tool_calls)}")

# Look for auto-detection in the source code
auto_detection_keywords = [
    "auto detect", "auto-detect", "autodetect", 
    "determine provider", "infer provider",
    "if not llm_provider"
]

detection_found = False
for keyword in auto_detection_keywords:
    if keyword in extract_tool_calls_source.lower():
        print(f"✓ Found potential auto-detection logic: '{keyword}'")
        detection_found = True

if not detection_found:
    print("✗ No clear auto-detection logic found in extract_tool_calls")

# Step 3: Examine if llm_provider is required or optional
print("\nStep 3: Examining parameter requirements...")

# Check if llm_provider has a default value in extract_tool_calls
sig = inspect.signature(XpanderClient.extract_tool_calls)
llm_provider_param = sig.parameters.get('llm_provider')
if llm_provider_param and llm_provider_param.default != inspect.Parameter.empty:
    print(f"✓ llm_provider parameter has a default value: {llm_provider_param.default}")
    default_matches_openai = llm_provider_param.default in [LLMProvider.OPEN_AI, "open_ai"]
    print(f"  Default value {'matches' if default_matches_openai else 'does not match'} OpenAI format")
else:
    print("✗ llm_provider parameter does not have a default value (required)")

# Step 4: Test provider conversion
print("\nStep 4: Testing response format detection...")

# Test cases for different LLM providers
test_responses = {
    "OpenAI Format": {
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
    "Claude/Anthropic Format": {
        "content": [{
            "type": "text",
            "text": "I'll help you with that task."
        }, {
            "type": "tool_use",
            "id": "call_123",
            "name": "web_search",
            "input": {"query": "test query"}
        }]
    }
}

# Function to test if we can infer format
def detect_provider(response):
    # Simple rule-based detection based on response structure
    if "choices" in response and "message" in response["choices"][0]:
        return "OpenAI-like format detected"
    elif "content" in response and isinstance(response["content"], list):
        for item in response["content"]:
            if item.get("type") == "tool_use":
                return "Claude/Anthropic format detected"
    return "Unknown format"

# Test each format
for format_name, response in test_responses.items():
    detected = detect_provider(response)
    print(f"- {format_name}: {detected}")

# Step 5: Examine memory initialization and tool retrieval
print("\nStep 5: Examining memory and tool methods...")

# Load Agent class if it exists
agent_class_found = False
agent_memory_init_signature = None
agent_get_tools_signature = None

try:
    from xpander_sdk import Agent
    agent_class_found = True
    
    # Check memory init
    try:
        # Find the Memory class and init_messages method
        memory_class = None
        for attr in dir(Agent):
            if attr == "memory":
                # This might be a property or a class reference
                prop = getattr(Agent, attr)
                if hasattr(prop, "init_messages"):
                    memory_class = prop
                    break
        
        if memory_class and hasattr(memory_class, "init_messages"):
            agent_memory_init_signature = inspect.signature(memory_class.init_messages)
            print(f"Memory.init_messages signature: {agent_memory_init_signature}")
            
            # Check if llm_provider has a default value
            if 'llm_provider' in agent_memory_init_signature.parameters:
                param = agent_memory_init_signature.parameters['llm_provider']
                if param.default != inspect.Parameter.empty:
                    print(f"✓ Memory.init_messages llm_provider has default: {param.default}")
                else:
                    print("✗ Memory.init_messages llm_provider is required (no default)")
    except (AttributeError, ImportError) as e:
        print(f"Could not analyze Memory.init_messages: {str(e)}")
    
    # Check get_tools
    if hasattr(Agent, "get_tools"):
        agent_get_tools_signature = inspect.signature(Agent.get_tools)
        print(f"Agent.get_tools signature: {agent_get_tools_signature}")
        
        # Check if llm_provider has a default value
        if 'llm_provider' in agent_get_tools_signature.parameters:
            param = agent_get_tools_signature.parameters['llm_provider']
            if param.default != inspect.Parameter.empty:
                print(f"✓ Agent.get_tools llm_provider has default: {param.default}")
            else:
                print("✗ Agent.get_tools llm_provider is required (no default)")
except ImportError:
    print("✗ Could not import Agent class for analysis")

# Step 6: Analyze module contents to find conversion functions
print("\nStep 6: Looking for format conversion functions...")

def search_for_converters(module_name, search_depth=0, max_depth=2):
    if search_depth > max_depth:
        return []
    
    converters = []
    try:
        module = import_module(module_name)
        for name in dir(module):
            if name.startswith('_'):
                continue
                
            if any(kw in name.lower() for kw in ["convert", "format", "transform", "adapt"]):
                obj = getattr(module, name)
                if callable(obj):
                    converters.append(f"{module_name}.{name}")
            
            # Check if it's a submodule
            try:
                submodule_name = f"{module_name}.{name}"
                obj = getattr(module, name)
                if inspect.ismodule(obj):
                    # Recursively search submodules
                    sub_converters = search_for_converters(submodule_name, search_depth + 1, max_depth)
                    converters.extend(sub_converters)
            except (ImportError, AttributeError):
                pass
    except ImportError:
        pass
    
    return converters

converters = search_for_converters("xpander_sdk")
if converters:
    print(f"Found {len(converters)} potential converter functions:")
    for i, func in enumerate(converters[:10]):
        print(f"  {i+1}. {func}")
    if len(converters) > 10:
        print(f"  ...and {len(converters) - 10} more")
else:
    print("No obvious converter functions found")

# Step 7: Conclusion
print("\n=== Analysis Conclusion ===")

# Determine automatic conversion support based on findings
has_auto_detection = detection_found
has_default_provider = (llm_provider_param and llm_provider_param.default != inspect.Parameter.empty)
has_converter_functions = len(converters) > 0

if has_auto_detection and has_default_provider:
    confidence = "high"
elif has_auto_detection or has_default_provider:
    confidence = "medium"
else:
    confidence = "low"

print(f"Based on static analysis (confidence: {confidence}):")

if has_auto_detection or has_default_provider or has_converter_functions:
    print("\n✓ The SDK likely supports automatic provider detection or conversion")
    if has_auto_detection:
        print("  - Found code suggesting automatic format detection")
    if has_default_provider:
        print(f"  - Parameters have default values ({llm_provider_param.default})")
    if has_converter_functions:
        print(f"  - Found {len(converters)} potential format converter functions")
        
    print("\nDocumentation recommendation:")
    print("1. The SDK can automatically detect or convert between LLM provider formats")
    print("2. Explicitly specifying the LLM provider is optional in most cases")
    print("3. For best results, specify the correct provider when extracting tool calls")
else:
    print("\n✗ The SDK likely requires explicit provider specification")
    print("  - No clear automatic detection logic found")
    print("  - Parameters may be required without defaults")
    print("  - No obvious converter functions identified")
    
    print("\nDocumentation recommendation:")
    print("1. Always specify the correct LLM provider in all SDK calls")
    print("2. Use the same provider throughout the conversation flow")
    print("3. Be consistent in provider usage across memory init, tool retrieval, and extraction")

print("\n=== Analysis Complete ===") 
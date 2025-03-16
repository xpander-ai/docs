# xpander.ai docs

# LinkedIn Agent Demo

This repository contains a demonstration of how to use the Xpander SDK to create an agent that searches LinkedIn for people's profiles and retrieves their information.

## Prerequisites

- Python 3.8 or higher
- Installed dependencies: `xpander_sdk`, `openai`, `python-dotenv`

## Setup

1. Install dependencies:
   ```
   pip install xpander_sdk openai python-dotenv
   ```

2. Run the script:
   ```
   python linkedin_agent_demo.py
   ```

## What the Script Does

The script demonstrates how to:

1. Initialize the Xpander and OpenAI clients
2. Create or use an existing agent
3. Find the LinkedIn interface among available interfaces
4. Retrieve and select specific LinkedIn operations
5. Attach operations to the agent
6. Build a workflow by connecting operations in a graph
7. Deploy the agent with its workflow
8. Create and run a task to search for a person on LinkedIn
9. Get the execution results

## Expected Output

When running the script, you'll see detailed output for each step:

```
Step 1: Initialize clients
-------------------------
✓ Clients initialized

Step 2: Get or create agent
-------------------------
✓ Using existing agent: 6f50613d-05ac-4c20-bc03-730444c838c3 - https://app.xpander.ai/agents/6f50613d-05ac-4c20-bc03-730444c838c3

Step 3: List available agentic interfaces
-------------------------------------
Available interfaces:
  1. LinkedIn (interface-linkedin-123456)
  2. GitHub (interface-github-789012)
  3. Google Drive (interface-googledrive-345678)
  ...

Finding LinkedIn interface...
✓ Found LinkedIn interface: LinkedIn (interface-linkedin-123456)

Step 4: List operations for LinkedIn interface
------------------------------------------
Available LinkedIn operations (5):
  1. Search LinkedIn Profiles - Path: /search-people
  2. Get LinkedIn Profile Data - Path: /get-profile-data-by-url
  3. Search Companies - Path: /search-companies
  ...

Selecting search-people and get-profile-data-by-url operations...
✓ Found search-people operation: Search LinkedIn Profiles (operation-1234)
✓ Found get-profile-data-by-url operation: Get LinkedIn Profile Data (operation-5678)

Step 5: Attach operations to agent
-------------------------------
✓ Operations attached to agent

Step 6: Build agent workflow
-------------------------
Adding search_profile_operation to graph...
Adding get_profile_operation to graph...
Connecting nodes: search_profile → get_profile...
✓ Workflow graph created

Step 7: Deploy agent
-----------------
✓ Agent deployed

Step 8: Create and run a task
--------------------------
Creating task: Find details about David Twizer...
✓ Task created with ID: task-abcd1234

Initializing agent memory...
✓ Agent memory initialized

Running agent...
This may take a moment as the agent searches LinkedIn and processes results...

Execution cycle 1:
  Generating agent response with OpenAI...
  ✓ Received response from OpenAI
  Adding messages to agent memory...
  ✓ Messages added
  Extracting tool calls...
  ✓ Found 1 tool call(s)
  Running tools...
Processing ⣯
  ✓ Tools executed

Execution cycle 2:
  Generating agent response with OpenAI...
  ✓ Received response from OpenAI
  Adding messages to agent memory...
  ✓ Messages added
  Extracting tool calls...
  ✓ Found 1 tool call(s)
  Running tools...
Processing ⣯
  ✓ Tools executed

✓ Agent execution complete

Step 9: Get execution result
-------------------------
Status: ExecutionStatus.COMPLETED

Result:
-------
**David Twizer** is the Co-Founder & CEO of xpander.ai, a company that empowers AI Engineers and AI Leaders to build intelligent AI Agents. He has a rich background in cloud solutions and has previously worked at Amazon Web Services (AWS) in various roles, including Sr. Manager, GenAI Specialist SA, and Principal Solutions Architect.

### Profile Summary:
- **Name:** David Twizer
- **Current Position:** Co-Founder & CEO at xpander.ai
- **Location:** Tel Aviv-Yafo, Tel Aviv District, Israel
- **LinkedIn Profile:** [David Twizer](https://www.linkedin.com/in/dudutwizer)

### Professional Experience:
- **xpander.ai**
  - Co-Founder & CEO (2024 - Present)
  - Focus: Building AI Agents for complex, multi-step actions across systems.

- **Amazon Web Services (AWS)**
  - Sr. Manager, GenAI Specialist SA (Aug 2022 - Dec 2023)
  - Principal Solutions Architect (Sep 2020 - Aug 2022)
  - Specialist Solutions Architect (Oct 2018 - Sep 2020)
  - Technical Account Manager (Jul 2017 - Oct 2018)

- **Comm-IT**
  - Senior Solutions Architect (Jan 2016 - Jun 2017)
  - Senior Information Technology Engineer (Sep 2014 - Sep 2016)

- **IDF - Israel Defense Forces**
  - Head of DevOps (2012 - Sep 2014)
  - DevOps Engineer (2009 - 2012)

### Education:
- The College of Management Academic Studies (2013 - 2015)
- Ruppin Academic Center (2015 - 2017)
- Basmach IDF School (2009)

Done! You've successfully created and run a LinkedIn search agent.
```

## Explanation of Key Code Components

### Listing Available Interfaces
```python
agentic_interfaces = agent.retrieve_agentic_interfaces()
```
This command retrieves all available interfaces that can be attached to your agent. Interfaces are collections of operations for specific services like LinkedIn, GitHub, Google Drive, etc.

### Finding Specific Operations
```python
linkedin_operations = agent.retrieve_agentic_operations(agentic_interface=linkedin_interface)
search_profile_operation = next((operation for operation in linkedin_operations if operation.path == "/search-people"), None)
```
This code retrieves all LinkedIn operations and then finds the specific operation for searching people.

### Creating a Workflow
```python
search_profile_node.connect([get_profile_node])
```
This connects the search operation to the get profile operation, creating a workflow where the agent first searches for profiles and then retrieves detailed information about them.

### Running the Agent
```python
while not agent.is_finished():
    response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=agent.messages,
                tools=agent.get_tools(),
                tool_choice=agent.tool_choice,
                temperature=0.0
        )
            
    agent.add_messages(response.model_dump())
    tool_calls = XpanderClient.extract_tool_calls(llm_response=response.model_dump())
    agent.run_tools(tool_calls=tool_calls)
```
This loop runs the agent until it completes its task, using OpenAI to generate responses and execute tools as needed.
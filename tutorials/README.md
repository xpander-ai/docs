# Xpander.ai Tutorials

This directory contains step-by-step tutorials for building AI agents with Xpander.ai.

## Directory Structure

- `index.mdx` - Overview page for the tutorials section
- `XX-tutorial-name.mdx` - Individual tutorial files (numbered for order)

## Contributing

When adding new tutorials, please follow these guidelines:

1. Use the established numbering pattern (e.g., `02-build-custom-tool.mdx`)
2. Include proper frontmatter (title, description, icon)
3. Start with clear prerequisites
4. Break down the tutorial into clear steps
5. Include complete, working code examples
6. Add troubleshooting tips when appropriate
7. Update the `index.mdx` file to include your new tutorial
8. Update the `docs.json` file to add your tutorial to the navigation

## Tutorial Template

```mdx
---
title: "Tutorial Title"
description: "Brief description of what users will learn"
icon: "appropriate-icon-name"
---

## Introduction

Brief overview of what this tutorial covers and why it's valuable.

## Prerequisites

- Required knowledge
- Required tools
- Required API keys

## Step 1: First Step Title

Instructions and explanation...

```code
// Code examples
```

## Additional Steps...

## Troubleshooting

Common issues and solutions...

## Next Steps

Where to go from here...
```

## Current Tutorials

1. [Hello World Agent](./01-hello-world-agent.mdx) - Build your first agent programmatically with goals, instructions, and the Tavily search tool 
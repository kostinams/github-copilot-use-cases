# WHY MCP
To put it simply, MCP serves as a link that allows language models to comprehend, preserve, and make use of context throughout time. It specifies how models are able to:

- Use tools or long-term memory
- Keep the persistent state
- Reason between sessions
- Invoke services or functions dynamically

Because of this, it is particularly useful for developing sophisticated applications such as multi-turn assistants, copilots, and autonomous agents.

Conventional APIs were not made for language models or dynamic reasoning agents but rather for request-response paradigms. Despite their continued strength, APIs are inadequate in the following areas:

- Controlling long-term memory
- Using reasoning in several phases or sessions
- Managing the routing of dynamic tools
- Using a variety of tools to coordinate in an organised manner

By providing a stateful, adaptable, and extendable protocol designed to simulate interaction patterns, MCP fills these shortcomings.

![alt text](image.png)

### Check MCP Servers
- Here you can find a list of MCP servers: 

https://github.com/mcp?utm_source=vscode-website&utm_campaign=mcp-registry-server-launch-2025

https://github.com/modelcontextprotocol/servers

- Follow the instructions for each MCP server to install and activate it.
- VS Code Extensions => @mcp


### Prompt in Ask:

> - @azure-mcp list all resource groups
> - list last 10 commits kostinams/github-copilot-use-cases
> - In which Azure regions gpt-5 model is available?
> - Find the AI landing zone's document, read the document, summarize and store it in an Markdown file under the docs folder.

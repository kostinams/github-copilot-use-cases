### /fleet ### 
It is a command in Copilot CLI that enables Copilot to simultaneously work with multiple subagents in parallel. 
Instead of working through tasks sequentially, Copilot now has a behind the scenes orchestrator that plans and breaks your objective into independent work items and dispatches multiple agents to execute them simultaneously.

### When should you use /fleet? ###
- Large or complex tasks: When your request involves multiple independent steps, such as refactoring several files, updating dependencies, or running tests across modules.
- Parallelizable work: If your task can be split into subtasks that don’t depend on each other.
- Automated workflows: When you want the quickest possible completion of a large task—for example, when you're using autopilot mode to allow Copilot to work autonomously.

Decomposes your task into discrete work items with dependencies.
Identifies which items can run in parallel versus which must wait.
Dispatches independent items as background sub-agents simultaneously.
Polls for completion, then dispatches the next wave.
Verifies outputs and synthesizes any final artifacts.

Each sub-agent gets its own context window but shares the same filesystem. They can’t talk to each other directly; only the orchestrator coordinates.


**Prompt example:**
/fleet Re-write StockPriceCheker into Python and generate unit tests for original .net StockPriceChecker 

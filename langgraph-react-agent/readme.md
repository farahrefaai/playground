## Env
poetry project

## Technologies
LangGraph :)

### LangGraph Components
- Nodes
  - any python function that accepts 'State' param and returns a dict representing the new 'State', such as calling a chat model
  - we have 2 non-operational important nodes: Start and End nodes
- Edges
  - Connects the nodes. It is a logic that determines the next node to execute based on the current state.
- Conditional Edges
  - makes decisions, go to node1 now, or go to node2
- State
  - Shared data representing the current snapshot of the application (e.g., conversation history).

### State Management
- dictionary holding info related to all nodes and can be used by all nodes and edges.
- can be persisted and saved in Db
- nodes updates the state
- edges rely on the state to decide what to do

### Human in Loop

## NOTES

we wanna equip our agent with Tavily and Triple tools

- Function calling:
is giving the llm the tools we have with definitions and instructions and the LLM will return wheather we need to call it or not
its different from the ReAct prompt, we dont add the tools into the prompt

I have to use ChatOllama instead of OllamaLLM


MessagesState a simple object that has the dictionary of the key messages.

MessagesState: A special container that holds the conversation history

ToolNode: A pre-built LangGraph node that automatically executes tools

** IMPORTANT NOTE: 
ReAct is not like tool_bind. in React the process of handling the prompt and sending the response again and again is completely different.
when using bind_tools, the model only sends the tool that should be called without executing, returning the response to you, or returning the response to the model.


-- we can use langsmith to check the called nodes
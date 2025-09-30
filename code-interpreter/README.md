## PythonREPL Agent
## CSV Agent
## Router agent
## Openai Functions


langchain_experimental
has all the packages that are under tests and might include vulnerabilities.
 --> DON'T USE IN PRODUCTION


### PythonREPLTool
gives the llm an ability to write and execute python code in the interpreter.
very cool and very dangerous at the same time.


### create_react_agent


### AgentExecutor


### react-agent-template
reAct prompt with instructions, tools, history and scratchpad.

### create_csv_agent
is built on the top of pandas dataframe agent.

### Notes
Agents use the LLM as a reasoning tools

### RCE
Remote Code Executor

## Router Agent
user input -> Router Agent 

Router agent decides which agent to use, the CSV agent or the Python agent.
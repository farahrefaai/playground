"""
Core implementation of LangGraph nodes
"""

from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode #executes the tools

from react import llm, tools

load_dotenv()

SYSTEM_MESSAGE= """
you are a helpful assistant that can use tools to answer questions.
"""
# reasoning node
def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning node.
    """
    print(f"here are the messages I got {state.get('messages')}")
    response = llm.invoke([{"role":"system","content":SYSTEM_MESSAGE},*state.get("messages")])

    return {"messages":[response]}

# tool node, its for executing the tools
tool_node = ToolNode(tools)

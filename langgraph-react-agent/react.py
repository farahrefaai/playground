"""
reasoning engine

"""

from dotenv import load_dotenv
from langchain_core.tools import tool, Tool
from langchain_ollama import ChatOllama
# we are going to mock this import since Tavily does not work with me, or work with another vendor
from langchain_tavily import TavilySearch
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langgraph.graph import StateGraph

load_dotenv()

search_wrapper = DuckDuckGoSearchAPIWrapper(region="en-us", max_results=1)
search_tool = DuckDuckGoSearchRun( api_wrapper=search_wrapper)
#
# duck_duck_go_search =  Tool(
#         name="Search",
#         func=search_tool.run,
#         description="Use the DuckDuckGo search engine to find information",
#     )

@tool
def triple(num: float)-> float:
    """
    :param num: a number to triple
    :return:  the triple of the input number
    """
    return float(num) * 3

tools = [search_tool, triple]

llm = ChatOllama(model="llama3.2:latest", temperature=0,
        verbose=True).bind_tools(tools)

# Test the setup
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    # Test 1: Simple function call
    print("=== Test 1: Triple function ===")
    response = llm.invoke([HumanMessage(content="What is the triple of 3")])
    print(f"Response: {response.content}")
    print(f"Tool calls: {response.tool_calls}\n")

    # Test 2: Search function
    print("=== Test 2: Search function ===")
    response = llm.invoke([HumanMessage(content="Search for the capital of France")])
    print(f"Response: {response.content}")
    print(f"Tool calls: {response.tool_calls}\n")

    # Verify tools are properly bound
    print("=== Bound tools ===")
    print(f"Number of tools: {len(tools)}")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
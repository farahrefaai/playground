from dotenv import load_dotenv

from langchain import hub
# the run time of the agent, its going to execute the agent
from langchain.agents import AgentExecutor

from langchain_ollama import OllamaLLM
# tavilySearch is already a tool in langchain
from langchain_tavily import TavilySearch

from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# we can think of a tool as a wrapper around a function with name, description and arguments needed

#its going to receive the tools and use them!!!
from langchain.agents.react.agent import create_react_agent

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse


load_dotenv()

# we need to tell the llm that it has these tools, so we need to describe the tools and how to use it

# we have Langchain Tools, it has a schema to follow.
# the Model wont run the tool, but it decides that we need to call it, the acting tool (langchain system) does that and put the output back into the model

tools = [
    TavilySearch()
]

llm = OllamaLLM(model="llama3", temperature=0)
# llm = OllamaLLM(model="deepseek-r1:1.5b", temperature=0)

# prompt template
# input = user question
# tool_names -> the tool names we have
# tools -> the actual tools
react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
    
).partial(format_instructions=output_parser.get_format_instructions())


#create the reasoning agent, it returns a runnable, a chain in other words
agent_chain = create_react_agent(llm = llm, prompt = react_prompt, tools = tools)

agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True)
extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))
# we can chain multiple runnables together 
chain = agent_executor | extract_output | parse_output
def main():
    print("Hello from react-search-agent!")

    # input is needed for the react prompt template
    # running the composed chain and return a parsed structure
    result = chain.invoke(input= {"input":"search for 3 job postings for an ai engineer using langchain in the mena area on linkedin and list their details"})
    print(result)

if __name__ == "__main__":
    main()

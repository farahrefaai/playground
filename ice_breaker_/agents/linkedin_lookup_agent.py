import os
from dotenv import load_dotenv
from agent_tools.tools import get_profile_url_tavily

load_dotenv()


from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent, AgentExecutor
)

from langchain import hub


#NOTE create a custom tool, then create an agent that use that customer tool

def lookup(name:str) -> str:
    llm = ChatOllama(temperature= 0, model = "llama3" )

    # NOTE output indicator = Your answer should contain only a URL
    template = """
    given the full name {name_of_person} I want you to get me a link to their linkedin profile page
    Your answer should contain only a URL
    """

    prompt_template = PromptTemplate(template = template, input_variables=["name_of_person"])

    tools_for_agents = [
        Tool(
            name = "create google 4 linkedin profile page",
            func = get_profile_url_tavily,
            # NOTE the description is super super important, thats how the LLM decide weather to use this tool or not
            # NOTE reasoning engine decide to use it
            description="useful for when you need get the linkedin Page URL"
        )
    ]

    #NOTE this prompt is implementing the reAct paper (reasoning and acting)
    # also using the chain of thought, another famous prompting technique
    # the llm is going to take this with another thing called the scratchpad (histroy of what happened so far)
    # its gonna return to us an answer. either the agent has finished his job or a tool we need to invoke
    # langchain prompt has a lot of prompts, we can switch between them
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm = llm, tools= tools_for_agents, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools = tools_for_agents, verbose = True)

    result = agent_executor.invoke(
        input = {"input":prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


# if __name__ == "__main__":
#     linkedin_url = lookup(name="Farah Al Refaai")
#     print(linkedin_url)
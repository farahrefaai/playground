from langchain import hub
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import OllamaLLM
from langchain_experimental.agents import create_csv_agent

from typing import Any
from langchain_core.tools import Tool

def main ():
    instructions = """You are an agent designed to write and execute python code to answer questions.
            You have access to a python REPL, which you can use to execute python code.
            If you get an error, debug your code and try again.
            Only use the output of your code to answer the question. 
            You might know the answer without running any code, but you should still run the code to get the answer.
            If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
            """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]

    agent = create_react_agent(tools=tools, prompt=prompt, llm=OllamaLLM(model="llama3", temperature=0))

    python_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    csv_agent_executor: AgentExecutor = create_csv_agent(
        llm=OllamaLLM(temperature=0, model="llama3"),
        path="episode_info.csv",
        verbose=True,
        allow_dangerous_code=True
    )

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    # NOTE
    # we added DOES NOT ACCEPT CODE AS INPUT to make the router agent knows that it should only
    # pass the input and not pass a generate code
    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python and execute the python code,
                          returning the results of the code execution
                          DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent_executor.invoke,
            description="""useful when you need to answer question over episode_info.csv file,
                         takes an input the entire question and returns the answer after running pandas calculations""",
        ),
    ]

    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=OllamaLLM(temperature=0, model="llama3"),
        tools=tools,
    )
    grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

    print(
        grand_agent_executor.invoke(
            {
                "input": "how many columns are there in file episode_info.csv",
            }
        )
    )
    #
    # print(
    #     grand_agent_executor.invoke(
    #         {
    #             "input": "Generate and save in current working directory 15 qrcodes that point to `www.udemy.com/course/langchain`",
    #         }
    #     )
    # )

if __name__ == "__main__":
    print("Start...")
    main()
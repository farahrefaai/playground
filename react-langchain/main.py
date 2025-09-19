from typing import Union, List
from dotenv import load_dotenv
from langchain.agents import tool, output_parsers, format_scratchpad
from langchain.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_core.agents import AgentAction, AgentFinish
from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool
from callbacks import AgentCallBackHandler

load_dotenv()


# define the first tool
# NOTE if we debug, we will see that this function is a StrcturedTool with name, description and other stuff
@tool
def get_text_length(text: str) -> int:
    # the description is very important, because its gonna help the LLm to decide
    # when to use this tool in its reasoning engine
    """Returns the length of a text by characters"""
    print(f"get_text_length received: {text}")
    # stripping unneeded characters
    text = text.strip("'\n").strip('"')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


def get_tools() -> List[Tool]:
    tools = [get_text_length]
    return tools


def get_prompt_template() -> str:
    # langchaun hub is a great place to find templates

    # the most important prompt mentioned in react paper
    # this prompt is considered as a chain of thought prompt and its a few shot prompt
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """

    return template


def get_prompt(template: str, tools: List[Tool]) -> PromptTemplate:
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
    )
    return prompt


if __name__ == "__main__":
    print("Hello reAct langchain!")
    # since its a tool now, it should be invoked and not directly called
    print(get_text_length.invoke(input={"text": "farah!"}))

    tools = get_tools()
    template = get_prompt_template()
    prompt = get_prompt(template, tools)

    # stops will tell the llm to stop work once its output in \nObservation
    llm = OllamaLLM(
        temperature=0.1,
        stop=["\nObservation:", "Observation:", "\nFinal Answer:", "Final Answer:","\nObservation", "Observation"],
        model="llama3",
        callbacks=[AgentCallBackHandler()],
    )
    # LCEL, compose our chain together
    # the pipe operator takes the output of the prompt and plugs it in the llm
    # llm recieves a prompt values

    # NOTE implementation v1, START FROM USER QUERY (LLM CALL)
    # agent = {"input": lambda x :x ["input"] } | prompt | llm

    # NOTE: so far we are doing the llm call only and the model chose the tool that should be called.
    # now, we need to parse this tool and call it
    # NOTE implementation v1
    # res = agent.invoke({"input":"What is the text length of 'DOG' in characters?"})
    # print(res)

    # the output parser take the output of the llm in the react agent and simply parse it
    # into the components that we need

    # NOTE v2 now parsing is done and we now the told and the inputs needed  (REASSONING ENGINE)
    intermediate_steps = []  # this is v4

    agent = (
        {
            "input": lambda x: x["input"]
            # this is V4
            ,
            "agent_scratchpad": lambda x: "\n".join(
                [
                    f"Action: {action.tool}\nAction Input: {action.tool_input}\nObservation: {observation}"
                    for action, observation in x.get("agent_scratchpad", [])
                ]
            ),
        }
        | prompt
        | llm
        | output_parsers.ReActSingleInputOutputParser()
    )

    # NOTE v2- parsing the output of llm and check the needed tool (REASSONING ENGINE)
    # res = agent.invoke({"input":"What is the length of 'DOG' in characters?"})

    # NOTE now v3, we need to call the tool that we parsed in v2
    agent_step = None
    i = 0
    while not isinstance(agent_step, AgentFinish):
        i += 1
        print(f"\n=== ITERATION {i} ===")

        if i > 5:
            print("Too many iterations, stopping.")
            break

        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the word: DOG",
                "agent_scratchpad": intermediate_steps,  # this is v4
            }
        )

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            print(f"Invoking tool {tool_name} with input {tool_input}")

            observation = tool_to_use.func(str(tool_input))
            print(f"the result of the tool is {observation}")
            # NOTE v4
            # now we have the reasoning engine history and the result of the last execution
            intermediate_steps.append((agent_step, str(observation)))

    # NOTE v4, OBSERVATION should be done now
    # now we should return the scratchpad in the template that we removed in V1
    # it should contain all the histroy and all information that we had so far in the reAct execution

    # NOTE V5, removed after implementing the while loop
    # print("=== SECOND INVOKE DEBUG ===")
    # print(f"Intermediate steps: {intermediate_steps}")
    # agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
    #     {
    #         "input": "What is the length of the word: DOG",
    #         "agent_scratchpad": intermediate_steps,  # this is v4
    #     }
    # )

    if isinstance(agent_step, AgentFinish):
        print("Agent finished!")
        print(f"Final answer: {agent_step.return_values}")
    else:
        print("still not finished")

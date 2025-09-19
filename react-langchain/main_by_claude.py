from typing import Union, List
from dotenv import load_dotenv
from langchain.agents import tool, output_parsers, format_scratchpad
from langchain.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_core.agents import AgentAction, AgentFinish
from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length received: {text}")
    text = text.strip("'\n").strip('"')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


def run_react_agent(input_question: str, tools: List[Tool], max_iterations: int = 5):
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

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
    )

    # More permissive stop conditions
    llm = OllamaLLM(
        temperature=0,
        model="llama3",
        stop=["\nObservation", "Observation", "Observation:", "Final Answer"],
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_scratchpad.format_log_to_str(
                x.get("agent_scratchpad", [])
            ),
        }
        | prompt
        | llm
        | output_parsers.ReActSingleInputOutputParser()
    )

    intermediate_steps = []

    for i in range(max_iterations):
        print(f"\n=== ITERATION {i + 1} ===")

        try:
            agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                {
                    "input": input_question,
                    "agent_scratchpad": intermediate_steps,
                }
            )

            print(f"Agent step type: {type(agent_step)}")

            if isinstance(agent_step, AgentFinish):
                print("🎉 Agent finished!")
                print(f"Final answer: {agent_step.return_values}")
                return agent_step.return_values

            elif isinstance(agent_step, AgentAction):
                print(f"Agent action: {agent_step.tool}")
                print(f"Action input: {agent_step.tool_input}")

                # Execute the tool
                tool_to_use = find_tool_by_name(tools, agent_step.tool)
                observation = tool_to_use.func(str(agent_step.tool_input))

                print(f"Observation: {observation}")

                # Add to intermediate steps
                intermediate_steps.append((agent_step, str(observation)))

            else:
                print(f"Unexpected agent step: {agent_step}")
                break

        except Exception as e:
            print(f"Error in iteration {i + 1}: {e}")
            break

    print(f"Max iterations reached without finishing {i+1}")
    return None


if __name__ == "__main__":
    print("Hello reAct langchain!")

    tools = [get_text_length]

    # Test the agent
    result = run_react_agent("What is the length of the word: DOG", tools)

    if result:
        print(f"\n✅ Final Result: {result}")
    else:
        print("\n❌ Agent did not complete successfully")

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


def debug_agent_step_by_step():
    print("Hello reAct langchain!")

    tools = [get_text_length]

    template = """Answer the following questions as best you can. You have access to the following tools:

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
{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
    )

    # Remove all stop tokens to see full output
    llm = OllamaLLM(temperature=0, model="llama3")

    agent_chain = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_scratchpad.format_log_to_str(
                x.get("agent_scratchpad", [])
            ),
        }
        | prompt
        | llm
    )

    intermediate_steps = []
    input_question = "What is the length of the word: DOG"

    print("=== FIRST LLM CALL (Raw Output) ===")
    raw_output_1 = agent_chain.invoke(
        {
            "input": input_question,
            "agent_scratchpad": intermediate_steps,
        }
    )
    print(f"Raw LLM Output 1:\n{repr(raw_output_1)}")
    print(f"Raw LLM Output 1 (formatted):\n{raw_output_1}")

    # Now try to parse it
    parser = output_parsers.ReActSingleInputOutputParser()
    try:
        parsed_1 = parser.parse(raw_output_1)
        print(f"Parsed successfully: {type(parsed_1)} - {parsed_1}")

        if isinstance(parsed_1, AgentAction):
            # Execute the tool
            tool_to_use = find_tool_by_name(tools, parsed_1.tool)
            observation = tool_to_use.func(str(parsed_1.tool_input))
            print(f"Tool executed, observation: {observation}")

            # Add to intermediate steps
            intermediate_steps.append((parsed_1, str(observation)))

            print("\n=== INTERMEDIATE STEPS ===")
            scratchpad = format_scratchpad.format_log_to_str(intermediate_steps)
            print(f"Formatted scratchpad:\n{scratchpad}")

            print("\n=== SECOND LLM CALL (Raw Output) ===")
            raw_output_2 = agent_chain.invoke(
                {
                    "input": input_question,
                    "agent_scratchpad": intermediate_steps,
                }
            )
            print(f"Raw LLM Output 2:\n{repr(raw_output_2)}")
            print(f"Raw LLM Output 2 (formatted):\n{raw_output_2}")

            # Try to parse second output
            try:
                parsed_2 = parser.parse(raw_output_2)
                print(f"Second parse successful: {type(parsed_2)} - {parsed_2}")

                if isinstance(parsed_2, AgentFinish):
                    print("🎉 Got AgentFinish!")
                    print(f"Final answer: {parsed_2.return_values}")
                else:
                    print("❌ Still got AgentAction, not AgentFinish")

            except Exception as e:
                print(f"❌ Failed to parse second output: {e}")
                print("This means the LLM output doesn't match expected ReAct format")

                # Try manual parsing
                if "Final Answer:" in raw_output_2:
                    final_answer = raw_output_2.split("Final Answer:")[-1].strip()
                    print(f"✅ Found 'Final Answer:' manually: {final_answer}")
                else:
                    print("❌ No 'Final Answer:' found in output")

    except Exception as e:
        print(f"❌ Failed to parse first output: {e}")


def simple_manual_agent():
    """A simplified version that manually handles the ReAct loop"""
    print("\n" + "=" * 50)
    print("MANUAL REACT IMPLEMENTATION")
    print("=" * 50)

    tools = [get_text_length]

    # Simpler template
    template = """You are a helpful assistant that can use tools. 

Available tools:
- get_text_length: Returns the length of a text by characters

Question: {input}

Think step by step and use this format:
Thought: [your reasoning]
Action: [tool name]
Action Input: [input for the tool]

OR if you have the answer:
Thought: [your reasoning]
Final Answer: [the final answer]

{history}

Thought:"""

    llm = OllamaLLM(temperature=0, model="llama3")

    input_question = "What is the length of the word DOG?"
    history = ""

    for i in range(3):  # Max 3 iterations
        print(f"\n--- Iteration {i+1} ---")

        prompt_text = template.format(input=input_question, history=history)
        print(f"Prompt:\n{prompt_text}")

        response = llm.invoke(prompt_text)
        print(f"LLM Response:\n{response}")

        # Simple parsing
        if "Final Answer:" in response:
            final_answer = response.split("Final Answer:")[-1].strip()
            print(f"🎉 Found final answer: {final_answer}")
            break

        elif "Action:" in response and "Action Input:" in response:
            # Extract action and input
            lines = response.split("\n")
            action = None
            action_input = None

            for line in lines:
                if line.startswith("Action:"):
                    action = line.replace("Action:", "").strip()
                elif line.startswith("Action Input:"):
                    action_input = line.replace("Action Input:", "").strip()

            if action and action_input:
                print(f"Action: {action}, Input: {action_input}")

                if action == "get_text_length":
                    result = get_text_length.func(action_input)
                    print(f"Tool result: {result}")

                    # Add to history
                    history += f"\nThought: {response}"
                    history += f"\nAction: {action}"
                    history += f"\nAction Input: {action_input}"
                    history += f"\nObservation: {result}"

        else:
            print("❌ Could not parse response properly")
            break


if __name__ == "__main__":
    print("DEBUGGING REACT AGENT")
    print("=" * 30)

    # First try the detailed debugging
    debug_agent_step_by_step()

    # Then try the manual version
    simple_manual_agent()

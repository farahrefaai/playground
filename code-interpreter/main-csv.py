from langchain_experimental.agents.agent_toolkits import create_csv_agent

from langchain_ollama import OllamaLLM

def main():
    csv_agent = create_csv_agent(
        llm=OllamaLLM(temperature=0, model="llama3"),
        path="episode_info.csv",
        verbose=True,
        allow_dangerous_code=True
    )

    # csv_agent.invoke(
    #     input={"input": "how many columns are there in file episode_info.csv"}
    # )
    csv_agent.invoke(
        input={
            "input": "which season has the most episodes?"
        }
    )


if __name__ == "__main__":
    print("Start...")
    main()
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


# Load environment variables from a .env file
# not needed now, but useful for future development
load_dotenv()



def main():
    print("Hello from hello-world-langchain!")
    llm = OllamaLLM(model="llama3")
    response = llm("What is the capital of Lebanon?")
    print("Response from Ollama LLM:", response)


if __name__ == "__main__":
    main()

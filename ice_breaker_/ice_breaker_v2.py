from langchain_core.prompts import PromptTemplate
# this is a paid model, to get quota, I need to pay
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

# NOTE let the llm work on scraped data you provide on runtime.


if __name__ == "__main__":
    print("Hello LangChain!")

    # this means the information is gonna change
    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)
    llm = ChatOllama(temperature=0,model = "llama3")
    chain = summary_prompt_template | llm | StrOutputParser()

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/farah-refaai-95588a15b/")

    res = chain.invoke(input={"information":linkedin_data})

    print(res)


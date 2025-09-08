from langchain_core.prompts import PromptTemplate
# this is a paid model, to get quota, I need to pay
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

#NOTE create an Agent that has linkedin tool and give the llm this tool in order to utilize it

def ice_break_with(name:str) -> str:
    # NOTE get linkedin info
    linkedin_url = linkedin_lookup_agent(name= name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    # NOTE summerize the info that I have in the way I want
    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)

    llm = ChatOllama(temperature=0,model = "llama3")

    chain = summary_prompt_template | llm 

    res = chain.invoke(input={"information":linkedin_data})

    print(res)


if __name__ == "__main__":
    print("Ice Breaker Enter")
    ice_break_with(name="Farah Refaai")

    

    


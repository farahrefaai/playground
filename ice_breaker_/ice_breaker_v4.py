from langchain_core.prompts import PromptTemplate
# this is a paid model, to get quota, I need to pay
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from output_parsers import summary_parser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

#NOTE v3 + using pydantic parser

def ice_break_with(name:str) -> str:
    # NOTE get linkedin info
    linkedin_url = linkedin_lookup_agent(name= name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    # NOTE summerize the info that I have in the way I want
    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], 
                                             template = summary_template,
                                             # NOTE setting the format
                                             partial_variables={"format_instructions":summary_parser.get_format_instructions()})

    llm = ChatOllama(temperature=0,model = "llama3")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information":linkedin_data})

    print(res)


if __name__ == "__main__":
    print("Ice Breaker Enter")
    ice_break_with(name="Farah Refaai")

    

    


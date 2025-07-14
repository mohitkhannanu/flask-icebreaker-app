# the main file for the project
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
#from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> tuple[Summary, str]: 
    linkedin_username = linkedin_lookup_agent(name=name)  # look up agent to get the URL
    print(linkedin_username)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username
    )  # scraping the URL linked page using third party tools
    summary_template = """
    given the Linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    #chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser #LCEL - LangChain Expression Language
    res:Summary = chain.invoke(input={"information": linkedin_data})  # passing the scraped linkedin data to the chain
    return res, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    load_dotenv()
    print("Entering the Icebreaker")
    ice_break_with("Mohit Khanna Mastercard")

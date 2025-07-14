# this is the tool for lookup agent, essentially it calls tavily search to scrape the internet/google
# and get the URL based on the serach string
from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """searches for linkedin page"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res

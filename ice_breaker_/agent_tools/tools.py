from langchain_tavily import TavilySearch

def get_profile_url_tavily(search_query: str):
    """
    Searches for linkedin or Twitter Profile pages.
    """

    search = TavilySearch()
    res = search.run(f"{search_query}")

    return res



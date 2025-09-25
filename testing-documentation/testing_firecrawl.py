from firecrawl import Firecrawl
import os
from dotenv import load_dotenv

load_dotenv()


firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Scrape a website:
doc = firecrawl.search(query="what is the price of gold now")
print(doc)

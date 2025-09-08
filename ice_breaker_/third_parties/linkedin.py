# using https://app.scrapin.io/ scaper to get linked info

import os
import requests

from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from linkedin profiles,
    manually scrape the information from the linkedin profiles
    """
    
    if mock:
        # inorder to not consume all scrapin credits, we saved a json file in gist and we ready to debug using it
        linkedin_profile_url = "https://gist.githubusercontent.com/farahrefaai/506118f791ad3b9804d38d1c9cbc906b/raw/27ffc3c18cdd20a2cb0ec0edc3fb91aa29c4144a/farah-alrefaai-srapin.json"

        response = requests.get(linkedin_profile_url, timeout=10)

    else:
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"

        params = {
            "apikey":os.environ["SCRAPI_API_KEY"],
            "linkedInUrl":linkedin_profile_url
        }

        response = requests.get(
            api_endpoint,
            params= params,
            timeout= 10
        )

    data = response.json().get("person")

    data = {
        k:v for k,v in data.items() if v not in ([],"", None)
        and k not in ["certifications"]
    }

    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/farah-refaai-95588a15b/", mock=True))
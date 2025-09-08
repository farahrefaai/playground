from agents import linkedin_lookup_agent

if __name__ == "__main__":
    linkedin_url = linkedin_lookup_agent.lookup(name="Farah Refaai")
    print(linkedin_url)
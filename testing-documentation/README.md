# LangChain Documentation Helper


```
pipenv --python 3.13
pipenv shell
```

# flow

## Ingestion (PART 1) -> RAG

first part of our RAG pipeline is to ingest the LangChain documentation, and index in into our vector store
using Tavily (or any other source). we are going to do:
- take the latest documentation
- map all urls
- scrape the urls

then we are going to add some metadata and index everything to our vectorestore

Since my account on Tavily doesn't work well, am going to use firecrawl. 
firecrawl.

I've noticed that firecrawl langchain integration is not working properly, so am not going to use the integration, will use firecrawl directly.

Since am getting a lot of credit issues, and I don't wanna pay, ill mock the firecrawl and use it.



## Crawling
Web crawling is the process where a search engine's software (a "crawler") automatically and endlessly explores the web by following links from page to page, collecting information about what's on each page to build a massive, searchable index.

Crawling its mapping (returns a list of all urls found) + extracting the content of each URL.

after mapping, we extract in batching using coroutines not in sequence. However, we wanna wait for all batches to finish and then do the work on them once.

The Tavily extract API supports batch processing as well

## Mocking the crawler

since am facing issues with Tavily, Exa, and Firecrawl, I decided to create a mock for Firecrawl and use it.



---

## FLOWs
Load -> split -> embed -> store

Source -> Load (in our case into langchain documents) -> Transform (from source structure to langchain structure) -> Split -> Embed -> Store -> Retieve

#### the hardest stage is to get the data for the system.

#### its important to use coroutines with these heavy tasks


## LLM CHUNKING STRATEGIES
1- Fixed-size chunking

2- sliding window approach

3- Recursively divide text

## NOTES
### try to use the size that avoid you hitting the rate limits

### the embedding function can't be reversed, the voctorstore stores both the text and the vector because of this. from the vector we can't know the original text.

### After the ingestion is done, now its the time to implement RAG 

## Retrieval, Augmentation, and generation (PART 2)

### in core.py we do:
write the implementation of retrieval augmentation

1- get the question and turn it into a vector

2- get the relevant documents to that question

3- augment the prompt with the needed context and send it to the llm


## create_retrieval_chain
performes the retrieval process, it has two arguments

1- the retriever (vector store) that retrieves the relevant vectors

2- the docs chain, takes the retrieved docs and run the question with the retrieved docs to the llm


## create_stuff_documents_chain
performes the augmentation, recieves the prompt and the context and send everything to the llm
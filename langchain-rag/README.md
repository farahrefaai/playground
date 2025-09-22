Introduction to vector databases

- embeddings
- vector stores (Pinecone)
- RetrievalQA Chain
- LangChain document loaders
- LangChain text splitters

## LangChain document loaders

langchain helps interacting with a lot of 3rd parties

langchain has a wrappers around the third parties that make it easy
to connect and retrieve data that we can process

this data comes in the form of Documents. and a Document holds a text and other important metadata (ex source).

so we're going to load the data as documents, and send them to llm


## LangChain text splitters
when we want to deal with long pieces of text, its necessary to split it up to chunks

## embeddings
the idea is to create a vector space from the text, such that the distance between the vectors
in the space have a certain meaning

a vector can represent a word, a sentence, a paragraph, audio, image, or an entire document

Embedding Model takes objects and do some magic, and then return the vector representation of the objects

in good embedding models (encoder), text with similar semantic meaning, will be represented 
by vectors that are close to each other in the vector space. (we can check this by the distance between the vectors)

in RAG, we send the Query (user input) with the Context to the embedding model

## Prompt Augmentation
the llm is not trained on a specific data, however, using the context, the llm is able to find the answer.
its like saying, use these information to answer the question

the neighbors in the vector space are the context

## FLOW

Problem: we wanna search in a very very large book

Solution:
1. split the book into chunks
2. create embeddings for each chunk
3. store the embeddings in a vector database (ex: pinecone)
4. when a user asks a question, create an embedding for the question
5. search the vector database for the most similar embeddings to the question embedding
6. get the closest chunks of text
7. the context is ready
8. send the query and the context to the llm to get the answer



load -> split -> embed -> store

for splitting, we have to determine the chunk size and the chunk overlap. the overlap ensures that the split doesn't disturb the context meaning

### the rule of thumb when chunking is to keep the chunk size small enough so:
    1- it would fit in the context window, and the context window usually is going to be holding a couple of chunks, 
    2- it should be big enough so if we would read it as a human beings, we would know what this chunk means and it has a value and semantic meaning. ELSE it wont help the llm give us the answer we want

### 2nd rule of thumb: garbage in, garbage out

    overlaping data is not useful when we dont want to use context between chuncks.

## RAG flow

    Ingestion -> Retrieval
    ingestion part is to populate our database. It is the first part of the RAG

    Second part is Retrieval. It is taking the user's question, embedding it, turn it into a vector. Then using the vector store to find those relevant vectors which are relevant documents and this is the relevant context. Then taking the original question, augmenting it with the chunks and then sending everything to the LLM to get back the answer we want when its grounded with the relevant context.


## NOTE: Everything in Gen AI application development revolves around a prompt.
# in this file we are going to take a medium article
# loadi it, split it into chuncks, embed every chunk
# and store the vectors in the vectordb

import os
from dotenv import load_dotenv
# we have a lot of loaders: facebook, whatsapp, huggingface, etc
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone.vectorstores import Pinecone, PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
load_dotenv()


if __name__ == "__main__":

    loader = TextLoader("mediumblog1.txt")
    # from metadata, we can tell the source of info we got
    document = loader.load()

    print("splitting")
  
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    texts  = text_splitter.split_documents(document)

    print(f"created {len(texts)} chunks")

    embeddings = OllamaEmbeddings(model="all-minilm")

    print("ingesting")

    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.getenv("INDEX_NAME"))

    print("finish")
    


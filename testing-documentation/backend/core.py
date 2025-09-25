'''write the implementation of retrieval augmentation
1- get the question and turn it into a vector
2- get the relevant documents to that question
3- augment the prompt with the needed context and send it to the llm

'''


import os
from dotenv import load_dotenv
from langchain import hub
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from typing import List, Dict, Any

INDEX_NAME = "langchain-doc-index"
load_dotenv()


def run_llm(query:str, chat_history:List[Dict[str,Any]]):
    embedding = OllamaEmbeddings(model = "all-minilm")

    # the retrieval to get the relevant documents
    # similarity search
    docsearch = Chroma(persist_directory="chroma_db", embedding_function=embedding)

    chat = OllamaLLM(model="llama3", temperature=1)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_document_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(llm = chat, retriever=docsearch.as_retriever(), prompt = rephrase_prompt)


    retrieval_chain = create_retrieval_chain(history_aware_retriever, stuff_document_chain)

    result = retrieval_chain.invoke(input = {"input":query, "chat_history":chat_history})

    # this is for steamlit
    new_result = {
        "query": result['input'],
        "result": result['answer'],
        "source_documents": result['context']
    }
    print(new_result)
    return new_result





if __name__ == "__main__":
    res = run_llm(query = "What is a Langchain?")

    print(res['result'])


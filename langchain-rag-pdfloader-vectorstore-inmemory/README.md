pipenv is used

in this repo, a pdf loader and a local vector store were used.


PyPDFLoader helps us load pdf documments

Local Vectorstore (FAISS) -- released by meta

## RetrievalQA chain
The prompt and the llm are handled by the create_stuff_document_chain
The retreiving embeddings and calling the create_stuff_document_chain is handled by create_retrieval_chain

While invoking, create_stuff_document_chain is constant, and create_retrieval_chain is changing the input.
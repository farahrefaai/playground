from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub


load_dotenv()

if __name__ == "__main__":
    print("hello")

    pdf_path = "reAct-paper.pdf"

    loader = PyPDFLoader(file_path=pdf_path)

    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap =30, separator="\n" )
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OllamaEmbeddings(model ="llama3")
    vectorestore = FAISS.from_documents(documents = docs,embedding=embeddings)

    vectorestore.save_local("faiss_index_react")

    new_vectorstore = FAISS.load_local("faiss_index_react", embeddings, allow_dangerous_deserialization=True)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(OllamaLLM(model = "llama3"), retrieval_qa_chat_prompt)

    retreival_chain = create_retrieval_chain(new_vectorstore.as_retriever(), combine_docs_chain)

    res = retreival_chain.invoke({"input":"give me the gist of reAct in 3 sentences"})

    print(res)

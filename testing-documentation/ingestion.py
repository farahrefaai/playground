from dotenv import load_dotenv
import asyncio
import os
import ssl
from typing import List
import certifi

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # incase we wanna use the local db
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from firecrawl import Firecrawl

from firecrawlMock import FireCrawlMock, Document as CrawlDocument, CrawlJob
from mapper import FirecrawlMapper

from logger import (
    Colors,
    log_error,
    log_warning,
    log_info,
    log_header,
    log_success,
)

load_dotenv()

# NOTE --- this is for requesting the Tavily APIs
# Configure SSL context to use certifi certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# NOTE --- this embeddings doesn't accept chunk_size and retry_min_seconds
embeddings = OllamaEmbeddings(model="all-minilm")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# NOTE --- since I've reached the credits, I created a mock class
# firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
firecrawl = FireCrawlMock(api_key=os.getenv("FIRECRAWL_API_KEY"))

async def index_documents_async(documents: List[Document], batch_size: int = 50):
    """Process documents in batches asynchronously"""
    log_header("VECTOR STORAGE STAGE")
    log_info(f" VectorStore Indexing: Preparing to add {len(documents)} documents to vectorstore", Colors.DARKCYAN)

    # Create batches
    batches = [
        documents[i: i+batch_size] for i in range(0, len(documents), batch_size)]

    log_info(f" VectorStore Indexing: Split into {len(batches)} batches of {batch_size} documents each", Colors.DARKCYAN)

    # Process all batches concurrently
    async def add_batch(batch: List[Document], batch_num:int):
        try:
            await vectorstore.aadd_documents(batch)
            log_success(f"VectorStore Indexing: Successfully added {batch_num}/{len(batch)} documents to vectorstore")
        except Exception as e:
            log_error(f"Failed to add {batch_num}/{len(batch)} documents to vectorstore -- {e}")
            return False
        return  True

    # Process batches concurrently
    # creating for each batch a coroutine
    tasks = [add_batch(batch, i+1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Count Successful batches
    successful = sum(1 for result in results if result is True)

    if successful == len(batches):
        log_success(f"VectorStore Indexing: Successfully added {successful}/{len(batches)} documents to vectorstore")
    else:
        log_warning(f"VectorStore Indexing: Processed {successful}/{len(batches)} documents to vectorstore")



async def main():
    """Main async function to orchestrate the entire process"""
    url = "https://python.langchain.com"

    log_header("DOCUMENTATION INGESTION PIPELINE")
    log_info(f"Firecrawl: Starting to Crawl documentation from {url}", Colors.PURPLE)

    # are we able to send instructions to decide to crawl a page or not?
    # with tavily, when sending instructions, we can increase the max_depth

    # ------- Source and Load Parts
    firecrawl_crawl_job :CrawlJob = firecrawl.crawl(
        url="https://python.langchain.com", max_discovery_depth=1, limit=1
    )
    print(f"all done and this is the extracted firecrawl {firecrawl_crawl_job}")

    crawled_documents: List[CrawlDocument] = [
        Document(
            page_content=result.markdown,
            metadata={"source": result.metadata.url},
        )
        for result in firecrawl_crawl_job.data
    ]

    log_success(f"Firecrawl: Finished Crawling documentation from {url} -- {crawled_documents}")


    # ------- Transform Part
    firecrawl_mapper :FirecrawlMapper = FirecrawlMapper()
    langchain_documents = firecrawl_mapper.firecrawl_document_to_langchain_documents(crawled_documents)

    log_success(f"DATA IS TRANSFORMED: {len(langchain_documents)}")

    # ------- SPLITTING PART -- split documents into chunks
    log_header("DOCUMENTATION CHUNKING PHASE")
    log_info(f"Text Splitter: Processing {len(langchain_documents)} documents with 4000 chunk size and 200 overlap", Colors.YELLOW)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    splitted_docs = text_splitter.split_documents(langchain_documents)

    log_success(f"TEXT SPLITTER: Created {len(splitted_docs)} chunks from {len(langchain_documents)} documents")

    #Process documents asynchronously
    await index_documents_async(splitted_docs, batch_size=500)

    log_header("PIPELINE COMPLETE")
    log_success(f" Documentation ingestion pipeline finished successfully!")
    log_info(f" Summary:",Colors.BOLD)
    log_info(f"    - URLS mapped: {len(firecrawl_crawl_job.data)}")
    log_info(f"    - Chunks created: {len(splitted_docs)}")



if __name__ == "__main__":
    print("Welcome to Ingestion!")
    asyncio.run(main())

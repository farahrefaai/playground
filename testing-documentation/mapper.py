from firecrawl.v2.types import Document as firecrawlDocument
from langchain_core.documents import Document as langchainDocument
from typing import List

class FirecrawlMapper:
    def firecrawl_document_to_langchain_documents(self, firecrawl_document : List[firecrawlDocument]) -> List[langchainDocument]:
        langchain_documents: list[langchainDocument] = []
        for doc in firecrawl_document:
            langchain_documents.append(langchainDocument(
                metadata=doc.metadata,
                page_content = doc.page_content,
            ))

        return langchain_documents
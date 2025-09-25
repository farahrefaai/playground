from langchain_community.document_loaders.firecrawl import FireCrawlLoader

import os
from typing import List, Literal
from firecrawl.v2.types import CrawlJob, Document, DocumentMetadata

class FireCrawlMock:
    def __init__(self, api_key):
        self.api_key = api_key

    def crawl(self,url: str, max_discovery_depth: int, limit: int) -> CrawlJob:
        """
        Mock function that returns a list of CrawlJob
        the list contains a static data related to langchain documents
        """

        # Create a list of 5 CrawlJob elements simulating LangChain document crawling
        crawl_job = CrawlJob(
            status="completed",
            data=[
                Document(
                    metadata=DocumentMetadata(
                        url= "https://python.langchain.com/docs/get_started/quickstart",
                        title= "Quickstart | LangChain",
                        description= "Get started with LangChain in Python - build your first application",
                        keywords= [
                            "langchain",
                            "quickstart",
                            "python",
                            "llm",
                            "getting started",
                        ],
        ),
                    markdown="""# Quickstart

        Welcome to LangChain! This guide will help you get started with building your first LangChain application.

        ## Installation

        First, install LangChain:

        ```bash
        pip install langchain langchain-openai
        ```

        ## Your First Chain

        Let's create a simple chain that uses OpenAI's GPT model:

        ```python
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate

        llm = ChatOpenAI()
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])

        chain = prompt | llm
        result = chain.invoke({"input": "What is LangChain?"})
        print(result.content)
        ```

        ## Next Steps

        Now that you have your first chain running, explore:
        - **Prompt Templates**: Create reusable prompts
        - **Output Parsers**: Structure your model outputs
        - **Retrieval**: Add external data to your applications.
        
         A LangChain chain is a fundamental workflow that links modular components, such as language models (LLMs), prompt templates, data sources, or external tools, to automate multi-step tasks. Chains work by passing the output of one component as the input to the next in a sequence, creating a streamlined, context-aware pipeline. This allows developers to build sophisticated applications that go beyond simple LLM interactions by integrating various functionalities into a single, organized workflow. 
        """,
                ),
                Document(metadata=DocumentMetadata(
                    url="https://python.langchain.com/docs/modules/agents",

                        title= "Agents | LangChain",
                        description= "Learn how to build intelligent agents with LangChain that can use tools and reason about actions",
                        keywords=[
                            "langchain",
                            "agents",
                            "tools",
                            "reasoning",
                            "autonomous",
                        ]
                ),
                    markdown="""# Agents

        Agents are systems that use language models to determine which actions to take and in what order.

        ## Core Concepts

        An agent consists of:
        - **Agent**: The language model that decides what actions to take
        - **Tools**: Functions the agent can call
        - **AgentExecutor**: The runtime that calls the agent and executes actions

        ## Building Your First Agent

        ```python
        from langchain import hub
        from langchain.agents import AgentExecutor, create_openai_tools_agent
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langchain_openai import ChatOpenAI

        # Initialize tools
        search = TavilySearchResults(max_results=2)
        tools = [search]

        # Get the prompt
        prompt = hub.pull("hwchase17/openai-tools-agent")

        # Choose the LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # Construct the OpenAI Tools agent
        agent = create_openai_tools_agent(llm, tools, prompt)

        # Create an agent executor
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        ```

        ## Agent Types

        LangChain supports various agent types:
        - **OpenAI Tools Agent**: Uses OpenAI's function calling
        - **ReAct Agent**: Reasoning and acting in language models
        - **Self-ask with search**: Breaks down complex questions
        """,
                ),
                Document(metadata=DocumentMetadata(
                    url="https://python.langchain.com/docs/modules/data_connection/vectorstores",
                        title= "Vector Stores | LangChain",
                        description= "Store and search over unstructured data using vector embeddings in LangChain",
                        keywords= [
                            "langchain",
                            "vector stores",
                            "embeddings",
                            "similarity search",
                            "retrieval",
                        ]
                ),
                    markdown="""# Vector Stores

        Vector stores are databases that can store and search over unstructured data by converting it into embeddings.

        ## What are Vector Stores?

        Vector stores allow you to:
        - Store documents as vector embeddings
        - Perform similarity searches
        - Retrieve relevant documents based on semantic similarity

        ## Popular Vector Store Integrations

        LangChain integrates with many vector stores:
        - **Chroma**: Open-source embedding database
        - **Pinecone**: Managed vector database
        - **Weaviate**: Open-source vector search engine
        - **FAISS**: Facebook AI Similarity Search

        ## Basic Usage Example

        ```python
        from langchain_community.document_loaders import TextLoader
        from langchain_openai import OpenAIEmbeddings
        from langchain_text_splitters import CharacterTextSplitter
        from langchain_community.vectorstores import Chroma

        # Load documents
        loader = TextLoader("state_of_the_union.txt")
        documents = loader.load()

        # Split documents
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # Create embeddings
        embeddings = OpenAIEmbeddings()

        # Create vector store
        db = Chroma.from_documents(docs, embeddings)

        # Search
        query = "What did the president say about Ketanji Brown Jackson"
        docs = db.similarity_search(query)
        print(docs[0].page_content)
        ```
        """,
                ),
                Document(metadata=DocumentMetadata(
                    url="https://python.langchain.com/docs/modules/chains",
                        title= "Chains | LangChain",
                        description= "Combine multiple components together to create cohesive applications with LangChain chains",
                        keywords= [
                            "langchain",
                            "chains",
                            "components",
                            "llm",
                            "prompts",
                            "sequential",
                        ]
                ),
                    markdown="""# Chains

        Chains allow you to combine multiple components together to create a cohesive application.

        ## LCEL (LangChain Expression Language)

        The most important method for building chains is using LangChain Expression Language (LCEL):

        ```python
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
        model = ChatOpenAI()
        output_parser = StrOutputParser()

        chain = prompt | model | output_parser

        chain.invoke({"topic": "ice cream"})
        ```

        ## Chain Types

        ### Sequential Chains
        Run multiple chains in sequence:

        ```python
        from langchain.chains import LLMChain, SequentialChain

        # First chain
        first_prompt = ChatPromptTemplate.from_template("What is the capital of {country}?")
        first_chain = LLMChain(llm=llm, prompt=first_prompt, output_key="capital")

        # Second chain
        second_prompt = ChatPromptTemplate.from_template("What is the population of {capital}?")
        second_chain = LLMChain(llm=llm, prompt=second_prompt, output_key="population")

        # Combine chains
        overall_chain = SequentialChain(
            chains=[first_chain, second_chain],
            input_variables=["country"],
            output_variables=["capital", "population"]
        )
        ```

        ### Router Chains
        Route inputs to different sub-chains based on content.
        """,
                ),
                Document(metadata=DocumentMetadata(
                    url="https://python.langchain.com/docs/modules/memory",
                        title= "Memory | LangChain",
                        description= "Add state and memory to your LangChain applications for context-aware conversations",
                        keywords= [
                            "langchain",
                            "memory",
                            "conversation",
                            "state",
                            "context",
                            "chat history",
                        ]
                ),
                    markdown="""# Memory

        Memory gives a language model the ability to remember previous interactions in a conversation.

        ## Types of Memory

        LangChain provides several memory implementations:

        ### ConversationBufferMemory
        Stores the entire conversation history:

        ```python
        from langchain.memory import ConversationBufferMemory
        from langchain_openai import ChatOpenAI
        from langchain.chains import ConversationChain

        llm = ChatOpenAI(temperature=0)
        memory = ConversationBufferMemory()
        conversation = ConversationChain(
            llm=llm, 
            memory=memory, 
            verbose=True
        )

        conversation.predict(input="Hi there!")
        conversation.predict(input="What's my name?")
        ```

        ### ConversationBufferWindowMemory
        Only keeps a sliding window of recent interactions:

        ```python
        from langchain.memory import ConversationBufferWindowMemory

        memory = ConversationBufferWindowMemory(k=2)  # Keep last 2 interactions
        ```

        ### ConversationSummaryMemory
        Summarizes the conversation over time:

        ```python
        from langchain.memory import ConversationSummaryMemory

        memory = ConversationSummaryMemory(llm=llm)
        ```

        ## Using Memory with LCEL

        ```python
        from langchain_core.runnables.history import RunnableWithMessageHistory
        from langchain_community.chat_message_histories import ChatMessageHistory

        store = {}

        def get_session_history(session_id: str) -> ChatMessageHistory:
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        with_message_history = RunnableWithMessageHistory(chain, get_session_history)
        ```
        """,
                ),
            ],
        )

        return crawl_job

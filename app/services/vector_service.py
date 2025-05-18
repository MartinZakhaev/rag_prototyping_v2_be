import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME", "rag-virtual-assistant")

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  # Dimension for Gemini embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Initialize vector store
vector_store = PineconeVectorStore(
    index=pc.Index(index_name),
    embedding=embeddings,
    text_key="text"
)

async def add_documents_to_vector_store(documents, document_id):
    """Add document chunks to the vector store"""
    # Add metadata to each document
    for doc in documents:
        doc.metadata["document_id"] = document_id
    
    # Add documents to vector store
    vector_store.add_documents(documents)
    
    return {"status": "success"}

async def query_vector_store(query, top_k=5):
    """Query the vector store for relevant documents"""
    results = vector_store.similarity_search(query, k=top_k)
    return results
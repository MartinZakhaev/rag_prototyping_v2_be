import os
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.vector_service import query_vector_store, vector_store
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

async def get_rag_response(query):
    """Get a response using RAG (Retrieval Augmented Generation)"""
    # Query vector store for relevant documents
    context_docs = await query_vector_store(query)
    
    # Extract text from documents to use as context
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    # Create a prompt with the context and query
    prompt = f"""
    Kamu adalah asisten virtual yang membantu menjawab pertanyaan berdasarkan dokumen yang diberikan.
    Gunakan konteks berikut untuk menjawab pertanyaan pengguna.
    Jika jawabannya tidak ada dalam konteks, katakan bahwa kamu tidak tahu jawabannya.
    Selalu berikan jawaban dalam Bahasa Indonesia.
    
    Konteks:
    {context}
    
    Pertanyaan: {query}
    
    Jawaban:
    """
    
    # Get response from LLM
    response = llm.invoke(prompt)
    
    return response.content
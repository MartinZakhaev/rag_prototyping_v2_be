from fastapi import UploadFile
import os
import uuid
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.vector_service import add_documents_to_vector_store

async def process_document(file: UploadFile):
    """Process an uploaded document and add it to the vector store"""
    # Generate a unique ID for the document
    document_id = str(uuid.uuid4())
    
    # Create a temporary file to save the upload
    file_extension = os.path.splitext(file.filename)[1].lower()
    temp_file_path = f"temp_{document_id}{file_extension}"
    
    try:
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Load document based on file type
        if file_extension == ".pdf":
            loader = PyPDFLoader(temp_file_path)
        elif file_extension in [".docx", ".doc"]:
            loader = Docx2txtLoader(temp_file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Add document chunks to vector store
        await add_documents_to_vector_store(splits, document_id)
        
        return {"document_id": document_id}
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
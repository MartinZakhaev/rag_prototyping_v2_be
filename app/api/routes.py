from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
import io

from app.services.document_service import process_document
from app.services.rag_service import get_rag_response
from app.services.tts_service import text_to_speech

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document for the knowledge base"""
    try:
        result = await process_document(file)
        return {"message": "Document processed successfully", "document_id": result["document_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat(message: str = Form(...), voice_response: bool = Form(False)):
    """Process a text chat message and return a response"""
    try:
        # Get response from RAG system
        response = await get_rag_response(message)
        
        # If voice response is requested, convert text to speech
        if voice_response:
            audio_content = await text_to_speech(response)
            return {
                "text": response,
                "audio": audio_content
            }
        
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice")
async def voice_chat(audio: UploadFile = File(...)):
    """Process a voice message, convert to text, get response, and return text and audio"""
    try:
        # Here you would implement speech-to-text
        # For now, we'll assume the text is extracted from the audio
        message = "Extracted text from audio"  # Placeholder
        
        # Get response from RAG system
        response = await get_rag_response(message)
        
        # Convert response to speech
        audio_content = await text_to_speech(response)
        
        return {
            "text": response,
            "audio": audio_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audio/{response_id}")
async def get_audio(response_id: str):
    """Stream audio response"""
    try:
        # Retrieve audio content (implementation depends on how you store it)
        audio_content = b"audio_bytes"  # Placeholder
        
        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type="audio/mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
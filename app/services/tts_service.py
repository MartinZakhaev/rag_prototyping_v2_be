import os
from google.cloud import texttospeech
from dotenv import load_dotenv
import base64

load_dotenv()

# Initialize Text-to-Speech client
client = texttospeech.TextToSpeechClient()

async def text_to_speech(text):
    """Convert text to speech using Google TTS"""
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="id-ID",  # Indonesian
        name="id-ID-Standard-A",  # Use an Indonesian voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    # Select the type of audio file
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Return the audio content as base64 encoded string
    return base64.b64encode(response.audio_content).decode("utf-8")
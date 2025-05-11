import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import numpy as np
from googletrans import Translator
from langdetect import detect

def transcribe_audio(audio_path):
    """
    Transcribe audio file to text using Google Speech Recognition
    """
    r = sr.Recognizer()
    wav_file_name = None
    
    # Convert input to wav as SpeechRecognition works better with wav
    try:
        sound = AudioSegment.from_file(audio_path)
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        wav_file_name = wav_file.name
        sound.export(wav_file_name, format="wav")
        
        with sr.AudioFile(wav_file_name) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)  # Uses Google's Speech Recognition API
            os.unlink(wav_file_name)  # Clean up the temporary WAV file
            return text
    except Exception as e:
        if wav_file_name and os.path.exists(wav_file_name):
            os.unlink(wav_file_name)  # Ensure cleanup in case of error
        print(f"Error in transcription: {e}")
        return None

def detect_language(text):
    """
    Detect the language of the input text
    Returns language code: 'en', 'ta', 'hi'
    """
    try:
        lang = detect(text)
        return lang
    except:
        # Default to English if detection fails
        return 'en'

def translate_text(text, source_lang, target_lang):
    """
    Translate text from source language to target language
    
    Note: For simplicity, if translation fails, we'll just return the original text
    """
    # No actual translation for this prototype - for production, connect to a translation API
    # We still detect language but skip actual translation to avoid coroutine errors
    
    # Just return the original text for now
    print(f"Would translate from {source_lang} to {target_lang}: {text}")
    return text

def save_audio_bytes(audio_data, sample_rate=48000):
    """
    Save audio data as bytes to a temporary WAV file
    
    Args:
        audio_data: NumPy array of audio data
        sample_rate: Sample rate in Hz
    
    Returns:
        Path to the saved temporary file
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_path = tmp_file.name
            
        # Convert to 16-bit audio and save
        audio_segment = AudioSegment(
            audio_data.tobytes(), 
            frame_rate=sample_rate,
            sample_width=2,  # 16-bit
            channels=1       # Mono
        )
        audio_segment.export(tmp_path, format="wav")
        
        return tmp_path
    except Exception as e:
        print(f"Error saving audio: {e}")
        return None

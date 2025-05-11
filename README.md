# Multilingual Medical Assistant

A Streamlit-based web application that acts as a multilingual medical assistant, capable of:
- Accepting voice input in English, Tamil, and Hindi
- Automatically detecting the language of input
- Translating non-English inputs to English for processing
- Providing basic medical diagnoses through a rule-based system
- Responding with voice output in the user's input language

## Features

- Voice input system for symptom description
- Support for multiple languages (English, Tamil, Hindi)
- Automatic language detection
- Translation pipeline for non-English inputs
- Rule-based symptom analysis and diagnosis
- Text-to-speech output in the user's language

## Technical Details

This application is built using:
- **Streamlit**: Web application framework
- **SpeechRecognition**: For capturing voice input
- **Pydub**: For audio processing
- **gTTS (Google Text-to-Speech)**: For voice output
- **Googletrans**: For language translation
- **Langdetect**: For language detection

## Usage

1. Select your preferred language (English, Tamil, or Hindi)
2. Click the record button and describe your symptoms by voice
3. Wait for the system to process your input
4. View the detected symptoms and diagnosis
5. Listen to the voice response or download the audio file

## Disclaimer

This application is for educational purposes only. Always consult with a qualified healthcare professional for medical advice, diagnosis, or treatment.

## Running the Application


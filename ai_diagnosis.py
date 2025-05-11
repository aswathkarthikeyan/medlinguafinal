"""
AI-powered diagnosis engine for the medical assistant application.
This module provides more advanced diagnosis capabilities using OpenAI's GPT model.
"""

import os
import json
from openai import OpenAI
from symptoms_db import common_symptoms

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
DEFAULT_MODEL = "gpt-4o"

# Initialize the OpenAI client
def get_openai_client():
    """Get an initialized OpenAI client if API key is available"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def get_ai_diagnosis(symptoms, transcript, openai_client=None):
    """
    Get an AI-powered diagnosis based on symptoms and transcript
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description of their symptoms
        openai_client: Optional OpenAI client instance
        
    Returns:
        str: AI-generated diagnosis or None if AI not available
    """
    if not openai_client:
        openai_client = get_openai_client()
        
    if not openai_client:
        return None
        
    # Format the symptoms with descriptions for more context
    symptom_descriptions = []
    for symptom in symptoms:
        if symptom in common_symptoms:
            symptom_descriptions.append(f"- {symptom}: {common_symptoms[symptom]}")
    
    symptoms_text = "\n".join(symptom_descriptions)
    
    system_message = """You are a medical assistant AI that provides basic health information and suggestions.
    Your task is to analyze the patient's symptoms and provide a thoughtful, informative response.
    
    Important guidelines:
    1. Do NOT make definitive diagnoses or claim medical authority
    2. Always encourage consulting a healthcare professional for proper diagnosis and treatment
    3. Provide general information about possible causes of symptoms
    4. Suggest basic self-care measures when appropriate
    5. Mention when symptoms might require urgent medical attention
    6. Be compassionate and informative
    7. If symptoms suggest a serious condition, emphasize the importance of immediate medical care
    8. Recognize patterns across multiple symptoms
    9. Consider both common and concerning possible causes
    10. Keep your response concise but thorough (under 250 words)
    """
    
    user_message = f"""Patient's description: "{transcript}"
    
    Detected symptoms:
    {symptoms_text}
    
    Based on these symptoms, please provide:
    1. A brief assessment of possible causes
    2. General information about these symptoms
    3. Basic self-care recommendations, if appropriate
    4. When the patient should seek professional medical care
    """
    
    try:
        response = openai_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=700,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI diagnosis: {e}")
        return None
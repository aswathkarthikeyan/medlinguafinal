from symptoms_db import common_symptoms
from free_ai_diagnosis import get_free_api_diagnosis
from advanced_diagnosis import advanced_diagnose_symptoms
from huggingface_lite import detect_symptoms_multilingual, get_diagnosis_multilingual, get_model_info
from utils import detect_language
from symptom_condition_map import generate_specific_diagnosis
from web_search_emulation import perform_web_search
import re

def diagnose_symptoms(transcript, lang=None):
    """
    Analyze the transcript to identify symptoms and provide a comprehensive diagnosis
    using enhanced multi-layered approach with specific condition mapping and web search emulation
    
    Args:
        transcript: The patient's description of their symptoms
        lang: Language code (en, ta, hi) - if None, language will be detected
        
    Returns:
        tuple: (detected_symptoms, diagnosis_text)
    """
    # If language not specified, detect it
    if not lang:
        lang = detect_language(transcript)
    
    # Use our Hugging Face model for multilingual symptom detection first
    try:
        # First try with Hugging Face multilingual model
        huggingface_symptoms = detect_symptoms_multilingual(transcript, lang)
        
        # Combine with our traditional symptom detection for better coverage
        traditional_symptoms = []
        try:
            # Use our comprehensive symptom detection
            traditional_symptoms, _, _ = advanced_diagnose_symptoms(transcript, lang)
        except Exception as e:
            print(f"Error in traditional symptom detection: {e}")
        
        # Combine symptoms from both approaches
        all_symptoms = list(set(huggingface_symptoms + traditional_symptoms))
        
        # STEP 1: Try specific condition diagnosis first (most accurate)
        if all_symptoms:
            specific_diagnosis, recommendations, confidence, condition = generate_specific_diagnosis(transcript, all_symptoms, lang)
            
            # If we got a specific diagnosis with good confidence, use it
            if specific_diagnosis and confidence >= 0.5:
                return all_symptoms, specific_diagnosis
        
        # STEP 2: Try Hugging Face model diagnosis
        if huggingface_symptoms:
            # Generate diagnosis using Hugging Face multilingual model
            diagnosis_text, diagnosis_info = get_diagnosis_multilingual(huggingface_symptoms, transcript, lang)
            
            # Check if the model produced a confident diagnosis
            if diagnosis_info.get("confidence", 0) >= 0.5 and diagnosis_info.get("condition"):
                return huggingface_symptoms, diagnosis_text
        
        # STEP 3: Try advanced diagnosis system
        if not all_symptoms:
            # If no symptoms detected yet, try advanced diagnosis system
            detected_symptoms, diagnosis_text, additional_info = advanced_diagnose_symptoms(transcript, lang)
            
            if detected_symptoms and additional_info.get("confidence_score", 0) > 0.5:
                return detected_symptoms, diagnosis_text
            
            # Add any newly detected symptoms
            all_symptoms = list(set(all_symptoms + detected_symptoms))
        
        # STEP 4: If we have symptoms but no confident diagnosis, try web search emulation
        if all_symptoms:
            # Simulate web search for more specific information
            search_results = perform_web_search(all_symptoms, transcript, lang)
            if search_results and search_results.get("analysis"):
                return all_symptoms, search_results["analysis"]
        
        # STEP 5: Fallback to free API diagnosis as a last resort
        try:
            if all_symptoms:
                diagnosis = get_free_api_diagnosis(all_symptoms, transcript)
                return all_symptoms, diagnosis
            else:
                # Try to get any diagnosis even with no symptoms
                simple_symptoms, diagnosis = [], get_free_api_diagnosis([], transcript)
                return simple_symptoms, diagnosis
        except Exception as e:
            print(f"Error in free API diagnosis fallback: {e}")
            if all_symptoms:
                # If we have symptoms but all diagnosis methods failed, use our basic rule-based system
                return all_symptoms, generate_diagnosis(all_symptoms)
            else:
                return [], "I couldn't identify any specific symptoms from your description. Please try again with more details about how you're feeling."
        
    except Exception as e:
        print(f"Error in main diagnosis flow: {e}")
        
        # Final fallback - extract symptoms using the simplest method and use rule-based diagnosis
        try:
            # Extract symptoms using simple keyword matching
            simple_symptoms = []
            for symptom, description in common_symptoms.items():
                clean_symptom = symptom.replace("_", " ")
                if clean_symptom in transcript.lower():
                    simple_symptoms.append(symptom)
            
            if simple_symptoms:
                # Generate diagnosis using the rule-based system
                diagnosis = generate_diagnosis(simple_symptoms)
                return simple_symptoms, diagnosis
            else:
                # Fall back to the legacy rule-based system
                return generate_legacy_diagnosis(transcript)
                
        except Exception as e2:
            print(f"Error in final fallback: {e2}")
            # Fall back to the legacy rule-based system
            return generate_legacy_diagnosis(transcript)

def generate_legacy_diagnosis(transcript):
    """
    Legacy function for extracting symptoms and generating a diagnosis
    when the advanced systems fail
    
    Args:
        transcript: The English transcript of the patient's symptoms
        
    Returns:
        tuple: (detected_symptoms, diagnosis_text)
    """
    # Basic symptom extraction
    transcript_lower = transcript.lower()
    detected_symptoms = []
    
    # Check for common symptoms in the transcript
    for symptom, description in common_symptoms.items():
        clean_symptom = symptom.replace("_", " ")
        if clean_symptom in transcript_lower:
            detected_symptoms.append(symptom)
    
    # Check for some common symptom patterns
    if "head" in transcript_lower and any(word in transcript_lower for word in ["pain", "ache", "hurt"]):
        if "headache" not in detected_symptoms:
            detected_symptoms.append("headache")
    
    if "stomach" in transcript_lower and any(word in transcript_lower for word in ["pain", "ache", "hurt"]):
        if "abdominal_pain" not in detected_symptoms:
            detected_symptoms.append("abdominal_pain")
    
    if "throat" in transcript_lower and any(word in transcript_lower for word in ["sore", "pain", "hurt"]):
        if "sore_throat" not in detected_symptoms:
            detected_symptoms.append("sore_throat")
    
    if "cough" in transcript_lower:
        if "cough" not in detected_symptoms:
            detected_symptoms.append("cough")
    
    if "fever" in transcript_lower or "temperature" in transcript_lower:
        if "fever" not in detected_symptoms:
            detected_symptoms.append("fever")
    
    # If no symptoms detected
    if not detected_symptoms:
        return [], "I couldn't identify any specific symptoms from your description. Please try again with more details about how you're feeling."
    
    # Generate diagnosis using the symptoms
    diagnosis = generate_diagnosis(detected_symptoms)
    return detected_symptoms, diagnosis

def generate_diagnosis(symptoms):
    """
    Generate a diagnosis based on detected symptoms
    """
    # Urgent/emergency conditions that require immediate attention
    emergency_conditions = {
        "chest_pain": "Chest pain can be a sign of a serious condition such as a heart attack or pulmonary issue. Please seek immediate medical attention at the nearest emergency room or call emergency services.",
        "shortness_of_breath": "Sudden or severe difficulty breathing can indicate a serious medical condition. Please seek immediate medical attention.",
        "severe_headache": "A sudden, severe headache could be a sign of a serious condition. If accompanied by confusion, stiff neck, or vision changes, please seek immediate medical attention.",
        "seizure": "Seizures require immediate medical evaluation. Please seek emergency medical care."
    }
    
    # Check for emergency symptoms first
    for symptom, response in emergency_conditions.items():
        if symptom in symptoms:
            return response
    
    # Define various disease patterns
    disease_patterns = [
        {
            "condition": "Influenza-like illness",
            "symptoms": ["fever", "headache", "body_ache", "fatigue"],
            "min_match": 3,
            "diagnosis": "Your symptoms suggest you may have a viral infection like the flu. Rest, drink fluids, and take over-the-counter pain relievers if needed. If symptoms worsen or persist beyond 3-4 days, please consult a doctor."
        },
        {
            "condition": "Common cold",
            "symptoms": ["cough", "sore_throat", "runny_nose", "congestion", "sneezing"],
            "min_match": 3,
            "diagnosis": "Your symptoms suggest you may have a common cold. Rest, stay hydrated, and use over-the-counter cold medications for symptom relief. If symptoms worsen or you develop a high fever, please consult a doctor."
        },
        {
            "condition": "Migraine",
            "symptoms": ["headache", "sensitivity_to_light", "sensitivity_to_sound", "nausea"],
            "min_match": 2,
            "diagnosis": "Your symptoms suggest you may be experiencing a migraine. Rest in a dark, quiet room and consider over-the-counter pain relievers. If this is a recurring issue, please consult a doctor for proper treatment options."
        },
        {
            "condition": "Gastroenteritis",
            "symptoms": ["abdominal_pain", "nausea", "vomiting", "diarrhea"],
            "min_match": 2,
            "diagnosis": "Your symptoms could indicate a digestive issue such as gastroenteritis (stomach flu) or food poisoning. Stay hydrated, eat bland foods, and rest. If symptoms are severe or persist beyond 24-48 hours, please consult a doctor."
        },
        {
            "condition": "Allergic reaction",
            "symptoms": ["rash", "itching", "hives", "sneezing", "runny_nose", "congestion"],
            "min_match": 2,
            "diagnosis": "You may be experiencing an allergic reaction. Avoid potential allergens and consider over-the-counter antihistamines for relief. If the rash spreads or is accompanied by difficulty breathing, seek immediate medical attention."
        },
        {
            "condition": "Respiratory infection",
            "symptoms": ["cough", "fever", "shortness_of_breath", "chest_tightness", "wheezing"],
            "min_match": 2,
            "diagnosis": "Your symptoms suggest a respiratory infection. Rest, stay hydrated, and monitor your breathing. If you develop high fever, severe shortness of breath, or symptoms worsen, please seek medical attention promptly."
        },
        {
            "condition": "Urinary tract infection",
            "symptoms": ["painful_urination", "urinary_frequency", "urinary_urgency", "abdominal_pain"],
            "min_match": 2,
            "diagnosis": "Your symptoms could indicate a urinary tract infection. Drink plenty of water and seek medical attention, as antibiotics may be necessary for treatment."
        },
        {
            "condition": "Sinus infection",
            "symptoms": ["headache", "congestion", "facial_pain", "runny_nose", "loss_of_smell"],
            "min_match": 3,
            "diagnosis": "You may have a sinus infection. Try nasal saline rinses, steam inhalation, and over-the-counter decongestants. If symptoms persist beyond 10 days or are severe, consult a healthcare provider."
        }
    ]
    
    # Check for disease patterns
    for pattern in disease_patterns:
        matching_symptoms = set(symptoms) & set(pattern["symptoms"])
        if len(matching_symptoms) >= pattern["min_match"]:
            return pattern["diagnosis"]
    
    # Single symptom diagnoses for common symptoms
    single_symptom_responses = {
        "fever": "Fever can be a sign of infection. Rest, stay hydrated, and consider over-the-counter fever reducers. If your fever is high (above 102°F/39°C) or lasts more than three days, please consult a doctor.",
        "headache": "Your headache may be due to tension, dehydration, or eyestrain. Rest, stay hydrated, and consider over-the-counter pain relievers. If headaches are severe or recurring, please consult a doctor.",
        "cough": "Your cough could be due to a respiratory infection, allergies, or irritation. Stay hydrated, use honey (if not allergic) for cough relief, and consider over-the-counter cough medications. If the cough persists beyond two weeks or is accompanied by shortness of breath, please consult a doctor.",
        "sore_throat": "Your sore throat may be due to a viral infection or allergies. Gargle with warm salt water, stay hydrated, and consider throat lozenges for relief. If symptoms persist beyond a week or are accompanied by high fever, please consult a doctor.",
        "dizziness": "Dizziness can be caused by many factors including dehydration, inner ear issues, or low blood pressure. Stay hydrated, avoid sudden movements, and sit or lie down when feeling dizzy. If dizziness is severe or persistent, please consult a doctor.",
        "fatigue": "Fatigue can be caused by many factors including stress, poor sleep, or underlying medical conditions. Ensure you're getting adequate rest, staying hydrated, and eating well. If fatigue persists or is severe, please consult a healthcare provider.",
        "nausea": "Nausea can be caused by digestive issues, motion sickness, or other conditions. Try small, bland meals, stay hydrated, and rest. If nausea persists or is accompanied by severe vomiting, please consult a doctor.",
        "back_pain": "Back pain could be due to muscle strain, poor posture, or overexertion. Rest, use ice or heat therapy, and consider over-the-counter pain relievers. If pain is severe, persistent, or accompanied by numbness or weakness, consult a healthcare provider."
    }
    
    # Check if any of our single symptoms have specific advice
    for symptom in symptoms:
        if symptom in single_symptom_responses:
            return single_symptom_responses[symptom]
    
    # General case if no patterns match
    symptom_list = ", ".join(symptoms[:5])  # Limit to first 5 symptoms for readability
    if len(symptoms) > 5:
        symptom_list += ", and others"
        
    return f"Based on your reported symptoms ({symptom_list}), you may be experiencing a health issue requiring attention. Monitor your symptoms, rest, and stay hydrated. If symptoms persist or worsen, please consult a healthcare professional for proper diagnosis and treatment."

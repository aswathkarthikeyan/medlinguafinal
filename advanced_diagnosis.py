"""
Advanced medical diagnosis engine using comprehensive symptom analysis 
and medical pattern recognition.
"""

import re
import json
from enhanced_symptoms_db import (
    extensive_symptoms, 
    advanced_symptoms, 
    medical_conditions, 
    expanded_symptom_keywords,
    check_symptom_relationships,
    body_system_symptoms
)
from huggingface_lite import (
    detect_symptoms_multilingual,
    get_diagnosis_multilingual,
    get_model_info,
    translate_symptoms
)

def advanced_symptom_detection(transcript):
    """
    Advanced symptom detection using natural language processing 
    and comprehensive symptom database
    
    Args:
        transcript: The patient's description of their symptoms
    
    Returns:
        list: Detected symptoms with confidence scores
    """
    # Convert transcript to lowercase for easier matching
    transcript_lower = transcript.lower()
    
    # Initialize symptom detection
    detected_symptoms = {}  # Dictionary to store symptom and confidence score
    
    # First pass: Exact keyword matching with expanded keywords
    for symptom, keywords in expanded_symptom_keywords.items():
        for keyword in keywords:
            # Check for the keyword with word boundaries
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, transcript_lower):
                # If symptom already detected, increase confidence
                if symptom in detected_symptoms:
                    detected_symptoms[symptom] += 1
                else:
                    detected_symptoms[symptom] = 1
    
    # Second pass: Context-based detection for compound symptoms
    # This looks for symptom relationships in close proximity
    compound_patterns = [
        # Headache types
        (r'(?:severe|bad|worst|intense|terrible|horrible)\s+(?:\w+\s+){0,3}?headache', "severe_headache", 2),
        (r'(?:throbbing|pounding|pulsating)\s+(?:\w+\s+){0,3}?(?:head|headache)', "migraine", 1.5),
        (r'(?:one|1)\s+(?:\w+\s+){0,2}?side\s+(?:\w+\s+){0,2}?(?:head|headache)', "migraine", 1.5),
        (r'headache\s+(?:\w+\s+){0,4}?(?:nausea|vomit|sensitive|light|sound)', "migraine", 1.5),
        (r'(?:pressure|tight|band|squeezing)\s+(?:\w+\s+){0,3}?(?:around|head|headache)', "tension_headache", 1.5),
        
        # Chest pain types
        (r'(?:chest\s+pain|pain\s+in\s+chest)\s+(?:\w+\s+){0,5}?(?:arm|jaw|shoulder|neck|back)', "heart_attack_symptoms", 2),
        (r'(?:squeezing|crushing|pressure|heavy|tight)\s+(?:\w+\s+){0,3}?(?:chest|heart)', "heart_attack_symptoms", 2),
        (r'(?:chest|heart)\s+(?:\w+\s+){0,3}?(?:squeezing|crushing|pressure|heavy|tight)', "heart_attack_symptoms", 2),
        
        # Breathing issues
        (r'(?:hard|difficult|trouble)\s+(?:\w+\s+){0,2}?(?:breath|breathing)', "shortness_of_breath", 1.5),
        (r'(?:can\'?t|cannot|couldn\'?t)\s+(?:\w+\s+){0,2}?(?:breath|breathe)', "shortness_of_breath", 2),
        (r'(?:short|catch)\s+(?:\w+\s+){0,2}?(?:breath|breathing)', "shortness_of_breath", 1.5),
        
        # Abdominal symptoms
        (r'(?:stomach|abdominal|belly)\s+(?:\w+\s+){0,3}?(?:cramp|pain|ache)', "abdominal_pain", 1.5),
        (r'(?:cramp|pain|ache)\s+(?:\w+\s+){0,3}?(?:stomach|abdominal|belly)', "abdominal_pain", 1.5),
        (r'(?:diarrhea|loose\s+stool)\s+(?:\w+\s+){0,4}?(?:vomit|nausea)', "gastroenteritis", 2),
        
        # Fever patterns
        (r'(?:high|bad|severe)\s+(?:\w+\s+){0,2}?fever', "high_fever", 2),
        (r'temperature\s+(?:\w+\s+){0,3}?(?:1\d\d|[3-9]\d\.\d|10[0-9])', "fever", 2),  # Matches 100+ degrees
        
        # Joint symptoms
        (r'(?:joint|knee|ankle|elbow|wrist|shoulder)\s+(?:\w+\s+){0,3}?(?:pain|ache|sore|stiff)', "joint_pain", 1.5),
        (r'(?:pain|ache|sore|stiff)\s+(?:\w+\s+){0,3}?(?:joint|knee|ankle|elbow|wrist|shoulder)', "joint_pain", 1.5),
        (r'(?:swollen|swelling)\s+(?:\w+\s+){0,3}?(?:joint|knee|ankle|elbow|wrist|shoulder)', "joint_swelling", 1.5),
        
        # Skin issues
        (r'(?:rash|redness|spots|bumps)\s+(?:\w+\s+){0,3}?(?:itch|itchy|itching)', "itchy_rash", 1.5),
        (r'(?:itch|itchy|itching)\s+(?:\w+\s+){0,3}?(?:rash|redness|spots|bumps)', "itchy_rash", 1.5),
        
        # Vision/eye symptoms
        (r'(?:blurr(?:y|ed)|blurred)\s+(?:\w+\s+){0,2}?(?:vision|sight|see)', "blurred_vision", 1.5),
        (r'(?:double|seeing\s+double)\s+(?:\w+\s+){0,2}?(?:vision|sight|see)', "double_vision", 1.5),
        
        # Neurological symptoms
        (r'(?:dizz(?:y|iness)|light\s*headed)\s+(?:\w+\s+){0,4}?(?:fall|fell|faint)', "severe_dizziness", 2),
        (r'(?:numb|numbness|tingling)\s+(?:\w+\s+){0,3}?(?:arm|hand|leg|foot|face)', "numbness", 1.5),
        (r'(?:weak|weakness)\s+(?:\w+\s+){0,3}?(?:arm|hand|leg|foot|body)', "muscle_weakness", 1.5),
        
        # Sleep issues
        (r'(?:can\'?t|cannot|couldn\'?t|trouble|difficult(?:y)?)\s+(?:\w+\s+){0,2}?(?:sleep|fall asleep)', "insomnia", 1.5),
        (r'(?:wake|waking)\s+(?:\w+\s+){0,3}?(?:night|up|sleep)', "sleep_disturbance", 1.5)
    ]
    
    for pattern, symptom, confidence in compound_patterns:
        if re.search(pattern, transcript_lower):
            if symptom in detected_symptoms:
                detected_symptoms[symptom] += confidence
            else:
                detected_symptoms[symptom] = confidence
    
    # Third pass: Proximity-based symptom relationships
    # This detects when multiple related terms appear close together
    proximity_patterns = [
        # Respiratory conditions
        (["cough", "fever", "tired", "fatigue", "body", "ache"], "influenza_like_illness", 3, 0.5),
        (["cough", "congestion", "runny", "nose", "sneeze", "sore", "throat"], "common_cold", 3, 0.5),
        
        # Gastrointestinal conditions
        (["nausea", "vomit", "diarrhea", "stomach", "cramp", "fever"], "gastroenteritis", 3, 0.5),
        (["heartburn", "chest", "burn", "lying", "down", "after", "eating"], "gerd", 3, 0.5),
        
        # Migraine patterns
        (["headache", "light", "sound", "sensitive", "nausea"], "migraine", 3, 0.5),
        
        # Allergic patterns
        (["sneeze", "itch", "eye", "runny", "nose", "congestion"], "allergic_rhinitis", 3, 0.5),
        
        # UTI patterns 
        (["urine", "pain", "burn", "frequent", "urgency"], "urinary_tract_infection", 3, 0.5)
    ]
    
    for terms, symptom, min_matches, proximity_score in proximity_patterns:
        term_count = sum(1 for term in terms if term in transcript_lower)
        if term_count >= min_matches:
            if symptom in detected_symptoms:
                detected_symptoms[symptom] += proximity_score * term_count
            else:
                detected_symptoms[symptom] = proximity_score * term_count
    
    # Fourth pass: Body system analysis - check if multiple symptoms from the same body system are present
    # This helps detect patterns of system-specific issues
    system_detected_symptoms = {}
    
    for symptom in detected_symptoms:
        # Find which body system(s) this symptom belongs to
        for system, symptoms in body_system_symptoms.items():
            if symptom in symptoms:
                if system not in system_detected_symptoms:
                    system_detected_symptoms[system] = []
                system_detected_symptoms[system].append(symptom)
    
    # Boost confidence for symptoms within the same body system when multiple are detected
    for system, symptoms in system_detected_symptoms.items():
        if len(symptoms) > 1:  # If multiple symptoms from the same system
            boost = min(0.5 * len(symptoms), 2.0)  # Cap the boost at 2.0
            for symptom in symptoms:
                detected_symptoms[symptom] += boost
    
    # If no symptoms detected so far, use a fallback approach with broader word matching
    if not detected_symptoms:
        common_health_terms = [
            # General symptoms
            ("pain", ["pain", "ache", "hurt", "sore", "discomfort"]),
            ("fever", ["fever", "temperature", "hot", "chills", "cold sweats"]),
            ("fatigue", ["tired", "exhausted", "fatigue", "no energy", "weak"]),
            ("headache", ["head", "headache", "migraine"]),
            ("dizziness", ["dizzy", "lightheaded", "faint", "vertigo", "spinning"]),
            ("nausea", ["nausea", "sick", "queasy", "vomit", "throw up"]),
            
            # Body parts with "pain/ache/hurt" inference
            ("chest_pain", ["chest"]),
            ("abdominal_pain", ["stomach", "belly", "abdomen"]),
            ("back_pain", ["back"]),
            ("joint_pain", ["joint", "knee", "elbow", "wrist", "ankle", "shoulder"]),
            ("throat_symptoms", ["throat", "swallow"]),
            ("breathing_issues", ["breath", "breathing", "inhale", "exhale"]),
            ("skin_issues", ["skin", "rash", "itch"]),
            ("eye_issues", ["eye", "vision", "see", "sight"]),
            ("ear_issues", ["ear", "hearing", "deaf", "ringing"])
        ]
        
        for symptom, terms in common_health_terms:
            for term in terms:
                if term in transcript_lower:
                    detected_symptoms[symptom] = 0.5  # Lower confidence for this fallback method
                    break
    
    # Convert to sorted list of (symptom, confidence) tuples and sort by confidence
    symptom_list = [(symptom, score) for symptom, score in detected_symptoms.items()]
    symptom_list.sort(key=lambda x: x[1], reverse=True)
    
    # Return just the symptom names, keeping order of confidence
    return [symptom for symptom, _ in symptom_list]

def generate_advanced_diagnosis(symptoms, transcript):
    """
    Generate a comprehensive diagnosis based on advanced symptom analysis
    
    Args:
        symptoms: List of detected symptoms
        transcript: Original symptom description
        
    Returns:
        dict: Detailed diagnosis information
    """
    # Check for emergency symptoms first
    emergency_symptoms = {
        "chest_pain": "Chest pain can be a sign of a serious condition such as a heart attack or pulmonary issue. Please seek immediate medical attention.",
        "heart_attack_symptoms": "Your symptoms may indicate a heart attack. Please seek emergency medical attention immediately.",
        "severe_headache": "A sudden, severe headache could indicate a serious condition. Please seek immediate medical attention, especially if accompanied by confusion, stiff neck, or vision changes.",
        "shortness_of_breath": "Severe difficulty breathing may indicate a serious condition. Please seek immediate medical attention.",
        "stroke_symptoms": "Your symptoms may indicate a stroke. Please seek emergency medical attention immediately.",
        "anaphylaxis": "Your symptoms suggest a severe allergic reaction. Please seek emergency medical attention immediately.",
        "seizure": "Seizures require immediate medical evaluation. Please seek emergency medical care.",
        "severe_abdominal_pain": "Severe abdominal pain, especially if sudden and accompanied by other symptoms, may indicate a serious condition requiring immediate medical attention."
    }
    
    for symptom in symptoms[:5]:  # Check the top 5 symptoms for emergency conditions
        if symptom in emergency_symptoms:
            return {
                "diagnosis_text": f"⚠️ MEDICAL ATTENTION ADVISED: {emergency_symptoms[symptom]}",
                "severity": "emergency",
                "confidence": "high",
                "detected_symptoms": symptoms[:10],  # Include only top 10 symptoms
                "possible_conditions": [],
                "recommendations": ["Seek immediate medical attention", "Do not delay getting emergency care", "Call emergency services if symptoms are severe"]
            }
    
    # Check for symptom relationships to identify possible conditions
    possible_conditions = check_symptom_relationships(symptoms)
    
    # If no specific conditions detected from relationships
    if not possible_conditions:
        # Generate general diagnosis based on the symptoms
        
        # First, categorize symptoms by body system
        system_symptoms = {}
        for symptom in symptoms:
            for system, system_symptom_list in body_system_symptoms.items():
                if symptom in system_symptom_list:
                    if system not in system_symptoms:
                        system_symptoms[system] = []
                    system_symptoms[system].append(symptom)
        
        # Determine primary affected body system
        primary_system = None
        max_symptoms = 0
        for system, system_symptom_list in system_symptoms.items():
            if len(system_symptom_list) > max_symptoms:
                max_symptoms = len(system_symptom_list)
                primary_system = system
        
        # Generate diagnosis text based on primary system and symptoms
        if primary_system:
            diagnosis_text = f"Based on your symptoms, you may be experiencing an issue primarily affecting your {primary_system} system. "
            
            # Add specific information for common systems
            system_advice = {
                "respiratory": "Respiratory issues can be caused by infections, allergies, or underlying conditions. Rest, stay hydrated, and monitor your breathing. If you experience severe shortness of breath, seek immediate medical attention.",
                "gastrointestinal": "Digestive issues can be caused by infections, food intolerance, or inflammatory conditions. Try eating bland foods, staying hydrated, and avoiding trigger foods. If symptoms are severe or persistent, consult a healthcare provider.",
                "neurological": "Neurological symptoms should be taken seriously. Rest, avoid triggers like bright lights or screens if they worsen symptoms, and consider over-the-counter pain relievers if appropriate. If symptoms are severe or unusual, consult a healthcare provider.",
                "musculoskeletal": "Musculoskeletal pain may be due to strain, inflammation, or injury. Rest the affected area, apply ice for acute pain or heat for chronic pain, and consider over-the-counter pain relievers. If pain is severe or persistent, consult a healthcare provider.",
                "cardiovascular": "Cardiovascular symptoms should be evaluated by a healthcare professional. If you experience chest pain, especially with shortness of breath, sweating, or pain radiating to the arm or jaw, seek immediate medical attention.",
                "integumentary": "Skin issues can be caused by allergies, infections, or inflammatory conditions. Avoid scratching, use mild soaps, and consider over-the-counter antihistamines or hydrocortisone cream for mild symptoms. If symptoms are severe or spreading, consult a healthcare provider."
            }
            
            if primary_system in system_advice:
                diagnosis_text += system_advice[primary_system]
            
            # Add general recommendations
            recommendations = [
                "Monitor your symptoms and note any changes",
                "Stay hydrated and get adequate rest",
                "Avoid activities that worsen symptoms",
                "Consider over-the-counter medications appropriate for your symptoms",
                "Consult a healthcare provider if symptoms are severe, persistent, or worsening"
            ]
            
            return {
                "diagnosis_text": diagnosis_text,
                "severity": "moderate",
                "confidence": "medium",
                "detected_symptoms": symptoms[:10],
                "possible_conditions": [],
                "recommendations": recommendations
            }
        
        # If no clear body system identified, provide general advice
        general_text = "Based on your description, I've identified several symptoms but no clear pattern indicating a specific condition. "
        general_text += "It's important to monitor your symptoms and seek medical attention if they persist or worsen. "
        general_text += "Consider keeping a symptom diary to track when symptoms occur and what might trigger them."
        
        return {
            "diagnosis_text": general_text,
            "severity": "mild to moderate",
            "confidence": "low",
            "detected_symptoms": symptoms[:10],
            "possible_conditions": [],
            "recommendations": [
                "Monitor your symptoms and note any changes",
                "Stay hydrated and get adequate rest",
                "Consider over-the-counter medications appropriate for your specific symptoms",
                "Consult a healthcare provider if symptoms persist more than a few days",
                "Bring a list of your symptoms when consulting a healthcare provider"
            ]
        }
    
    # If specific conditions were identified
    # Use the highest matching condition for primary diagnosis
    top_condition = possible_conditions[0]
    
    # Generate diagnosis text
    diagnosis_text = f"Based on your symptoms, you may be experiencing {top_condition['condition']}. "
    diagnosis_text += f"{top_condition['description']} "
    
    # Add severity information if available
    if 'severity' in top_condition:
        diagnosis_text += f"This is typically a {top_condition['severity']} condition. "
    
    # Add other possible conditions
    if len(possible_conditions) > 1:
        diagnosis_text += "Other possible conditions include: "
        for condition in possible_conditions[1:]:
            diagnosis_text += f"{condition['condition']}, "
        diagnosis_text = diagnosis_text.rstrip(", ") + ". "
    
    # Create recommendations list
    recommendations = []
    
    # Use condition-specific recommendations if available
    if 'recommendations' in top_condition:
        recommendations.extend(top_condition['recommendations'])
    else:
        # Default recommendations
        recommendations = [
            "Consult with a healthcare provider for proper diagnosis and treatment",
            "Monitor your symptoms and note any changes",
            "Stay hydrated and get adequate rest",
            "Avoid activities that worsen symptoms"
        ]
    
    # Add disclaimer
    diagnosis_text += "\n\nDISCLAIMER: This is not a professional medical diagnosis. If symptoms are severe or concerning, please consult a healthcare provider."
    
    return {
        "diagnosis_text": diagnosis_text,
        "severity": top_condition.get('severity', 'moderate'),
        "confidence": "medium",
        "detected_symptoms": symptoms[:10],
        "possible_conditions": possible_conditions,
        "recommendations": recommendations
    }

def advanced_diagnose_symptoms(transcript, lang="en"):
    """
    Perform comprehensive symptom analysis and diagnosis using advanced techniques
    with multilingual BioGPT-style language understanding from Hugging Face models.
    
    Args:
        transcript: Patient's description of symptoms
        lang: Language code (en, ta, hi)
        
    Returns:
        tuple: (detected_symptoms, diagnosis_text, additional_info)
    """
    # Safeguard against empty input
    if not transcript or len(transcript.strip()) == 0:
        return [], "Please provide some details about your symptoms.", {}
    
    # Use Hugging Face multilingual model for symptom detection
    huggingface_symptoms = detect_symptoms_multilingual(transcript, lang)
    
    # Also use our traditional advanced symptom detection as backup
    standard_symptoms = advanced_symptom_detection(transcript)
    
    # Combine both approaches for better detection
    detected_symptoms = list(set(huggingface_symptoms + standard_symptoms))
    
    # If no symptoms detected
    if not detected_symptoms:
        return [], "I couldn't identify any specific symptoms from your description. Please try again with more details about how you're feeling.", {}
    
    # Get diagnosis using Hugging Face multilingual model
    diagnosis_text, diagnosis_info = get_diagnosis_multilingual(detected_symptoms, transcript, lang)
    
    # Include fallback logic in case the Hugging Face model doesn't produce good results
    if not diagnosis_info.get("condition") or diagnosis_info.get("confidence", 0) < 0.4:
        # Fall back to our standard advanced diagnosis if Hugging Face model results are low confidence
        try:
            # Generate comprehensive diagnosis with standard system
            diagnosis_result = generate_advanced_diagnosis(detected_symptoms, transcript)
            
            # Extract the diagnosis text
            diagnosis_text = diagnosis_result["diagnosis_text"]
            
            # Return with standard analysis
            return detected_symptoms, diagnosis_text, {
                "diagnosis_text": diagnosis_text,
                "analysis_engine": "Advanced Symptom Analysis",
                "model_info": get_model_info(),
                "confidence_score": 0.6,
                "recommendations": diagnosis_result.get("recommendations", []),
                "possible_conditions": diagnosis_result.get("possible_conditions", [])
            }
        except Exception as e:
            # If everything fails, just return the Hugging Face model result
            print(f"Error in advanced diagnosis fallback: {e}")
    
    # Return Hugging Face model-based diagnosis
    return detected_symptoms, diagnosis_text, {
        "diagnosis_text": diagnosis_text,
        "analysis_engine": "Hugging Face BioGPT Multilingual",
        "model_info": get_model_info(),
        "confidence_score": diagnosis_info.get("confidence", 0.7),
        "condition": diagnosis_info.get("condition", ""),
        "recommendations": diagnosis_info.get("recommendations", [])
    }
"""
Free AI-powered diagnosis engine for the medical assistant application.
This module provides diagnosis capabilities using a free API.
"""

import requests
import json
import time
from symptoms_db import common_symptoms

# Free API endpoints for medical information and diagnosis
NINJAS_ENDPOINT = "https://api.api-ninjas.com/v1/symptoms"
MEDICAL_INFO_ENDPOINT = "https://disease-info-api.herokuapp.com/diseases"
HEALTH_API_ENDPOINT = "https://health-advice-api.p.rapidapi.com/advice"

def get_free_api_diagnosis(symptoms, transcript):
    """
    Get a diagnosis from free APIs based on symptoms and transcript
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description of their symptoms
        
    Returns:
        str: Generated diagnosis text
    """
    # Try multiple methods to get diagnosis info
    diagnosis_text = ""
    
    # Method 1: Use symptoms database for detailed information
    symptom_details = []
    for symptom in symptoms[:5]:  # Limit to top 5 symptoms for relevance
        if symptom in common_symptoms:
            clean_symptom = symptom.replace("_", " ")
            symptom_details.append({
                "name": clean_symptom,
                "description": common_symptoms[symptom]
            })
    
    # Method 2: Use direct web-based symptom matching
    try:
        symptom_query = " ".join([s.replace("_", " ") for s in symptoms[:3]])
        query = f"{symptom_query}"
        
        # Request medical info (no API key required)
        response = direct_medical_advice(query)
        if response:
            diagnosis_text += response
    except Exception as e:
        print(f"Error getting free API diagnosis: {e}")
        # Fall back to local knowledge base
        diagnosis_text = generate_comprehensive_diagnosis(symptoms, transcript)
    
    # If both methods failed or returned minimal results
    if len(diagnosis_text.strip()) < 100:
        diagnosis_text = generate_comprehensive_diagnosis(symptoms, transcript)
    
    return diagnosis_text

def direct_medical_advice(query):
    """Generate medical advice directly using pattern matching and medical knowledge base"""
    # This is a fallback function that uses our built-in knowledge
    # to generate advice without relying on external APIs
    
    common_conditions = {
        "headache": """Headaches can be caused by various factors including tension, migraines, sinusitis, or dehydration. 
        For tension headaches, try relaxation techniques, adequate rest, and over-the-counter pain relievers like acetaminophen or ibuprofen.
        For migraines, rest in a dark, quiet room and consider prescription medications if they're frequent.
        Stay hydrated and maintain regular sleep patterns to prevent headaches.
        If headaches are severe, sudden, or accompanied by other symptoms like confusion or stiff neck, seek immediate medical attention.""",
        
        "fever": """Fever is your body's natural defense against infection. 
        For mild fevers (up to 102°F/38.9°C), rest, stay hydrated, and take acetaminophen or ibuprofen if needed.
        Cool compresses or lukewarm baths may help reduce fever.
        For high fevers (above 102°F/38.9°C), persistent fevers lasting more than 3 days, or fevers with severe symptoms,
        seek medical attention as they may indicate serious infection requiring specific treatment.""",
        
        "cough": """Coughs can be caused by viral infections, allergies, asthma, or other respiratory conditions.
        For dry coughs, try honey (if not allergic and over 1 year old), lozenges, or cough suppressants.
        For productive coughs with mucus, stay hydrated and consider expectorants to help clear the airways.
        Humidifiers can help with both types of coughs.
        If coughing persists beyond 3 weeks, produces discolored mucus, or is accompanied by shortness of breath,
        consult a healthcare provider.""",
        
        "sore throat": """Sore throats are commonly caused by viral infections, but can also be due to bacterial infections or allergies.
        Gargle with warm salt water, use throat lozenges, drink warm liquids, and take over-the-counter pain relievers.
        If your sore throat is severe, lasts longer than a week, or comes with high fever or difficulty swallowing,
        see a doctor as you might need antibiotics for bacterial infections like strep throat.""",
        
        "stomach pain": """Abdominal pain can result from various conditions including indigestion, gas, food poisoning, or more serious issues.
        For mild stomach pain, try resting, avoiding trigger foods, and using over-the-counter antacids if appropriate.
        A heating pad might help with cramping.
        If pain is severe, persistent, or accompanied by vomiting, fever, or blood in stool,
        seek immediate medical attention as it could indicate appendicitis, gallbladder issues, or other serious conditions.""",
        
        "nausea": """Nausea can be caused by motion sickness, food poisoning, medication side effects, or various illnesses.
        Try eating small, bland meals, staying hydrated with clear fluids, and avoiding strong smells or flavors.
        Ginger in various forms (tea, candy, capsules) may help reduce nausea.
        If nausea persists beyond 24-48 hours, is accompanied by severe vomiting, or prevents keeping any fluids down,
        seek medical attention to prevent dehydration.""",
        
        "dizziness": """Dizziness can result from inner ear issues, low blood pressure, dehydration, or medication side effects.
        When feeling dizzy, sit or lie down immediately to prevent falls. Stay hydrated and avoid sudden position changes.
        If dizziness is severe, persistent, or accompanied by other symptoms like chest pain or severe headache,
        seek medical attention as it could indicate serious conditions requiring treatment.""",
        
        "rash": """Skin rashes can be caused by allergic reactions, infections, or various skin conditions.
        For mild rashes, avoid scratching, use mild soaps, apply cold compresses, and try over-the-counter antihistamines or hydrocortisone cream.
        If a rash is widespread, painful, blistering, or accompanied by fever or breathing difficulties,
        seek immediate medical attention as it could indicate a severe allergic reaction or serious infection.""",
        
        "joint pain": """Joint pain commonly results from inflammation, injury, or conditions like arthritis or gout.
        Rest the affected joints, apply ice for acute pain or heat for chronic pain, and consider over-the-counter pain relievers.
        Gentle stretching and maintaining a healthy weight can help reduce joint stress.
        If joint pain is severe, accompanied by significant swelling, redness, or inability to use the joint,
        consult a healthcare provider for proper diagnosis and treatment.""",
        
        "fatigue": """Fatigue can be caused by sleep deprivation, stress, medical conditions, or medication side effects.
        Improve sleep habits, maintain regular physical activity, stay hydrated, and manage stress through techniques like meditation.
        If fatigue is persistent, severe, or significantly impacts daily life despite adequate rest,
        consult a healthcare provider to rule out underlying conditions like anemia, thyroid disorders, or chronic fatigue syndrome."""
    }
    
    # Check if any key symptoms match our knowledge base
    for key_term, advice in common_conditions.items():
        if key_term in query.lower():
            return advice
    
    # If no specific match, return general health advice
    general_advice = """Based on your symptoms, here are some general health recommendations:

1. Rest and allow your body time to recover
2. Stay hydrated by drinking plenty of water
3. Maintain a balanced diet rich in fruits and vegetables
4. Get adequate sleep (7-9 hours for most adults)
5. Avoid alcohol and caffeine, which can worsen many conditions
6. Consider over-the-counter medications appropriate for your symptoms
7. Monitor your symptoms and note any changes or worsening

If your symptoms persist for more than a few days, worsen suddenly, or are accompanied by high fever, severe pain, or difficulty breathing, please consult a healthcare professional for proper diagnosis and treatment. This information is not a substitute for professional medical advice."""

    return general_advice

def generate_comprehensive_diagnosis(symptoms, transcript):
    """
    Generate a detailed diagnosis based on symptoms and transcript using a rule-based expert system
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description
        
    Returns:
        str: Comprehensive diagnosis text
    """
    # Create a knowledge base of common symptom combinations and their associated conditions
    symptom_patterns = [
        {
            "pattern": ["fever", "cough", "fatigue", "body_ache", "headache"],
            "condition": "Influenza (Flu)",
            "description": """Influenza is a viral infection that attacks your respiratory system. Common symptoms include fever, body aches, fatigue, cough, and headache.

Management:
- Rest and get plenty of fluids
- Take over-the-counter fever reducers and pain relievers
- Stay home to avoid spreading the virus
- Consider antiviral medications if diagnosed within 48 hours of symptom onset

When to seek medical attention:
- Difficulty breathing or shortness of breath
- Persistent chest pain or pressure
- Confusion or inability to stay alert
- Severe or persistent vomiting
- Symptoms that improve but then return with fever and worse cough"""
        },
        {
            "pattern": ["cough", "sore_throat", "runny_nose", "congestion", "sneezing"],
            "condition": "Common Cold",
            "description": """The common cold is a viral infection of your nose and throat. Symptoms typically include runny nose, congestion, sneezing, sore throat, and cough.

Management:
- Rest and stay hydrated
- Use over-the-counter cold remedies to relieve symptoms
- Gargle with salt water for sore throat
- Use saline nasal drops or sprays for congestion
- Consider honey for cough (if over 1 year of age)

When to seek medical attention:
- Fever above 101.3°F (38.5°C)
- Symptoms that last more than 10 days
- Severe or unusual symptoms
- Worsening symptoms after initial improvement"""
        },
        {
            "pattern": ["headache", "sensitivity_to_light", "sensitivity_to_sound", "nausea", "aura"],
            "condition": "Migraine",
            "description": """Migraines are recurring headaches that cause moderate to severe throbbing or pulsing pain, often on one side of the head. Symptoms can include headache, sensitivity to light and sound, nausea, and sometimes visual disturbances (aura).

Management:
- Rest in a quiet, dark room
- Apply cold compresses to the forehead or neck
- Take over-the-counter pain medications at the first sign of migraine
- Stay hydrated
- Consider prescription medications for frequent migraines

When to seek medical attention:
- Severe headache that comes on suddenly (thunderclap headache)
- Headache with fever, stiff neck, confusion, seizures, double vision, weakness, or numbness
- Headache after a head injury
- Chronic headaches that worsen after coughing, exertion, or sudden movement"""
        },
        {
            "pattern": ["abdominal_pain", "nausea", "vomiting", "diarrhea", "fever"],
            "condition": "Gastroenteritis (Stomach Flu)",
            "description": """Gastroenteritis is an inflammation of the digestive tract that can be caused by viruses, bacteria, or parasites. Symptoms include diarrhea, nausea, vomiting, abdominal pain, and sometimes fever.

Management:
- Stay hydrated with water, clear broths, or oral rehydration solutions
- Eat bland, easy-to-digest foods when able to eat
- Avoid dairy, caffeine, alcohol, and fatty or highly seasoned foods
- Rest to help your body fight the infection

When to seek medical attention:
- Unable to keep liquids down for 24 hours
- Vomiting blood or seeing blood in bowel movements
- Fever above 102°F (39°C)
- Severe abdominal pain
- Signs of dehydration (excessive thirst, dry mouth, little or no urination, severe weakness, dizziness, or lightheadedness)"""
        },
        {
            "pattern": ["rash", "itching", "hives", "swelling", "difficulty_breathing"],
            "condition": "Allergic Reaction",
            "description": """Allergic reactions occur when your immune system reacts to a foreign substance that's typically harmless. Symptoms can range from mild (rash, itching) to severe (anaphylaxis with difficulty breathing and swelling).

Management for mild allergic reactions:
- Avoid the allergen if known
- Take over-the-counter antihistamines
- Use hydrocortisone cream for skin reactions
- Take cool baths or apply cool compresses

When to seek emergency medical attention:
- Difficulty breathing or swallowing
- Swelling of the lips, tongue, or throat
- Feeling faint or dizzy
- Rapid heartbeat
- Vomiting or severe nausea

If you have a history of severe allergic reactions, use your epinephrine auto-injector (if prescribed) and seek emergency care immediately."""
        },
        {
            "pattern": ["shortness_of_breath", "wheezing", "chest_tightness", "cough"],
            "condition": "Asthma Exacerbation",
            "description": """Asthma is a condition that affects the airways in the lungs, causing them to narrow and swell, producing extra mucus. This can make breathing difficult and trigger coughing, wheezing, and shortness of breath.

Management:
- Use prescribed rescue inhaler (usually albuterol) as directed
- Avoid triggers such as allergens, cold air, or exercise if known to cause symptoms
- Follow your asthma action plan if you have one
- Use a peak flow meter to monitor breathing

When to seek emergency medical attention:
- Severe shortness of breath or difficulty speaking
- No improvement after using a rescue inhaler
- Straining chest muscles to breathe
- Blue tint to lips or fingernails
- Rapid progression of symptoms"""
        },
        {
            "pattern": ["painful_urination", "frequent_urination", "urgency", "abdominal_pain", "blood_in_urine"],
            "condition": "Urinary Tract Infection (UTI)",
            "description": """A urinary tract infection affects any part of your urinary system, including kidneys, bladder, ureters, and urethra. Women are at greater risk. Symptoms often include painful urination, increased frequency, urgency, and sometimes abdominal pain or blood in urine.

Management:
- Drink plenty of water to help flush out bacteria
- Urinate when you feel the need (don't hold it)
- Take prescribed antibiotics if diagnosed with a UTI
- Consider over-the-counter pain relievers for discomfort

When to seek medical attention:
- Fever and chills
- Nausea and vomiting
- Back or side pain
- Any UTI symptoms in men or children (they should always see a doctor)
- Symptoms that don't improve with treatment
- Blood in urine"""
        }
    ]
    
    # Extended symptom patterns for more comprehensive coverage
    additional_patterns = [
        {
            "pattern": ["chest_pain", "shortness_of_breath", "sweating", "nausea", "lightheadedness"],
            "condition": "Possible Cardiac Issue (Requires Immediate Medical Attention)",
            "description": """The symptoms you're experiencing could indicate a serious cardiac condition that requires immediate medical evaluation. These symptoms can sometimes represent a heart attack or other cardiovascular emergency.

DO NOT ATTEMPT SELF-TREATMENT. SEEK EMERGENCY MEDICAL ATTENTION IMMEDIATELY BY CALLING YOUR LOCAL EMERGENCY NUMBER (such as 911 in the US).

While waiting for emergency services:
- Chew and swallow an aspirin if not allergic and if advised by emergency dispatcher
- Rest in a comfortable position
- Loosen tight clothing
- Stay as calm as possible"""
        },
        {
            "pattern": ["sudden_headache", "confusion", "one_sided_weakness", "trouble_speaking", "vision_changes"],
            "condition": "Possible Stroke (Requires Immediate Medical Attention)",
            "description": """The symptoms you're describing could indicate a stroke, which is a medical emergency. Remember the acronym FAST:
- Face: Is one side of the face drooping?
- Arms: Is there weakness or numbness in one arm?
- Speech: Is speech slurred or strange?
- Time: If you observe any of these signs, call emergency services immediately.

DO NOT WAIT OR ATTEMPT SELF-TREATMENT. SEEK EMERGENCY MEDICAL ATTENTION IMMEDIATELY BY CALLING YOUR LOCAL EMERGENCY NUMBER (such as 911 in the US).

Every minute counts during a stroke as brain tissue is rapidly damaged."""
        },
        {
            "pattern": ["high_fever", "stiff_neck", "headache", "confusion", "sensitivity_to_light"],
            "condition": "Possible Meningitis (Requires Immediate Medical Attention)",
            "description": """The combination of symptoms you're experiencing could indicate meningitis, an inflammation of the membranes surrounding your brain and spinal cord. This is a serious medical emergency that requires immediate attention.

DO NOT ATTEMPT SELF-TREATMENT. SEEK EMERGENCY MEDICAL ATTENTION IMMEDIATELY BY CALLING YOUR LOCAL EMERGENCY NUMBER (such as 911 in the US).

Bacterial meningitis can be life-threatening and requires prompt antibiotic treatment."""
        },
        {
            "pattern": ["sore_throat", "fever", "swollen_glands", "difficulty_swallowing", "white_spots_tonsils"],
            "condition": "Possible Strep Throat",
            "description": """Your symptoms suggest you may have strep throat, a bacterial infection that requires medical treatment. Strep throat is caused by group A Streptococcus bacteria.

Management:
- See a healthcare provider for proper diagnosis and treatment
- Take antibiotics as prescribed if diagnosed with strep throat
- Rest your voice and throat
- Drink warm liquids and cold foods to soothe your throat
- Use over-the-counter pain relievers for discomfort
- Gargle with salt water
- Use throat lozenges (if age appropriate)

When to seek medical attention:
- Difficulty breathing or swallowing
- Drooling (especially in children)
- Temperature over 101°F (38.3°C)
- Rash
- Joint pain

Without proper treatment, strep throat can lead to complications like rheumatic fever or kidney inflammation."""
        },
        {
            "pattern": ["congestion", "facial_pain", "thick_nasal_discharge", "reduced_smell", "headache"],
            "condition": "Sinusitis",
            "description": """Your symptoms suggest sinusitis, an inflammation or swelling of the tissue lining the sinuses. This can be caused by infection, allergies, or anatomical issues.

Management:
- Use saline nasal irrigation or nasal sprays
- Apply warm compresses to the face
- Breathe in steam from a hot shower
- Use over-the-counter decongestants for short periods (3-5 days)
- Take pain relievers for discomfort
- Stay hydrated and get plenty of rest

When to seek medical attention:
- Symptoms lasting more than 10 days
- Fever above 101°F (38.3°C)
- Severe headache or facial pain
- Multiple episodes of sinusitis within a year
- Symptoms that worsen after initial improvement

If caused by bacteria, you may need antibiotics from a healthcare provider."""
        },
        {
            "pattern": ["diarrhea", "abdominal_cramps", "bloating", "gas", "food_sensitivity"],
            "condition": "Irritable Bowel Syndrome (IBS)",
            "description": """Your symptoms suggest irritable bowel syndrome (IBS), a common disorder affecting the large intestine. IBS is a chronic condition that requires long-term management.

Management:
- Identify and avoid trigger foods (common triggers include dairy, wheat, citrus fruits, beans, cabbage, and carbonated drinks)
- Eat smaller meals more frequently
- Increase fiber intake gradually
- Stay well hydrated
- Manage stress through relaxation techniques
- Exercise regularly
- Consider probiotics
- Avoid caffeine and alcohol which can stimulate the intestines

When to seek medical attention:
- Weight loss
- Diarrhea that awakens you from sleep
- Rectal bleeding
- Iron deficiency anemia
- Persistent pain not relieved by passing gas or bowel movement
- Family history of colon cancer, inflammatory bowel disease, or celiac disease

A healthcare provider can help rule out other conditions and develop an appropriate treatment plan."""
        }
    ]
    
    # Combine all patterns
    all_patterns = symptom_patterns + additional_patterns
    
    # Convert symptoms to a set for easier matching
    symptom_set = set(symptoms)
    
    # Find the best matching pattern
    best_match = None
    highest_match_count = 0
    
    for pattern in all_patterns:
        pattern_set = set(pattern["pattern"])
        matching_symptoms = symptom_set.intersection(pattern_set)
        match_count = len(matching_symptoms)
        
        # If this pattern has more matching symptoms than our current best, update
        if match_count > highest_match_count and match_count >= 2:  # Need at least 2 matching symptoms
            highest_match_count = match_count
            best_match = pattern
    
    # If we found a good match, return its description
    if best_match:
        return f"""Based on your symptoms, you may be experiencing {best_match['condition']}.\n\n{best_match['description']}\n\nDISCLAIMER: This is not a professional medical diagnosis. If symptoms are severe or concerning, please consult a healthcare provider."""
    
    # If no good pattern match, generate a generic response based on individual symptoms
    response_parts = []
    response_parts.append("Based on the symptoms you've described, here's some information that may be helpful:")
    
    # Add information about each symptom (up to 5 for readability)
    for symptom in symptoms[:5]:
        clean_symptom = symptom.replace("_", " ")
        if symptom in common_symptoms:
            response_parts.append(f"\n- {clean_symptom.capitalize()}: {common_symptoms[symptom]}")
            
            # Add some general advice for common symptoms
            if symptom == "fever":
                response_parts.append("  For fever management: Rest, stay hydrated, and consider over-the-counter fever reducers. Seek medical attention for high fevers above 102°F (39°C) or fevers lasting more than three days.")
            elif symptom == "headache":
                response_parts.append("  For headache relief: Rest in a quiet, dark room, stay hydrated, and consider over-the-counter pain relievers. For severe or unusual headaches, consult a healthcare provider.")
            elif symptom == "cough":
                response_parts.append("  For cough management: Stay hydrated, use honey (if over 1 year old), and consider over-the-counter cough medications. Seek medical attention if cough is severe, produces colored mucus, or lasts more than two weeks.")
            elif symptom == "nausea" or symptom == "vomiting":
                response_parts.append("  For nausea/vomiting: Sip clear fluids slowly, avoid solid foods until nausea subsides, and try ginger tea. Seek medical attention if vomiting is severe or persistent.")
            elif symptom == "diarrhea":
                response_parts.append("  For diarrhea management: Stay hydrated with water and electrolyte solutions, eat bland foods, and avoid dairy, caffeine, and fatty foods. Seek medical attention if diarrhea is severe or lasts more than 2-3 days.")
    
    # Add general advice
    response_parts.append("\nGeneral recommendations:")
    response_parts.append("- Get plenty of rest to allow your body to recover")
    response_parts.append("- Stay hydrated by drinking plenty of fluids")
    response_parts.append("- Monitor your symptoms for any changes or worsening")
    response_parts.append("- Consider over-the-counter medications appropriate for your specific symptoms")
    
    # When to see a doctor
    response_parts.append("\nConsult a healthcare provider if:")
    response_parts.append("- Your symptoms are severe or getting worse")
    response_parts.append("- You have a high fever (above 102°F/39°C)")
    response_parts.append("- Your symptoms persist for more than a few days")
    response_parts.append("- You have chronic medical conditions or a compromised immune system")
    
    # Add disclaimer
    response_parts.append("\nDISCLAIMER: This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.")
    
    return "\n".join(response_parts)
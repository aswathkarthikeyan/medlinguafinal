"""
Serious Condition Analyzer Module

This module provides specialized analysis for potentially life-threatening or serious medical conditions
based on symptom input. It evaluates symptoms against known patterns of serious conditions and
provides urgency-based recommendations.
"""

# Dictionary mapping serious conditions to their symptoms, descriptions, and urgency levels
SERIOUS_CONDITIONS = {
    "myocardial_infarction": {
        "name": "Myocardial Infarction (Heart Attack)",
        "symptoms": ["chest_pain", "left_arm_pain", "shortness_of_breath", "sweating", "nausea", 
                    "jaw_pain", "upper_back_pain", "dizziness", "fatigue"],
        "description": "A heart attack occurs when blood flow to part of the heart is blocked, causing damage to heart muscle. Chest pain or discomfort is the most common symptom, often described as pressure, squeezing, or fullness. Pain may radiate to the jaw, neck, back, or arms (especially the left arm).",
        "urgency": "High",
        "match_threshold": 1,  # Make heart attack easy to trigger in potential risks section
        "required_symptoms": []  # No required symptoms when showing as potential risk
    },
    "stroke": {
        "name": "Stroke",
        "symptoms": ["sudden_numbness", "facial_drooping", "arm_weakness", "speech_difficulty", 
                    "sudden_confusion", "sudden_headache", "vision_problems", "dizziness", 
                    "loss_of_balance"],
        "description": "A stroke occurs when blood flow to the brain is interrupted, causing brain cells to die from lack of oxygen. The FAST acronym helps identify symptoms: Face drooping, Arm weakness, Speech difficulties, Time to call emergency services.",
        "urgency": "High",
        "match_threshold": 2
    },
    "pulmonary_embolism": {
        "name": "Pulmonary Embolism",
        "symptoms": ["sudden_shortness_of_breath", "chest_pain", "cough", "rapid_heartbeat", 
                    "sweating", "anxiety", "fainting", "coughing_up_blood"],
        "description": "A pulmonary embolism is a blockage in one of the pulmonary arteries in the lungs, often caused by blood clots that travel from the legs. Sudden shortness of breath and chest pain that worsens with deep breathing are key symptoms.",
        "urgency": "High",
        "match_threshold": 2
    },
    "sepsis": {
        "name": "Sepsis",
        "symptoms": ["fever", "high_fever", "chills", "rapid_breathing", "rapid_heartbeat", 
                    "confusion", "extreme_pain", "clammy_skin", "shortness_of_breath"],
        "description": "Sepsis is a life-threatening condition caused by the body's extreme response to an infection. It triggers a cascade of changes that can damage multiple organ systems. Early symptoms may include fever, increased heart rate, and rapid breathing.",
        "urgency": "High",
        "match_threshold": 3
    },
    "anaphylaxis": {
        "name": "Anaphylaxis (Severe Allergic Reaction)",
        "symptoms": ["hives", "itching", "swelling", "difficulty_breathing", "throat_tightness", 
                    "nausea", "vomiting", "dizziness", "fainting", "rapid_heartbeat"],
        "description": "Anaphylaxis is a severe, potentially life-threatening allergic reaction that can occur within seconds or minutes of exposure to an allergen. It causes the immune system to release chemicals that can lead to shock. Key symptoms include difficulty breathing, swelling of the throat, and a rapid drop in blood pressure.",
        "urgency": "High",
        "match_threshold": 3
    },
    "meningitis": {
        "name": "Meningitis",
        "symptoms": ["sudden_high_fever", "severe_headache", "stiff_neck", "nausea", "vomiting", 
                    "sensitivity_to_light", "confusion", "seizures", "rash"],
        "description": "Meningitis is an inflammation of the membranes surrounding the brain and spinal cord, often caused by bacterial or viral infection. The classic symptoms are sudden onset of high fever, severe headache, and stiff neck. Light sensitivity and confusion are also common.",
        "urgency": "High",
        "match_threshold": 3
    },
    "appendicitis": {
        "name": "Appendicitis",
        "symptoms": ["abdominal_pain", "right_lower_abdominal_pain", "nausea", "vomiting", 
                    "loss_of_appetite", "low_grade_fever", "abdominal_swelling"],
        "description": "Appendicitis is inflammation of the appendix, often causing pain that begins around the navel and shifts to the lower right abdomen. The pain typically worsens over 12-24 hours and is accompanied by nausea and vomiting.",
        "urgency": "Medium",
        "match_threshold": 2
    },
    "diabetic_ketoacidosis": {
        "name": "Diabetic Ketoacidosis (DKA)",
        "symptoms": ["excessive_thirst", "frequent_urination", "nausea", "vomiting", 
                    "abdominal_pain", "weakness", "fatigue", "fruity_breath", "confusion"],
        "description": "DKA is a serious complication of diabetes characterized by the body producing high levels of ketones due to insufficient insulin. It typically develops slowly but can become life-threatening quickly. Symptoms include excessive thirst, frequent urination, and a distinctive fruity odor to the breath.",
        "urgency": "Medium",
        "match_threshold": 3
    },
    "intracranial_hemorrhage": {
        "name": "Intracranial Hemorrhage",
        "symptoms": ["sudden_severe_headache", "altered_consciousness", "nausea", "vomiting", 
                    "stiff_neck", "seizures", "vision_changes", "difficulty_speaking", 
                    "weakness_on_one_side"],
        "description": "An intracranial hemorrhage is bleeding inside the skull that can result from trauma or occur spontaneously. A sudden, severe headache (often described as the 'worst headache ever') is a hallmark symptom, especially for subarachnoid hemorrhage.",
        "urgency": "High",
        "match_threshold": 2
    },
    "aortic_dissection": {
        "name": "Aortic Dissection",
        "symptoms": ["sudden_severe_chest_pain", "severe_back_pain", "severe_abdominal_pain", 
                    "shortness_of_breath", "weakness", "loss_of_consciousness", "sweating", 
                    "difficulty_speaking"],
        "description": "Aortic dissection occurs when the inner layer of the aorta tears, allowing blood to flow between the layers and forcing them apart. The classic symptom is sudden, severe chest or back pain described as ripping or tearing, often radiating to the back.",
        "urgency": "High",
        "match_threshold": 2
    },
    "bowel_obstruction": {
        "name": "Bowel Obstruction",
        "symptoms": ["abdominal_pain", "abdominal_cramping", "vomiting", "bloating", "inability_to_pass_gas", 
                    "constipation", "diarrhea", "loud_bowel_sounds", "abdominal_swelling"],
        "description": "Bowel obstruction occurs when something blocks the small or large intestine, preventing the normal passage of digestive contents. Symptoms include crampy abdominal pain, vomiting, and inability to pass gas or stool.",
        "urgency": "Medium",
        "match_threshold": 3
    },
    "pneumonia": {
        "name": "Pneumonia",
        "symptoms": ["cough", "fever", "shortness_of_breath", "chest_pain", "fatigue", 
                    "sweating", "chills", "nausea", "confusion"],
        "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid. Symptoms can range from mild to severe and include cough with phlegm, fever, chills, and difficulty breathing.",
        "urgency": "Medium",
        "match_threshold": 3
    },
    "acute_pancreatitis": {
        "name": "Acute Pancreatitis",
        "symptoms": ["upper_abdominal_pain", "abdominal_pain_radiating_to_back", "nausea", 
                    "vomiting", "fever", "rapid_pulse", "tenderness_when_touching_abdomen"],
        "description": "Acute pancreatitis is sudden inflammation of the pancreas that can cause excruciating pain. The pain is often in the upper abdomen and may radiate to the back. It frequently worsens after eating, especially foods high in fat.",
        "urgency": "Medium",
        "match_threshold": 2
    },
    "hypertensive_crisis": {
        "name": "Hypertensive Crisis",
        "symptoms": ["severe_headache", "shortness_of_breath", "nosebleeds", "severe_anxiety", 
                    "blurred_vision", "chest_pain", "confusion", "seizures"],
        "description": "A hypertensive crisis is a severe increase in blood pressure that can lead to a stroke or organ damage. Symptoms may include severe headache, shortness of breath, and nosebleeds. A systolic blood pressure reading over 180 or diastolic over 120 may indicate a crisis.",
        "urgency": "High",
        "match_threshold": 2
    },
    "severe_dehydration": {
        "name": "Severe Dehydration",
        "symptoms": ["extreme_thirst", "dry_mouth", "little_or_no_urination", "dark_urine", 
                    "sunken_eyes", "lethargy", "confusion", "lightheadedness", "rapid_heartbeat"],
        "description": "Severe dehydration occurs when the body loses too much fluid and electrolytes, disrupting normal functions. It can be life-threatening, especially in young children and elderly people. Signs include extreme thirst, minimal urination, and confusion.",
        "urgency": "Medium",
        "match_threshold": 3
    }
}

# Symptom keyword mapping for better matching with natural language descriptions
SYMPTOM_KEYWORDS = {
    "chest_pain": ["chest pain", "chest discomfort", "chest pressure", "chest tightness", "chest heaviness", "crushing pain"],
    "left_arm_pain": ["left arm pain", "arm pain", "pain radiating to arm", "left arm discomfort"],
    "shortness_of_breath": ["shortness of breath", "difficulty breathing", "can't breathe", "hard to breathe", "breathlessness", "trouble breathing"],
    "sudden_shortness_of_breath": ["sudden shortness of breath", "suddenly can't breathe", "abruptly hard to breathe"],
    "sweating": ["sweating", "cold sweat", "perspiration", "clammy", "diaphoresis"],
    "nausea": ["nausea", "feeling sick", "queasy", "want to vomit", "sick to stomach"],
    "jaw_pain": ["jaw pain", "pain in jaw", "jaw discomfort", "pain radiating to jaw"],
    "upper_back_pain": ["upper back pain", "pain between shoulder blades", "upper back discomfort"],
    "dizziness": ["dizziness", "lightheaded", "light headed", "feel faint", "vertigo", "room spinning"],
    "fatigue": ["fatigue", "extreme tiredness", "exhaustion", "no energy", "weakness"],
    "sudden_numbness": ["sudden numbness", "numbness", "can't feel", "loss of sensation", "tingling"],
    "facial_drooping": ["face drooping", "facial droop", "droopy face", "face dropped", "drooping mouth"],
    "arm_weakness": ["arm weakness", "weak arm", "can't lift arm", "arm feels heavy"],
    "speech_difficulty": ["speech difficulty", "slurred speech", "trouble speaking", "can't speak clearly", "words not coming out right"],
    "sudden_confusion": ["sudden confusion", "confused", "disoriented", "not making sense", "altered mental status"],
    "sudden_headache": ["sudden headache", "worst headache", "thunderclap headache", "explosive headache", "severe headache"],
    "vision_problems": ["vision problems", "blurred vision", "double vision", "loss of vision", "blind spot", "can't see"],
    "loss_of_balance": ["loss of balance", "unsteady", "can't stand", "falling over", "coordination problem", "unstable when walking"],
    "cough": ["cough", "coughing", "persistent cough", "dry cough", "hacking cough"],
    "coughing_up_blood": ["coughing up blood", "blood in phlegm", "blood in sputum", "hemoptysis"],
    "rapid_heartbeat": ["rapid heartbeat", "racing heart", "heart racing", "palpitations", "heart pounding", "fast pulse"],
    "fever": ["fever", "elevated temperature", "feeling hot", "high temperature", "feverish"],
    "high_fever": ["high fever", "temperature above 102", "very high temperature", "severe fever"],
    "chills": ["chills", "shivering", "feeling cold", "body shakes", "rigors"],
    "rapid_breathing": ["rapid breathing", "breathing fast", "shortness of breath", "hyperventilation", "tachypnea"],
    "confusion": ["confusion", "disoriented", "not making sense", "altered mental status", "delirium"],
    "extreme_pain": ["extreme pain", "worst pain", "severe pain", "agonizing pain", "excruciating pain"],
    "clammy_skin": ["clammy skin", "cold skin", "damp skin", "cold and sweaty"],
    "hives": ["hives", "welts", "raised bumps", "urticaria", "itchy rash"],
    "itching": ["itching", "itchiness", "scratchy", "pruritus"],
    "swelling": ["swelling", "puffiness", "edema", "bloating", "facial swelling", "swollen lips", "swollen tongue"],
    "difficulty_breathing": ["difficulty breathing", "shortness of breath", "can't breathe", "trouble breathing", "breathlessness"],
    "throat_tightness": ["throat tightness", "tight throat", "throat closing", "choking sensation", "throat swelling"],
    "vomiting": ["vomiting", "throwing up", "getting sick", "emesis"],
    "fainting": ["fainting", "passed out", "loss of consciousness", "blackout", "syncope"],
    "sudden_high_fever": ["sudden high fever", "fever that came on quickly", "rapid onset fever"],
    "severe_headache": ["severe headache", "terrible headache", "pounding headache", "throbbing head pain"],
    "stiff_neck": ["stiff neck", "neck stiffness", "can't bend neck", "painful to move neck", "rigid neck"],
    "sensitivity_to_light": ["sensitivity to light", "light hurts eyes", "photophobia", "light bothers me"],
    "seizures": ["seizures", "convulsions", "fits", "shaking episode", "epileptic episode"],
    "rash": ["rash", "skin outbreak", "red spots", "skin lesions", "spots on skin"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "belly pain", "stomach ache", "abdominal cramps"],
    "right_lower_abdominal_pain": ["right lower abdominal pain", "right lower quadrant pain", "pain in lower right abdomen", "pain in right side of abdomen"],
    "loss_of_appetite": ["loss of appetite", "not hungry", "don't want to eat", "anorexia", "no appetite"],
    "low_grade_fever": ["low grade fever", "slight fever", "mild fever", "temperature slightly elevated"],
    "abdominal_swelling": ["abdominal swelling", "stomach bloating", "belly distension", "swollen abdomen"],
    "excessive_thirst": ["excessive thirst", "very thirsty", "unquenchable thirst", "polydipsia"],
    "frequent_urination": ["frequent urination", "peeing a lot", "polyuria", "urinating often"],
    "fruity_breath": ["fruity breath", "sweet smelling breath", "acetone breath", "breath smells like fruit"],
    "sudden_severe_headache": ["sudden severe headache", "worst headache ever", "thunderclap headache", "explosive headache"],
    "altered_consciousness": ["altered consciousness", "decreased alertness", "stupor", "lethargy", "not responding normally"],
    "weakness_on_one_side": ["weakness on one side", "one-sided weakness", "hemiparesis", "weak on left/right side"],
    "sudden_severe_chest_pain": ["sudden severe chest pain", "ripping chest pain", "tearing pain in chest", "worst chest pain ever"],
    "severe_back_pain": ["severe back pain", "terrible back pain", "worst back pain", "ripping back pain", "tearing back pain"],
    "severe_abdominal_pain": ["severe abdominal pain", "terrible stomach pain", "worst abdominal pain", "excruciating belly pain"],
    "loss_of_consciousness": ["loss of consciousness", "passed out", "fainted", "blacked out", "syncope"],
    "abdominal_cramping": ["abdominal cramping", "stomach cramps", "belly cramps", "intestinal cramps"],
    "bloating": ["bloating", "feeling bloated", "distended abdomen", "swollen belly"],
    "inability_to_pass_gas": ["inability to pass gas", "can't pass gas", "can't fart", "no gas movement"],
    "constipation": ["constipation", "can't have bowel movement", "no bowel movement", "unable to defecate"],
    "diarrhea": ["diarrhea", "loose stools", "watery stools", "frequent bowel movements"],
    "loud_bowel_sounds": ["loud bowel sounds", "stomach gurgling", "abdominal noises", "hyperactive bowel sounds"],
    "chest_pain": ["chest pain", "chest discomfort", "chest pressure", "chest tightness"],
    "upper_abdominal_pain": ["upper abdominal pain", "pain in upper stomach", "epigastric pain", "pain below ribs"],
    "abdominal_pain_radiating_to_back": ["abdominal pain radiating to back", "stomach pain going to back", "belly pain extends to back"],
    "tenderness_when_touching_abdomen": ["tender abdomen", "pain when pressing on abdomen", "abdomen hurts to touch"],
    "severe_anxiety": ["severe anxiety", "extreme worry", "panic", "overwhelming fear"],
    "nosebleeds": ["nosebleeds", "bleeding from nose", "epistaxis"],
    "extreme_thirst": ["extreme thirst", "severe thirst", "insatiable thirst", "very thirsty"],
    "dry_mouth": ["dry mouth", "mouth dryness", "parched mouth", "not enough saliva"],
    "little_or_no_urination": ["little urination", "no urination", "not peeing", "oliguria", "anuria"],
    "dark_urine": ["dark urine", "concentrated urine", "dark yellow urine", "brown urine"],
    "sunken_eyes": ["sunken eyes", "eyes look hollow", "eyes seem receded"],
    "lethargy": ["lethargy", "excessive sleepiness", "hard to wake up", "unusually tired", "listless"]
}

# Additional patterns for condition recognition in natural language
CONDITION_PATTERNS = {
    "myocardial_infarction": ["heart attack", "cardiac arrest", "mi", "coronary", "heart pain"],
    "stroke": ["stroke", "brain attack", "cerebrovascular accident", "cva", "brain clot"],
    "pulmonary_embolism": ["pulmonary embolism", "pe", "lung clot", "blood clot in lung"],
    "sepsis": ["sepsis", "blood infection", "septic", "infection in blood"],
    "anaphylaxis": ["anaphylaxis", "anaphylactic", "severe allergic reaction", "allergy attack"],
    "meningitis": ["meningitis", "brain infection", "spinal infection", "meninges infection"],
    "appendicitis": ["appendicitis", "inflamed appendix", "appendix infection"],
    "diabetic_ketoacidosis": ["diabetic ketoacidosis", "dka", "ketoacidosis", "diabetic emergency"],
    "intracranial_hemorrhage": ["brain bleed", "intracranial hemorrhage", "bleeding in brain", "cerebral hemorrhage"],
    "aortic_dissection": ["aortic dissection", "torn aorta", "aortic tear", "aortic rupture"],
    "bowel_obstruction": ["bowel obstruction", "intestinal blockage", "blocked intestine", "intestinal obstruction"],
    "pneumonia": ["pneumonia", "lung infection", "chest infection", "bronchopneumonia"],
    "acute_pancreatitis": ["pancreatitis", "inflamed pancreas", "pancreas inflammation"],
    "hypertensive_crisis": ["hypertensive crisis", "hypertensive emergency", "blood pressure emergency", "malignant hypertension"],
    "severe_dehydration": ["dehydration", "severe dehydration", "fluid loss", "not enough fluids"]
}


def detect_serious_symptoms(transcript):
    """
    Detect symptoms in transcript that might indicate serious or life-threatening conditions
    
    Args:
        transcript: The patient's description of their symptoms
        
    Returns:
        dict: Detected symptoms mapped to their standardized names
    """
    transcript_lower = transcript.lower()
    detected_symptoms = {}
    
    # Check for symptom keywords in transcript
    for symptom_key, keyword_list in SYMPTOM_KEYWORDS.items():
        for keyword in keyword_list:
            if keyword.lower() in transcript_lower:
                detected_symptoms[symptom_key] = keyword
                break
    
    return detected_symptoms


def detect_mentioned_conditions(transcript):
    """
    Detect if any specific conditions are mentioned directly in the transcript
    
    Args:
        transcript: The patient's description of their symptoms
        
    Returns:
        list: Conditions mentioned in the transcript
    """
    transcript_lower = transcript.lower()
    mentioned_conditions = []
    
    for condition_key, pattern_list in CONDITION_PATTERNS.items():
        for pattern in pattern_list:
            if pattern.lower() in transcript_lower:
                mentioned_conditions.append(condition_key)
                break
    
    return mentioned_conditions


def analyze_serious_conditions(transcript, language="en"):
    """
    Analyze transcript for potential serious or life-threatening conditions,
    with additional priority placed on specific life-threatening conditions
    
    Args:
        transcript: The patient's description of their symptoms
        language: Language code (en, ta, hi)
        
    Returns:
        list: List of dictionaries containing condition information
    """
    # Detect symptoms and directly mentioned conditions
    detected_symptoms = detect_serious_symptoms(transcript)
    mentioned_conditions = detect_mentioned_conditions(transcript)
    
    # Match symptoms to serious conditions
    matched_conditions = {}
    
    # First check for explicitly mentioned conditions
    for condition_key in mentioned_conditions:
        if condition_key in SERIOUS_CONDITIONS:
            matched_conditions[condition_key] = {
                "name": SERIOUS_CONDITIONS[condition_key]["name"],
                "description": SERIOUS_CONDITIONS[condition_key]["description"],
                "urgency": SERIOUS_CONDITIONS[condition_key]["urgency"],
                "match_score": 5,  # High score for directly mentioned conditions
                "matching_symptoms": []
            }
    
    # Then check for symptom-based matches
    for condition_key, condition_data in SERIOUS_CONDITIONS.items():
        if condition_key in matched_conditions:
            continue  # Skip if already added from direct mentions
        
        matching_symptoms = []
        for symptom in condition_data["symptoms"]:
            if symptom in detected_symptoms:
                matching_symptoms.append(symptom)
        
        # Basic match score is the number of matching symptoms
        match_score = len(matching_symptoms)
        
        # Boost score for priority life-threatening conditions
        priority_conditions = ["myocardial_infarction", "stroke", "pulmonary_embolism", 
                              "sepsis", "anaphylaxis", "intracranial_hemorrhage"]
        if condition_key in priority_conditions and match_score > 0:
            match_score += 3  # Significant boost for life-threatening conditions
        
        # Check if the condition requires specific symptoms to be present
        required_symptoms_present = True
        if "required_symptoms" in condition_data:
            required_symptoms_present = all(symptom in matching_symptoms for symptom in condition_data["required_symptoms"])
        
        # Only consider conditions that meet the threshold AND have all required symptoms if specified
        if match_score >= condition_data["match_threshold"] and required_symptoms_present:
            matched_conditions[condition_key] = {
                "name": condition_data["name"],
                "description": condition_data["description"],
                "urgency": condition_data["urgency"],
                "match_score": match_score,
                "matching_symptoms": matching_symptoms
            }
    
    # Sort conditions by urgency and match score
    sorted_conditions = sorted(
        matched_conditions.values(), 
        key=lambda x: (0 if x["urgency"] == "High" else (1 if x["urgency"] == "Medium" else 2), -x["match_score"])
    )
    
    # Special case for "left hand pain" or "left arm pain" + other cardiac symptoms -> consider heart attack
    transcript_lower = transcript.lower()
    if ("left hand" in transcript_lower or "left arm" in transcript_lower) and "pain" in transcript_lower:
        # Only add heart attack if there are other cardiac symptoms present
        cardiac_symptoms = ["chest", "breath", "dizz", "nausea", "sweat", "pressure"]
        has_other_cardiac_symptoms = any(symptom in transcript_lower for symptom in cardiac_symptoms)
        
        if has_other_cardiac_symptoms:
            # Check if myocardial_infarction is already in the list
            if not any(c.get("name") == "Myocardial Infarction (Heart Attack)" for c in sorted_conditions):
                # Add heart attack as a potential serious condition
                sorted_conditions.insert(0, {
                    "name": "Myocardial Infarction (Heart Attack)",
                    "description": "A heart attack occurs when blood flow to part of the heart is blocked, causing damage to heart muscle. Pain radiating to the left arm or hand can be a key symptom, especially when accompanied by chest discomfort, shortness of breath, or dizziness.",
                    "urgency": "High",
                    "match_score": 5,
                    "matching_symptoms": ["left_arm_pain"]
                })
    
    return sorted_conditions[:3]


def generate_serious_condition_analysis(transcript, language="en"):
    """
    Generate a formatted analysis of potential serious conditions based on symptoms,
    prioritizing life-threatening or serious conditions with concise, focused outputs.
    
    Args:
        transcript: The patient's description of their symptoms
        language: Language code (en, ta, hi)
        
    Returns:
        str: Formatted analysis text
    """
    conditions = analyze_serious_conditions(transcript, language)
    
    # Take only top 1-2 conditions with highest urgency
    if conditions:
        # Sort by urgency first (High > Medium > Low), then by match score
        conditions = sorted(
            conditions, 
            key=lambda x: (0 if x["urgency"] == "High" else (1 if x["urgency"] == "Medium" else 2), -x["match_score"])
        )
        # Limit to top 2 conditions
        conditions = conditions[:2]
    
    if not conditions:
        if language == "en":
            return "Based on the symptoms provided, no specific life-threatening conditions were identified.\n\n*This is not a professional diagnosis. Please consult a licensed medical professional for accurate evaluation.*"
        elif language == "ta":
            return "வழங்கப்பட்ட அறிகுறிகளின் அடிப்படையில், எந்த குறிப்பிட்ட உயிருக்கு ஆபத்தான நிலைமைகளும் கண்டறியப்படவில்லை.\n\n*இது ஒரு தொழில்முறை மருத்துவ ஆலோசனை அல்ல. துல்லியமான மதிப்பீட்டிற்கு உரிமம் பெற்ற மருத்துவ நிபுணரை அணுகவும்.*"
        elif language == "hi":
            return "प्रदान किए गए लक्षणों के आधार पर, कोई विशिष्ट जीवन के लिए खतरनाक स्थितियों की पहचान नहीं की गई।\n\n*यह एक पेशेवर निदान नहीं है। कृपया सटीक मूल्यांकन के लिए लाइसेंस प्राप्त चिकित्सा पेशेवर से परामर्श करें।*"
        else:
            return "Based on the symptoms provided, no specific life-threatening conditions were identified.\n\n*This is not a professional diagnosis. Please consult a licensed medical professional for accurate evaluation.*"
    
    # Generate text based on language
    if language == "en":
        result = "Based on your symptoms, potential serious condition"
        result += "s" if len(conditions) > 1 else ""
        result += " include:\n\n"
        
        for condition in conditions:
            result += f"**{condition['name']}**. "
            result += f"{condition['description']}\n\n"
        
        result += "*This is not a professional diagnosis. Please consult a licensed medical professional for accurate evaluation.*"
        
    elif language == "ta":
        result = "உங்கள் அறிகுறிகளின் அடிப்படையில், சாத்தியமான தீவிர நிலைமை"
        result += "கள்" if len(conditions) > 1 else ""
        result += ":\n\n"
        
        for condition in conditions:
            result += f"**{condition['name']}**. "
            result += f"{condition['description']}\n\n"
        
        result += "*இது ஒரு தொழில்முறை மருத்துவ ஆலோசனை அல்ல. துல்லியமான மதிப்பீட்டிற்கு உரிமம் பெற்ற மருத்துவ நிபுணரை அணுகவும்.*"
        
    elif language == "hi":
        result = "आपके लक्षणों के आधार पर, संभावित गंभीर स्थिति"
        result += "यां" if len(conditions) > 1 else ""
        result += ":\n\n"
        
        for condition in conditions:
            result += f"**{condition['name']}**. "
            result += f"{condition['description']}\n\n"
        
        result += "*यह एक पेशेवर निदान नहीं है। कृपया सटीक मूल्यांकन के लिए लाइसेंस प्राप्त चिकित्सा पेशेवर से परामर्श करें।*"
        
    else:
        # Default to English for unsupported languages
        result = "Based on your symptoms, potential serious condition"
        result += "s" if len(conditions) > 1 else ""
        result += " include:\n\n"
        
        for condition in conditions:
            result += f"**{condition['name']}**. "
            result += f"{condition['description']}\n\n"
        
        result += "*This is not a professional diagnosis. Please consult a licensed medical professional for accurate evaluation.*"
    
    return result
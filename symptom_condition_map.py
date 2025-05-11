"""
Extensive symptom-to-condition mapping for more specific diagnosis when direct model output
is not confident enough.
"""

# Dictionary mapping specific symptoms to possible conditions with confidence scores
SYMPTOM_CONDITION_MAP = {
    # Hand/arm symptoms
    "hand_pain": {
        "carpal_tunnel_syndrome": 0.7,
        "arthritis": 0.6,
        "tendonitis": 0.5,
        "fracture": 0.4,
        "repetitive_strain_injury": 0.6,
        "nerve_compression": 0.5
    },
    "left_hand_pain": {
        "carpal_tunnel_syndrome": 0.6,
        "arthritis": 0.6,
        "tendonitis": 0.5,
        "ulnar_nerve_entrapment": 0.5,
        "cubital_tunnel_syndrome": 0.5
    },
    "right_hand_pain": {
        "carpal_tunnel_syndrome": 0.6,
        "arthritis": 0.6,
        "tendonitis": 0.5,
        "de_quervains_tenosynovitis": 0.4
    },
    "wrist_pain": {
        "carpal_tunnel_syndrome": 0.8,
        "arthritis": 0.6,
        "tendonitis": 0.7,
        "ganglion_cyst": 0.5,
        "sprain": 0.6
    },
    "finger_pain": {
        "trigger_finger": 0.7,
        "arthritis": 0.7,
        "fracture": 0.5,
        "gout": 0.4,
        "paronychia": 0.4
    },
    "elbow_pain": {
        "tennis_elbow": 0.7,
        "golfers_elbow": 0.6,
        "arthritis": 0.5,
        "bursitis": 0.6,
        "olecranon_fracture": 0.3
    },
    "arm_pain": {
        "muscle_strain": 0.6,
        "tendonitis": 0.5,
        "nerve_impingement": 0.5,
        "humerus_fracture": 0.3,
        "angina": 0.3  # Left arm pain can be a cardiac symptom
    },
    
    # Head/face symptoms
    "headache": {
        "tension_headache": 0.7,
        "migraine": 0.6,
        "cluster_headache": 0.4,
        "sinus_headache": 0.5,
        "hypertension": 0.3,
        "brain_tumor": 0.1
    },
    "severe_headache": {
        "migraine": 0.7,
        "intracranial_hemorrhage": 0.3,
        "meningitis": 0.4,
        "brain_aneurysm": 0.2,
        "temporal_arteritis": 0.3
    },
    "facial_pain": {
        "sinusitis": 0.6,
        "trigeminal_neuralgia": 0.5,
        "tmj_disorder": 0.6,
        "dental_abscess": 0.5,
        "facial_cellulitis": 0.3
    },
    
    # Chest symptoms
    "chest_pain": {
        "angina": 0.6,
        "myocardial_infarction": 0.5,
        "costochondritis": 0.5,
        "acid_reflux": 0.4,
        "pneumonia": 0.3,
        "pulmonary_embolism": 0.3,
        "anxiety": 0.4
    },
    "left_chest_pain": {
        "angina": 0.7,
        "myocardial_infarction": 0.6,
        "pericarditis": 0.4,
        "costochondritis": 0.4
    },
    "difficulty_breathing": {
        "asthma": 0.7,
        "copd": 0.6,
        "pneumonia": 0.6,
        "pulmonary_embolism": 0.4,
        "heart_failure": 0.4,
        "anxiety": 0.5,
        "allergic_reaction": 0.5
    },
    
    # Abdominal symptoms
    "abdominal_pain": {
        "gastritis": 0.6,
        "appendicitis": 0.4,
        "ulcers": 0.5,
        "ibs": 0.6,
        "gallstones": 0.5,
        "kidney_stones": 0.4,
        "diverticulitis": 0.4,
        "pancreatitis": 0.3
    },
    "right_abdominal_pain": {
        "appendicitis": 0.7,
        "gallbladder_disease": 0.6,
        "hepatitis": 0.4,
        "kidney_stones": 0.4,
        "ibs": 0.4
    },
    "left_abdominal_pain": {
        "diverticulitis": 0.6,
        "kidney_stones": 0.5,
        "pancreatitis": 0.4,
        "splenic_injury": 0.3,
        "ibs": 0.4
    },
    "upper_abdominal_pain": {
        "gastritis": 0.7,
        "peptic_ulcer": 0.6,
        "acid_reflux": 0.6,
        "pancreatitis": 0.5,
        "gallbladder_disease": 0.5
    },
    "lower_abdominal_pain": {
        "appendicitis": 0.5,
        "diverticulitis": 0.5,
        "urinary_tract_infection": 0.6,
        "ibs": 0.6,
        "inflammatory_bowel_disease": 0.5,
        "ovarian_cyst": 0.4,
        "ectopic_pregnancy": 0.3
    },
    
    # Back symptoms
    "back_pain": {
        "muscle_strain": 0.7,
        "herniated_disc": 0.5,
        "sciatica": 0.5,
        "arthritis": 0.5,
        "kidney_infection": 0.4,
        "kidney_stones": 0.4,
        "ankylosing_spondylitis": 0.3
    },
    "upper_back_pain": {
        "muscle_strain": 0.7,
        "poor_posture": 0.6,
        "herniated_disc": 0.4,
        "osteoarthritis": 0.4,
        "vertebral_compression_fracture": 0.3
    },
    "lower_back_pain": {
        "muscle_strain": 0.6,
        "herniated_disc": 0.6,
        "sciatica": 0.6,
        "spinal_stenosis": 0.5,
        "arthritis": 0.4,
        "kidney_infection": 0.3
    },
    
    # Leg symptoms
    "leg_pain": {
        "muscle_strain": 0.6,
        "sciatica": 0.5,
        "peripheral_artery_disease": 0.4,
        "deep_vein_thrombosis": 0.4,
        "arthritis": 0.5,
        "fracture": 0.3
    },
    "knee_pain": {
        "osteoarthritis": 0.7,
        "meniscus_tear": 0.6,
        "acl_injury": 0.5,
        "patellofemoral_pain_syndrome": 0.6,
        "bursitis": 0.5,
        "gout": 0.3
    },
    "ankle_pain": {
        "sprain": 0.7,
        "fracture": 0.5,
        "tendonitis": 0.6,
        "arthritis": 0.4,
        "gout": 0.3
    },
    "foot_pain": {
        "plantar_fasciitis": 0.7,
        "fracture": 0.4,
        "gout": 0.4,
        "arthritis": 0.5,
        "bunion": 0.5,
        "morton_neuroma": 0.4
    },
    
    # Throat/neck symptoms
    "sore_throat": {
        "pharyngitis": 0.7,
        "tonsillitis": 0.6,
        "strep_throat": 0.6,
        "common_cold": 0.5,
        "flu": 0.4,
        "mononucleosis": 0.3
    },
    "neck_pain": {
        "muscle_strain": 0.7,
        "cervical_spondylosis": 0.5,
        "herniated_disc": 0.5,
        "meningitis": 0.2,
        "lymphadenopathy": 0.3
    },
    
    # Ear symptoms
    "ear_pain": {
        "ear_infection": 0.7,
        "swimmers_ear": 0.5,
        "eustachian_tube_dysfunction": 0.5,
        "temporomandibular_joint_disorder": 0.4,
        "ear_trauma": 0.3
    },
    "hearing_loss": {
        "ear_wax_buildup": 0.5,
        "ear_infection": 0.5,
        "age_related_hearing_loss": 0.6,
        "acoustic_neuroma": 0.2,
        "menieres_disease": 0.4,
        "ototoxic_medications": 0.3
    },
    
    # Eye symptoms
    "eye_pain": {
        "corneal_abrasion": 0.6,
        "conjunctivitis": 0.6,
        "glaucoma": 0.5,
        "uveitis": 0.4,
        "foreign_body": 0.5,
        "sinusitis": 0.3
    },
    "blurred_vision": {
        "refractive_error": 0.6,
        "cataracts": 0.5,
        "diabetes": 0.4,
        "glaucoma": 0.4,
        "migraine": 0.4,
        "hypertension": 0.3,
        "retinal_detachment": 0.3
    },
    
    # General symptoms
    "fever": {
        "viral_infection": 0.7,
        "bacterial_infection": 0.6,
        "common_cold": 0.5,
        "flu": 0.6,
        "covid19": 0.5,
        "urinary_tract_infection": 0.4
    },
    "fatigue": {
        "anemia": 0.5,
        "depression": 0.5,
        "hypothyroidism": 0.5,
        "chronic_fatigue_syndrome": 0.4,
        "sleep_apnea": 0.5,
        "diabetes": 0.4,
        "heart_failure": 0.3
    },
    "dizziness": {
        "vertigo": 0.6,
        "inner_ear_problems": 0.6,
        "low_blood_pressure": 0.5,
        "anemia": 0.4,
        "anxiety": 0.4,
        "vestibular_migraine": 0.4,
        "stroke": 0.2
    },
    "nausea": {
        "gastroenteritis": 0.8,
        "food_poisoning": 0.8,
        "migraine": 0.6,
        "pregnancy": 0.5,
        "vestibular_disorders": 0.5,
        "medication_side_effect": 0.6,
        "stomach_flu": 0.7,
        "morning_sickness": 0.6,
        "motion_sickness": 0.6,
        "labyrinthitis": 0.5
    },
    "vomiting": {
        "gastroenteritis": 0.9,
        "food_poisoning": 0.9,
        "stomach_flu": 0.8,
        "migraine": 0.5,
        "labyrinthitis": 0.5,
        "morning_sickness": 0.7,
        "appendicitis": 0.4,
        "concussion": 0.4,
        "alcohol_poisoning": 0.7,
        "medication_side_effect": 0.6
    },
    "vomit": {
        "gastroenteritis": 0.9,
        "food_poisoning": 0.9,
        "stomach_flu": 0.8,
        "migraine": 0.5,
        "labyrinthitis": 0.5,
        "morning_sickness": 0.7,
        "appendicitis": 0.4,
        "concussion": 0.4,
        "alcohol_poisoning": 0.7,
        "medication_side_effect": 0.6
    },
    "joint_pain": {
        "osteoarthritis": 0.7,
        "rheumatoid_arthritis": 0.6,
        "gout": 0.5,
        "lupus": 0.4,
        "lyme_disease": 0.3,
        "viral_infection": 0.4
    }
}

# Descriptions of conditions for better understanding
CONDITION_DESCRIPTIONS = {
    "carpal_tunnel_syndrome": "Pressure on the median nerve in the wrist causing pain, numbness, and tingling in the hand and fingers, particularly the thumb, index, middle, and ring fingers.",
    "arthritis": "Inflammation of joints causing pain, stiffness, and reduced range of motion. Common types include osteoarthritis and rheumatoid arthritis.",
    "tendonitis": "Inflammation of tendons (tissues connecting muscles to bones) resulting from repetitive movements or injury.",
    "fracture": "A break in a bone, often causing severe pain, swelling, bruising, and difficulty using the affected area.",
    "repetitive_strain_injury": "Damage to muscles, nerves, and tendons caused by repetitive movements, often affecting the hands, wrists, and forearms.",
    "ulnar_nerve_entrapment": "Compression of the ulnar nerve, which runs along the inner side of the elbow, causing numbness and tingling in the ring and little fingers.",
    "trigger_finger": "A condition where a finger gets stuck in a bent position and then straightens with a snap, like a trigger being pulled and released.",
    "tennis_elbow": "Inflammation of the tendons joining the forearm muscles to the outside of the elbow, commonly caused by overuse.",
    "migraine": "Recurring headaches of moderate to severe intensity, often with nausea, vomiting, and sensitivity to light and sound.",
    "tension_headache": "Mild to moderate pain that feels like a tight band around the head, often related to stress or muscle tension.",
    "sinusitis": "Inflammation of the sinus lining causing facial pain, pressure, congestion, and sometimes headache.",
    "anemia": "A condition where you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues, causing fatigue, weakness, and pale skin.",
    "angina": "Chest pain caused by reduced blood flow to the heart, often described as pressure, squeezing, or fullness.",
    "myocardial_infarction": "Heart attack, caused by blocked blood flow to the heart muscle, often featuring chest pain, shortness of breath, and nausea.",
    "costochondritis": "Inflammation of the cartilage connecting ribs to the breastbone, causing chest pain that may mimic a heart attack.",
    "appendicitis": "Inflammation of the appendix causing pain that typically starts around the navel and shifts to the lower right abdomen.",
    "gallbladder_disease": "Problems affecting the gallbladder, often causing pain in the upper right abdomen, especially after eating fatty foods.",
    "kidney_stones": "Hard deposits of minerals and salts that form in the kidneys and can cause severe pain when passing through the urinary tract.",
    "sciatica": "Pain that radiates along the sciatic nerve, which runs from the lower back through the hips and down each leg.",
    "herniated_disc": "A problem with a rubbery disc between the spinal bones, causing pain, numbness, or weakness in an arm or leg.",
    "plantar_fasciitis": "Inflammation of the thick band of tissue that runs across the bottom of the foot, causing heel pain.",
    "strep_throat": "Bacterial infection causing throat pain and difficulty swallowing, often with fever and swollen lymph nodes.",
    "conjunctivitis": "Pink eye, inflammation of the transparent membrane that lines the eyelid and eyeball, causing redness and irritation.",
    "vertigo": "A sensation of spinning or movement when there is no actual movement, often caused by inner ear problems.",
    "gastroenteritis": "Inflammation of the lining of the intestines caused by a virus, bacteria, or parasites, often causing diarrhea and vomiting.",
    "food_poisoning": "Illness caused by consuming contaminated food or drink, typically resulting in vomiting, diarrhea, abdominal pain, and sometimes fever.",
    "stomach_flu": "Viral infection affecting the stomach and intestines, causing nausea, vomiting, diarrhea, and abdominal cramping.",
    "morning_sickness": "Nausea and vomiting that occurs during pregnancy, typically in the first trimester.",
    "motion_sickness": "A feeling of nausea and dizziness that can occur when traveling in a car, boat, plane, or other moving vehicle.",
    "labyrinthitis": "An inner ear infection or inflammation that can cause dizziness, nausea, and balance problems."
}

# Comprehensive multilingual translations of common condition terms
CONDITION_TRANSLATIONS = {
    "carpal_tunnel_syndrome": {
        "en": "Carpal Tunnel Syndrome",
        "ta": "கார்பல் டனல் சிண்ட்ரோம்",
        "hi": "कार्पल टनल सिंड्रोम"
    },
    "arthritis": {
        "en": "Arthritis",
        "ta": "மூட்டுவலி",
        "hi": "गठिया रोग"
    },
    "tendonitis": {
        "en": "Tendonitis",
        "ta": "டெண்டனைடிஸ்",
        "hi": "टेंडनाइटिस"
    },
    "fracture": {
        "en": "Fracture",
        "ta": "எலும்பு முறிவு",
        "hi": "फ्रैक्चर"
    },
    "migraine": {
        "en": "Migraine",
        "ta": "ஒற்றைத் தலைவலி",
        "hi": "माइग्रेन"
    },
    "sinusitis": {
        "en": "Sinusitis",
        "ta": "சைனசைடிஸ்",
        "hi": "साइनसाइटिस"
    },
    "heart_attack": {
        "en": "Heart Attack",
        "ta": "இதயத் தாக்கம்",
        "hi": "दिल का दौरा"
    },
    "appendicitis": {
        "en": "Appendicitis",
        "ta": "குடல்வால் அழற்சி",
        "hi": "अपेंडिसाइटिस"
    },
    "kidney_stones": {
        "en": "Kidney Stones",
        "ta": "சிறுநீரக கற்கள்",
        "hi": "किडनी स्टोन"
    },
    "herniated_disc": {
        "en": "Herniated Disc",
        "ta": "முதுகெலும்பு தட்டு விலகல்",
        "hi": "हर्निएटेड डिस्क"
    },
    "anemia": {
        "en": "Anemia",
        "ta": "இரத்த சோகை",
        "hi": "एनीमिया"
    }
}

# Treatment recommendations by condition
TREATMENT_RECOMMENDATIONS = {
    "carpal_tunnel_syndrome": [
        "Wear a wrist splint during activities or at night",
        "Take short breaks during repetitive activities",
        "Apply cold packs to reduce swelling",
        "Over-the-counter pain relievers may help"
    ],
    "arthritis": [
        "Gentle exercise like swimming or walking",
        "Apply hot or cold packs to reduce pain",
        "Over-the-counter anti-inflammatory medications",
        "Maintain a healthy weight to reduce joint stress"
    ],
    "tendonitis": [
        "Rest the affected area",
        "Apply ice to reduce inflammation",
        "Compression bandages can reduce swelling",
        "Consider over-the-counter anti-inflammatory medications"
    ],
    "migraine": [
        "Rest in a quiet, dark room",
        "Apply a cold compress to the forehead",
        "Stay hydrated and consider over-the-counter pain relievers",
        "Identify and avoid personal migraine triggers"
    ],
    "tension_headache": [
        "Practice stress management techniques",
        "Maintain good posture",
        "Try gentle massage of the neck and temples",
        "Over-the-counter pain relievers may help"
    ],
    "sinusitis": [
        "Use a saline nasal spray to rinse sinuses",
        "Apply warm compresses to the face",
        "Stay hydrated to thin mucus",
        "Consider over-the-counter decongestants"
    ],
    "anemia": [
        "Increase iron-rich foods in your diet (red meat, leafy greens, beans)",
        "Take vitamin C with iron-rich foods to improve absorption",
        "Consider iron supplements if recommended by a doctor",
        "Get adequate vitamin B12 and folate from diet or supplements"
    ],
    "gastroenteritis": {
        "home_remedies": [
            "Stay hydrated with water, clear broths, or oral rehydration solutions",
            "Rest and avoid solid foods for a few hours",
            "Gradually reintroduce bland foods like rice, toast, and bananas",
            "Avoid dairy, caffeine, alcohol, and fatty foods until recovered",
            "Use a heating pad on low setting for abdominal discomfort"
        ],
        "medical_treatments": [
            "Anti-diarrheal medications (if not caused by certain bacteria)",
            "Anti-nausea medications to prevent vomiting",
            "Probiotics to restore gut flora",
            "Prescription antibiotics if caused by bacterial infection",
            "Intravenous (IV) fluids in severe cases of dehydration"
        ],
        "when_to_visit": [
            "If unable to keep fluids down for 24 hours",
            "If vomiting has continued for more than 2 days",
            "If diarrhea has continued for more than 5 days",
            "If there is blood in vomit or stool",
            "If there are signs of dehydration (extreme thirst, dry mouth, little or no urination)",
            "EMERGENCY: If experiencing severe abdominal pain"
        ]
    },
    "food_poisoning": {
        "home_remedies": [
            "Drink plenty of fluids to prevent dehydration",
            "Rest to help your body fight the infection",
            "Avoid solid foods until vomiting stops",
            "Gradually eat bland, low-fat foods like toast and rice",
            "Avoid dairy, caffeine, alcohol, and fatty foods"
        ],
        "medical_treatments": [
            "Anti-diarrheal medications for non-severe cases",
            "Anti-nausea medications to control vomiting",
            "Antibiotics if caused by certain bacteria",
            "IV fluids for severe dehydration",
            "Hospitalization in severe cases"
        ],
        "when_to_visit": [
            "If symptoms last more than 3 days",
            "If unable to keep liquids down",
            "If you see blood in your vomit or stool",
            "If you have a fever above 101.5°F (38.6°C)",
            "EMERGENCY: If experiencing severe abdominal pain or cramps",
            "EMERGENCY: If showing signs of severe dehydration (extreme thirst, very dry mouth, little or no urination)"
        ]
    },
    "stomach_flu": {
        "home_remedies": [
            "Get plenty of rest to help your body recover",
            "Stay hydrated with water, broth, or oral rehydration solutions",
            "Eat small, bland meals when appetite returns",
            "Try ginger or peppermint tea to calm nausea",
            "Use a heating pad on low setting for abdominal comfort"
        ],
        "medical_treatments": [
            "Anti-nausea medications to control vomiting",
            "Anti-diarrheal medications (if appropriate)",
            "IV fluids if dehydration is severe",
            "Probiotics to restore healthy gut bacteria"
        ],
        "when_to_visit": [
            "If symptoms persist for more than a few days",
            "If you can't keep fluids down for 24 hours",
            "If experiencing high fever (102°F or higher)",
            "If there is blood in vomit or stool",
            "EMERGENCY: If showing signs of dehydration (extreme thirst, dark urine, dizziness)"
        ]
    }
}


def get_specific_conditions(symptoms, transcript):
    """
    Get specific conditions based on symptoms detected in transcript
    
    Args:
        symptoms (list): List of detected symptom keywords
        transcript (str): Original symptom description
        
    Returns:
        dict: Conditions with confidence scores
    """
    # Convert transcript to lowercase for searching
    transcript_lower = transcript.lower()
    
    # Initialize dictionary for conditions
    conditions_dict = {}
    
    # First check for directional/specific symptoms in transcript
    directional_patterns = {
        "left_hand": ["left hand", "left palm", "left arm hand"],
        "right_hand": ["right hand", "right palm", "right arm hand"],
        "left_arm": ["left arm", "left elbow", "left shoulder"],
        "right_arm": ["right arm", "right elbow", "right shoulder"],
        "left_leg": ["left leg", "left thigh", "left calf"],
        "right_leg": ["right leg", "right thigh", "right calf"],
        "left_chest": ["left chest", "left side chest", "left breast"],
        "right_chest": ["right chest", "right side chest", "right breast"],
        "upper_back": ["upper back", "shoulder blade", "between shoulder"],
        "lower_back": ["lower back", "lumbar", "back waist"],
        "left_back": ["left side back", "left back"],
        "right_back": ["right side back", "right back"],
        "right_abdomen": ["right side abdomen", "right stomach", "right side stomach"],
        "left_abdomen": ["left side abdomen", "left stomach", "left side stomach"],
        "upper_abdomen": ["upper abdomen", "upper stomach", "epigastric"],
        "lower_abdomen": ["lower abdomen", "lower stomach", "below belly button"]
    }
    
    # Check for directional patterns in transcript
    for specific_symptom, patterns in directional_patterns.items():
        for pattern in patterns:
            if pattern in transcript_lower:
                # Get base symptom (removing left/right/upper/lower part)
                parts = specific_symptom.split("_")
                if len(parts) > 1:
                    base_symptom = parts[1] + "_pain"  # e.g., hand_pain, arm_pain
                    specific_symptom_key = parts[0] + "_" + base_symptom  # e.g., left_hand_pain
                    
                    # Check if specific symptom exists in our map
                    if specific_symptom_key in SYMPTOM_CONDITION_MAP:
                        for condition, confidence in SYMPTOM_CONDITION_MAP[specific_symptom_key].items():
                            if condition not in conditions_dict:
                                conditions_dict[condition] = confidence
                            else:
                                conditions_dict[condition] += confidence
                    
                    # Also check base symptom
                    if base_symptom in SYMPTOM_CONDITION_MAP:
                        for condition, confidence in SYMPTOM_CONDITION_MAP[base_symptom].items():
                            if condition not in conditions_dict:
                                conditions_dict[condition] = confidence * 0.8  # Lower confidence for general symptom
                            else:
                                conditions_dict[condition] += confidence * 0.5
    
    # Check for symptoms in our standard symptoms list
    for symptom in symptoms:
        if symptom in SYMPTOM_CONDITION_MAP:
            for condition, confidence in SYMPTOM_CONDITION_MAP[symptom].items():
                if condition not in conditions_dict:
                    conditions_dict[condition] = confidence
                else:
                    conditions_dict[condition] += confidence * 0.7  # Reduce weight for duplicate additions
    
    # Sort conditions by confidence
    sorted_conditions = sorted(conditions_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Return the top conditions
    return {condition: confidence for condition, confidence in sorted_conditions[:5]}


def get_condition_info(condition_name, lang="en"):
    """
    Get detailed information about a condition
    
    Args:
        condition_name: Name of the condition
        lang: Language code
        
    Returns:
        dict: Condition information including description and treatments
    """
    condition_info = {}
    
    # Get condition description
    if condition_name in CONDITION_DESCRIPTIONS:
        condition_info["description"] = CONDITION_DESCRIPTIONS[condition_name]
    
    # Get condition name in specified language
    if condition_name in CONDITION_TRANSLATIONS:
        if lang in CONDITION_TRANSLATIONS[condition_name]:
            condition_info["name"] = CONDITION_TRANSLATIONS[condition_name][lang]
        else:
            condition_info["name"] = CONDITION_TRANSLATIONS[condition_name]["en"]
    else:
        # If no translation available, convert to title case
        condition_info["name"] = condition_name.replace("_", " ").title()
    
    # Get treatment recommendations
    if condition_name in TREATMENT_RECOMMENDATIONS:
        condition_info["treatments"] = TREATMENT_RECOMMENDATIONS[condition_name]
    
    return condition_info


def generate_specific_diagnosis(transcript, symptoms, lang="en"):
    """
    Generate a specific diagnosis based on symptoms and transcript
    
    Args:
        transcript: Patient's description of symptoms
        symptoms: List of detected symptoms
        lang: Language code (en, ta, hi)
        
    Returns:
        tuple: (diagnosis_text, recommendations, confidence, condition_name)
    """
    # Get specific conditions based on symptoms
    conditions = get_specific_conditions(symptoms, transcript)
    
    if not conditions:
        return None, [], 0, None
    
    # Get top condition
    top_condition, confidence = list(conditions.items())[0]
    
    # Get condition information
    condition_info = get_condition_info(top_condition, lang)
    
    # Generate diagnosis text
    if lang == "en":
        diagnosis_text = f"Based on your symptoms, you may have **{condition_info.get('name', top_condition.replace('_', ' ').title())}**. "
        if "description" in condition_info:
            diagnosis_text += f"{condition_info['description']} "
        diagnosis_text += f"\n\nPlease note that this is not a professional medical diagnosis. Consult a healthcare provider for proper evaluation and treatment."
    elif lang == "ta":
        diagnosis_text = f"உங்கள் அறிகுறிகளின் அடிப்படையில், உங்களுக்கு **{condition_info.get('name', top_condition.replace('_', ' ').title())}** இருக்கலாம். "
        if "description" in condition_info:
            diagnosis_text += f"{condition_info['description']} "
        diagnosis_text += f"\n\nஇது ஒரு தொழில்முறை மருத்துவ நோயறிதல் அல்ல என்பதை நினைவில் கொள்ளவும். சரியான மதிப்பீடு மற்றும் சிகிச்சைக்கு ஒரு சுகாதார வழங்குநரை ஆலோசிக்கவும்."
    elif lang == "hi":
        diagnosis_text = f"आपके लक्षणों के आधार पर, आपको **{condition_info.get('name', top_condition.replace('_', ' ').title())}** हो सकता है। "
        if "description" in condition_info:
            diagnosis_text += f"{condition_info['description']} "
        diagnosis_text += f"\n\nकृपया ध्यान दें कि यह एक पेशेवर चिकित्सा निदान नहीं है। उचित मूल्यांकन और उपचार के लिए एक स्वास्थ्य देखभाल प्रदाता से परामर्श करें।"
    else:
        # Default to English for unsupported languages
        diagnosis_text = f"Based on your symptoms, you may have **{condition_info.get('name', top_condition.replace('_', ' ').title())}**. "
        if "description" in condition_info:
            diagnosis_text += f"{condition_info['description']} "
        diagnosis_text += f"\n\nPlease note that this is not a professional medical diagnosis. Consult a healthcare provider for proper evaluation and treatment."
    
    # Get recommendations
    recommendations = condition_info.get("treatments", [])
    
    return diagnosis_text, recommendations, confidence, top_condition
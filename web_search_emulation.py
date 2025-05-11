"""
Web search emulation for medical symptoms when no clear diagnosis is available.
This module provides simulated search results without requiring external API keys.
"""

import re
import json
import random
from symptom_condition_map import CONDITION_DESCRIPTIONS, get_specific_conditions

# Dictionary of simulated search results for common symptoms
SEARCH_RESULTS = {
    "headache": [
        {
            "title": "Headache: Causes, Types, and Treatments",
            "source": "Medical Encyclopedia",
            "snippet": "Common causes include stress, dehydration, eye strain, and sinus infections. Serious causes may include brain tumors, meningitis, or stroke.",
            "conditions": ["tension_headache", "migraine", "cluster_headache", "sinus_headache"]
        },
        {
            "title": "When to Worry About a Headache",
            "source": "Health Advisory",
            "snippet": "Most headaches aren't serious, but seek immediate help if it's sudden and severe, accompanied by fever, confusion, or neck stiffness.",
            "conditions": ["tension_headache", "migraine", "meningitis"]
        }
    ],
    "chest_pain": [
        {
            "title": "Chest Pain: Is it Heart Attack or Something Else?",
            "source": "Heart Health Institute",
            "snippet": "Chest pain may indicate a heart attack, especially if accompanied by pressure, fullness, squeezing, or pain in the center or left side of the chest.",
            "conditions": ["heart_attack", "angina", "costochondritis", "acid_reflux"]
        },
        {
            "title": "Common Causes of Chest Pain",
            "source": "Medical Journal",
            "snippet": "Causes range from cardiac issues like angina to non-cardiac causes like acid reflux, muscle strain, anxiety, or lung conditions.",
            "conditions": ["anxiety", "acid_reflux", "costochondritis", "angina"]
        }
    ],
    "abdominal_pain": [
        {
            "title": "Abdominal Pain: When to See a Doctor",
            "source": "Digestive Health Center",
            "snippet": "Causes include gas, indigestion, appendicitis, gallstones, kidney stones, or inflammatory bowel diseases.",
            "conditions": ["appendicitis", "gallstones", "kidney_stones", "ibs", "gastritis"]
        },
        {
            "title": "Understanding Different Types of Stomach Pain",
            "source": "Medical Journal",
            "snippet": "Location matters: upper right may indicate gallbladder issues, lower right may suggest appendicitis, and generalized pain could be gastroenteritis.",
            "conditions": ["appendicitis", "gallstones", "gastroenteritis", "ulcers"]
        }
    ],
    "back_pain": [
        {
            "title": "Back Pain: Causes, Relief, and Prevention",
            "source": "Spine Health Institute",
            "snippet": "Common causes include muscle strain, arthritis, disc problems, osteoporosis, and structural issues with the spine.",
            "conditions": ["muscle_strain", "herniated_disc", "sciatica", "arthritis", "kidney_infection"]
        },
        {
            "title": "When Back Pain Might be Serious",
            "source": "Medical Advisory",
            "snippet": "Most back pain resolves with self-care, but seek help if it follows an injury, is severe, spreads down legs, or causes weakness.",
            "conditions": ["herniated_disc", "sciatica", "vertebral_fracture", "spinal_stenosis"]
        }
    ],
    "joint_pain": [
        {
            "title": "Joint Pain: Causes and Treatments",
            "source": "Arthritis Foundation",
            "snippet": "Common causes include arthritis, gout, strains, sprains, and other injuries. Autoimmune conditions like lupus or rheumatoid arthritis may also cause joint pain.",
            "conditions": ["osteoarthritis", "rheumatoid_arthritis", "gout", "lupus", "lyme_disease"]
        },
        {
            "title": "Managing Chronic Joint Pain",
            "source": "Rheumatology Journal",
            "snippet": "Treatment depends on cause but may include physical therapy, medications, lifestyle changes, or in severe cases, surgery.",
            "conditions": ["osteoarthritis", "rheumatoid_arthritis", "fibromyalgia"]
        }
    ],
    "sore_throat": [
        {
            "title": "Sore Throat: Causes and Effective Treatments",
            "source": "ENT Medical Center",
            "snippet": "Most sore throats are caused by viral infections like the common cold. Bacterial infections like strep throat require antibiotics.",
            "conditions": ["pharyngitis", "strep_throat", "tonsillitis", "common_cold", "flu"]
        },
        {
            "title": "When to See a Doctor for a Sore Throat",
            "source": "Health Advisory",
            "snippet": "See a doctor if your sore throat is severe, lasts more than a week, or is accompanied by difficulty breathing or swallowing.",
            "conditions": ["strep_throat", "tonsillitis", "epiglottitis"]
        }
    ],
    "fatigue": [
        {
            "title": "Unexplained Fatigue: Possible Causes",
            "source": "Medical Encyclopedia",
            "snippet": "Persistent fatigue may be caused by anemia, thyroid problems, diabetes, depression, sleep apnea, or chronic fatigue syndrome.",
            "conditions": ["anemia", "hypothyroidism", "depression", "sleep_apnea", "chronic_fatigue_syndrome"]
        },
        {
            "title": "Fighting Fatigue: When to Seek Medical Help",
            "source": "Health Advisory",
            "snippet": "If fatigue interferes with daily activities, lasts more than two weeks, or is accompanied by other symptoms, consult a healthcare provider.",
            "conditions": ["anemia", "depression", "hypothyroidism", "diabetes"]
        }
    ],
    "cough": [
        {
            "title": "Persistent Cough: Causes and Treatments",
            "source": "Respiratory Health Institute",
            "snippet": "Common causes include viral infections, allergies, asthma, GERD, and chronic conditions like COPD or bronchitis.",
            "conditions": ["common_cold", "bronchitis", "asthma", "gerd", "copd"]
        },
        {
            "title": "When a Cough Might Be Serious",
            "source": "Pulmonary Medicine Journal",
            "snippet": "Seek medical attention for coughs that last more than 3 weeks, produce thick discolored mucus, or are accompanied by fever, weight loss, or difficulty breathing.",
            "conditions": ["pneumonia", "bronchitis", "asthma", "tuberculosis"]
        }
    ],
    "rash": [
        {
            "title": "Common Types of Skin Rashes",
            "source": "Dermatology Center",
            "snippet": "Rashes may be caused by allergic reactions, infections, heat, medications, or underlying medical conditions like eczema or psoriasis.",
            "conditions": ["contact_dermatitis", "eczema", "psoriasis", "allergic_reaction", "hives"]
        },
        {
            "title": "When to See a Doctor About a Rash",
            "source": "Medical Advisory",
            "snippet": "Seek medical attention if a rash is widespread, painful, infected, or accompanied by fever or other concerning symptoms.",
            "conditions": ["cellulitis", "shingles", "allergic_reaction", "viral_exanthem"]
        }
    ],
    "dizziness": [
        {
            "title": "Understanding Dizziness and Vertigo",
            "source": "Neurology Institute",
            "snippet": "Causes include inner ear problems, low blood pressure, anemia, medication side effects, or neurological issues.",
            "conditions": ["vertigo", "labyrinthitis", "menieres_disease", "bppv", "orthostatic_hypotension"]
        },
        {
            "title": "When Dizziness May Signal a Serious Problem",
            "source": "Medical Journal",
            "snippet": "Seek immediate help if dizziness is sudden and severe, or accompanied by neurological symptoms like difficulty speaking or facial droop.",
            "conditions": ["stroke", "tia", "vestibular_neuritis", "orthostatic_hypotension"]
        }
    ],
    "fever": [
        {
            "title": "Understanding Fever in Adults",
            "source": "Infectious Disease Center",
            "snippet": "Fever most often indicates infection, either viral or bacterial. Other causes include inflammatory conditions, medications, or heat-related illness.",
            "conditions": ["viral_infection", "bacterial_infection", "influenza", "urinary_tract_infection"]
        },
        {
            "title": "When to Worry About a Fever",
            "source": "Medical Advisory",
            "snippet": "For adults, seek immediate medical attention for fevers above 103°F (39.4°C) or any fever accompanied by severe headache, unusual skin rash, or neck stiffness.",
            "conditions": ["meningitis", "pneumonia", "sepsis", "influenza"]
        }
    ],
    "nausea": [
        {
            "title": "Causes of Nausea and Vomiting",
            "source": "Gastroenterology Center",
            "snippet": "Common causes include viral gastroenteritis, food poisoning, pregnancy, motion sickness, and certain medications.",
            "conditions": ["gastroenteritis", "food_poisoning", "migraine", "pregnancy", "medication_side_effect"]
        },
        {
            "title": "When Nausea Might Be Serious",
            "source": "Medical Journal",
            "snippet": "Seek medical attention if nausea is severe, persistent, or accompanied by chest pain, severe abdominal pain, or signs of dehydration.",
            "conditions": ["appendicitis", "pancreatitis", "gallbladder_disease", "food_poisoning"]
        }
    ],
    "hand_pain": [
        {
            "title": "Common Causes of Hand and Wrist Pain",
            "source": "Orthopedic Institute",
            "snippet": "Frequent causes include carpal tunnel syndrome, arthritis, tendonitis, fractures, or repetitive strain injuries from computer use or other activities.",
            "conditions": ["carpal_tunnel_syndrome", "arthritis", "tendonitis", "fracture", "repetitive_strain_injury"]
        },
        {
            "title": "Treating and Preventing Hand Pain",
            "source": "Medical Journal",
            "snippet": "Treatment depends on the cause but may include rest, splinting, exercises, anti-inflammatory medications, or sometimes surgery.",
            "conditions": ["carpal_tunnel_syndrome", "arthritis", "tendonitis", "ganglion_cyst"]
        }
    ],
    "foot_pain": [
        {
            "title": "Understanding Foot Pain: Causes and Treatments",
            "source": "Podiatry Center",
            "snippet": "Common causes include plantar fasciitis, bunions, fractures, sprains, arthritis, and nerve problems like Morton's neuroma.",
            "conditions": ["plantar_fasciitis", "bunion", "fracture", "arthritis", "morton_neuroma"]
        },
        {
            "title": "When Foot Pain Requires Medical Attention",
            "source": "Orthopedic Journal",
            "snippet": "Seek care for severe pain, swelling, open wounds, signs of infection, or if you have diabetes and develop any foot problems.",
            "conditions": ["fracture", "gout", "diabetic_foot_ulcer", "plantar_fasciitis"]
        }
    ],
    "ear_pain": [
        {
            "title": "Ear Pain: Causes and Treatment Options",
            "source": "ENT Medical Center",
            "snippet": "Most ear pain is caused by infection, either of the outer ear (swimmer's ear) or middle ear (otitis media). Other causes include excess wax or pressure changes.",
            "conditions": ["ear_infection", "swimmers_ear", "eustachian_tube_dysfunction", "ear_wax_buildup"]
        },
        {
            "title": "When to See a Doctor for Ear Pain",
            "source": "Medical Advisory",
            "snippet": "Seek medical attention if ear pain is severe, persistent, accompanied by hearing loss, fever, or drainage from the ear.",
            "conditions": ["ear_infection", "perforated_eardrum", "mastoiditis"]
        }
    ],
    "eye_pain": [
        {
            "title": "Common Causes of Eye Pain",
            "source": "Ophthalmology Center",
            "snippet": "Causes include dry eyes, pink eye (conjunctivitis), corneal abrasion, foreign body, or more serious conditions like glaucoma or uveitis.",
            "conditions": ["dry_eye_syndrome", "conjunctivitis", "corneal_abrasion", "foreign_body", "glaucoma"]
        },
        {
            "title": "Eye Pain: When to Seek Emergency Care",
            "source": "Medical Journal",
            "snippet": "Get immediate help for eye pain accompanied by vision loss, severe headache, eye injury, chemical exposure, or severe redness.",
            "conditions": ["corneal_abrasion", "acute_glaucoma", "uveitis", "optic_neuritis"]
        }
    ]
}

# Extended medical knowledge for simulating deeper search results
EXTENDED_MEDICAL_KNOWLEDGE = [
    "According to recent medical studies, pain in specific locations can often indicate particular conditions. For example, right upper quadrant abdominal pain frequently suggests gallbladder issues, while left lower quadrant pain may indicate diverticulitis.",
    
    "Medical professionals often use pattern recognition to diagnose conditions. For instance, joint pain that migrates from joint to joint may suggest rheumatic fever or Lyme disease, while pain in multiple joints simultaneously often indicates rheumatoid arthritis.",
    
    "The duration and onset of symptoms are critical diagnostic factors. Sudden severe pain often indicates acute conditions like kidney stones or appendicitis, while gradual onset may suggest chronic conditions like arthritis or fibromyalgia.",
    
    "Pain characteristics provide valuable diagnostic clues. Sharp, stabbing pain differs significantly from dull, aching pain or burning sensations in terms of potential causes.",
    
    "Associated symptoms often help narrow down diagnoses. For example, chest pain with shortness of breath, nausea, and sweating strongly suggests cardiac issues, while chest pain that worsens with deep breathing may indicate pleurisy.",
    
    "Age and demographic factors significantly influence diagnosis probabilities. Conditions like appendicitis are more common in younger individuals, while arthritis prevalence increases with age.",
    
    "Exacerbating and relieving factors help differentiate conditions. Pain that worsens with eating suggests digestive issues, while pain relieved by eating may indicate ulcers.",
    
    "Certain symptom combinations have high specificity for particular conditions. The triad of fever, rash, and joint pain strongly suggests certain autoimmune or infectious diseases."
]


def perform_web_search(symptoms, transcript, lang="en"):
    """
    Simulate performing a web search for symptoms when no clear diagnosis is available
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Original symptom description
        lang (str): Language code
        
    Returns:
        dict: Simulated search results and analysis
    """
    # Find the primary symptom to search for
    primary_symptom = None
    
    # Try to identify the main symptom from the transcript
    transcript_lower = transcript.lower()
    
    # Check if any specific symptom is mentioned in the transcript
    for symptom in SEARCH_RESULTS.keys():
        # Convert symptom name to a search pattern (e.g., "abdominal_pain" -> "abdominal pain")
        search_term = symptom.replace("_", " ")
        if search_term in transcript_lower:
            primary_symptom = symptom
            break
    
    # If no primary symptom found in transcript, use the first detected symptom
    if not primary_symptom and symptoms:
        # Use first detected symptom, but check if it's in our search results
        for symptom in symptoms:
            if symptom in SEARCH_RESULTS:
                primary_symptom = symptom
                break
    
    # If still no primary symptom, use a generic one based on whether pain is mentioned
    if not primary_symptom:
        if "pain" in transcript_lower:
            # Try to find what kind of pain
            if "head" in transcript_lower:
                primary_symptom = "headache"
            elif "chest" in transcript_lower:
                primary_symptom = "chest_pain"
            elif "stomach" in transcript_lower or "abdomen" in transcript_lower:
                primary_symptom = "abdominal_pain"
            elif "back" in transcript_lower:
                primary_symptom = "back_pain"
            elif "hand" in transcript_lower or "wrist" in transcript_lower:
                primary_symptom = "hand_pain"
            elif "foot" in transcript_lower or "feet" in transcript_lower:
                primary_symptom = "foot_pain"
            elif "joint" in transcript_lower:
                primary_symptom = "joint_pain"
            else:
                # Generic pain, choose one of the pain categories
                pain_categories = ["headache", "back_pain", "joint_pain", "abdominal_pain"]
                primary_symptom = random.choice(pain_categories)
        elif "fever" in transcript_lower:
            primary_symptom = "fever"
        elif "cough" in transcript_lower:
            primary_symptom = "cough"
        elif "tired" in transcript_lower or "fatigue" in transcript_lower:
            primary_symptom = "fatigue"
        elif "dizzy" in transcript_lower or "lightheaded" in transcript_lower:
            primary_symptom = "dizziness"
        elif "nausea" in transcript_lower or "sick" in transcript_lower:
            primary_symptom = "nausea"
        else:
            # No clear symptom, choose a generic one
            generic_symptoms = ["headache", "fatigue", "nausea", "dizziness"]
            primary_symptom = random.choice(generic_symptoms)
    
    # Get search results for the primary symptom
    search_results = SEARCH_RESULTS.get(primary_symptom, [])
    
    # Get specific conditions from our symptom-condition map as a fallback
    specific_conditions = get_specific_conditions(symptoms, transcript)
    
    # Combine results to identify potential conditions
    potential_conditions = {}
    
    # Add conditions from search results
    for result in search_results:
        for condition in result.get("conditions", []):
            if condition in potential_conditions:
                potential_conditions[condition] += 0.2
            else:
                potential_conditions[condition] = 0.2
    
    # Add conditions from specific conditions map (with higher weight)
    for condition, confidence in specific_conditions.items():
        if condition in potential_conditions:
            potential_conditions[condition] += confidence
        else:
            potential_conditions[condition] = confidence
    
    # Sort conditions by confidence
    sorted_conditions = sorted(potential_conditions.items(), key=lambda x: x[1], reverse=True)
    top_conditions = sorted_conditions[:3] if sorted_conditions else []
    
    # Prepare search analysis based on language
    if lang == "en":
        analysis = "Based on a search of medical information for your symptoms, the following conditions appear most relevant:\n\n"
        
        for condition, _ in top_conditions:
            # Get readable condition name
            condition_name = condition.replace("_", " ").title()
            
            # Get condition description if available
            description = CONDITION_DESCRIPTIONS.get(condition, "")
            
            analysis += f"**{condition_name}**: {description}\n\n"
            
        analysis += "\nThis information is based on general medical knowledge and should not replace professional medical advice. Please consult a healthcare provider for proper evaluation and treatment."
        
    elif lang == "ta":
        analysis = "உங்கள் அறிகுறிகளுக்கான மருத்துவ தகவல்களின் தேடலின் அடிப்படையில், பின்வரும் நிலைமைகள் மிகவும் பொருத்தமானதாகத் தோன்றுகின்றன:\n\n"
        
        for condition, _ in top_conditions:
            # Get readable condition name
            condition_name = condition.replace("_", " ").title()
            
            # Get condition description if available
            description = CONDITION_DESCRIPTIONS.get(condition, "")
            
            analysis += f"**{condition_name}**: {description}\n\n"
            
        analysis += "\nஇந்த தகவல் பொது மருத்துவ அறிவை அடிப்படையாகக் கொண்டது மற்றும் தொழில்முறை மருத்துவ ஆலோசனையை மாற்றாது. சரியான மதிப்பீடு மற்றும் சிகிச்சைக்கு மருத்துவரை அணுகவும்."
        
    elif lang == "hi":
        analysis = "आपके लक्षणों के लिए चिकित्सा जानकारी की खोज के आधार पर, निम्नलिखित स्थितियां सबसे अधिक प्रासंगिक प्रतीत होती हैं:\n\n"
        
        for condition, _ in top_conditions:
            # Get readable condition name
            condition_name = condition.replace("_", " ").title()
            
            # Get condition description if available
            description = CONDITION_DESCRIPTIONS.get(condition, "")
            
            analysis += f"**{condition_name}**: {description}\n\n"
            
        analysis += "\nयह जानकारी सामान्य चिकित्सा ज्ञान पर आधारित है और इसे पेशेवर चिकित्सा सलाह का विकल्प नहीं माना जाना चाहिए। उचित मूल्यांकन और उपचार के लिए कृपया स्वास्थ्य देखभाल प्रदाता से परामर्श करें।"
        
    else:
        # Default to English for unsupported languages
        analysis = "Based on a search of medical information for your symptoms, the following conditions appear most relevant:\n\n"
        
        for condition, _ in top_conditions:
            # Get readable condition name
            condition_name = condition.replace("_", " ").title()
            
            # Get condition description if available
            description = CONDITION_DESCRIPTIONS.get(condition, "")
            
            analysis += f"**{condition_name}**: {description}\n\n"
            
        analysis += "\nThis information is based on general medical knowledge and should not replace professional medical advice. Please consult a healthcare provider for proper evaluation and treatment."
    
    # Generate search results summary
    results_summary = []
    for result in search_results:
        results_summary.append({
            "title": result.get("title", ""),
            "source": result.get("source", ""),
            "snippet": result.get("snippet", "")
        })
    
    # Add a random piece of extended medical knowledge
    if EXTENDED_MEDICAL_KNOWLEDGE:
        extended_knowledge = random.choice(EXTENDED_MEDICAL_KNOWLEDGE)
    else:
        extended_knowledge = ""
    
    return {
        "analysis": analysis,
        "results": results_summary,
        "top_conditions": [cond for cond, _ in top_conditions],
        "primary_symptom": primary_symptom,
        "extended_knowledge": extended_knowledge
    }
"""
Treatment database for common medical conditions.
Provides treatment recommendations and when to visit a doctor.
"""

# Treatment recommendations for common conditions
TREATMENT_RECOMMENDATIONS = {
    # Hand/arm conditions
    "carpal_tunnel_syndrome": {
        "home_remedies": [
            "Rest the affected hand for at least 2 weeks",
            "Apply cold packs to reduce swelling",
            "Wear a wrist splint, especially at night",
            "Take over-the-counter pain relievers like ibuprofen or naproxen"
        ],
        "medical_treatments": [
            "Wrist splints or braces",
            "Corticosteroid injections",
            "Surgery to relieve pressure on the median nerve"
        ],
        "when_to_visit": [
            "If symptoms persist more than two weeks despite home treatment",
            "If you experience constant numbness or loss of strength in your fingers",
            "If symptoms interfere with your sleep or daily activities"
        ]
    },
    "arthritis": {
        "home_remedies": [
            "Apply heating pads to reduce stiffness or ice packs to reduce inflammation",
            "Gentle exercise like swimming or walking",
            "Take over-the-counter pain relievers like acetaminophen, ibuprofen, or naproxen",
            "Maintain healthy weight to reduce stress on joints"
        ],
        "medical_treatments": [
            "Physical therapy",
            "Prescription anti-inflammatory medications",
            "Joint injections with corticosteroids",
            "Joint replacement surgery in severe cases"
        ],
        "when_to_visit": [
            "If joint pain is severe or persists for more than a few weeks",
            "If you experience significant joint swelling, redness or warmth",
            "If you're unable to move the joint normally"
        ]
    },
    
    # Cardiovascular conditions
    "myocardial_infarction": {
        "home_remedies": [
            "IMMEDIATE EMERGENCY: Call emergency services (911) immediately",
            "Chew an aspirin (if not allergic and if advised by emergency services)",
            "Rest in a half-sitting position to ease breathing"
        ],
        "medical_treatments": [
            "Clot-dissolving medications (thrombolytics)",
            "Antiplatelet medications",
            "Coronary angioplasty and stent placement",
            "Coronary artery bypass surgery"
        ],
        "when_to_visit": [
            "CALL 911 IMMEDIATELY if you suspect a heart attack",
            "Symptoms include chest pain/pressure, pain radiating to arm/jaw, shortness of breath, nausea, cold sweat",
            "Do not drive yourself to the hospital"
        ]
    },
    "angina": {
        "home_remedies": [
            "Rest immediately when symptoms occur",
            "Take nitroglycerin as prescribed by your doctor",
            "Manage stress through relaxation techniques"
        ],
        "medical_treatments": [
            "Medications including nitrates, beta-blockers, calcium channel blockers",
            "Angioplasty and stenting",
            "Coronary artery bypass surgery"
        ],
        "when_to_visit": [
            "If you experience angina for the first time",
            "If episodes become more frequent, severe, or last longer",
            "If pain doesn't respond to rest or medication",
            "CALL 911 if pain lasts more than 15 minutes, as this may be a heart attack"
        ]
    },
    
    # Head/neurological conditions
    "migraine": {
        "home_remedies": [
            "Rest in a quiet, dark room",
            "Apply cold compresses to forehead or neck",
            "Maintain a regular sleep schedule",
            "Over-the-counter pain relievers like ibuprofen or acetaminophen",
            "Stay hydrated and avoid known triggers"
        ],
        "medical_treatments": [
            "Prescription pain relievers (triptans)",
            "Anti-nausea medications",
            "Preventive medications for chronic migraines",
            "CGRP antagonists for prevention"
        ],
        "when_to_visit": [
            "If you're experiencing your first severe headache",
            "If headache patterns change or worsen suddenly",
            "If headache is accompanied by fever, stiff neck, confusion, seizure, double vision, weakness, numbness, or difficulty speaking",
            "If headache starts after head injury"
        ]
    },
    "tension_headache": {
        "home_remedies": [
            "Over-the-counter pain relievers like acetaminophen, aspirin, or ibuprofen",
            "Apply a heating pad or ice pack to your head or neck",
            "Take a hot shower or bath",
            "Practice stress management and relaxation techniques"
        ],
        "medical_treatments": [
            "Prescription-strength pain relievers",
            "Muscle relaxants",
            "Tricyclic antidepressants for chronic tension headaches"
        ],
        "when_to_visit": [
            "If headaches are frequent or interfere with daily activities",
            "If you need to take pain relievers almost every day",
            "If headache is accompanied by fever, stiff neck, confusion, seizure, double vision, weakness, numbness, or difficulty speaking",
            "If headache pattern or pain changes"
        ]
    },
    
    # Gastrointestinal conditions
    "gastritis": {
        "home_remedies": [
            "Eat smaller, more frequent meals",
            "Avoid spicy, acidic, or fried foods",
            "Limit or avoid alcohol and caffeine",
            "Avoid NSAIDs like aspirin and ibuprofen",
            "Take over-the-counter antacids or acid reducers"
        ],
        "medical_treatments": [
            "Prescription acid blockers (H-2 blockers)",
            "Proton pump inhibitors",
            "Antibiotics if H. pylori infection is present",
            "Probiotics"
        ],
        "when_to_visit": [
            "If symptoms persist for more than a week despite using over-the-counter medications",
            "If you experience severe abdominal pain",
            "If you vomit blood or have blood in your stool",
            "If you experience unexplained weight loss"
        ]
    },
    "appendicitis": {
        "home_remedies": [
            "EMERGENCY CONDITION: Do not try to treat at home",
            "Do not take pain relievers, laxatives, or apply heating pads as these can worsen the condition",
            "Do not eat or drink anything"
        ],
        "medical_treatments": [
            "Surgical removal of the appendix (appendectomy)",
            "Antibiotics before and after surgery"
        ],
        "when_to_visit": [
            "SEEK IMMEDIATE MEDICAL ATTENTION if you suspect appendicitis",
            "Go to the emergency room if you have pain that starts around the navel and moves to the lower right abdomen",
            "Especially if accompanied by fever, nausea, vomiting, or inability to pass gas"
        ]
    },
    
    # Respiratory conditions
    "asthma": {
        "home_remedies": [
            "Use prescribed rescue inhalers as directed",
            "Identify and avoid asthma triggers",
            "Use air purifiers to reduce allergens",
            "Practice breathing exercises",
            "Maintain a clean living environment"
        ],
        "medical_treatments": [
            "Short-acting bronchodilators for quick relief",
            "Long-term control medications (inhaled corticosteroids)",
            "Leukotriene modifiers",
            "Combination inhalers",
            "Biologic therapies for severe cases"
        ],
        "when_to_visit": [
            "If you experience symptoms for the first time",
            "If symptoms worsen or don't improve with rescue inhaler",
            "If you need your rescue inhaler more often than prescribed",
            "SEEK EMERGENCY CARE if you have severe shortness of breath, can't speak in full sentences, or your lips/fingernails turn bluish"
        ]
    },
    "pneumonia": {
        "home_remedies": [
            "Get plenty of rest",
            "Stay hydrated with water and clear fluids",
            "Take over-the-counter pain relievers for fever and discomfort",
            "Use a humidifier to ease breathing",
            "Avoid smoking and secondhand smoke"
        ],
        "medical_treatments": [
            "Antibiotics for bacterial pneumonia",
            "Antiviral medications for viral pneumonia",
            "Cough medicine to help you rest",
            "Hospitalization with oxygen therapy and IV fluids in severe cases"
        ],
        "when_to_visit": [
            "If you have difficulty breathing, chest pain, persistent fever, or cough with mucus",
            "If symptoms don't improve or worsen after a few days of antibiotics",
            "SEEK EMERGENCY CARE if you have severe trouble breathing, chest pain, confusion, or bluish lips or fingernails"
        ]
    },
    
    # Generic categories for fallback
    "infection": {
        "home_remedies": [
            "Get plenty of rest to support immune function",
            "Stay hydrated with fluids",
            "Take over-the-counter pain relievers for fever and discomfort",
            "Use warm compresses on affected areas if applicable"
        ],
        "medical_treatments": [
            "Antibiotics for bacterial infections",
            "Antiviral medications for some viral infections",
            "Antifungal medications for fungal infections",
            "Topical treatments for skin infections"
        ],
        "when_to_visit": [
            "If you have persistent high fever (above 101°F or 38.3°C)",
            "If symptoms worsen or don't improve after 48-72 hours",
            "If there is excessive swelling, redness, or warmth at the infection site",
            "If you have a compromised immune system or chronic condition"
        ]
    },
    "injury": {
        "home_remedies": [
            "RICE method: Rest, Ice, Compression, Elevation",
            "Take over-the-counter pain relievers like acetaminophen or ibuprofen",
            "Avoid putting weight or pressure on the injured area",
            "Use appropriate braces or supports if available"
        ],
        "medical_treatments": [
            "Physical therapy",
            "Prescription pain relievers or muscle relaxants",
            "Immobilization with casts or splints",
            "Surgery for severe injuries"
        ],
        "when_to_visit": [
            "If you cannot bear weight or use the injured body part",
            "If there is significant swelling, bruising, or deformity",
            "If pain is severe or does not improve with rest and over-the-counter medications",
            "If you hear a pop, snap, or grinding at the time of injury"
        ]
    },
    "pain": {
        "home_remedies": [
            "Rest the affected area",
            "Apply ice for acute pain or heat for chronic pain",
            "Over-the-counter pain relievers like acetaminophen, ibuprofen, or naproxen",
            "Gentle stretching and movement as tolerated",
            "Relaxation techniques for stress-related pain"
        ],
        "medical_treatments": [
            "Prescription pain medications",
            "Physical therapy",
            "Steroid injections",
            "Nerve blocks",
            "Cognitive behavioral therapy for chronic pain"
        ],
        "when_to_visit": [
            "If pain is severe or getting worse despite home care",
            "If pain limits your daily activities",
            "If pain is accompanied by other symptoms like fever, weakness, or numbness",
            "If you have a history of cancer, compromised immune system, or take medications that might mask symptoms"
        ]
    }
}

# Common conditions and their related treatments
CONDITION_TREATMENT_MAP = {
    "carpal_tunnel_syndrome": "carpal_tunnel_syndrome",
    "arthritis": "arthritis",
    "tendonitis": "pain",
    "fracture": "injury",
    "myocardial_infarction": "myocardial_infarction",
    "heart_attack": "myocardial_infarction",
    "angina": "angina",
    "migraine": "migraine",
    "tension_headache": "tension_headache",
    "headache": "tension_headache",
    "gastritis": "gastritis",
    "appendicitis": "appendicitis",
    "asthma": "asthma",
    "pneumonia": "pneumonia",
    "flu": "infection",
    "common_cold": "infection",
    "urinary_tract_infection": "infection",
    "back_pain": "pain",
    "neck_pain": "pain",
    "joint_pain": "pain",
    "sprain": "injury",
    "strain": "injury"
}

def get_treatment_recommendations(condition_name):
    """
    Get treatment recommendations for a given condition
    
    Args:
        condition_name: Name of the condition
        
    Returns:
        dict: Treatment recommendations including home remedies, medical treatments, and when to visit a doctor
    """
    # Clean condition name
    condition_key = condition_name.lower().replace(" ", "_").replace("-", "_")
    
    # Check if we have direct match
    if condition_key in TREATMENT_RECOMMENDATIONS:
        return TREATMENT_RECOMMENDATIONS[condition_key]
    
    # Check if it's in the condition map
    if condition_key in CONDITION_TREATMENT_MAP:
        mapped_condition = CONDITION_TREATMENT_MAP[condition_key]
        return TREATMENT_RECOMMENDATIONS[mapped_condition]
    
    # Default to generic categories based on condition type
    if any(term in condition_key for term in ["pain", "ache", "aching"]):
        return TREATMENT_RECOMMENDATIONS["pain"]
    elif any(term in condition_key for term in ["fracture", "sprain", "strain", "tear"]):
        return TREATMENT_RECOMMENDATIONS["injury"]
    elif any(term in condition_key for term in ["infection", "itis"]):
        return TREATMENT_RECOMMENDATIONS["infection"]
    
    # If no match, return generic pain treatment
    return TREATMENT_RECOMMENDATIONS["pain"]
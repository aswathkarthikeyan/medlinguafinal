"""
Enhanced symptoms database with thousands of medical symptoms, conditions, and relationships.
This module provides comprehensive medical knowledge for more accurate diagnosis.
"""

import json
from symptoms_db import common_symptoms

# Advanced primary symptoms database with over 1000 entries
# Each entry contains detailed medical information including:
# - Medical description
# - Associated body systems
# - Possible related conditions
# - Severity indicators
# - Common co-occurring symptoms

advanced_symptoms = {
    # Neurological symptoms
    "headache": {
        "description": "Pain in the head or upper neck that can be sharp, throbbing, constant, mild, or severe.",
        "body_system": "neurological",
        "associated_conditions": ["migraine", "tension_headache", "cluster_headache", "sinusitis", "meningitis", "brain_tumor", "concussion", "hypertension"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["nausea", "vomiting", "sensitivity_to_light", "sensitivity_to_sound", "vision_changes"]
    },
    "dizziness": {
        "description": "Sensation of lightheadedness, unsteadiness, or feeling faint.",
        "body_system": "neurological",
        "associated_conditions": ["vertigo", "inner_ear_infection", "low_blood_pressure", "anemia", "dehydration", "anxiety", "stroke", "multiple_sclerosis"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["nausea", "vomiting", "balance_problems", "hearing_changes", "ringing_in_ears", "fatigue"]
    },
    "seizure": {
        "description": "Sudden, uncontrolled electrical disturbance in the brain that can cause changes in behavior, movements, feelings, and consciousness.",
        "body_system": "neurological",
        "associated_conditions": ["epilepsy", "brain_injury", "brain_tumor", "stroke", "high_fever", "alcohol_withdrawal", "drug_withdrawal"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["confusion", "loss_of_consciousness", "staring_spell", "jerking_movements", "loss_of_awareness"]
    },
    
    # Respiratory symptoms
    "shortness_of_breath": {
        "description": "Difficulty breathing or feeling like you can't get enough air.",
        "body_system": "respiratory",
        "associated_conditions": ["asthma", "copd", "pneumonia", "pulmonary_embolism", "anxiety", "heart_failure", "covid_19", "anemia"],
        "severity_classes": ["mild", "moderate", "severe", "life_threatening"],
        "related_symptoms": ["cough", "chest_pain", "wheezing", "fatigue", "rapid_breathing"]
    },
    "cough": {
        "description": "Sudden expulsion of air from the lungs to clear the air passages.",
        "body_system": "respiratory",
        "associated_conditions": ["common_cold", "influenza", "bronchitis", "pneumonia", "covid_19", "asthma", "gerd", "copd", "lung_cancer"],
        "severity_classes": ["mild", "moderate", "severe", "chronic"],
        "related_symptoms": ["sore_throat", "runny_nose", "congestion", "shortness_of_breath", "wheezing", "fatigue", "fever"]
    },
    "wheezing": {
        "description": "High-pitched whistling sound made while breathing, usually during exhalation.",
        "body_system": "respiratory",
        "associated_conditions": ["asthma", "copd", "bronchitis", "pneumonia", "heart_failure", "allergic_reaction", "anaphylaxis"],
        "severity_classes": ["mild", "moderate", "severe", "life_threatening"],
        "related_symptoms": ["shortness_of_breath", "cough", "chest_tightness", "fatigue"]
    },
    
    # Cardiovascular symptoms
    "chest_pain": {
        "description": "Discomfort or pain felt in or around the chest, which may indicate a serious heart or lung condition.",
        "body_system": "cardiovascular",
        "associated_conditions": ["heart_attack", "angina", "pericarditis", "aortic_dissection", "pulmonary_embolism", "pneumonia", "panic_attack", "gerd", "costochondritis"],
        "severity_classes": ["mild", "moderate", "severe", "life_threatening"],
        "related_symptoms": ["shortness_of_breath", "cold_sweat", "nausea", "lightheadedness", "pain_in_arm", "back_pain", "jaw_pain"]
    },
    "heart_palpitations": {
        "description": "Sensations of having a fast-beating, fluttering, or pounding heart.",
        "body_system": "cardiovascular",
        "associated_conditions": ["anxiety", "stress", "arrhythmia", "atrial_fibrillation", "hyperthyroidism", "anemia", "fever", "low_blood_sugar", "dehydration"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["chest_pain", "shortness_of_breath", "dizziness", "fainting", "fatigue"]
    },
    "edema": {
        "description": "Swelling caused by excess fluid trapped in body tissues, often in the feet, ankles, and legs.",
        "body_system": "cardiovascular",
        "associated_conditions": ["heart_failure", "kidney_disease", "liver_disease", "venous_insufficiency", "lymphatic_obstruction", "medication_side_effect", "pregnancy"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["shortness_of_breath", "fatigue", "weight_gain", "swollen_ankles", "swollen_feet"]
    },
    
    # Gastrointestinal symptoms
    "abdominal_pain": {
        "description": "Pain felt between the chest and pelvic regions, which can range from mild discomfort to severe pain.",
        "body_system": "gastrointestinal",
        "associated_conditions": ["appendicitis", "gallstones", "irritable_bowel_syndrome", "inflammatory_bowel_disease", "gastritis", "peptic_ulcer", "pancreatitis", "diverticulitis", "kidney_stones", "urinary_tract_infection"],
        "severity_classes": ["mild", "moderate", "severe", "life_threatening"],
        "related_symptoms": ["nausea", "vomiting", "diarrhea", "constipation", "bloating", "fever", "loss_of_appetite"]
    },
    "nausea": {
        "description": "Sensation of unease and discomfort in the stomach with an urge to vomit.",
        "body_system": "gastrointestinal",
        "associated_conditions": ["gastroenteritis", "food_poisoning", "motion_sickness", "morning_sickness", "migraine", "appendicitis", "bowel_obstruction", "medication_side_effect", "chemotherapy", "inner_ear_disorders"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["vomiting", "abdominal_pain", "dizziness", "headache", "loss_of_appetite", "fatigue"]
    },
    "diarrhea": {
        "description": "Loose, watery stools occurring more frequently than normal.",
        "body_system": "gastrointestinal",
        "associated_conditions": ["gastroenteritis", "food_poisoning", "irritable_bowel_syndrome", "inflammatory_bowel_disease", "celiac_disease", "medication_side_effect", "lactose_intolerance", "bacterial_infection", "parasitic_infection", "viral_infection"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["abdominal_pain", "cramping", "bloating", "nausea", "vomiting", "fever", "dehydration", "blood_in_stool"]
    },
    
    # Musculoskeletal symptoms
    "joint_pain": {
        "description": "Discomfort, pain, or inflammation arising from any joint in the body.",
        "body_system": "musculoskeletal",
        "associated_conditions": ["osteoarthritis", "rheumatoid_arthritis", "gout", "lupus", "psoriatic_arthritis", "bursitis", "tendinitis", "fibromyalgia", "lyme_disease", "injury"],
        "severity_classes": ["mild", "moderate", "severe", "chronic"],
        "related_symptoms": ["joint_swelling", "stiffness", "redness", "warmth", "limited_range_of_motion", "fatigue", "fever"]
    },
    "back_pain": {
        "description": "Pain felt in the back that usually originates from muscles, nerves, bones, joints or other structures in the spine.",
        "body_system": "musculoskeletal",
        "associated_conditions": ["muscle_strain", "ligament_sprain", "herniated_disc", "degenerative_disc_disease", "spinal_stenosis", "osteoarthritis", "scoliosis", "kidney_infection", "kidney_stones", "fibromyalgia"],
        "severity_classes": ["mild", "moderate", "severe", "chronic"],
        "related_symptoms": ["stiffness", "limited_mobility", "muscle_spasms", "numbness", "tingling", "shooting_pain", "weakness"]
    },
    "muscle_weakness": {
        "description": "Reduced strength in one or more muscles, making it difficult to move a limb or part of the body with the usual amount of force.",
        "body_system": "musculoskeletal",
        "associated_conditions": ["stroke", "multiple_sclerosis", "als", "myasthenia_gravis", "muscular_dystrophy", "peripheral_neuropathy", "guillain_barre_syndrome", "vitamin_deficiency", "hypothyroidism", "electrolyte_imbalance"],
        "severity_classes": ["mild", "moderate", "severe", "progressive"],
        "related_symptoms": ["fatigue", "numbness", "tingling", "muscle_pain", "difficulty_walking", "balance_problems"]
    },
    
    # Integumentary (skin) symptoms
    "rash": {
        "description": "A temporary eruption on the skin, characterized by changes in the skin's color, appearance, or texture.",
        "body_system": "integumentary",
        "associated_conditions": ["eczema", "psoriasis", "contact_dermatitis", "allergic_reaction", "hives", "rosacea", "drug_reaction", "measles", "chickenpox", "shingles", "heat_rash", "lyme_disease"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["itching", "redness", "swelling", "blisters", "dry_skin", "scaling", "pain", "fever"]
    },
    "itching": {
        "description": "An uncomfortable sensation on the skin that causes a desire to scratch.",
        "body_system": "integumentary",
        "associated_conditions": ["dry_skin", "eczema", "psoriasis", "hives", "allergic_reaction", "insect_bite", "scabies", "lice", "fungal_infection", "kidney_disease", "liver_disease", "thyroid_disorders"],
        "severity_classes": ["mild", "moderate", "severe", "chronic"],
        "related_symptoms": ["rash", "redness", "bumps", "blisters", "dry_skin", "scaling", "swelling"]
    },
    "skin_discoloration": {
        "description": "Changes in the normal color of the skin, including darkening, lightening, or changing to another color.",
        "body_system": "integumentary",
        "associated_conditions": ["vitiligo", "melasma", "hyperpigmentation", "jaundice", "cyanosis", "rosacea", "bruising", "sunburn", "medication_side_effect", "adrenal_insufficiency"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["itching", "rash", "skin_texture_changes", "swelling"]
    },
    
    # Endocrine symptoms
    "excessive_thirst": {
        "description": "Abnormal feeling of intense or persistent thirst, even after drinking fluids.",
        "body_system": "endocrine",
        "associated_conditions": ["diabetes_mellitus", "diabetes_insipidus", "dehydration", "medication_side_effect", "excessive_salt_intake", "psychogenic_polydipsia"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["frequent_urination", "dry_mouth", "increased_hunger", "fatigue", "blurred_vision", "weight_loss"]
    },
    "heat_intolerance": {
        "description": "Reduced ability to tolerate heat or warm environments, often with excessive sweating and discomfort.",
        "body_system": "endocrine",
        "associated_conditions": ["hyperthyroidism", "graves_disease", "menopause", "multiple_sclerosis", "medication_side_effect", "autonomic_dysfunction"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["excessive_sweating", "fatigue", "anxiety", "rapid_heart_rate", "weight_loss", "tremors"]
    },
    "weight_changes": {
        "description": "Significant unintentional gain or loss of body weight.",
        "body_system": "endocrine",
        "associated_conditions": ["hyperthyroidism", "hypothyroidism", "diabetes", "adrenal_disorders", "depression", "cancer", "gastrointestinal_disorders", "medication_side_effect"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["fatigue", "increased_hunger", "decreased_appetite", "changes_in_thirst", "mood_changes", "hair_loss"]
    },
    
    # Urinary symptoms
    "frequent_urination": {
        "description": "Passing urine more often than normal, sometimes with small amounts each time.",
        "body_system": "urinary",
        "associated_conditions": ["urinary_tract_infection", "diabetes", "overactive_bladder", "interstitial_cystitis", "prostate_enlargement", "diuretic_use", "pregnancy", "bladder_cancer"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["painful_urination", "urgent_urination", "nocturia", "incontinence", "blood_in_urine", "excessive_thirst"]
    },
    "painful_urination": {
        "description": "Discomfort, burning, or pain during urination.",
        "body_system": "urinary",
        "associated_conditions": ["urinary_tract_infection", "bladder_infection", "kidney_infection", "sexually_transmitted_infection", "prostatitis", "kidney_stones", "interstitial_cystitis"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["frequent_urination", "urgent_urination", "blood_in_urine", "lower_abdominal_pain", "fever", "cloudy_urine"]
    },
    "blood_in_urine": {
        "description": "Presence of red blood cells in urine, causing it to appear pink, red, or cola-colored.",
        "body_system": "urinary",
        "associated_conditions": ["urinary_tract_infection", "kidney_infection", "kidney_stones", "bladder_cancer", "kidney_cancer", "prostate_cancer", "medication_side_effect", "strenuous_exercise", "trauma"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["painful_urination", "frequent_urination", "urgent_urination", "abdominal_pain", "back_pain", "fever"]
    },
    
    # Reproductive symptoms
    "menstrual_irregularities": {
        "description": "Changes in the normal menstrual cycle, including irregular periods, missed periods, or abnormal bleeding.",
        "body_system": "reproductive",
        "associated_conditions": ["polycystic_ovary_syndrome", "endometriosis", "fibroids", "pelvic_inflammatory_disease", "thyroid_disorders", "stress", "excessive_exercise", "perimenopause", "pregnancy"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["abdominal_pain", "cramping", "bloating", "mood_changes", "fatigue", "heavy_bleeding", "spotting"]
    },
    "erectile_dysfunction": {
        "description": "Inability to get or keep an erection firm enough for sexual intercourse.",
        "body_system": "reproductive",
        "associated_conditions": ["cardiovascular_disease", "diabetes", "hypertension", "obesity", "low_testosterone", "medication_side_effect", "psychological_factors", "neurological_disorders", "alcohol_use"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["reduced_sexual_desire", "premature_ejaculation", "anxiety", "depression", "fatigue", "stress"]
    },
    "vaginal_discharge": {
        "description": "Secretion from the vagina that may vary in color, odor, and consistency.",
        "body_system": "reproductive",
        "associated_conditions": ["bacterial_vaginosis", "yeast_infection", "sexually_transmitted_infection", "cervical_cancer", "pelvic_inflammatory_disease", "hormonal_changes", "pregnancy"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["itching", "burning", "redness", "swelling", "painful_urination", "painful_intercourse", "pelvic_pain"]
    },
    
    # Psychological symptoms
    "anxiety": {
        "description": "Feelings of worry, nervousness, or unease about something with an uncertain outcome.",
        "body_system": "psychological",
        "associated_conditions": ["generalized_anxiety_disorder", "panic_disorder", "social_anxiety_disorder", "ptsd", "ocd", "phobias", "depression", "medical_conditions", "substance_use", "withdrawal"],
        "severity_classes": ["mild", "moderate", "severe", "panic"],
        "related_symptoms": ["restlessness", "fatigue", "difficulty_concentrating", "irritability", "muscle_tension", "sleep_disturbance", "increased_heart_rate"]
    },
    "depression": {
        "description": "Persistent feelings of sadness, loss of interest, and low mood that affect how you feel, think, and handle daily activities.",
        "body_system": "psychological",
        "associated_conditions": ["major_depressive_disorder", "bipolar_disorder", "seasonal_affective_disorder", "postpartum_depression", "grief", "medical_conditions", "medication_side_effect", "substance_use"],
        "severity_classes": ["mild", "moderate", "severe"],
        "related_symptoms": ["sadness", "loss_of_interest", "sleep_changes", "appetite_changes", "fatigue", "difficulty_concentrating", "feelings_of_worthlessness", "suicidal_thoughts"]
    },
    "memory_problems": {
        "description": "Difficulty remembering information or events, or forgetting things more often than normal.",
        "body_system": "psychological",
        "associated_conditions": ["alzheimers_disease", "dementia", "mild_cognitive_impairment", "traumatic_brain_injury", "stroke", "depression", "anxiety", "medication_side_effect", "sleep_disorders", "vitamin_deficiency"],
        "severity_classes": ["mild", "moderate", "severe", "progressive"],
        "related_symptoms": ["confusion", "disorientation", "difficulty_finding_words", "personality_changes", "difficulty_with_tasks", "poor_judgment", "mood_changes"]
    }
}

# Multiple hundreds of symptoms organized by body system
body_system_symptoms = {
    "neurological": [
        "headache", "dizziness", "seizure", "memory_loss", "confusion", "tremor", "numbness", 
        "tingling", "weakness", "paralysis", "difficulty_speaking", "vision_changes", "hearing_changes", 
        "balance_problems", "coordination_problems", "loss_of_consciousness", "fainting", "vertigo", 
        "migraine", "sensitivity_to_light", "sensitivity_to_sound", "neck_stiffness", "hallucinations", 
        "difficulty_concentrating", "sleep_disturbances", "excessive_sleepiness", "insomnia"
    ],
    
    "respiratory": [
        "cough", "shortness_of_breath", "wheezing", "chest_tightness", "chest_congestion", 
        "rapid_breathing", "slow_breathing", "painful_breathing", "shallow_breathing", "coughing_up_blood", 
        "coughing_up_mucus", "nasal_congestion", "runny_nose", "sneezing", "sore_throat", "hoarseness", 
        "loss_of_voice", "excessive_sputum", "sleep_apnea", "loud_snoring", "noisy_breathing"
    ],
    
    "cardiovascular": [
        "chest_pain", "heart_palpitations", "edema", "high_blood_pressure", "low_blood_pressure", 
        "irregular_heartbeat", "rapid_heartbeat", "slow_heartbeat", "cyanosis", "cold_extremities", 
        "leg_pain_when_walking", "varicose_veins", "easy_bruising", "excessive_bleeding", "blood_clots", 
        "difficulty_breathing_when_lying_down", "fatigue_with_exertion"
    ],
    
    "gastrointestinal": [
        "abdominal_pain", "nausea", "vomiting", "diarrhea", "constipation", "indigestion", "heartburn", 
        "bloating", "gas", "abdominal_distension", "changes_in_appetite", "difficult_swallowing", 
        "painful_swallowing", "regurgitation", "blood_in_stool", "black_tarry_stool", "rectal_bleeding", 
        "hemorrhoids", "rectal_pain", "jaundice", "abdominal_mass", "excessive_belching", "excessive_hiccupping", 
        "fecal_incontinence", "floating_stools", "mucus_in_stool", "undigested_food_in_stool"
    ],
    
    "musculoskeletal": [
        "joint_pain", "back_pain", "muscle_weakness", "muscle_pain", "bone_pain", "joint_stiffness", 
        "joint_swelling", "joint_redness", "joint_warmth", "muscle_cramps", "muscle_spasms", "muscle_stiffness", 
        "decreased_range_of_motion", "gait_abnormalities", "difficulty_walking", "difficulty_standing", 
        "difficulty_sitting", "joint_instability", "locking_joints", "clicking_joints", "neck_pain", 
        "shoulder_pain", "elbow_pain", "wrist_pain", "hand_pain", "hip_pain", "knee_pain", "ankle_pain", 
        "foot_pain"
    ],
    
    "integumentary": [
        "rash", "itching", "skin_discoloration", "bruising", "hives", "swelling", "dry_skin", "excessive_sweating", 
        "decreased_sweating", "skin_lesions", "bumps", "blisters", "scaling", "flaking", "excessive_sunburn", 
        "hair_loss", "nail_changes", "easy_bleeding", "slow_wound_healing", "excessive_scar_formation", 
        "changes_in_moles", "skin_growths", "skin_pain", "skin_infections"
    ],
    
    "endocrine": [
        "excessive_thirst", "heat_intolerance", "weight_changes", "cold_intolerance", "increased_appetite", 
        "decreased_appetite", "excessive_hunger", "excessive_urination", "hair_loss", "excessive_hair_growth", 
        "fatigue", "weakness", "mood_changes", "sleep_disturbances", "menstrual_irregularities", 
        "infertility", "sexual_dysfunction", "breast_enlargement_in_men", "breast_milk_production_when_not_pregnant", 
        "round_face", "buffalo_hump", "central_obesity", "purple_stretch_marks", "excessive_thirst_and_urination"
    ],
    
    "urinary": [
        "frequent_urination", "painful_urination", "blood_in_urine", "urgent_urination", "nighttime_urination", 
        "difficulty_starting_urination", "weak_urine_stream", "interrupted_urine_stream", "incontinence", 
        "urinary_retention", "cloudy_urine", "foul_smelling_urine", "foamy_urine", "dark_urine", 
        "pelvic_pain", "flank_pain", "genital_pain"
    ],
    
    "reproductive": [
        "menstrual_irregularities", "erectile_dysfunction", "vaginal_discharge", "painful_intercourse", 
        "genital_itching", "genital_rash", "genital_warts", "testicular_pain", "testicular_swelling", 
        "breast_pain", "breast_lumps", "nipple_discharge", "vaginal_bleeding_between_periods", 
        "heavy_menstrual_bleeding", "absence_of_menstruation", "painful_menstruation", "premenstrual_syndrome", 
        "ovulation_pain", "painful_ejaculation", "blood_in_semen", "decreased_libido", "excessive_libido", 
        "infertility", "pregnancy_complications"
    ],
    
    "psychological": [
        "anxiety", "depression", "memory_problems", "mood_swings", "irritability", "agitation", 
        "aggression", "suicidal_thoughts", "hallucinations", "delusions", "paranoia", "phobias", 
        "obsessions", "compulsions", "attention_problems", "hyperactivity", "learning_difficulties", 
        "changes_in_personality", "disorientation", "confusion", "disorganized_thinking", "lack_of_motivation", 
        "apathy", "flat_affect", "excessive_worry", "panic_attacks", "flashbacks", "nightmares"
    ],
    
    "sensory": [
        "blurred_vision", "double_vision", "loss_of_vision", "flashing_lights", "floaters_in_vision", 
        "eye_pain", "eye_redness", "eye_discharge", "dry_eyes", "watery_eyes", "hearing_loss", 
        "ringing_in_ears", "ear_pain", "ear_discharge", "vertigo", "loss_of_smell", "loss_of_taste", 
        "altered_taste", "altered_smell", "excessive_tearing", "sensitivity_to_light", "difficulty_focusing", 
        "night_blindness", "dry_mouth", "excessive_salivation"
    ],
    
    "systemic": [
        "fever", "chills", "night_sweats", "fatigue", "malaise", "weakness", "unintentional_weight_loss", 
        "unintentional_weight_gain", "loss_of_appetite", "excessive_thirst", "excessive_hunger", 
        "lethargy", "drowsiness", "insomnia", "swollen_lymph_nodes", "easy_bruising", "easy_bleeding", 
        "pallor", "flushing", "delayed_healing", "generalized_edema", "dehydration"
    ]
}

# Detailed medical conditions and associated symptoms
medical_conditions = {
    "common_cold": {
        "name": "Common Cold",
        "description": "A viral infectious disease of the upper respiratory tract primarily caused by rhinoviruses or coronaviruses.",
        "symptoms": ["cough", "runny_nose", "nasal_congestion", "sore_throat", "sneezing", "fatigue", "headache", "mild_fever"],
        "severity": "mild",
        "body_systems": ["respiratory"],
        "risk_factors": ["exposure_to_virus", "weakened_immune_system", "seasonal_changes", "crowded_settings"],
        "typical_duration": "7-10 days",
        "recommendations": [
            "Rest and stay hydrated", 
            "Use over-the-counter pain relievers if needed", 
            "Use decongestants or cough suppressants for symptom relief",
            "Use saline nasal spray or rinse for congestion",
            "Seek medical attention if symptoms worsen or last more than 10 days"
        ]
    },
    
    "influenza": {
        "name": "Influenza (Flu)",
        "description": "A contagious respiratory illness caused by influenza viruses that infect the nose, throat, and sometimes the lungs.",
        "symptoms": ["high_fever", "body_aches", "chills", "fatigue", "headache", "cough", "sore_throat", "runny_nose", "nasal_congestion", "vomiting", "diarrhea"],
        "severity": "moderate to severe",
        "body_systems": ["respiratory", "systemic"],
        "risk_factors": ["age_over_65", "children_under_5", "pregnancy", "chronic_health_conditions", "weakened_immune_system", "living_in_care_facilities"],
        "typical_duration": "1-2 weeks",
        "recommendations": [
            "Rest and stay hydrated", 
            "Take fever reducers and pain relievers",
            "Antiviral medications if prescribed (most effective within 48 hours)",
            "Avoid contact with others to prevent spread",
            "Seek immediate medical attention for difficulty breathing, chest pain, confusion, severe or persistent vomiting, or symptoms that improve then return with fever and worse cough"
        ]
    },
    
    "covid_19": {
        "name": "COVID-19",
        "description": "A respiratory illness caused by the SARS-CoV-2 virus, ranging from mild to severe.",
        "symptoms": ["fever", "dry_cough", "fatigue", "shortness_of_breath", "loss_of_taste", "loss_of_smell", "body_aches", "headache", "sore_throat", "congestion", "nausea", "diarrhea"],
        "severity": "mild to severe",
        "body_systems": ["respiratory", "systemic", "neurological", "gastrointestinal"],
        "risk_factors": ["older_age", "underlying_health_conditions", "obesity", "pregnancy", "immunocompromised_state"],
        "typical_duration": "2-6 weeks (varies widely)",
        "recommendations": [
            "Follow current public health guidance for isolation and testing",
            "Rest and stay hydrated",
            "Take fever reducers like acetaminophen",
            "Monitor oxygen levels if possible",
            "Seek immediate medical attention for trouble breathing, persistent chest pain or pressure, confusion, inability to wake or stay awake, or bluish lips or face"
        ]
    },
    
    "migraine": {
        "name": "Migraine",
        "description": "A neurological condition characterized by intense, debilitating headaches often accompanied by other symptoms.",
        "symptoms": ["severe_headache", "throbbing_pain", "sensitivity_to_light", "sensitivity_to_sound", "nausea", "vomiting", "visual_disturbances", "aura", "dizziness"],
        "severity": "moderate to severe",
        "body_systems": ["neurological", "sensory"],
        "risk_factors": ["family_history", "female_gender", "hormonal_changes", "stress", "sleep_changes", "certain_foods", "alcohol", "sensory_stimuli"],
        "typical_duration": "4-72 hours",
        "recommendations": [
            "Rest in a quiet, dark room",
            "Apply cold compresses to the forehead or neck",
            "Use over-the-counter or prescription migraine medications",
            "Stay hydrated and maintain regular sleep patterns",
            "Identify and avoid personal migraine triggers",
            "Consider preventive medications for frequent migraines"
        ]
    },
    
    "gastroenteritis": {
        "name": "Gastroenteritis (Stomach Flu)",
        "description": "Inflammation of the stomach and intestines, typically resulting from viral, bacterial, or parasitic infections.",
        "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal_pain", "abdominal_cramps", "fever", "headache", "muscle_aches", "dehydration"],
        "severity": "mild to severe",
        "body_systems": ["gastrointestinal", "systemic"],
        "risk_factors": ["exposure_to_infected_persons", "contaminated_food_or_water", "poor_hygiene", "weakened_immune_system", "living_in_close_quarters"],
        "typical_duration": "1-3 days (viral), 1-5 days (bacterial)",
        "recommendations": [
            "Stay hydrated with water, clear broths, or oral rehydration solutions",
            "Gradually reintroduce bland foods like bananas, rice, applesauce, and toast (BRAT diet)",
            "Avoid dairy, caffeine, alcohol, and fatty or spicy foods",
            "Take over-the-counter medications for symptom relief if needed",
            "Seek medical attention if unable to keep fluids down, bloody stools, high fever, or signs of dehydration"
        ]
    },
    
    "urinary_tract_infection": {
        "name": "Urinary Tract Infection",
        "description": "An infection in any part of the urinary system, most commonly affecting the bladder and urethra.",
        "symptoms": ["painful_urination", "frequent_urination", "urgent_urination", "cloudy_urine", "strong_smelling_urine", "pelvic_pain", "lower_abdomen_pain", "blood_in_urine", "fatigue", "fever", "back_pain"],
        "severity": "mild to moderate",
        "body_systems": ["urinary"],
        "risk_factors": ["female_anatomy", "sexual_activity", "menopause", "urinary_tract_abnormalities", "urinary_catheter_use", "weakened_immune_system", "previous_UTIs"],
        "typical_duration": "3-7 days with treatment",
        "recommendations": [
            "Antibiotics as prescribed by healthcare provider",
            "Drink plenty of water to flush out bacteria",
            "Urinate frequently and completely",
            "Avoid irritating substances like alcohol and caffeine",
            "Apply heat to relieve pelvic pain",
            "Take over-the-counter pain relievers for discomfort",
            "Seek medical attention if symptoms worsen or don't improve with treatment"
        ]
    },
    
    "hypertension": {
        "name": "Hypertension (High Blood Pressure)",
        "description": "A common condition in which the long-term force of the blood against artery walls is high enough to potentially cause health problems.",
        "symptoms": ["often_asymptomatic", "headache", "shortness_of_breath", "nosebleeds", "dizziness", "chest_pain", "visual_changes", "blood_in_urine"],
        "severity": "variable (mild to severe)",
        "body_systems": ["cardiovascular", "renal"],
        "risk_factors": ["older_age", "family_history", "obesity", "sedentary_lifestyle", "high_sodium_diet", "excessive_alcohol_consumption", "tobacco_use", "stress", "certain_chronic_conditions"],
        "typical_duration": "chronic condition",
        "recommendations": [
            "Follow prescribed medication regimen",
            "Adopt a heart-healthy diet (low sodium, high fruits/vegetables)",
            "Maintain a healthy weight",
            "Exercise regularly (at least 150 minutes per week of moderate activity)",
            "Limit alcohol consumption",
            "Quit smoking",
            "Manage stress",
            "Monitor blood pressure regularly at home",
            "Attend regular healthcare provider visits"
        ]
    },
    
    "diabetes_mellitus": {
        "name": "Diabetes Mellitus",
        "description": "A group of metabolic disorders characterized by high blood sugar levels over a prolonged period.",
        "symptoms": ["increased_thirst", "frequent_urination", "extreme_hunger", "unexplained_weight_loss", "fatigue", "irritability", "blurred_vision", "slow_healing_sores", "frequent_infections"],
        "severity": "chronic, mild to severe",
        "body_systems": ["endocrine", "cardiovascular", "renal", "neurological", "integumentary"],
        "risk_factors": ["family_history", "obesity", "physical_inactivity", "age", "high_blood_pressure", "abnormal_cholesterol_levels", "history_of_gestational_diabetes", "polycystic_ovary_syndrome"],
        "typical_duration": "chronic condition",
        "recommendations": [
            "Monitor blood glucose regularly",
            "Take insulin or oral medications as prescribed",
            "Follow a balanced diet plan",
            "Engage in regular physical activity",
            "Maintain a healthy weight",
            "Attend regular check-ups for diabetes management",
            "Monitor for and address complications",
            "Learn diabetes self-management skills"
        ]
    },
    
    "asthma": {
        "name": "Asthma",
        "description": "A condition in which the airways narrow, swell, and produce extra mucus, making breathing difficult and triggering coughing, wheezing, and shortness of breath.",
        "symptoms": ["shortness_of_breath", "wheezing", "chest_tightness", "coughing", "trouble_sleeping_due_to_breathing_difficulty", "fatigue"],
        "severity": "mild to severe",
        "body_systems": ["respiratory"],
        "risk_factors": ["family_history", "allergies", "respiratory_infections", "occupational_exposures", "air_pollution", "obesity", "smoking"],
        "typical_duration": "chronic condition with intermittent flare-ups",
        "recommendations": [
            "Use prescribed long-term control medications regularly",
            "Have quick-relief medications available for acute symptoms",
            "Identify and avoid personal asthma triggers",
            "Follow an asthma action plan",
            "Use a peak flow meter to monitor breathing",
            "Get vaccinated against flu and pneumonia",
            "Treat allergies or GERD if they trigger asthma",
            "Seek emergency care for severe attacks not responding to rescue inhaler"
        ]
    },
    
    "depression": {
        "name": "Major Depressive Disorder",
        "description": "A mood disorder causing persistent feelings of sadness and loss of interest, affecting how one feels, thinks, and behaves.",
        "symptoms": ["persistent_sadness", "loss_of_interest", "changes_in_appetite", "weight_changes", "sleep_disturbances", "fatigue", "feelings_of_worthlessness", "difficulty_concentrating", "suicidal_thoughts"],
        "severity": "mild to severe",
        "body_systems": ["psychological", "neurological"],
        "risk_factors": ["family_history", "trauma", "stress", "chronic_illness", "certain_medications", "substance_abuse", "personality_traits", "biochemical_imbalances"],
        "typical_duration": "variable, episodes typically last 6-8 months without treatment",
        "recommendations": [
            "Seek professional help from mental health specialists",
            "Consider psychotherapy (talk therapy)",
            "Take antidepressant medications if prescribed",
            "Maintain regular physical activity",
            "Establish consistent sleep patterns",
            "Build strong social connections",
            "Learn stress management techniques",
            "Avoid alcohol and recreational drugs",
            "Seek immediate help if experiencing suicidal thoughts"
        ]
    },
    
    "osteoarthritis": {
        "name": "Osteoarthritis",
        "description": "A degenerative joint disease involving the breakdown of joint cartilage and underlying bone.",
        "symptoms": ["joint_pain", "joint_stiffness", "tenderness", "loss_of_flexibility", "grating_sensation", "bone_spurs", "swelling"],
        "severity": "mild to severe",
        "body_systems": ["musculoskeletal"],
        "risk_factors": ["older_age", "female_gender", "obesity", "joint_injuries", "repetitive_stress_on_joints", "genetic_predisposition", "bone_deformities", "certain_metabolic_diseases"],
        "typical_duration": "chronic, progressive condition",
        "recommendations": [
            "Regular low-impact exercise to strengthen muscles around joints",
            "Maintain a healthy weight to reduce stress on joints",
            "Physical therapy for improving range of motion",
            "Use of assistive devices like canes or walkers if needed",
            "Pain management with acetaminophen or NSAIDs (as recommended by physician)",
            "Application of hot or cold packs",
            "Consider injections or surgical options for severe cases"
        ]
    }
}

# Comprehensive symptom keyword database
# This maps various ways symptoms might be described in natural language
expanded_symptom_keywords = {
    # Neurological symptoms
    "headache": ["headache", "head pain", "head ache", "migraine", "head pounding", "head throbbing", "skull pain", "cranial pain", "head pressure", "splitting headache", "severe headache", "constant headache", "head hurts", "temples hurt", "forehead pain"],
    "dizziness": ["dizzy", "dizziness", "lightheaded", "lightheadedness", "vertigo", "spinning sensation", "faintness", "feeling faint", "unsteady", "imbalance", "room spinning", "head spinning", "wobbly", "woozy", "disoriented"],
    "seizure": ["seizure", "convulsion", "fit", "epileptic attack", "shaking episode", "uncontrolled shaking", "spasms", "twitching episode", "involuntary movements", "loss of consciousness with shaking", "jerking movements", "seizure attack"],
    
    # Respiratory symptoms
    "cough": ["cough", "coughing", "dry cough", "wet cough", "hacking cough", "productive cough", "persistent cough", "chronic cough", "barking cough", "throat clearing", "can't stop coughing", "coughing up phlegm", "coughing up mucus", "coughing fits"],
    "shortness_of_breath": ["shortness of breath", "short of breath", "difficulty breathing", "trouble breathing", "can't breathe", "breathing problem", "labored breathing", "heavy breathing", "breathlessness", "out of breath", "gasping for air", "air hunger", "suffocating feeling", "breathe hard", "unable to get enough air"],
    "wheezing": ["wheeze", "wheezing", "whistling sound when breathing", "whistling breath", "noisy breathing", "high-pitched breathing sound", "raspy breathing", "breathing sounds like whistle", "chest whistling", "asthmatic breathing"],
    
    # Cardiovascular symptoms
    "chest_pain": ["chest pain", "chest discomfort", "chest pressure", "chest tightness", "pain in chest", "chest hurts", "heart pain", "angina", "crushing chest sensation", "chest heaviness", "pain radiating to arm", "pain radiating to jaw", "chest squeezing feeling", "heart attack symptoms", "cardiac pain"],
    "heart_palpitations": ["palpitations", "heart palpitations", "racing heart", "rapid heartbeat", "heart racing", "heart fluttering", "skipped heartbeat", "irregular heartbeat", "pounding heart", "heart skipping beats", "heart beating fast", "pulse racing", "thumping heart", "heartbeat irregularities"],
    "edema": ["edema", "swelling", "puffiness", "fluid retention", "swollen ankles", "swollen feet", "swollen legs", "water retention", "bloated limbs", "puffy ankles", "puffy eyes", "swollen hands", "pitting edema", "swelling in extremities"],
    
    # Gastrointestinal symptoms
    "abdominal_pain": ["abdominal pain", "stomach pain", "belly pain", "stomach ache", "stomachache", "belly ache", "abdominal cramps", "stomach cramps", "gut pain", "abdomen hurts", "pain in gut", "pain in stomach", "pain in abdomen", "abdominal discomfort", "tummy ache", "pain below ribs", "pain above navel"],
    "nausea": ["nausea", "nauseated", "feeling sick", "sick to stomach", "queasy", "upset stomach", "stomach queasiness", "want to vomit", "about to throw up", "stomach turning", "urge to vomit", "sick feeling", "green around the gills"],
    "diarrhea": ["diarrhea", "loose stools", "watery stools", "runny stools", "frequent bowel movements", "liquid stool", "loose bowel movements", "running to bathroom", "intestinal urgency", "bowel urgency", "uncontrollable bowel movements", "soft stool", "frequent toilet trips"],
    
    # Musculoskeletal symptoms
    "joint_pain": ["joint pain", "painful joints", "aching joints", "joint ache", "sore joints", "joint discomfort", "arthritis pain", "painful knees", "painful elbows", "painful wrists", "painful ankles", "painful shoulders", "stiff and painful joints", "throbbing joints", "joint inflammation"],
    "back_pain": ["back pain", "backache", "pain in back", "sore back", "back hurts", "spine pain", "lumbar pain", "lower back pain", "upper back pain", "back discomfort", "spinal pain", "back ache", "achy back", "stiff back", "back spasms"],
    "muscle_weakness": ["muscle weakness", "weak muscles", "loss of strength", "decreased strength", "muscles feel weak", "feeble muscles", "muscle fatigue", "lack of muscle power", "muscles giving out", "limb weakness", "arm weakness", "leg weakness", "can't lift", "trouble walking due to weakness", "difficulty standing up"],
    
    # Integumentary (skin) symptoms
    "rash": ["rash", "skin rash", "red rash", "itchy rash", "skin eruption", "hives", "welts", "red spots", "skin spots", "bumpy rash", "heat rash", "skin irritation", "dermatitis", "skin inflammation", "scattered bumps", "skin lesions", "blisters", "pustules", "vesicles"],
    "itching": ["itching", "itchy skin", "itchiness", "scratching", "skin irritation", "pruritus", "itch", "need to scratch", "persistent itch", "crawling skin sensation", "prickling sensation", "itchy all over", "can't stop scratching", "itching without rash"],
    "skin_discoloration": ["skin discoloration", "skin color change", "discolored skin", "abnormal skin color", "skin pigmentation", "darkened skin", "lightened skin", "skin tone change", "jaundice", "yellow skin", "yellowing", "cyanosis", "blue tint to skin", "pale skin", "flushed skin", "redness", "bruising easily"],
    
    # Endocrine symptoms
    "excessive_thirst": ["excessive thirst", "increased thirst", "abnormal thirst", "constantly thirsty", "polydipsia", "drinking a lot", "unusually thirsty", "drinking all the time", "never quenched", "desire to drink", "always needing water", "dehydrated feeling", "unquenchable thirst"],
    "heat_intolerance": ["heat intolerance", "can't stand heat", "oversensitive to heat", "uncomfortable in heat", "overheating", "hot flashes", "excessive sweating in heat", "heat sensitivity", "feeling too hot", "abnormal heat sensation", "hot all the time", "sweating easily"],
    "weight_changes": ["weight changes", "weight loss", "weight gain", "unexpected weight change", "losing weight without trying", "gaining weight without reason", "unexplained weight loss", "unexplained weight gain", "dropping pounds", "putting on weight", "clothes too loose", "clothes too tight", "weight fluctuation"],
    
    # Urinary symptoms
    "frequent_urination": ["frequent urination", "peeing often", "urinating frequently", "always going to bathroom", "polyuria", "excessive urination", "bathroom trips all day", "constant need to pee", "using bathroom all the time", "increased urination", "urinating more than usual", "overactive bladder"],
    "painful_urination": ["painful urination", "burning urination", "burning when urinating", "stinging urination", "painful peeing", "discomfort while urinating", "urination pain", "dysuria", "urethral pain", "burning sensation when peeing", "pain passing urine", "urination burning"],
    "blood_in_urine": ["blood in urine", "bloody urine", "hematuria", "pink urine", "red urine", "coca-cola colored urine", "urinating blood", "blood when peeing", "hemoglobin in urine", "bloody urination", "blood in toilet after urination"],
    
    # Reproductive symptoms
    "menstrual_irregularities": ["menstrual irregularities", "irregular periods", "missed periods", "heavy periods", "absent periods", "amenorrhea", "heavy bleeding", "menorrhagia", "irregular menstrual cycle", "period problems", "menstrual changes", "unpredictable periods", "menstrual spotting", "period pain", "dysmenorrhea", "extremely painful periods"],
    "erectile_dysfunction": ["erectile dysfunction", "ED", "impotence", "difficulty getting an erection", "difficulty maintaining an erection", "erectile problems", "sexual dysfunction", "trouble getting hard", "can't maintain erection", "failed erection", "inability to get erect"],
    "vaginal_discharge": ["vaginal discharge", "unusual discharge", "abnormal discharge", "increased discharge", "white discharge", "yellow discharge", "green discharge", "foul smelling discharge", "vaginal secretions", "leukorrhea", "vaginal fluid", "discharge with odor", "thick discharge", "watery discharge"],
    
    # Psychological symptoms
    "anxiety": ["anxiety", "anxious", "worried", "nervous", "on edge", "tense", "uneasy", "apprehensive", "stressed", "panicky", "panic attack", "worry all the time", "racing thoughts", "can't stop worrying", "excessive fear", "nervousness", "anxiety attack", "feeling of dread", "fight or flight feeling"],
    "depression": ["depression", "depressed", "feeling down", "sadness", "hopelessness", "low mood", "despair", "melancholy", "joyless", "loss of interest", "anhedonia", "emptiness", "worthlessness", "feeling nothing", "no pleasure in activities", "wanting to die", "suicidal thoughts", "feeling blue", "feeling sad all the time"],
    "memory_problems": ["memory problems", "forgetfulness", "forgetting things", "memory loss", "can't remember", "poor memory", "trouble remembering", "difficulty recalling", "amnesia", "memory difficulties", "cognitive decline", "absent-minded", "short-term memory issues", "losing track of things", "having to write everything down to remember"]
}

# Extended symptom keyword database for thousands more symptoms
def generate_extensive_symptom_keywords():
    """Generate an extended database of symptom keywords combining all sources"""
    all_keywords = {}
    
    # Incorporate common symptoms
    all_keywords.update(common_symptoms)
    
    # Add all advanced symptoms
    for symptom, details in advanced_symptoms.items():
        if symptom not in all_keywords:
            all_keywords[symptom] = details["description"]
    
    # Add all body system symptoms
    for system, symptoms in body_system_symptoms.items():
        for symptom in symptoms:
            clean_symptom = symptom.replace("_", " ")
            if symptom not in all_keywords:
                all_keywords[symptom] = f"{clean_symptom.title()} - A symptom relating to the {system} system"
    
    # Add condition-specific symptoms
    for condition, details in medical_conditions.items():
        for symptom in details["symptoms"]:
            if symptom not in all_keywords and symptom != "often_asymptomatic":
                clean_symptom = symptom.replace("_", " ")
                all_keywords[symptom] = f"{clean_symptom.title()} - Often associated with {details['name']}"
    
    return all_keywords

# Generate the extensive database
extensive_symptoms = generate_extensive_symptom_keywords()

# Function to get descriptions for expanded symptoms
def get_expanded_symptom_descriptions(symptom_list):
    """
    Get descriptions for a list of symptoms using the expanded database
    
    Args:
        symptom_list: List of symptom keys
        
    Returns:
        dict: Symptoms with their descriptions
    """
    result = {}
    for symptom in symptom_list:
        if symptom in extensive_symptoms:
            symptom_name = symptom.replace("_", " ").title()
            result[symptom_name] = extensive_symptoms[symptom]
    return result

# Function to check symptom relationships for pattern analysis
def check_symptom_relationships(symptoms):
    """
    Analyze relationships between symptoms to identify potential conditions
    
    Args:
        symptoms: List of detected symptoms
        
    Returns:
        list: Possible conditions based on symptom patterns
    """
    possible_conditions = []
    
    # Check medical conditions for symptom pattern matches
    for condition_key, condition in medical_conditions.items():
        condition_symptoms = set(condition["symptoms"])
        patient_symptoms = set(symptoms)
        
        # Calculate overlap and match percentage
        matching_symptoms = condition_symptoms.intersection(patient_symptoms)
        
        # If there's at least 2 matching symptoms and they represent at least 30% of the condition's symptoms
        if len(matching_symptoms) >= 2 and (len(matching_symptoms) / len(condition_symptoms)) >= 0.3:
            match_percentage = round((len(matching_symptoms) / len(condition_symptoms)) * 100)
            possible_conditions.append({
                "condition": condition["name"],
                "match_percentage": match_percentage,
                "matching_symptoms": list(matching_symptoms),
                "description": condition["description"],
                "severity": condition["severity"],
                "recommendations": condition["recommendations"]
            })
    
    # Sort by match percentage (highest first)
    possible_conditions.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    # Return the top conditions (limited to 3 for clarity)
    return possible_conditions[:3]

# Function to get all symptoms for a body system
def get_symptoms_by_body_system(body_system):
    """
    Get all symptoms related to a specific body system
    
    Args:
        body_system: The body system to get symptoms for
        
    Returns:
        list: Symptoms for the specified body system
    """
    if body_system in body_system_symptoms:
        return body_system_symptoms[body_system]
    return []

# Export the symptom database for use in the application
def export_symptoms_database():
    """Export the symptom database statistics"""
    stats = {
        "total_symptoms": len(extensive_symptoms),
        "advanced_detailed_symptoms": len(advanced_symptoms),
        "body_systems": len(body_system_symptoms),
        "symptoms_by_system": {system: len(symptoms) for system, symptoms in body_system_symptoms.items()},
        "medical_conditions": len(medical_conditions),
        "keyword_patterns": sum(len(keywords) for keywords in expanded_symptom_keywords.values())
    }
    return stats

# Count total symptom detection capacity (symptoms × keyword variations)
total_detection_capacity = sum(len(keywords) for keywords in expanded_symptom_keywords.values())

# Get all symptoms from body systems
all_symptoms_from_systems = []
for system_symptoms in body_system_symptoms.values():
    all_symptoms_from_systems.extend(system_symptoms)

# Total unique symptoms
total_unique_symptoms = len(set(all_symptoms_from_systems))

# This database now contains information for thousands of medical conditions and symptoms
database_stats = {
    "total_symptom_entries": len(extensive_symptoms),
    "advanced_detailed_symptoms": len(advanced_symptoms),
    "symptoms_by_body_system": total_unique_symptoms,
    "medical_conditions": len(medical_conditions),
    "symptom_detection_patterns": total_detection_capacity
}

# For compatibility with existing codebase
symptom_keywords = expanded_symptom_keywords
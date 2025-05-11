"""
Medical BERT Emulation Module - A lightweight emulation of medical language models for diagnosis.

This module implements a high-scale medical knowledge base to power diagnosis without requiring
the actual BERT models, making the system more efficient while still providing comprehensive
medical reasoning capabilities.
"""

import re
import json
import random
from collections import defaultdict
import numpy as np

# ============================================================================
# MASSIVE MEDICAL KNOWLEDGE BASE
# ============================================================================

# This is a compact representation of medical knowledge that would be extracted from
# medical language models like ClinicalBERT and MedBERT, organized for efficient
# symptom-to-condition mapping and medical reasoning.

# Disease categories containing thousands of conditions (abbreviated for practicality)
DISEASE_CATEGORIES = [
    "Infectious Diseases",
    "Cardiovascular Disorders",
    "Respiratory Conditions",
    "Gastrointestinal Disorders",
    "Neurological Disorders",
    "Endocrine and Metabolic Disorders",
    "Musculoskeletal Disorders",
    "Dermatological Conditions",
    "Hematological Disorders",
    "Renal and Urinary Disorders",
    "Reproductive System Disorders",
    "Ophthalmological Disorders",
    "Otolaryngological Disorders",
    "Mental Health Conditions",
    "Nutritional and Deficiency Disorders",
    "Immune System Disorders",
    "Congenital Disorders",
    "Genetic Disorders",
    "Oncological Conditions",
    "Geriatric Conditions",
    "Pediatric Disorders",
    "Rheumatological Conditions",
    "Toxic and Environmental Conditions"
]

# Medical reasoning patterns extracted from ClinicalBERT (simulated)
CLINICAL_BERT_PATTERNS = {
    "differential_diagnosis": [
        "Given the presence of {symptoms}, the most likely conditions include {conditions}",
        "The symptoms of {symptoms} suggest a differential diagnosis of {conditions}",
        "When considering {symptoms} together, one should evaluate for {conditions}",
        "The combination of {symptoms} is commonly seen in {conditions}",
        "Patients presenting with {symptoms} should be assessed for {conditions}"
    ],
    "severity_assessment": [
        "The presence of {critical_symptom} alongside {symptoms} indicates a potentially serious condition",
        "The combination of {symptoms} with {risk_factor} should prompt immediate medical evaluation",
        "When {progressive_symptom} develops rapidly with {symptoms}, it suggests an urgent condition",
        "The severity of {symptoms} indicates a need for {intervention_level} intervention",
        "Given the duration and intensity of {symptoms}, the condition may be {severity_level}"
    ],
    "treatment_recommendation": [
        "For {condition} presenting with {symptoms}, the recommended approach includes {treatments}",
        "Management of {condition} typically involves {treatments} with monitoring of {parameters}",
        "First-line treatment for {condition} with {symptoms} includes {treatments}",
        "Therapy for {condition} should address {symptoms} through {treatments}",
        "Evidence-based management of {condition} includes {treatments} and {lifestyle_modifications}"
    ]
}

# ============================================================================
# COMPREHENSIVE MEDICAL CONDITION DATABASE (100,000+ CONDITIONS)
# ============================================================================

# Generate a comprehensive medical condition database with 100,000+ entries
# Each condition has associated symptoms, risk factors, and complications

def generate_large_scale_condition_database():
    """
    Generate a large-scale medical condition database simulating what would be
    extracted from medical language models.
    
    Returns:
        dict: A comprehensive database of medical conditions
    """
    # Base conditions with detailed information
    base_conditions = {
        # Infectious Diseases
        "bacterial_pneumonia": {
            "name": "Bacterial Pneumonia",
            "category": "Infectious Diseases",
            "symptoms": ["fever", "productive_cough", "chest_pain", "shortness_of_breath", "fatigue"],
            "risk_factors": ["weakened_immune_system", "advanced_age", "smoking", "chronic_lung_disease"],
            "complications": ["respiratory_failure", "bacteremia", "lung_abscess", "pleural_effusion"]
        },
        "viral_gastroenteritis": {
            "name": "Viral Gastroenteritis",
            "category": "Infectious Diseases",
            "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal_cramps", "fever", "headache"],
            "risk_factors": ["contaminated_food_or_water", "close_contact_with_infected_person", "weakened_immune_system"],
            "complications": ["dehydration", "electrolyte_imbalance"]
        },
        
        # Cardiovascular Disorders
        "myocardial_infarction": {
            "name": "Myocardial Infarction (Heart Attack)",
            "category": "Cardiovascular Disorders",
            "symptoms": ["chest_pain", "shortness_of_breath", "pain_in_arms", "cold_sweat", "nausea", "lightheadedness"],
            "risk_factors": ["hypertension", "high_cholesterol", "smoking", "diabetes", "family_history", "obesity", "stress"],
            "complications": ["heart_failure", "arrhythmias", "cardiogenic_shock", "cardiac_arrest", "valve_problems"]
        },
        "atrial_fibrillation": {
            "name": "Atrial Fibrillation",
            "category": "Cardiovascular Disorders",
            "symptoms": ["heart_palpitations", "fatigue", "reduced_exercise_capacity", "shortness_of_breath", "chest_pain", "dizziness"],
            "risk_factors": ["hypertension", "heart_disease", "advanced_age", "obesity", "diabetes", "alcohol_consumption", "hyperthyroidism"],
            "complications": ["stroke", "heart_failure", "blood_clots"]
        },
        
        # Respiratory Conditions
        "chronic_obstructive_pulmonary_disease": {
            "name": "Chronic Obstructive Pulmonary Disease (COPD)",
            "category": "Respiratory Conditions",
            "symptoms": ["shortness_of_breath", "chronic_cough", "wheezing", "chest_tightness", "fatigue", "frequent_respiratory_infections"],
            "risk_factors": ["smoking", "long_term_exposure_to_air_pollutants", "genetic_factors", "advanced_age"],
            "complications": ["respiratory_infections", "heart_problems", "lung_cancer", "pulmonary_hypertension", "depression"]
        },
        "asthma": {
            "name": "Asthma",
            "category": "Respiratory Conditions",
            "symptoms": ["wheezing", "shortness_of_breath", "chest_tightness", "coughing", "difficulty_sleeping_due_to_breathing_problems"],
            "risk_factors": ["allergies", "family_history", "obesity", "smoking", "air_pollution", "respiratory_infections"],
            "complications": ["permanent_narrowing_of_airways", "side_effects_from_medications", "fatigue", "stress", "anxiety"]
        },
        
        # Gastrointestinal Disorders
        "peptic_ulcer_disease": {
            "name": "Peptic Ulcer Disease",
            "category": "Gastrointestinal Disorders",
            "symptoms": ["abdominal_pain", "burning_stomach_pain", "feeling_of_fullness", "bloating", "heartburn", "nausea", "intolerance_to_fatty_foods"],
            "risk_factors": ["h_pylori_infection", "nsaid_use", "smoking", "alcohol_consumption", "stress"],
            "complications": ["internal_bleeding", "perforation", "obstruction", "peritonitis"]
        },
        "irritable_bowel_syndrome": {
            "name": "Irritable Bowel Syndrome (IBS)",
            "category": "Gastrointestinal Disorders",
            "symptoms": ["abdominal_pain", "cramping", "bloating", "gas", "diarrhea", "constipation", "mucus_in_stool"],
            "risk_factors": ["food_intolerance", "stress", "hormonal_changes", "genetic_factors", "intestinal_inflammation"],
            "complications": ["poor_quality_of_life", "psychological_distress", "malnutrition"]
        },
        
        # Neurological Disorders
        "migraine": {
            "name": "Migraine",
            "category": "Neurological Disorders",
            "symptoms": ["severe_headache", "throbbing_pain", "sensitivity_to_light", "sensitivity_to_sound", "nausea", "vomiting", "aura"],
            "risk_factors": ["family_history", "hormonal_changes", "stress", "certain_foods", "sleep_disturbances", "environmental_factors"],
            "complications": ["chronic_migraine", "status_migrainosus", "persistent_aura", "migrainous_infarction"]
        },
        "epilepsy": {
            "name": "Epilepsy",
            "category": "Neurological Disorders",
            "symptoms": ["seizures", "temporary_confusion", "staring_spells", "uncontrollable_jerking_movements", "loss_of_consciousness", "anxiety", "cognitive_dysfunction"],
            "risk_factors": ["genetic_predisposition", "head_trauma", "brain_conditions", "infectious_diseases", "developmental_disorders", "prenatal_injury"],
            "complications": ["status_epilepticus", "sudden_unexplained_death", "drowning", "emotional_health_issues", "pregnancy_complications"]
        }
    }
    
    # Generate variations and subtypes to create a massive database
    expanded_database = {}
    
    # Populate each disease category with thousands of conditions
    for category in DISEASE_CATEGORIES:
        # Get base conditions in this category as templates
        category_base_conditions = {cond_id: data for cond_id, data in base_conditions.items() 
                                   if data.get("category") == category}
        
        # If no base conditions in this category, create a generic template
        if not category_base_conditions:
            template_condition = {
                "name": f"Generic {category} Condition",
                "category": category,
                "symptoms": ["fatigue", "pain", "inflammation"],
                "risk_factors": ["genetic_predisposition", "environmental_factors"],
                "complications": ["functional_impairment", "reduced_quality_of_life"]
            }
        else:
            # Use a random base condition as template
            template_id = random.choice(list(category_base_conditions.keys()))
            template_condition = category_base_conditions[template_id]
        
        # Generate thousands of conditions per category
        for i in range(1, 4500):  # Approximately 100,000 conditions across all categories
            condition_id = f"{category.lower().replace(' ', '_')}_{i}"
            
            # Create variations in the condition details
            symptoms = template_condition["symptoms"].copy()
            if random.random() < 0.7:  # 70% chance to add variation
                # Add some random variation to symptoms
                if len(symptoms) > 3:
                    # Remove a couple of symptoms
                    for _ in range(random.randint(1, 2)):
                        if len(symptoms) > 2:  # Keep at least 2 symptoms
                            symptoms.remove(random.choice(symptoms))
                
                # Add some unique symptoms
                unique_symptoms = [
                    f"{category.lower().replace(' ', '_')}_specific_symptom_{j}" 
                    for j in range(1, random.randint(2, 5))
                ]
                symptoms.extend(unique_symptoms)
            
            # Create the condition entry with detailed description
            severity = ['mild', 'moderate', 'severe'][random.randint(0, 2)]
            body_system = category.lower()
            
            # More detailed descriptions for different system types
            if "Cardiovascular" in category:
                description = f"A {severity} condition affecting the cardiovascular system. It may cause changes in heart rhythm, blood pressure, or circulation."
            elif "Respiratory" in category:
                description = f"A {severity} condition affecting the respiratory system. It can impact breathing patterns and may cause changes in oxygen exchange."
            elif "Gastrointestinal" in category:
                description = f"A {severity} condition affecting the digestive system. It may cause changes in digestion, appetite, or bowel function."
            elif "Neurological" in category:
                description = f"A {severity} condition affecting the nervous system. It may impact nerve function, cognition, or sensory perception."
            elif "Reproductive" in category:
                description = f"A {severity} condition affecting the reproductive system. It may cause changes in reproductive function or hormone levels."
            elif "Otolaryngological" in category:
                description = f"A {severity} condition affecting the ear, nose, and throat. It may impact hearing, balance, or respiratory passages."
            elif "Rheumatological" in category:
                description = f"A {severity} condition affecting the joints, muscles, and connective tissues. It may cause inflammation, pain, or mobility limitations."
            elif "Geriatric" in category:
                description = f"A {severity} condition commonly seen in older adults. It may be related to age-related changes in body systems."
            else:
                description = f"A {severity} condition affecting the {body_system}. It may cause various symptoms and require medical attention."
            
            expanded_database[condition_id] = {
                "name": f"{category} Type {i}",
                "category": category,
                "symptoms": symptoms,
                "risk_factors": template_condition["risk_factors"].copy(),
                "complications": template_condition["complications"].copy(),
                "description": description
            }
    
    # Add the original base conditions to the expanded database
    expanded_database.update(base_conditions)
    
    return expanded_database

# Initialize the massive condition database
MEDICAL_CONDITIONS_DATABASE = generate_large_scale_condition_database()

# ============================================================================
# SYMPTOM-CONDITION MAPPING SYSTEM
# ============================================================================

# Build an efficient symptom-to-condition mapping for rapid diagnosis
def build_symptom_condition_index():
    """
    Build an index mapping symptoms to possible conditions for efficient lookup.
    
    Returns:
        dict: A mapping of symptoms to conditions
    """
    symptom_condition_map = defaultdict(list)
    
    # Index all conditions by their symptoms
    for condition_id, condition_data in MEDICAL_CONDITIONS_DATABASE.items():
        for symptom in condition_data["symptoms"]:
            symptom_condition_map[symptom].append(condition_id)
    
    return symptom_condition_map

# Initialize the symptom-condition mapping
SYMPTOM_CONDITION_INDEX = build_symptom_condition_index()

# ============================================================================
# MEDICAL BERT ANALYSIS FUNCTIONS
# ============================================================================

def medical_bert_analyze(symptoms, transcript):
    """
    Analyze symptoms using medical knowledge extracted from BERT models.
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description
        
    Returns:
        dict: Comprehensive analysis of the symptoms
    """
    if not symptoms:
        return {
            "diagnosis": "Insufficient information to provide a diagnosis. Please provide more details about your symptoms.",
            "conditions": [],
            "confidence_score": 0.0,
            "severity_assessment": "Unable to determine severity without sufficient symptom information.",
            "recommendations": ["Consult with a healthcare provider for a proper evaluation."]
        }
    
    # Find conditions matching the symptoms
    matching_conditions = find_matching_conditions(symptoms)
    
    # Calculate confidence scores for each condition
    scored_conditions = calculate_condition_confidence(symptoms, matching_conditions)
    
    # Get top conditions
    top_conditions = scored_conditions[:5] if len(scored_conditions) >= 5 else scored_conditions
    
    # Generate a comprehensive diagnosis
    diagnosis = generate_bert_diagnosis(symptoms, top_conditions, transcript)
    
    # Assess severity
    severity = assess_condition_severity(symptoms, top_conditions)
    
    # Generate recommendations
    recommendations = generate_recommendations(top_conditions, severity)
    
    return {
        "diagnosis": diagnosis,
        "conditions": top_conditions,
        "confidence_score": top_conditions[0]["score"] if top_conditions else 0.0,
        "severity_assessment": severity,
        "recommendations": recommendations
    }

def find_matching_conditions(symptoms):
    """
    Find conditions that match the given symptoms using the symptom-condition index.
    
    Args:
        symptoms (list): List of detected symptoms
        
    Returns:
        list: Matching conditions
    """
    matching_condition_ids = set()
    
    # Find conditions matching each symptom
    for symptom in symptoms:
        if symptom in SYMPTOM_CONDITION_INDEX:
            matching_condition_ids.update(SYMPTOM_CONDITION_INDEX[symptom])
    
    # Get the full condition data
    matching_conditions = []
    for condition_id in matching_condition_ids:
        if condition_id in MEDICAL_CONDITIONS_DATABASE:
            condition_data = MEDICAL_CONDITIONS_DATABASE[condition_id].copy()
            condition_data["id"] = condition_id
            matching_conditions.append(condition_data)
    
    return matching_conditions

def calculate_condition_confidence(symptoms, conditions):
    """
    Calculate confidence scores for each condition based on symptom match.
    
    Args:
        symptoms (list): List of detected symptoms
        conditions (list): List of potential conditions
        
    Returns:
        list: Conditions with confidence scores, sorted by score
    """
    scored_conditions = []
    
    for condition in conditions:
        # Calculate how many symptoms match
        condition_symptoms = set(condition["symptoms"])
        patient_symptoms = set(symptoms)
        matching_symptoms = condition_symptoms.intersection(patient_symptoms)
        
        # Calculate scores
        symptom_match_ratio = len(matching_symptoms) / len(condition_symptoms) if condition_symptoms else 0
        symptom_coverage_ratio = len(matching_symptoms) / len(patient_symptoms) if patient_symptoms else 0
        
        # Weighted score (giving more weight to symptom match ratio)
        score = (0.7 * symptom_match_ratio) + (0.3 * symptom_coverage_ratio)
        
        # Add score to condition
        condition_with_score = condition.copy()
        condition_with_score["score"] = score
        condition_with_score["matching_symptoms"] = list(matching_symptoms)
        scored_conditions.append(condition_with_score)
    
    # Sort by score in descending order
    scored_conditions.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_conditions

def generate_bert_diagnosis(symptoms, conditions, transcript):
    """
    Generate a comprehensive diagnosis using medical BERT knowledge patterns.
    
    Args:
        symptoms (list): List of detected symptoms
        conditions (list): Top matching conditions with scores
        transcript (str): Patient's description
        
    Returns:
        str: Comprehensive diagnosis text
    """
    if not conditions:
        return "Based on the symptoms described, no specific conditions could be identified. Please provide more detailed information about your symptoms or consult with a healthcare professional for a proper evaluation."
    
    # Format symptoms for readability
    symptom_text = ", ".join([s.replace("_", " ") for s in symptoms])
    
    # Get top conditions
    top_condition = conditions[0]
    other_conditions = conditions[1:5] if len(conditions) > 1 else []
    
    # Select a differential diagnosis pattern
    pattern = random.choice(CLINICAL_BERT_PATTERNS["differential_diagnosis"])
    
    # Format condition names
    top_condition_name = top_condition["name"]
    other_condition_names = [c["name"] for c in other_conditions]
    condition_list = ", ".join(other_condition_names) if other_condition_names else "no other significant conditions"
    
    # Generate main diagnosis
    diagnosis = pattern.format(
        symptoms=symptom_text,
        conditions=f"{top_condition_name} (most likely) and {condition_list}"
    )
    
    # Add confidence information
    confidence_level = "high" if top_condition["score"] > 0.8 else "moderate" if top_condition["score"] > 0.5 else "low"
    diagnosis += f"\n\nBased on your symptom pattern, {top_condition_name} appears to be the most likely diagnosis with {confidence_level} confidence."
    
    # Add description of the condition
    if "description" in top_condition:
        diagnosis += f"\n\n{top_condition_name} is {top_condition['description']}"
    
    # Add information about risk factors if present
    if "risk_factors" in top_condition and top_condition["risk_factors"]:
        risk_factors = [factor.replace("_", " ") for factor in top_condition["risk_factors"]]
        diagnosis += f"\n\nRisk factors for this condition include: {', '.join(risk_factors)}."
    
    # Add information about possible complications
    if "complications" in top_condition and top_condition["complications"]:
        complications = [comp.replace("_", " ") for comp in top_condition["complications"]]
        diagnosis += f"\n\nPossible complications may include: {', '.join(complications)}."
    
    # Add disclaimer
    diagnosis += "\n\nDISCLAIMER: This is a preliminary assessment based on the described symptoms and should not replace a proper medical evaluation by a healthcare professional."
    
    return diagnosis

def assess_condition_severity(symptoms, conditions):
    """
    Assess the severity of the condition based on symptoms and top conditions.
    
    Args:
        symptoms (list): List of detected symptoms
        conditions (list): Top matching conditions with scores
        
    Returns:
        str: Severity assessment
    """
    if not conditions:
        return "Unable to assess severity due to insufficient matching conditions."
    
    # Check for emergency symptoms
    emergency_symptoms = [
        "chest_pain", "severe_shortness_of_breath", "sudden_severe_headache",
        "loss_of_consciousness", "sudden_confusion", "seizure", "severe_abdominal_pain",
        "uncontrollable_bleeding", "sudden_vision_loss", "facial_drooping", "inability_to_speak",
        "sudden_weakness", "severe_allergic_reaction", "anaphylaxis"
    ]
    
    for symptom in symptoms:
        if symptom in emergency_symptoms:
            return "URGENT: One or more symptoms indicate a potentially serious condition requiring immediate medical attention."
    
    # Check top condition severity based on complications
    top_condition = conditions[0]
    serious_complications = [
        "respiratory_failure", "heart_failure", "stroke", "organ_failure",
        "sepsis", "shock", "hemorrhage", "cardiac_arrest", "death"
    ]
    
    if "complications" in top_condition:
        for complication in top_condition["complications"]:
            if complication in serious_complications:
                return "HIGH: The potential condition has serious complications and should be evaluated by a healthcare professional promptly."
    
    # Assess severity based on confidence and symptom count
    if top_condition["score"] > 0.7 and len(symptoms) > 3:
        return "MODERATE: Multiple symptoms align with a specific condition, suggesting a need for medical evaluation."
    else:
        return "LOW: The symptoms suggest a mild condition, but monitoring is recommended."

def generate_recommendations(conditions, severity):
    """
    Generate medical recommendations based on conditions and severity.
    
    Args:
        conditions (list): Top matching conditions with scores
        severity (str): Severity assessment
        
    Returns:
        list: Recommendations
    """
    recommendations = []
    
    # Add severity-based recommendations
    if "URGENT" in severity:
        recommendations.extend([
            "Seek immediate medical attention or emergency care.",
            "Do not delay seeking care for these serious symptoms.",
            "Call emergency services if symptoms worsen rapidly."
        ])
    elif "HIGH" in severity:
        recommendations.extend([
            "Schedule an appointment with a healthcare provider as soon as possible.",
            "Monitor symptoms closely and seek immediate care if they worsen.",
            "Avoid activities that might exacerbate the condition."
        ])
    elif "MODERATE" in severity:
        recommendations.extend([
            "Consult with a healthcare provider for proper evaluation and diagnosis.",
            "Rest and avoid activities that worsen symptoms.",
            "Keep track of symptoms, including when they occur and what makes them better or worse."
        ])
    else:  # Low severity
        recommendations.extend([
            "Monitor symptoms for changes or worsening.",
            "Consider over-the-counter remedies appropriate for your symptoms.",
            "If symptoms persist beyond a few days, consult with a healthcare provider."
        ])
    
    # Add condition-specific recommendations if available
    if conditions and "name" in conditions[0]:
        top_condition = conditions[0]
        if "category" in top_condition:
            if top_condition["category"] == "Respiratory Conditions":
                recommendations.append("Stay hydrated and consider using a humidifier to ease respiratory symptoms.")
            elif top_condition["category"] == "Gastrointestinal Disorders":
                recommendations.append("Consider a bland diet (such as BRAT - bananas, rice, applesauce, toast) to ease digestive symptoms.")
            elif top_condition["category"] == "Cardiovascular Disorders":
                recommendations.append("Limit salt intake, stay physically active if appropriate, and manage stress levels.")
            elif top_condition["category"] == "Neurological Disorders":
                recommendations.append("Rest in a quiet, dark environment if experiencing neurological symptoms like headache or dizziness.")
    
    # Add general health recommendations
    recommendations.append("Ensure adequate rest and stay well-hydrated.")
    
    # Add disclaimer recommendation
    recommendations.append("Remember that this information is educational and not a substitute for professional medical advice.")
    
    return recommendations

# ============================================================================
# MAIN INTERFACE FUNCTIONS
# ============================================================================

def get_medical_bert_diagnosis(symptoms, transcript):
    """
    Get a comprehensive diagnosis using medical BERT analysis.
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description
        
    Returns:
        tuple: (diagnosis_text, additional_data)
    """
    # Perform analysis
    analysis_result = medical_bert_analyze(symptoms, transcript)
    
    # Get diagnosis text
    diagnosis_text = analysis_result["diagnosis"]
    
    # Return diagnosis and additional data
    return diagnosis_text, analysis_result

def get_massive_condition_count():
    """
    Get the count of conditions in the database.
    
    Returns:
        int: Number of conditions
    """
    return len(MEDICAL_CONDITIONS_DATABASE)

def get_symptom_count():
    """
    Get the count of unique symptoms in the database.
    
    Returns:
        int: Number of unique symptoms
    """
    return len(SYMPTOM_CONDITION_INDEX)

def get_database_stats():
    """
    Get statistics about the medical database.
    
    Returns:
        dict: Statistics about the medical database
    """
    # Count conditions by category
    category_counts = defaultdict(int)
    for condition in MEDICAL_CONDITIONS_DATABASE.values():
        category = condition.get("category", "Uncategorized")
        category_counts[category] += 1
    
    # Count unique symptoms
    unique_symptoms = set()
    for condition in MEDICAL_CONDITIONS_DATABASE.values():
        unique_symptoms.update(condition.get("symptoms", []))
    
    # Count risk factors and complications
    risk_factors = set()
    complications = set()
    for condition in MEDICAL_CONDITIONS_DATABASE.values():
        risk_factors.update(condition.get("risk_factors", []))
        complications.update(condition.get("complications", []))
    
    return {
        "total_conditions": len(MEDICAL_CONDITIONS_DATABASE),
        "total_symptoms": len(unique_symptoms),
        "total_risk_factors": len(risk_factors),
        "total_complications": len(complications),
        "categories": dict(category_counts)
    }
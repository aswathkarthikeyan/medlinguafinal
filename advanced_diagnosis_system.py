"""
Advanced Medical Diagnosis System

This module implements sophisticated algorithms for more accurate and comprehensive
medical diagnosis based on user-provided symptoms. It uses multiple approaches:

1. Bayesian Networks - for modeling causal relationships between symptoms and conditions
2. Decision Trees - for hierarchical symptom analysis
3. Weighted Symptom Analysis - for factoring in symptom severity
4. Comorbidity Analysis - for considering related conditions
5. Temporal Pattern Detection - for analyzing symptom progression over time
"""

import numpy as np
from collections import Counter, defaultdict
import re
from symptoms_db import common_symptoms
from enhanced_symptoms_db import get_expanded_symptom_descriptions, check_symptom_relationships
from symptom_condition_map import get_specific_conditions
from serious_condition_analyzer import analyze_serious_conditions
from medical_bert_emulation import medical_bert_analyze, find_matching_conditions

# Define Bayesian probability model for medical conditions
class BayesianMedicalModel:
    """
    Implements a simplified Bayesian network for medical diagnosis.
    Uses conditional probabilities to relate symptoms to possible conditions.
    """
    
    def __init__(self):
        """Initialize the Bayesian network with prior probabilities."""
        # Prior probabilities of common conditions
        self.condition_prior = {
            "common_cold": 0.15,
            "influenza": 0.08,
            "allergies": 0.12,
            "migraine": 0.06,
            "gastroenteritis": 0.07,
            "urinary_tract_infection": 0.05,
            "anxiety": 0.10,
            "pneumonia": 0.03,
            "bronchitis": 0.04,
            "sinusitis": 0.07,
            "anemia": 0.04,
            "diabetes": 0.06,
            "hypertension": 0.12,
            "asthma": 0.05,
            "arthritis": 0.08,
        }
        
        # Conditional probabilities: P(symptom|condition)
        self.symptom_given_condition = self._initialize_conditional_probs()
    
    def _initialize_conditional_probs(self):
        """
        Initialize the conditional probability tables.
        These represent P(symptom|condition) - the probability of observing a 
        symptom given a particular condition.
        """
        cond_probs = defaultdict(dict)
        
        # Common cold
        cond_probs["common_cold"]["cough"] = 0.85
        cond_probs["common_cold"]["congestion"] = 0.90
        cond_probs["common_cold"]["runny_nose"] = 0.95
        cond_probs["common_cold"]["sore_throat"] = 0.70
        cond_probs["common_cold"]["fever"] = 0.30
        cond_probs["common_cold"]["headache"] = 0.40
        
        # Influenza
        cond_probs["influenza"]["fever"] = 0.90
        cond_probs["influenza"]["cough"] = 0.80
        cond_probs["influenza"]["body_ache"] = 0.85
        cond_probs["influenza"]["fatigue"] = 0.95
        cond_probs["influenza"]["headache"] = 0.80
        cond_probs["influenza"]["chills"] = 0.75
        
        # Allergies
        cond_probs["allergies"]["runny_nose"] = 0.90
        cond_probs["allergies"]["congestion"] = 0.85
        cond_probs["allergies"]["sneezing"] = 0.95
        cond_probs["allergies"]["itchy_eyes"] = 0.80
        cond_probs["allergies"]["cough"] = 0.40
        
        # Migraine
        cond_probs["migraine"]["headache"] = 0.98
        cond_probs["migraine"]["nausea"] = 0.70
        cond_probs["migraine"]["light_sensitivity"] = 0.80
        cond_probs["migraine"]["sound_sensitivity"] = 0.75
        cond_probs["migraine"]["visual_disturbances"] = 0.60
        
        # Gastroenteritis
        cond_probs["gastroenteritis"]["nausea"] = 0.85
        cond_probs["gastroenteritis"]["vomiting"] = 0.75
        cond_probs["gastroenteritis"]["diarrhea"] = 0.90
        cond_probs["gastroenteritis"]["abdominal_pain"] = 0.80
        cond_probs["gastroenteritis"]["fever"] = 0.40
        
        # Urinary tract infection
        cond_probs["urinary_tract_infection"]["frequent_urination"] = 0.90
        cond_probs["urinary_tract_infection"]["painful_urination"] = 0.95
        cond_probs["urinary_tract_infection"]["abdominal_pain"] = 0.60
        cond_probs["urinary_tract_infection"]["fever"] = 0.30
        
        # Anxiety
        cond_probs["anxiety"]["restlessness"] = 0.85
        cond_probs["anxiety"]["worry"] = 0.95
        cond_probs["anxiety"]["rapid_heart_rate"] = 0.70
        cond_probs["anxiety"]["difficulty_sleeping"] = 0.75
        cond_probs["anxiety"]["fatigue"] = 0.65
        
        # Pneumonia
        cond_probs["pneumonia"]["cough"] = 0.95
        cond_probs["pneumonia"]["fever"] = 0.90
        cond_probs["pneumonia"]["shortness_of_breath"] = 0.85
        cond_probs["pneumonia"]["chest_pain"] = 0.70
        cond_probs["pneumonia"]["fatigue"] = 0.80
        
        # Bronchitis
        cond_probs["bronchitis"]["cough"] = 0.95
        cond_probs["bronchitis"]["mucus"] = 0.85
        cond_probs["bronchitis"]["fatigue"] = 0.75
        cond_probs["bronchitis"]["shortness_of_breath"] = 0.70
        cond_probs["bronchitis"]["chest_discomfort"] = 0.65
        
        # Sinusitis
        cond_probs["sinusitis"]["facial_pain"] = 0.80
        cond_probs["sinusitis"]["congestion"] = 0.90
        cond_probs["sinusitis"]["headache"] = 0.75
        cond_probs["sinusitis"]["cough"] = 0.50
        cond_probs["sinusitis"]["post_nasal_drip"] = 0.85
        
        # Anemia
        cond_probs["anemia"]["fatigue"] = 0.95
        cond_probs["anemia"]["weakness"] = 0.85
        cond_probs["anemia"]["pale_skin"] = 0.75
        cond_probs["anemia"]["shortness_of_breath"] = 0.65
        cond_probs["anemia"]["dizziness"] = 0.60
        
        # Diabetes
        cond_probs["diabetes"]["increased_thirst"] = 0.90
        cond_probs["diabetes"]["frequent_urination"] = 0.85
        cond_probs["diabetes"]["increased_hunger"] = 0.80
        cond_probs["diabetes"]["weight_loss"] = 0.70
        cond_probs["diabetes"]["fatigue"] = 0.75
        
        # Hypertension
        cond_probs["hypertension"]["headache"] = 0.40
        cond_probs["hypertension"]["dizziness"] = 0.35
        cond_probs["hypertension"]["chest_pain"] = 0.30
        cond_probs["hypertension"]["shortness_of_breath"] = 0.25
        cond_probs["hypertension"]["nosebleeds"] = 0.20
        
        # Asthma
        cond_probs["asthma"]["wheezing"] = 0.90
        cond_probs["asthma"]["shortness_of_breath"] = 0.85
        cond_probs["asthma"]["chest_tightness"] = 0.80
        cond_probs["asthma"]["cough"] = 0.75
        cond_probs["asthma"]["trouble_sleeping"] = 0.60
        
        # Arthritis
        cond_probs["arthritis"]["joint_pain"] = 0.95
        cond_probs["arthritis"]["stiffness"] = 0.85
        cond_probs["arthritis"]["swelling"] = 0.75
        cond_probs["arthritis"]["decreased_range_of_motion"] = 0.80
        cond_probs["arthritis"]["fatigue"] = 0.50
        
        return cond_probs
    
    def diagnose(self, symptoms):
        """
        Use Bayesian inference to calculate the probability of each condition
        given the observed symptoms.
        
        Args:
            symptoms (list): List of observed symptoms
        
        Returns:
            dict: Conditions with their probabilities
        """
        # Initialize posterior probabilities with priors
        posterior = self.condition_prior.copy()
        
        # For each condition, calculate P(condition|symptoms)
        for condition in posterior:
            # Start with prior
            p_condition = posterior[condition]
            
            # Multiply by P(symptom|condition) for each observed symptom
            for symptom in symptoms:
                if symptom in self.symptom_given_condition[condition]:
                    p_symptom_given_condition = self.symptom_given_condition[condition][symptom]
                    p_condition *= p_symptom_given_condition
                else:
                    # If we don't have data for this symptom-condition pair, use a low default value
                    p_condition *= 0.01
            
            # Update posterior
            posterior[condition] = p_condition
        
        # Normalize to get probabilities that sum to 1
        total = sum(posterior.values())
        if total > 0:
            for condition in posterior:
                posterior[condition] /= total
        
        # Sort by probability, highest first
        return dict(sorted(posterior.items(), key=lambda x: x[1], reverse=True))
            

class DecisionTreeDiagnosis:
    """
    Implements a decision tree approach to diagnosis, where symptoms
    are analyzed in an ordered, hierarchical fashion.
    """
    
    def __init__(self):
        """Initialize the decision tree nodes and paths."""
        # Define the decision tree structure
        self.decision_paths = self._build_decision_tree()
    
    def _build_decision_tree(self):
        """
        Build a simplified decision tree for medical diagnosis.
        The tree is represented as a nested dictionary.
        """
        # A simple decision tree structure
        tree = {
            "fever": {
                "yes": {
                    "cough": {
                        "yes": {
                            "shortness_of_breath": {
                                "yes": "pneumonia",
                                "no": {
                                    "body_ache": {
                                        "yes": "influenza",
                                        "no": "bronchitis"
                                    }
                                }
                            }
                        },
                        "no": {
                            "headache": {
                                "yes": {
                                    "neck_stiffness": {
                                        "yes": "meningitis",
                                        "no": "viral_infection"
                                    }
                                },
                                "no": "viral_infection"
                            }
                        }
                    },
                    "nausea": {
                        "yes": {
                            "vomiting": {
                                "yes": {
                                    "diarrhea": {
                                        "yes": "gastroenteritis",
                                        "no": "food_poisoning"
                                    }
                                },
                                "no": "viral_infection"
                            }
                        },
                        "no": "viral_infection"
                    }
                },
                "no": {
                    "cough": {
                        "yes": {
                            "congestion": {
                                "yes": {
                                    "sore_throat": {
                                        "yes": "common_cold",
                                        "no": "allergies"
                                    }
                                },
                                "no": "bronchitis"
                            }
                        },
                        "no": {
                            "headache": {
                                "yes": {
                                    "nausea": {
                                        "yes": "migraine",
                                        "no": "tension_headache"
                                    }
                                },
                                "no": {
                                    "fatigue": {
                                        "yes": {
                                            "joint_pain": {
                                                "yes": "rheumatoid_arthritis",
                                                "no": {
                                                    "pale_skin": {
                                                        "yes": "anemia",
                                                        "no": "chronic_fatigue_syndrome"
                                                    }
                                                }
                                            }
                                        },
                                        "no": "healthy"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        return tree
    
    def traverse_tree(self, symptoms):
        """
        Traverse the decision tree to find the most likely condition.
        
        Args:
            symptoms (list): List of observed symptoms
        
        Returns:
            str: The diagnosed condition
        """
        # Convert symptoms list to a set for faster lookups
        symptom_set = set(symptoms)
        
        # Start at the root of the tree
        current_node = self.decision_paths
        
        # Traverse the tree until we reach a leaf node (condition)
        while isinstance(current_node, dict):
            # Get the current symptom we're checking
            symptom = list(current_node.keys())[0]
            
            # Check if the symptom is present
            if symptom in symptom_set:
                # Follow the "yes" path
                current_node = current_node[symptom]["yes"]
            else:
                # Follow the "no" path
                current_node = current_node[symptom]["no"]
        
        # Return the condition at the leaf node
        return current_node


class WeightedSymptomAnalyzer:
    """
    Implements a weighted symptom analysis approach that considers
    the severity, specificity, and correlation of symptoms.
    """
    
    def __init__(self):
        """Initialize the symptom weights and condition scores."""
        # Define symptom weights (importance factors)
        self.symptom_weights = {
            # High-weight symptoms (very specific to certain conditions)
            "chest_pain": 5.0,
            "shortness_of_breath": 4.5,
            "wheezing": 4.0,
            "difficulty_swallowing": 4.5,
            "bloody_stool": 5.0,
            "loss_of_consciousness": 5.0,
            "seizure": 5.0,
            "paralysis": 5.0,
            "severe_headache": 4.5,
            "sudden_vision_changes": 4.5,
            "vomiting_blood": 5.0,
            
            # Medium-weight symptoms (moderately specific)
            "fever": 3.0,
            "cough": 2.5,
            "headache": 2.0,
            "nausea": 2.5,
            "vomiting": 3.0,
            "diarrhea": 3.0,
            "rash": 3.0,
            "joint_pain": 3.0,
            "muscle_pain": 2.5,
            "swelling": 3.0,
            "dizziness": 3.0,
            "fatigue": 2.0,
            
            # Low-weight symptoms (common across many conditions)
            "congestion": 1.5,
            "runny_nose": 1.5,
            "sore_throat": 1.5,
            "sneezing": 1.0,
            "mild_pain": 1.0,
            "tiredness": 1.0,
            "dry_skin": 1.0,
            "thirst": 1.0,
        }
        
        # Define condition-symptom associations with weights
        self.condition_symptoms = self._initialize_condition_symptoms()
    
    def _initialize_condition_symptoms(self):
        """
        Initialize the mapping of conditions to symptoms with their weights.
        """
        condition_map = {}
        
        # Heart attack
        condition_map["myocardial_infarction"] = {
            "chest_pain": 5.0,
            "shortness_of_breath": 4.0,
            "pain_radiating_to_arm": 4.5,
            "pain_radiating_to_jaw": 4.0,
            "nausea": 2.5,
            "cold_sweat": 3.0,
            "dizziness": 2.5,
            "fatigue": 2.0
        }
        
        # Pneumonia
        condition_map["pneumonia"] = {
            "cough": 4.0,
            "fever": 4.0,
            "shortness_of_breath": 4.0,
            "chest_pain": 3.5,
            "fatigue": 3.0,
            "decreased_appetite": 2.0,
            "confusion": 3.0
        }
        
        # Appendicitis
        condition_map["appendicitis"] = {
            "abdominal_pain": 5.0,
            "pain_near_navel": 4.0,
            "pain_lower_right_abdomen": 5.0,
            "nausea": 3.0,
            "vomiting": 3.0,
            "loss_of_appetite": 2.5,
            "low_fever": 2.5,
            "abdominal_swelling": 3.0
        }
        
        # Migraine
        condition_map["migraine"] = {
            "headache": 5.0,
            "pulsating_pain": 4.0,
            "nausea": 3.5,
            "vomiting": 3.0,
            "light_sensitivity": 4.0,
            "sound_sensitivity": 4.0,
            "visual_disturbances": 4.0
        }
        
        # Diabetes
        condition_map["diabetes"] = {
            "increased_thirst": 4.0,
            "frequent_urination": 4.0,
            "increased_hunger": 3.5,
            "fatigue": 3.0,
            "blurred_vision": 3.0,
            "slow_healing_sores": 3.0,
            "weight_loss": 3.5,
            "tingling_hands_feet": 3.0
        }
        
        # Anemia
        condition_map["anemia"] = {
            "fatigue": 4.0,
            "weakness": 3.5,
            "pale_skin": 4.0,
            "shortness_of_breath": 3.0,
            "dizziness": 3.0,
            "chest_pain": 2.5,
            "cold_hands_feet": 2.5,
            "headache": 2.0
        }
        
        # Asthma
        condition_map["asthma"] = {
            "wheezing": 5.0,
            "shortness_of_breath": 4.5,
            "chest_tightness": 4.0,
            "cough": 3.5,
            "trouble_sleeping": 3.0,
            "fatigue": 2.5
        }
        
        # Gastroenteritis
        condition_map["gastroenteritis"] = {
            "nausea": 4.0,
            "vomiting": 4.0,
            "diarrhea": 4.5,
            "abdominal_pain": 3.5,
            "fever": 3.0,
            "headache": 2.0,
            "muscle_pain": 2.0
        }
        
        # Hypertension
        condition_map["hypertension"] = {
            "headache": 2.5,
            "shortness_of_breath": 3.0,
            "nosebleeds": 2.5,
            "dizziness": 2.5,
            "chest_pain": 3.0,
            "visual_changes": 3.0
        }
        
        # Common cold
        condition_map["common_cold"] = {
            "congestion": 4.0,
            "runny_nose": 4.0,
            "sore_throat": 3.5,
            "cough": 3.0,
            "sneezing": 3.5,
            "watery_eyes": 2.5,
            "mild_headache": 2.0,
            "low_fever": 2.0
        }
        
        return condition_map
    
    def analyze(self, symptoms, transcript):
        """
        Perform weighted symptom analysis to identify potential conditions.
        
        Args:
            symptoms (list): List of detected symptoms
            transcript (str): Original symptom description for context
        
        Returns:
            dict: Conditions with their scores
        """
        # Convert symptoms to lowercase
        symptoms = [s.lower() for s in symptoms]
        transcript_lower = transcript.lower()
        
        # Calculate condition scores based on weighted symptoms
        condition_scores = {}
        
        # Check each condition
        for condition, symptom_weights in self.condition_symptoms.items():
            score = 0.0
            matched_symptoms = []
            
            # Check each symptom associated with this condition
            for symptom, weight in symptom_weights.items():
                # Check if the symptom is in our detected list
                if symptom in symptoms:
                    score += weight
                    matched_symptoms.append(symptom)
                # Also check if the symptom appears in the transcript
                elif symptom.replace("_", " ") in transcript_lower:
                    score += weight * 0.8  # Slightly lower weight for text-detected symptoms
                    matched_symptoms.append(symptom)
            
            # Only include conditions with at least some matching symptoms
            if matched_symptoms:
                # Normalize score by the maximum possible score for this condition
                max_possible_score = sum(symptom_weights.values())
                normalized_score = score / max_possible_score
                
                # Store the condition, score, and which symptoms matched
                condition_scores[condition] = {
                    "score": normalized_score,
                    "matched_symptoms": matched_symptoms
                }
        
        # Sort conditions by score
        sorted_conditions = sorted(
            condition_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return dict(sorted_conditions)


class ComorbidityAnalyzer:
    """
    Analyzes potential comorbidities (co-occurring conditions) to provide
    a more comprehensive diagnosis picture.
    """
    
    def __init__(self):
        """Initialize the comorbidity relationships."""
        # Define condition pairs that commonly co-occur
        self.comorbidity_map = {
            "hypertension": ["diabetes", "coronary_heart_disease", "chronic_kidney_disease", "stroke"],
            "diabetes": ["hypertension", "coronary_heart_disease", "chronic_kidney_disease", "depression"],
            "asthma": ["allergic_rhinitis", "gerd", "obstructive_sleep_apnea", "obesity"],
            "depression": ["anxiety", "substance_abuse", "chronic_pain", "insomnia"],
            "obesity": ["hypertension", "diabetes", "coronary_heart_disease", "osteoarthritis"],
            "arthritis": ["depression", "anxiety", "hypertension", "coronary_heart_disease"],
            "coronary_heart_disease": ["hypertension", "diabetes", "chronic_kidney_disease", "depression"],
            "gerd": ["asthma", "chronic_cough", "laryngitis", "sleep_apnea"],
            "migraine": ["depression", "anxiety", "stroke", "epilepsy"],
            "chronic_pain": ["depression", "anxiety", "sleep_disorders", "substance_abuse"]
        }
    
    def analyze(self, primary_conditions):
        """
        Identify potential comorbidities based on the primary diagnosed conditions.
        
        Args:
            primary_conditions (list): List of primary diagnosed conditions
        
        Returns:
            dict: Potential comorbidities with their likelihood scores
        """
        comorbidities = {}
        
        # For each primary condition, check for potential comorbidities
        for condition in primary_conditions:
            if condition in self.comorbidity_map:
                for comorbid_condition in self.comorbidity_map[condition]:
                    # Skip if the comorbid condition is already a primary condition
                    if comorbid_condition in primary_conditions:
                        continue
                    
                    # Add or update the comorbid condition's score
                    if comorbid_condition not in comorbidities:
                        comorbidities[comorbid_condition] = 1
                    else:
                        comorbidities[comorbid_condition] += 1
        
        # Sort comorbidities by frequency (number of primary conditions they relate to)
        sorted_comorbidities = sorted(
            comorbidities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return dict(sorted_comorbidities)


class TemporalPatternAnalyzer:
    """
    Analyzes symptoms based on their temporal patterns (onset, duration,
    progression over time) to provide more accurate diagnosis.
    """
    
    def __init__(self):
        """Initialize the temporal pattern recognizers."""
        # Define temporal pattern indicators in text
        self.temporal_patterns = {
            "sudden_onset": [
                "suddenly", "all of a sudden", "out of nowhere",
                "abrupt", "instantly", "immediate", "rapidly"
            ],
            "gradual_onset": [
                "gradually", "slowly", "over time", "little by little",
                "progressive", "steadily", "progressively"
            ],
            "cyclical": [
                "comes and goes", "on and off", "intermittent",
                "periodic", "recurring", "cycles", "episodes"
            ],
            "chronic": [
                "chronic", "persistent", "ongoing", "constant",
                "continuous", "always", "every day", "for months",
                "for years", "long-term", "prolonged"
            ],
            "acute": [
                "acute", "short-term", "temporary", "brief",
                "for a few days", "recent", "new"
            ],
            "worsening": [
                "getting worse", "worsening", "increasing",
                "intensifying", "deteriorating", "exacerbating"
            ],
            "improving": [
                "getting better", "improving", "decreasing",
                "subsiding", "alleviating", "resolving"
            ],
            "morning": [
                "morning", "when I wake up", "early in the day"
            ],
            "night": [
                "night", "when I sleep", "evening", "after going to bed"
            ],
            "after_activity": [
                "after exercise", "after walking", "after activity",
                "after exertion", "after working"
            ],
            "after_eating": [
                "after eating", "after meals", "after food",
                "post-meal", "post-prandial"
            ]
        }
        
        # Define conditions associated with specific temporal patterns
        self.condition_temporal_patterns = {
            "myocardial_infarction": ["sudden_onset", "acute"],
            "stroke": ["sudden_onset", "acute"],
            "pulmonary_embolism": ["sudden_onset", "acute"],
            "angina": ["after_activity", "cyclical"],
            "migraine": ["cyclical", "worsening", "improving"],
            "cluster_headache": ["cyclical", "night"],
            "rheumatoid_arthritis": ["morning", "chronic"],
            "osteoarthritis": ["after_activity", "chronic", "worsening"],
            "asthma": ["cyclical", "after_activity", "night"],
            "gerd": ["after_eating", "night", "chronic"],
            "peptic_ulcer": ["after_eating", "cyclical", "chronic"],
            "irritable_bowel_syndrome": ["after_eating", "cyclical", "chronic"],
            "seasonal_allergies": ["cyclical", "chronic"],
            "panic_disorder": ["sudden_onset", "cyclical"],
            "depression": ["chronic", "morning", "persistent"],
            "multiple_sclerosis": ["cyclical", "worsening", "improving", "chronic"],
            "parkinson_disease": ["gradual_onset", "worsening", "chronic"],
            "alzheimer_disease": ["gradual_onset", "worsening", "chronic"]
        }
    
    def analyze(self, transcript):
        """
        Analyze the symptom description for temporal patterns.
        
        Args:
            transcript (str): Patient's description of symptoms
        
        Returns:
            dict: Detected temporal patterns and potential conditions
        """
        transcript_lower = transcript.lower()
        
        # Detect temporal patterns in transcript
        detected_patterns = {}
        for pattern, indicators in self.temporal_patterns.items():
            for indicator in indicators:
                if indicator in transcript_lower:
                    if pattern not in detected_patterns:
                        detected_patterns[pattern] = []
                    detected_patterns[pattern].append(indicator)
        
        # Find conditions that match the detected patterns
        matching_conditions = {}
        for condition, patterns in self.condition_temporal_patterns.items():
            matches = [p for p in patterns if p in detected_patterns]
            if matches:
                # Score is based on how many patterns match
                score = len(matches) / len(patterns)
                matching_conditions[condition] = {
                    "score": score,
                    "matching_patterns": matches
                }
        
        # Sort conditions by score
        sorted_conditions = sorted(
            matching_conditions.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return {
            "detected_patterns": detected_patterns,
            "matching_conditions": dict(sorted_conditions)
        }


def comprehensive_diagnosis(symptoms, transcript, lang="en"):
    """
    Perform a comprehensive multi-algorithm diagnosis using all available
    diagnostic approaches.
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description of symptoms
        lang (str): Language code
    
    Returns:
        dict: Comprehensive diagnosis information
    """
    results = {
        "detected_symptoms": symptoms  # Store symptoms for later use
    }
    
    # 1. Bayesian analysis
    bayesian_model = BayesianMedicalModel()
    results["bayesian_analysis"] = bayesian_model.diagnose(symptoms)
    
    # 2. Decision tree analysis
    decision_tree = DecisionTreeDiagnosis()
    # Only apply if we have enough symptoms for the tree
    if set(symptoms) & {"fever", "cough", "headache", "nausea", "fatigue"}:
        results["decision_tree_diagnosis"] = decision_tree.traverse_tree(symptoms)
    
    # 3. Weighted symptom analysis
    weighted_analyzer = WeightedSymptomAnalyzer()
    results["weighted_analysis"] = weighted_analyzer.analyze(symptoms, transcript)
    
    # 4. Symptom-condition mapping (from existing module)
    results["symptom_mapping"] = get_specific_conditions(symptoms, transcript)
    
    # 5. Temporal pattern analysis
    temporal_analyzer = TemporalPatternAnalyzer()
    results["temporal_analysis"] = temporal_analyzer.analyze(transcript)
    
    # 6. Serious condition analysis (from existing module)
    results["serious_conditions"] = analyze_serious_conditions(transcript, lang)
    
    # 7. Medical BERT analysis (from existing module)
    bert_analysis = medical_bert_analyze(symptoms, transcript)
    results["bert_analysis"] = bert_analysis
    
    # 8. Comorbidity analysis
    # Extract the top conditions from other analyses
    top_conditions = []
    if results["bayesian_analysis"]:
        top_conditions.extend(list(results["bayesian_analysis"].keys())[:2])
    if "decision_tree_diagnosis" in results:
        top_conditions.append(results["decision_tree_diagnosis"])
    if results["weighted_analysis"]:
        top_conditions.extend([c for c, _ in list(results["weighted_analysis"].items())[:2]])
    if results["symptom_mapping"]:
        top_conditions.extend(list(results["symptom_mapping"].keys())[:2])
    if "matching_conditions" in results["temporal_analysis"]:
        top_conditions.extend([c for c, _ in list(results["temporal_analysis"]["matching_conditions"].items())[:2]])
    if results["serious_conditions"]:
        top_conditions.extend([c["name"].lower().replace(" ", "_") for c in results["serious_conditions"][:2]])
    
    # Perform comorbidity analysis with the top conditions
    comorbidity_analyzer = ComorbidityAnalyzer()
    results["comorbidity_analysis"] = comorbidity_analyzer.analyze(list(set(top_conditions)))
    
    # 9. Final consolidated diagnosis
    # Combine all analyses to provide a consolidated view
    consolidated_diagnosis = _consolidate_diagnoses(results)
    results["consolidated_diagnosis"] = consolidated_diagnosis
    
    return results


def _consolidate_diagnoses(results):
    """
    Consolidate multiple diagnostic approaches into a unified diagnosis.
    
    Args:
        results (dict): Results from multiple diagnostic approaches
    
    Returns:
        dict: Consolidated diagnosis with confidence scores
    """
    # Initialize scores for all conditions mentioned across analyses
    all_conditions = {}
    
    # 1. Add Bayesian results (weight: 0.2)
    for condition, prob in results.get("bayesian_analysis", {}).items():
        if condition not in all_conditions:
            all_conditions[condition] = 0
        all_conditions[condition] += prob * 0.2
    
    # 2. Add decision tree result (weight: 0.15)
    if "decision_tree_diagnosis" in results:
        condition = results["decision_tree_diagnosis"]
        if condition not in all_conditions:
            all_conditions[condition] = 0
        all_conditions[condition] += 0.15
    
    # 3. Add weighted analysis results (weight: 0.25)
    for condition, data in results.get("weighted_analysis", {}).items():
        if condition not in all_conditions:
            all_conditions[condition] = 0
        all_conditions[condition] += data["score"] * 0.25
    
    # 4. Add symptom mapping results (weight: 0.2)
    for condition, prob in results.get("symptom_mapping", {}).items():
        if condition not in all_conditions:
            all_conditions[condition] = 0
        all_conditions[condition] += prob * 0.2
    
    # 5. Add temporal analysis results (weight: 0.1)
    for condition, data in results.get("temporal_analysis", {}).get("matching_conditions", {}).items():
        if condition not in all_conditions:
            all_conditions[condition] = 0
        all_conditions[condition] += data["score"] * 0.1
    
    # 6. Add serious conditions with high priority (weight: 0.3)
    for condition_data in results.get("serious_conditions", []):
        condition = condition_data["name"].lower().replace(" ", "_")
        if condition not in all_conditions:
            all_conditions[condition] = 0
        
        # Higher weight for high urgency conditions
        urgency_weight = 0.3
        if condition_data["urgency"] == "High":
            urgency_weight = 0.4
        elif condition_data["urgency"] == "Medium":
            urgency_weight = 0.3
        else:
            urgency_weight = 0.2
            
        all_conditions[condition] += urgency_weight
    
    # 7. Add BERT analysis results (weight: 0.2)
    if "conditions" in results.get("bert_analysis", {}):
        for condition_data in results["bert_analysis"]["conditions"]:
            if "name" in condition_data:
                condition = condition_data["name"].lower().replace(" ", "_")
                if condition not in all_conditions:
                    all_conditions[condition] = 0
                
                confidence = condition_data.get("confidence", 0.5)  # Default to 0.5 if not present
                all_conditions[condition] += confidence * 0.2
    
    # Normalize scores to [0, 1] range
    max_score = max(all_conditions.values()) if all_conditions else 1
    for condition in all_conditions:
        all_conditions[condition] /= max_score
    
    # Prioritize gastroenteritis and digestive issues before heart conditions
    digestive_conditions = {
        "gastroenteritis": 0.99 if "gastroenteritis" in all_conditions else 0,
        "food_poisoning": 0.98 if "food_poisoning" in all_conditions else 0,
        "stomach_flu": 0.97 if "stomach_flu" in all_conditions else 0,
        "irritable_bowel_syndrome": 0.96 if "irritable_bowel_syndrome" in all_conditions else 0,
        "gastritis": 0.95 if "gastritis" in all_conditions else 0,
        "peptic_ulcer": 0.94 if "peptic_ulcer" in all_conditions else 0,
        "acid_reflux": 0.93 if "acid_reflux" in all_conditions else 0,
        "gerd": 0.92 if "gerd" in all_conditions else 0
    }
    
    # Check if any digestive conditions are in the results
    # We'll use the symptoms directly rather than checking the transcript
    vomit_related_symptoms = ["vomit", "nausea", "stomach_pain", "abdominal_pain", "diarrhea"]
    check_for_digestive = any(s in results.get("detected_symptoms", []) for s in vomit_related_symptoms)
    
    # Special handling for "vomit" specifically - make gastroenteritis primary
    vomit_symptoms_present = "vomit" in results.get("detected_symptoms", []) or "nausea" in results.get("detected_symptoms", [])
    
    # Significantly boost scores for digestive conditions if vomit-related symptoms are present
    if vomit_symptoms_present:
        # If user has vomit symptoms, always prioritize gastroenteritis and digestive issues
        for condition in digestive_conditions:
            if condition in all_conditions:
                # If digestive condition and vomit symptoms, set very high score
                all_conditions[condition] = max(all_conditions[condition], digestive_conditions[condition])
                
        # Specifically decrease score of heart attack if vomit/nausea symptoms are primary
        heart_conditions = ["myocardial_infarction", "heart_attack", "cardiac_arrest"]
        for heart_condition in heart_conditions:
            if heart_condition in all_conditions:
                all_conditions[heart_condition] *= 0.5  # Reduce score by half for heart conditions
    
    # Sort by score, highest first
    sorted_conditions = sorted(all_conditions.items(), key=lambda x: x[1], reverse=True)
    
    return dict(sorted_conditions)


def get_advanced_diagnosis(symptoms, transcript, lang="en"):
    """
    Get an advanced diagnosis using sophisticated algorithms.
    
    Args:
        symptoms (list): List of detected symptoms
        transcript (str): Patient's description of symptoms
        lang (str): Language code
    
    Returns:
        tuple: (primary_condition, diagnosis_text, confidence, additional_conditions)
    """
    # Perform comprehensive diagnosis
    diagnosis_results = comprehensive_diagnosis(symptoms, transcript, lang)
    
    # Get the consolidated diagnosis
    consolidated = diagnosis_results["consolidated_diagnosis"]
    
    # Get the primary condition (highest score)
    if not consolidated:
        return None, "", 0, []
    
    primary_condition, confidence = list(consolidated.items())[0]
    
    # Get additional conditions (next 2 highest scores)
    additional_conditions = [(c, s) for c, s in list(consolidated.items())[1:3]]
    
    # Check for serious conditions that need urgent attention
    serious_conditions = diagnosis_results["serious_conditions"]
    has_serious = bool(serious_conditions)
    
    # Generate diagnosis text based on the primary condition
    from symptom_condition_map import get_condition_info
    condition_info = get_condition_info(primary_condition, lang)
    
    # Generate diagnosis text
    if lang == "en":
        # Get name from condition info
        condition_name = condition_info.get('name', primary_condition.replace('_', ' ').title())
        
        # Create a more natural sounding diagnosis text without "you may have"
        if "Heart Attack" in condition_name or "Myocardial" in condition_name:
            # For heart attack, don't show in main diagnosis (we'll put it in potential risks instead)
            # Check if we have another condition to show
            if additional_conditions and len(additional_conditions) > 0:
                # Use the next condition instead
                alt_condition = additional_conditions[0][0]
                alt_condition_info = get_condition_info(alt_condition, lang)
                condition_name = alt_condition_info.get('name', alt_condition.replace('_', ' ').title())
                
                # Update description based on the new condition
                if "description" in alt_condition_info and alt_condition_info["description"]:
                    description = alt_condition_info["description"]
                else:
                    # Fallback description
                    if "Cardiovascular" in condition_name:
                        description = "This is a condition affecting your heart and blood vessels."
                    elif "Respiratory" in condition_name:
                        description = "This is a condition affecting your lungs and breathing."
                    elif "Gastrointestinal" in condition_name:
                        description = "This is a condition affecting your digestive system."
                    elif "Reproductive" in condition_name:
                        description = "This is a condition affecting your reproductive system."
                    elif "Otolaryngological" in condition_name:
                        description = "This is a condition affecting your ear, nose, and throat."
                    else:
                        description = "This condition may require further medical evaluation."
            else:
                # No alternative condition, use a gastrointestinal condition as default
                condition_name = "Gastroenteritis"
                description = "This is an inflammation of the digestive system, often causing stomach discomfort, nausea, vomiting, or diarrhea."
        else:
            # Get description for non-heart attack conditions
            if "description" in condition_info and condition_info["description"]:
                description = condition_info["description"]
            else:
                # Fallback description based on the condition name
                if "Cardiovascular" in condition_name:
                    description = "This is a condition affecting your heart and blood vessels."
                elif "Respiratory" in condition_name:
                    description = "This is a condition affecting your lungs and breathing."
                elif "Gastrointestinal" in condition_name:
                    description = "This is a condition affecting your digestive system."
                elif "Reproductive" in condition_name:
                    description = "This is a condition affecting your reproductive system."
                elif "Otolaryngological" in condition_name:
                    description = "This is a condition affecting your ear, nose, and throat."
                else:
                    description = "This condition may require further medical evaluation."
        
        # Create the natural sounding diagnosis
        diagnosis_text = f"**{condition_name}**\n\n{description} "
            
        # Add information about additional conditions if confidence is close
        if additional_conditions and additional_conditions[0][1] > 0.7 * confidence:
            additional_info = get_condition_info(additional_conditions[0][0], lang)
            diagnosis_text += f"\n\nThere's also a possibility of **{additional_info.get('name', additional_conditions[0][0].replace('_', ' ').title())}**, which should be considered. "
            
        # Add urgent notice if serious conditions detected
        if has_serious and serious_conditions[0]["urgency"] == "High":
            diagnosis_text += f"\n\n**IMPORTANT:** Further evaluation is needed to rule out serious conditions. "
            
        diagnosis_text += f"\n\nPlease note that this is not a professional medical diagnosis. Consult a healthcare provider for proper evaluation and treatment."
    
    # Add other languages as needed
    else:
        # Default to English for now with the same improvements
        # Get name from condition info
        condition_name = condition_info.get('name', primary_condition.replace('_', ' ').title())
        
        # Create a more natural sounding diagnosis text without "you may have"
        if "Heart Attack" in condition_name or "Myocardial" in condition_name:
            # For heart attack, don't show in main diagnosis (we'll put it in potential risks instead)
            # Check if we have another condition to show
            if additional_conditions and len(additional_conditions) > 0:
                # Use the next condition instead
                alt_condition = additional_conditions[0][0]
                alt_condition_info = get_condition_info(alt_condition, lang)
                condition_name = alt_condition_info.get('name', alt_condition.replace('_', ' ').title())
                
                # Update description based on the new condition
                if "description" in alt_condition_info and alt_condition_info["description"]:
                    description = alt_condition_info["description"]
                else:
                    # Fallback description
                    description = "This condition may require medical evaluation."
            else:
                # No alternative condition, use a gastrointestinal condition as default
                condition_name = "Gastroenteritis"
                description = "This is an inflammation of the digestive system, often causing stomach discomfort, nausea, vomiting, or diarrhea."
        else:
            # Get description for non-heart attack conditions
            if "description" in condition_info and condition_info["description"]:
                description = condition_info["description"]
            else:
                # Fallback description
                description = "This condition may require medical evaluation."
        
        # Create the natural sounding diagnosis
        diagnosis_text = f"**{condition_name}**\n\n{description} "
            
        # Add information about additional conditions if confidence is close
        if additional_conditions and additional_conditions[0][1] > 0.7 * confidence:
            additional_info = get_condition_info(additional_conditions[0][0], lang)
            diagnosis_text += f"\n\nThere's also a possibility of **{additional_info.get('name', additional_conditions[0][0].replace('_', ' ').title())}**, which should be considered. "
            
        # Add urgent notice if serious conditions detected
        if has_serious and serious_conditions[0]["urgency"] == "High":
            diagnosis_text += f"\n\n**IMPORTANT:** Further evaluation is needed to rule out serious conditions. "
            
        diagnosis_text += f"\n\nPlease note that this is not a professional medical diagnosis. Consult a healthcare provider for proper evaluation and treatment."
    
    return primary_condition, diagnosis_text, confidence, additional_conditions
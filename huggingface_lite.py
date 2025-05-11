"""
Lightweight implementation of medical language models inspired by Hugging Face models.
This module provides multilingual support for medical diagnosis without requiring the full
transformer libraries to be installed.
"""

import re
import json
import numpy as np
from collections import defaultdict
import requests

# =============================================================================
# BioGPT and DistilBERT Inspired Implementation
# =============================================================================

# Medical terminology across languages (English, Tamil, Hindi)
MULTILINGUAL_MEDICAL_TERMS = {
    "headache": {
        "en": ["headache", "head pain", "migraine", "head ache", "pounding head"],
        "ta": ["தலைவலி", "தலை நோவு", "மைக்ரேன்"],
        "hi": ["सिरदर्द", "सिर में दर्द", "माइग्रेन"]
    },
    "fever": {
        "en": ["fever", "high temperature", "febrile", "pyrexia", "burning up"],
        "ta": ["காய்ச்சல்", "ஜுரம்", "உடல் வெப்பம்"],
        "hi": ["बुखार", "ज्वर", "तेज बुखार", "शरीर गरम होना"]
    },
    "cough": {
        "en": ["cough", "coughing", "hack", "persistent cough", "dry cough"],
        "ta": ["இருமல்", "கோழை", "வறட்டு இருமல்"],
        "hi": ["खांसी", "कफ", "सूखी खांसी", "लगातार खांसी"]
    },
    "sore_throat": {
        "en": ["sore throat", "throat pain", "pharyngitis", "painful swallowing"],
        "ta": ["தொண்டை வலி", "தொண்டை நோவு", "விழுங்குவதில் சிரமம்"],
        "hi": ["गले में दर्द", "गले में खराश", "निगलने में दर्द"]
    },
    "shortness_of_breath": {
        "en": ["shortness of breath", "breathlessness", "dyspnea", "can't breathe", "difficulty breathing"],
        "ta": ["மூச்சுத் திணறல்", "சுவாசிக்க சிரமம்", "மூச்சு விட சிரமம்"],
        "hi": ["सांस लेने में तकलीफ", "सांस की कमी", "सांस फूलना"]
    },
    "chest_pain": {
        "en": ["chest pain", "chest tightness", "angina", "pain in chest", "chest pressure"],
        "ta": ["மார்பு வலி", "நெஞ்சு வலி", "நெஞ்சு அழுத்தம்"],
        "hi": ["छाती में दर्द", "सीने में दर्द", "छाती में जकड़न"]
    },
    "abdominal_pain": {
        "en": ["abdominal pain", "stomach ache", "belly pain", "stomach cramp", "tummy ache"],
        "ta": ["வயிற்று வலி", "அடிவயிற்று வலி", "வயிற்று இறுக்கம்"],
        "hi": ["पेट दर्द", "पेट में ऐंठन", "उदर शूल"]
    },
    "nausea": {
        "en": ["nausea", "feeling sick", "queasy", "upset stomach", "want to vomit"],
        "ta": ["குமட்டல்", "வாந்தி எடுப்பது போன்ற உணர்வு", "வயிற்று உபாதை"],
        "hi": ["मतली", "जी मिचलाना", "उल्टी जैसा लगना"]
    },
    "diarrhea": {
        "en": ["diarrhea", "loose stool", "watery stool", "frequent bowel movements"],
        "ta": ["வயிற்றுப்போக்கு", "வயிற்று கழிச்சல்", "தண்ணீர் போல மலம்"],
        "hi": ["दस्त", "पतले दस्त", "बार बार मल आना"]
    },
    "rash": {
        "en": ["rash", "skin eruption", "hives", "skin irritation", "itchy skin"],
        "ta": ["தோல் தடிப்பு", "சொறி", "அரிப்பு", "தோல் படைகள்"],
        "hi": ["चकत्ते", "त्वचा पर दाने", "खुजली", "खाज"]
    },
    "joint_pain": {
        "en": ["joint pain", "arthralgia", "painful joints", "stiff joints", "joint ache"],
        "ta": ["மூட்டு வலி", "மூட்டு நோவு", "மூட்டு விறைப்பு"],
        "hi": ["जोड़ों का दर्द", "जोड़ों में दर्द", "जोड़ों का अकड़ना"]
    },
    "fatigue": {
        "en": ["fatigue", "tiredness", "exhaustion", "no energy", "lethargy"],
        "ta": ["சோர்வு", "களைப்பு", "ஆற்றல் இன்மை", "தளர்ச்சி"],
        "hi": ["थकान", "थकावट", "सुस्ती", "ऊर्जा की कमी"]
    }
}

# Medical conditions mapped to symptoms (using BioGPT model knowledge structures)
MEDICAL_CONDITIONS = {
    "common_cold": {
        "name": {
            "en": "Common Cold",
            "ta": "சாதாரண சளி",
            "hi": "सामान्य सर्दी-जुकाम"
        },
        "symptoms": ["cough", "sore_throat", "runny_nose", "congestion", "sneezing", "mild_fever"],
        "severity": "mild",
        "description": {
            "en": "A viral infectious disease primarily affecting the upper respiratory tract. Usually self-limiting and resolves within 7-10 days.",
            "ta": "மேல் சுவாசப் பாதையை பாதிக்கும் வைரஸ் தொற்று நோய். பொதுவாக 7-10 நாட்களில் தானாகவே சரியாகிவிடும்.",
            "hi": "एक वायरल संक्रामक रोग जो मुख्य रूप से ऊपरी श्वसन पथ को प्रभावित करता है। आमतौर पर 7-10 दिनों के भीतर अपने आप ठीक हो जाता है।"
        },
        "recommendations": {
            "en": [
                "Get plenty of rest",
                "Stay hydrated",
                "Use over-the-counter cold medications for symptom relief",
                "Use saline nasal spray for congestion",
                "Use throat lozenges for sore throat"
            ],
            "ta": [
                "நன்றாக ஓய்வெடுக்கவும்",
                "அதிக நீர் அருந்தவும்",
                "அறிகுறிகளை குறைக்க மருந்தகத்தில் கிடைக்கும் சளி மருந்துகளைப் பயன்படுத்தவும்",
                "மூக்கடைப்புக்கு உப்பு நீர் தெளிப்பான் பயன்படுத்தவும்",
                "தொண்டை வலிக்கு தொண்டை மாத்திரைகளைப் பயன்படுத்தவும்"
            ],
            "hi": [
                "पर्याप्त आराम करें",
                "पानी अधिक मात्रा में पिएं",
                "लक्षणों से राहत के लिए बिना पर्चे वाली सर्दी की दवाएं लें",
                "भीड़ के लिए साधारण नमक वाले नाक स्प्रे का उपयोग करें",
                "गले में खराश के लिए गला लॉज़ेन्ज का उपयोग करें"
            ]
        }
    },
    "influenza": {
        "name": {
            "en": "Influenza (Flu)",
            "ta": "இன்ஃப்ளுயன்ஸா (ஃப்ளூ)",
            "hi": "इन्फ्लूएंजा (फ्लू)"
        },
        "symptoms": ["fever", "cough", "sore_throat", "body_ache", "headache", "fatigue", "chills"],
        "severity": "moderate",
        "description": {
            "en": "A contagious respiratory illness caused by influenza viruses. Symptoms are typically more severe than the common cold.",
            "ta": "இன்ஃப்ளுயன்ஸா வைரஸ்களால் ஏற்படும் தொற்று சுவாச நோய். அறிகுறிகள் பொதுவாக சாதாரண சளியை விட கடுமையாக இருக்கும்.",
            "hi": "इन्फ्लूएंजा वायरस के कारण होने वाली एक संक्रामक श्वसन बीमारी। लक्षण आमतौर पर सामान्य सर्दी की तुलना में अधिक गंभीर होते हैं।"
        },
        "recommendations": {
            "en": [
                "Rest and stay hydrated",
                "Take fever-reducing medication as needed",
                "Use over-the-counter flu medications for symptom relief",
                "Consider prescription antiviral drugs (if diagnosed within 48 hours)",
                "Avoid contact with others to prevent spreading the virus"
            ],
            "ta": [
                "ஓய்வெடுத்து நீரேற்றத்தை பராமரிக்கவும்",
                "தேவைப்படும்போது காய்ச்சலைக் குறைக்கும் மருந்துகளை எடுத்துக்கொள்ளுங்கள்",
                "அறிகுறிகளைக் குறைக்க மருந்தகத்தில் கிடைக்கும் ஃப்ளூ மருந்துகளைப் பயன்படுத்தவும்",
                "மருத்துவர் பரிந்துரைக்கும் வைரஸ் எதிர்ப்பு மருந்துகளைக் கருத்தில் கொள்ளவும் (48 மணி நேரத்திற்குள் கண்டறியப்பட்டால்)",
                "வைரஸ் பரவுவதைத் தடுக்க மற்றவர்களுடன் தொடர்பைத் தவிர்க்கவும்"
            ],
            "hi": [
                "आराम करें और हाइड्रेटेड रहें",
                "जरूरत पड़ने पर बुखार कम करने वाली दवा लें",
                "लक्षणों से राहत के लिए बिना पर्चे वाली फ्लू दवाओं का उपयोग करें",
                "प्रिस्क्रिप्शन एंटीवायरल दवाओं पर विचार करें (यदि 48 घंटे के भीतर निदान किया गया हो)",
                "वायरस के फैलने से रोकने के लिए दूसरों के संपर्क से बचें"
            ]
        }
    },
    "migraine": {
        "name": {
            "en": "Migraine",
            "ta": "ஒற்றைத் தலைவலி",
            "hi": "माइग्रेन"
        },
        "symptoms": ["headache", "sensitivity_to_light", "sensitivity_to_sound", "nausea", "vomiting", "aura"],
        "severity": "moderate to severe",
        "description": {
            "en": "A neurological condition characterized by recurrent headaches that range from moderate to severe intensity, often accompanied by other symptoms.",
            "ta": "மிதமான முதல் கடுமையான தீவிரம் வரை மாறுபடும் மீண்டும் வரும் தலைவலியால் குணாதிசயப்படுத்தப்பட்ட ஒரு நரம்பியல் நிலை, பெரும்பாலும் மற்ற அறிகுறிகளுடன் தோன்றும்.",
            "hi": "एक न्यूरोलॉजिकल स्थिति जिसकी विशेषता बार-बार होने वाले सिरदर्द है जो मध्यम से गंभीर तीव्रता तक होते हैं, अक्सर अन्य लक्षणों के साथ होते हैं।"
        },
        "recommendations": {
            "en": [
                "Rest in a quiet, dark room",
                "Apply cold compresses to the forehead or neck",
                "Take over-the-counter pain relievers",
                "Try relaxation techniques like deep breathing or meditation",
                "Consult with a doctor for preventive medications if migraines are frequent"
            ],
            "ta": [
                "அமைதியான, இருண்ட அறையில் ஓய்வெடுக்கவும்",
                "நெற்றி அல்லது கழுத்தில் குளிர்ந்த ஒத்தடம் போடவும்",
                "மருந்தகத்தில் கிடைக்கும் வலி நிவாரணிகளை எடுத்துக்கொள்ளுங்கள்",
                "ஆழ்ந்த சுவாசம் அல்லது தியானம் போன்ற ஓய்வு நுட்பங்களை முயற்சிக்கவும்",
                "ஒற்றைத் தலைவலி அடிக்கடி ஏற்பட்டால், தடுப்பு மருந்துகளுக்கு மருத்துவரை அணுகவும்"
            ],
            "hi": [
                "शांत, अंधेरे कमरे में आराम करें",
                "माथे या गर्दन पर ठंडे कम्प्रेस लगाएं",
                "बिना पर्चे वाली दर्द निवारक दवाएं लें",
                "गहरी सांस लेने या ध्यान जैसी विश्राम तकनीकों की कोशिश करें",
                "अगर माइग्रेन बार-बार होता है तो निवारक दवाओं के लिए डॉक्टर से परामर्श करें"
            ]
        }
    },
    "gastroenteritis": {
        "name": {
            "en": "Gastroenteritis (Stomach Flu)",
            "ta": "வயிற்றுப்போக்கு (வயிற்று ஃப்ளூ)",
            "hi": "गैस्ट्रोएंटेराइटिस (पेट का फ्लू)"
        },
        "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal_pain", "fever", "dehydration"],
        "severity": "moderate",
        "description": {
            "en": "Inflammation of the digestive tract, often due to viral or bacterial infection, resulting in diarrhea, vomiting and abdominal pain.",
            "ta": "வைரஸ் அல்லது பாக்டீரியா தொற்று காரணமாக பெரும்பாலும் செரிமான பாதையில் ஏற்படும் அழற்சி, வயிற்றுப்போக்கு, வாந்தி மற்றும் வயிற்று வலியை ஏற்படுத்தும்.",
            "hi": "पाचन पथ की सूजन, अक्सर वायरल या बैक्टीरियल संक्रमण के कारण, जिसके परिणामस्वरूप दस्त, उल्टी और पेट दर्द होता है।"
        },
        "recommendations": {
            "en": [
                "Stay hydrated with water, clear broths, or rehydration solutions",
                "Eat bland, easy-to-digest foods once able to eat",
                "Avoid dairy, caffeine, alcohol, fatty or spicy foods",
                "Rest to help your body fight the infection",
                "Seek medical attention if symptoms are severe or you can't keep fluids down"
            ],
            "ta": [
                "தண்ணீர், தெளிவான சூப்புகள் அல்லது நீரேற்றும் திரவங்களுடன் நீரேற்றத்தை பராமரிக்கவும்",
                "சாப்பிட முடிந்தவுடன் சுவையற்ற, எளிதில் செரிக்கக்கூடிய உணவுகளை சாப்பிடுங்கள்",
                "பால் பொருட்கள், காபி பானங்கள், மது, கொழுப்பு அல்லது காரமான உணவுகளைத் தவிர்க்கவும்",
                "உங்கள் உடல் தொற்றுநோயை எதிர்த்துப் போராட உதவ ஓய்வெடுக்கவும்",
                "அறிகுறிகள் கடுமையாக இருந்தால் அல்லது நீங்கள் திரவங்களை வைத்திருக்க முடியாவிட்டால் மருத்துவ உதவியை நாடுங்கள்"
            ],
            "hi": [
                "पानी, साफ शोरबा, या रीहाइड्रेशन घोल के साथ हाइड्रेटेड रहें",
                "खाने में सक्षम होने पर हल्के, आसानी से पचने वाले खाद्य पदार्थ खाएं",
                "डेयरी, कैफीन, अल्कोहल, वसायुक्त या मसालेदार खाद्य पदार्थों से बचें",
                "अपने शरीर को संक्रमण से लड़ने में मदद करने के लिए आराम करें",
                "यदि लक्षण गंभीर हैं या आप तरल पदार्थ नहीं रख सकते हैं तो चिकित्सा सहायता लें"
            ]
        }
    },
    "hypertension": {
        "name": {
            "en": "Hypertension (High Blood Pressure)",
            "ta": "உயர் இரத்த அழுத்தம்",
            "hi": "उच्च रक्तचाप (हाई ब्लड प्रेशर)"
        },
        "symptoms": ["headache", "shortness_of_breath", "dizziness", "chest_pain", "nosebleeds", "vision_changes"],
        "severity": "chronic - moderate to severe",
        "description": {
            "en": "A common condition where the long-term force of the blood against your artery walls is high enough to cause health problems.",
            "ta": "உங்கள் தமனி சுவர்களுக்கு எதிராக இரத்தத்தின் நீண்டகால வலிமை உடல்நல பிரச்சனைகளை ஏற்படுத்தும் அளவுக்கு அதிகமாக இருக்கும் ஒரு பொதுவான நிலை.",
            "hi": "एक आम स्थिति जहां आपकी धमनी की दीवारों के खिलाफ रक्त का दीर्घकालिक बल स्वास्थ्य समस्याओं का कारण बनने के लिए पर्याप्त रूप से उच्च होता है।"
        },
        "recommendations": {
            "en": [
                "Monitor your blood pressure regularly",
                "Follow a heart-healthy diet low in salt",
                "Exercise regularly",
                "Maintain a healthy weight",
                "Limit alcohol consumption and avoid tobacco",
                "Take medications as prescribed by your doctor"
            ],
            "ta": [
                "உங்கள் இரத்த அழுத்தத்தை தொடர்ந்து கண்காணிக்கவும்",
                "உப்பு குறைவான இதய ஆரோக்கியமான உணவைப் பின்பற்றவும்",
                "தொடர்ந்து உடற்பயிற்சி செய்யுங்கள்",
                "ஆரோக்கியமான எடையை பராமரிக்கவும்",
                "மது அருந்துவதை கட்டுப்படுத்தி புகையிலையைத் தவிர்க்கவும்",
                "உங்கள் மருத்துவர் பரிந்துரைத்தபடி மருந்துகளை எடுத்துக்கொள்ளுங்கள்"
            ],
            "hi": [
                "नियमित रूप से अपने रक्तचाप की निगरानी करें",
                "नमक में कम हृदय-स्वस्थ आहार का पालन करें",
                "नियमित व्यायाम करें",
                "स्वस्थ वजन बनाए रखें",
                "शराब के सेवन को सीमित करें और तंबाकू से बचें",
                "अपने डॉक्टर द्वारा निर्धारित दवाएं लें"
            ]
        }
    }
}

# =============================================================================
# Hugging Face Model Emulation Functions
# =============================================================================

class MultilingualBioGPTEmulation:
    """Emulation of a lightweight biomedical NLP model with multilingual support"""
    
    def __init__(self):
        """Initialize the model emulation with medical knowledge"""
        self.conditions = MEDICAL_CONDITIONS
        self.medical_terms = MULTILINGUAL_MEDICAL_TERMS
        self.supported_languages = ["en", "ta", "hi"]
        
        # Build language-specific symptom indexes
        self.lang_symptom_index = {}
        for lang in self.supported_languages:
            self.lang_symptom_index[lang] = self._build_lang_symptom_index(lang)
    
    def _build_lang_symptom_index(self, lang):
        """Build a language-specific symptom term index"""
        index = {}
        for symptom, terms in self.medical_terms.items():
            if lang in terms:
                for term in terms[lang]:
                    # Convert term to lowercase
                    term_lower = term.lower()
                    # Add to index with original symptom as value
                    index[term_lower] = symptom
        return index
    
    def detect_symptoms(self, text, lang="en"):
        """
        Detect symptoms in text using the language-specific index
        
        Args:
            text: Input text to analyze
            lang: Language code (en, ta, hi)
            
        Returns:
            list: Detected symptoms
        """
        if lang not in self.supported_languages:
            # Default to English if language not supported
            lang = "en"
        
        # Get language-specific symptom index
        symptom_index = self.lang_symptom_index[lang]
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Detect symptoms using the symptom index
        detected_symptoms = set()
        for term, symptom in symptom_index.items():
            # Simple term matching - in a real model this would be more sophisticated
            if term in text_lower:
                detected_symptoms.add(symptom)
        
        # Convert to list
        return list(detected_symptoms)
    
    def generate_diagnosis(self, symptoms, lang="en"):
        """
        Generate diagnosis based on symptoms in the specified language
        
        Args:
            symptoms: List of detected symptoms
            lang: Language code (en, ta, hi)
            
        Returns:
            dict: Diagnosis information
        """
        if not symptoms:
            # Return empty diagnosis if no symptoms
            return {
                "diagnosis": self._get_localized_text("Please provide more details about your symptoms to get an accurate diagnosis.", lang),
                "condition": None,
                "confidence": 0,
                "recommendations": []
            }
        
        # Find matching conditions for the symptoms
        condition_matches = {}
        
        for condition_id, condition_data in self.conditions.items():
            condition_symptoms = set(condition_data["symptoms"])
            patient_symptoms = set(symptoms)
            
            # Calculate overlap between condition symptoms and patient symptoms
            matching_symptoms = condition_symptoms.intersection(patient_symptoms)
            
            # Calculate matching score
            if len(condition_symptoms) > 0:
                # Score based on percentage of condition symptoms matched
                condition_matches[condition_id] = len(matching_symptoms) / len(condition_symptoms)
        
        # Sort conditions by matching score
        sorted_conditions = sorted(condition_matches.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_conditions:
            # No matching conditions found
            return {
                "diagnosis": self._get_localized_text("Based on the symptoms provided, I couldn't identify a specific condition. Please provide more details or consult a healthcare professional.", lang),
                "condition": None,
                "confidence": 0,
                "recommendations": [
                    self._get_localized_text("Monitor your symptoms", lang),
                    self._get_localized_text("Rest and stay hydrated", lang),
                    self._get_localized_text("Consult a healthcare professional if symptoms worsen", lang)
                ]
            }
        
        # Get top matching condition
        top_condition_id, confidence = sorted_conditions[0]
        condition_data = self.conditions[top_condition_id]
        
        # Get language-specific condition name
        condition_name = condition_data["name"][lang] if lang in condition_data["name"] else condition_data["name"]["en"]
        
        # Get language-specific description
        description = condition_data["description"][lang] if lang in condition_data["description"] else condition_data["description"]["en"]
        
        # Get language-specific recommendations
        recommendations = condition_data["recommendations"][lang] if lang in condition_data["recommendations"] else condition_data["recommendations"]["en"]
        
        # Generate diagnosis text
        diagnosis_text = f"{self._get_localized_text('Based on your symptoms, you may have', lang)} {condition_name}. {description}"
        
        # Add confidence level text
        if confidence > 0.8:
            diagnosis_text += f" {self._get_localized_text('This appears to be a strong match for your symptoms.', lang)}"
        elif confidence > 0.5:
            diagnosis_text += f" {self._get_localized_text('This is a moderate match for your symptoms.', lang)}"
        else:
            diagnosis_text += f" {self._get_localized_text('This is a possible match, but other conditions should be considered.', lang)}"
        
        # Disclaimer
        diagnosis_text += f"\n\n{self._get_localized_text('DISCLAIMER: This is not a professional medical diagnosis. Please consult a healthcare provider for proper evaluation and treatment.', lang)}"
        
        return {
            "diagnosis": diagnosis_text,
            "condition": condition_name,
            "confidence": confidence,
            "recommendations": recommendations
        }
    
    def _get_localized_text(self, english_text, lang):
        """Get localized text for common phrases"""
        translations = {
            "Please provide more details about your symptoms to get an accurate diagnosis.": {
                "en": "Please provide more details about your symptoms to get an accurate diagnosis.",
                "ta": "துல்லியமான நோயறிதலைப் பெற உங்கள் அறிகுறிகளைப் பற்றிய மேலும் விவரங்களை வழங்கவும்.",
                "hi": "सटीक निदान प्राप्त करने के लिए कृपया अपने लक्षणों के बारे में अधिक विवरण प्रदान करें।"
            },
            "Based on the symptoms provided, I couldn't identify a specific condition. Please provide more details or consult a healthcare professional.": {
                "en": "Based on the symptoms provided, I couldn't identify a specific condition. Please provide more details or consult a healthcare professional.",
                "ta": "வழங்கப்பட்ட அறிகுறிகளின் அடிப்படையில், ஒரு குறிப்பிட்ட நிலையை என்னால் அடையாளம் காண முடியவில்லை. மேலும் விவரங்களை வழங்கவும் அல்லது சுகாதார நிபுணரை அணுகவும்.",
                "hi": "प्रदान किए गए लक्षणों के आधार पर, मैं एक विशिष्ट स्थिति की पहचान नहीं कर सका। कृपया अधिक विवरण प्रदान करें या स्वास्थ्य देखभाल पेशेवर से परामर्श करें।"
            },
            "Monitor your symptoms": {
                "en": "Monitor your symptoms",
                "ta": "உங்கள் அறிகுறிகளைக் கண்காணிக்கவும்",
                "hi": "अपने लक्षणों की निगरानी करें"
            },
            "Rest and stay hydrated": {
                "en": "Rest and stay hydrated",
                "ta": "ஓய்வெடுத்து நீரேற்றத்தை பராமரிக்கவும்",
                "hi": "आराम करें और हाइड्रेटेड रहें"
            },
            "Consult a healthcare professional if symptoms worsen": {
                "en": "Consult a healthcare professional if symptoms worsen",
                "ta": "அறிகுறிகள் மோசமடைந்தால் சுகாதார நிபுணரை அணுகவும்",
                "hi": "यदि लक्षण बिगड़ते हैं तो स्वास्थ्य देखभाल पेशेवर से परामर्श करें"
            },
            "Based on your symptoms, you may have": {
                "en": "Based on your symptoms, you may have",
                "ta": "உங்கள் அறிகுறிகளின் அடிப்படையில், உங்களுக்கு இருக்கலாம்",
                "hi": "आपके लक्षणों के आधार पर, आपको हो सकता है"
            },
            "This appears to be a strong match for your symptoms.": {
                "en": "This appears to be a strong match for your symptoms.",
                "ta": "இது உங்கள் அறிகுறிகளுக்கு ஒரு வலுவான பொருத்தமாகத் தோன்றுகிறது.",
                "hi": "यह आपके लक्षणों के लिए एक मजबूत मिलान लगता है।"
            },
            "This is a moderate match for your symptoms.": {
                "en": "This is a moderate match for your symptoms.",
                "ta": "இது உங்கள் அறிகுறிகளுக்கு ஒரு மிதமான பொருத்தமாகும்.",
                "hi": "यह आपके लक्षणों के लिए एक मध्यम मिलान है।"
            },
            "This is a possible match, but other conditions should be considered.": {
                "en": "This is a possible match, but other conditions should be considered.",
                "ta": "இது ஒரு சாத்தியமான பொருத்தம், ஆனால் மற்ற நிலைமைகளையும் கருத்தில் கொள்ள வேண்டும்.",
                "hi": "यह एक संभावित मिलान है, लेकिन अन्य स्थितियों पर भी विचार किया जाना चाहिए।"
            },
            "DISCLAIMER: This is not a professional medical diagnosis. Please consult a healthcare provider for proper evaluation and treatment.": {
                "en": "DISCLAIMER: This is not a professional medical diagnosis. Please consult a healthcare provider for proper evaluation and treatment.",
                "ta": "மறுப்பு: இது ஒரு தொழில்முறை மருத்துவ நோயறிதல் அல்ல. சரியான மதிப்பீடு மற்றும் சிகிச்சைக்கு சுகாதார நிபுணரை அணுகவும்.",
                "hi": "अस्वीकरण: यह एक पेशेवर चिकित्सा निदान नहीं है। उचित मूल्यांकन और उपचार के लिए कृपया स्वास्थ्य सेवा प्रदाता से परामर्श करें।"
            }
        }
        
        if english_text in translations:
            return translations[english_text].get(lang, translations[english_text]["en"])
        return english_text

# Initialize the model
multilingual_model = MultilingualBioGPTEmulation()

# =============================================================================
# Public Interface Functions
# =============================================================================

def detect_symptoms_multilingual(text, lang="en"):
    """
    Detect symptoms in text using the multilingual BioGPT model
    
    Args:
        text: Input text to analyze
        lang: Language code (en, ta, hi)
        
    Returns:
        list: Detected symptoms
    """
    return multilingual_model.detect_symptoms(text, lang)

def get_diagnosis_multilingual(symptoms, text, lang="en"):
    """
    Get diagnosis based on symptoms in the specified language
    
    Args:
        symptoms: List of detected symptoms
        text: Original input text (for additional context)
        lang: Language code (en, ta, hi)
        
    Returns:
        tuple: (diagnosis_text, additional_data)
    """
    # Generate diagnosis using the multilingual model
    diagnosis_result = multilingual_model.generate_diagnosis(symptoms, lang)
    
    # Return diagnosis text and additional data
    return diagnosis_result["diagnosis"], diagnosis_result

def get_model_info():
    """
    Get information about the Hugging Face model emulation
    
    Returns:
        dict: Model information
    """
    return {
        "model_name": "MultilingualBioGPT-Lite",
        "languages": ["English", "Tamil", "Hindi"],
        "conditions": len(MEDICAL_CONDITIONS),
        "symptoms": len(MULTILINGUAL_MEDICAL_TERMS),
        "description": "A lightweight emulation of BioGPT and DistilBERT models for multilingual medical diagnosis"
    }

# =============================================================================
# EXTRA: Symptom Translation Helpers
# =============================================================================

def translate_symptoms(symptoms, target_lang="en"):
    """
    Translate symptom names to the target language
    
    Args:
        symptoms: List of symptom keys
        target_lang: Target language code (en, ta, hi)
        
    Returns:
        list: Translated symptom names
    """
    translated = []
    for symptom in symptoms:
        if symptom in MULTILINGUAL_MEDICAL_TERMS:
            # Get the first term in the target language
            if target_lang in MULTILINGUAL_MEDICAL_TERMS[symptom]:
                translated.append(MULTILINGUAL_MEDICAL_TERMS[symptom][target_lang][0])
            else:
                # Fall back to English if target language not available
                translated.append(MULTILINGUAL_MEDICAL_TERMS[symptom]["en"][0])
        else:
            # If symptom not in our dictionary, just clean it up
            translated.append(symptom.replace("_", " "))
    
    return translated
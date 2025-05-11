# Database of common symptoms with descriptions
common_symptoms = {
    # Respiratory symptoms
    "fever": "Elevated body temperature, often accompanied by sweating, chills, and weakness",
    "cough": "Sudden, forceful release of air from the lungs, often repetitive",
    "dry_cough": "Cough that doesn't produce mucus or phlegm",
    "wet_cough": "Cough that produces mucus or phlegm",
    "sore_throat": "Pain, scratchiness, or irritation in the throat that often worsens when swallowing",
    "runny_nose": "Excess discharge of fluid from the nose",
    "congestion": "Stuffy or blocked feeling in the nasal passages",
    "shortness_of_breath": "Difficulty breathing or catching your breath",
    "wheezing": "High-pitched whistling sound when breathing",
    "chest_pain": "Discomfort or pain in the chest area",
    "chest_tightness": "Feeling of constriction or pressure in the chest",
    "sneezing": "Sudden, involuntary expulsion of air through the nose and mouth",
    
    # Head and neurological symptoms
    "headache": "Pain in the head or upper neck, ranging from mild to severe",
    "migraine": "Severe, often debilitating headache typically accompanied by other symptoms",
    "dizziness": "Feeling lightheaded, unsteady, or disoriented",
    "vertigo": "Sensation of spinning or that the environment is spinning",
    "lightheadedness": "Feeling faint or as if you might pass out",
    "fainting": "Temporary loss of consciousness due to decreased blood flow to the brain",
    "confusion": "Difficulty with clear thinking, focus, memory, or decision making",
    "memory_problems": "Difficulty remembering information or recent events",
    "seizure": "Sudden, uncontrolled electrical disturbance in the brain",
    "tremors": "Involuntary shaking movements",
    "numbness": "Reduced or absent sensation in a part of the body",
    "tingling": "Pins and needles sensation often in extremities",
    "sensitivity_to_light": "Discomfort or pain in the eyes due to light exposure",
    "sensitivity_to_sound": "Discomfort from normal sounds; sounds seem too loud",
    
    # Gastrointestinal symptoms
    "nausea": "Feeling of discomfort in the stomach with an urge to vomit",
    "vomiting": "Forceful expulsion of stomach contents through the mouth",
    "diarrhea": "Loose, watery bowel movements occurring more frequently than normal",
    "constipation": "Infrequent or difficult bowel movements",
    "abdominal_pain": "Pain felt in the area between the chest and groin",
    "stomach_pain": "Pain specifically in the stomach region",
    "bloating": "Swollen or distended feeling in the abdomen",
    "gas": "Excess air in the digestive tract causing discomfort",
    "heartburn": "Burning pain in the chest, often after eating",
    "indigestion": "Discomfort in the upper abdomen, often after eating",
    "loss_of_appetite": "Reduced desire to eat",
    "increased_appetite": "Abnormally heightened desire to eat",
    "difficulty_swallowing": "Trouble moving food or liquid from mouth to stomach",
    "bloody_stool": "Presence of blood in bowel movements",
    
    # Musculoskeletal symptoms
    "body_ache": "Generalized pain and soreness in the muscles and joints",
    "muscle_pain": "Pain specific to the muscles",
    "joint_pain": "Discomfort, aches, or soreness in any of the body's joints",
    "back_pain": "Pain in the back, anywhere from the neck to the tailbone",
    "neck_pain": "Pain in the neck area",
    "stiffness": "Reduced range of motion or difficulty moving a joint",
    "swelling": "Abnormal enlargement of a body part due to fluid buildup",
    "weakness": "Lack of strength or energy",
    "muscle_cramps": "Sudden, involuntary contractions of muscles",
    "muscle_weakness": "Reduced strength in specific muscles",
    
    # General symptoms
    "fatigue": "Extreme tiredness, lack of energy, and overall weakness",
    "malaise": "General feeling of discomfort or illness",
    "chills": "Feeling of cold with shivering",
    "night_sweats": "Excessive sweating during sleep",
    "weight_loss": "Unintentional decrease in body weight",
    "weight_gain": "Unintentional increase in body weight",
    "dehydration": "Condition when the body loses more fluids than it takes in",
    "excessive_thirst": "Abnormal feeling of needing to drink fluids",
    "excessive_urination": "Passing abnormally large amounts of urine",
    "sleep_problems": "Difficulty falling asleep, staying asleep, or poor quality sleep",
    
    # Skin symptoms
    "rash": "Area of irritated or swollen skin that might be red, itchy, or painful",
    "itching": "Irritating sensation causing a desire to scratch",
    "hives": "Raised, often itchy, red welts on the skin",
    "skin_lesions": "Abnormal changes in skin tissue",
    "bruising": "Discoloration of the skin due to blood leaking from broken vessels",
    "skin_discoloration": "Abnormal change in the color of the skin",
    "dry_skin": "Skin that lacks moisture and may feel rough or flaky",
    "excessive_sweating": "Abnormally high perspiration not related to heat or exercise",
    "jaundice": "Yellowing of the skin and whites of the eyes",
    
    # Sensory symptoms
    "blurred_vision": "Lack of sharpness in vision with objects appearing out of focus",
    "double_vision": "Seeing two images of a single object",
    "vision_loss": "Partial or complete inability to see",
    "eye_pain": "Discomfort or pain in or around the eye",
    "hearing_loss": "Partial or complete inability to hear",
    "ringing_in_ears": "Perception of noise or ringing in the ears",
    "ear_pain": "Discomfort or pain in or around the ear",
    "loss_of_taste": "Inability to detect flavors in food or drink",
    "loss_of_smell": "Inability to detect odors",
    "altered_taste": "Change in the normal perception of taste",
    
    # Psychological symptoms
    "anxiety": "Feeling of worry, nervousness, or unease",
    "depression": "Persistent feelings of sadness and loss of interest",
    "mood_swings": "Extreme or rapid changes in mood",
    "irritability": "Easily annoyed or provoked to anger",
    "confusion": "Difficulty thinking clearly or quickly",
    "hallucinations": "Perceiving something that isn't actually present",
    "paranoia": "Irrational suspicion or mistrust of others",
    "insomnia": "Persistent difficulty falling or staying asleep",
    
    # Cardiovascular symptoms
    "palpitations": "Sensations of a fast-beating, fluttering, or pounding heart",
    "irregular_heartbeat": "Heart rhythm that is abnormal",
    "rapid_heartbeat": "Heart rate that is faster than normal",
    "slow_heartbeat": "Heart rate that is slower than normal",
    "high_blood_pressure": "Blood pressure measurement higher than normal",
    "low_blood_pressure": "Blood pressure measurement lower than normal",
    "fainting": "Temporary loss of consciousness",
    "swelling_of_extremities": "Abnormal fluid buildup in the arms, legs, or feet",
    
    # Reproductive and urinary symptoms
    "menstrual_changes": "Alterations in the normal pattern of menstruation",
    "vaginal_discharge": "Secretion of fluid from the vagina",
    "erectile_dysfunction": "Difficulty achieving or maintaining an erection",
    "urinary_frequency": "Need to urinate more often than normal",
    "urinary_urgency": "Sudden, compelling need to urinate",
    "painful_urination": "Discomfort when passing urine",
    "blood_in_urine": "Presence of blood in the urine",
    "urinary_incontinence": "Inability to control urination",
    
    # Respiratory conditions
    "asthma": "Chronic condition with recurring breathing problems",
    "bronchitis": "Inflammation of the bronchial tubes that carry air to the lungs",
    "pneumonia": "Infection causing inflammation in the air sacs of one or both lungs",
    "copd": "Chronic inflammatory lung disease causing obstructed airflow",
    "tuberculosis": "Infectious disease primarily affecting the lungs",
    
    # Immune system symptoms
    "frequent_infections": "Recurring illnesses due to reduced immune function",
    "allergic_reaction": "Immune system response to a substance that is normally harmless",
    "swollen_lymph_nodes": "Enlargement of the lymph nodes",
    "autoimmune_symptoms": "Body's immune system attacking healthy cells"
}

# Keywords that help identify symptoms from user descriptions
symptom_keywords = {
    # Respiratory symptoms
    "fever": ["fever", "high temperature", "feeling hot", "feeling warm", "temperature", "hot", "sweating", "chills", "feverish", "burning up"],
    "cough": ["cough", "coughing", "hack", "coughing up", "i am coughing", "i have a cough", "coughing fit"],
    "dry_cough": ["dry cough", "nonproductive cough", "cough without mucus", "cough without phlegm", "tickle in throat"],
    "wet_cough": ["wet cough", "productive cough", "coughing up mucus", "phlegm", "coughing up phlegm", "mucus in cough"],
    "sore_throat": ["sore throat", "throat pain", "throat hurts", "painful to swallow", "scratchy throat", "throat is sore", "throat", "my throat hurts", "strep", "pharyngitis"],
    "runny_nose": ["runny nose", "nasal discharge", "nose running", "mucus from nose", "dripping nose", "my nose is running", "runny", "rhinorrhea"],
    "congestion": ["congestion", "stuffy nose", "blocked nose", "nasal congestion", "clogged nose", "stuffed up", "my nose is blocked", "congested", "sinuses blocked"],
    "shortness_of_breath": ["shortness of breath", "can't breathe", "difficulty breathing", "hard to breathe", "breathless", "struggling to breathe", "can't catch my breath", "breathing problems", "dyspnea"],
    "wheezing": ["wheezing", "whistling when breathing", "whistling breath", "whistling sound in chest", "wheezy", "asthmatic breathing"],
    "chest_pain": ["chest pain", "pain in chest", "chest discomfort", "chest pressure", "heart pain", "my chest hurts", "pain when breathing", "pleurisy"],
    "chest_tightness": ["chest tightness", "tight chest", "constriction in chest", "chest feels tight", "compressed chest feeling"],
    "sneezing": ["sneezing", "achoo", "multiple sneezes", "constant sneezing", "sneezing fits"],
    
    # Head and neurological symptoms
    "headache": ["headache", "head pain", "head ache", "head is pounding", "head hurts", "my head hurts", "pain in my head", "head", "pain in the head", "pounding head"],
    "migraine": ["migraine", "severe headache", "debilitating headache", "headache with nausea", "headache with light sensitivity", "aura"],
    "dizziness": ["dizziness", "dizzy", "feeling faint", "i feel dizzy", "feeling dizzy", "lightheaded", "light headed", "woozy"],
    "vertigo": ["vertigo", "room spinning", "spinning sensation", "world spinning", "movement sensation", "balance problem"],
    "lightheadedness": ["lightheaded", "light headed", "feeling faint", "near fainting", "pre-syncope", "almost passed out"],
    "fainting": ["fainting", "passed out", "loss of consciousness", "blacking out", "syncope", "collapsed"],
    "confusion": ["confusion", "disoriented", "can't think clearly", "mental fog", "foggy thinking", "confused", "disorientation"],
    "memory_problems": ["memory problems", "forgetful", "can't remember", "memory loss", "difficulty remembering", "amnesia", "short term memory issues"],
    "seizure": ["seizure", "convulsion", "fit", "epileptic episode", "shaking uncontrollably", "seizure episode"],
    "tremors": ["tremors", "shaking", "trembling", "hands shaking", "involuntary movement", "shaky hands"],
    "numbness": ["numbness", "numb", "no feeling", "loss of sensation", "pins and needles", "part of body numb"],
    "tingling": ["tingling", "pins and needles", "prickling sensation", "tingling sensation", "paresthesia"],
    "sensitivity_to_light": ["light sensitivity", "sensitive to light", "lights hurt my eyes", "photophobia", "bright light hurts", "light hurts my eyes"],
    "sensitivity_to_sound": ["sound sensitivity", "sensitive to noise", "noise hurts my ears", "sounds too loud", "hyperacusis"],
    
    # Gastrointestinal symptoms
    "nausea": ["nausea", "nauseated", "feel sick", "queasy", "want to vomit", "stomach churning", "i feel like vomiting", "feel like throwing up", "sick to my stomach"],
    "vomiting": ["vomiting", "throwing up", "vomited", "puking", "threw up", "getting sick", "i am vomiting", "vomit", "regurgitating"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool", "frequent bowel movements", "loose bowel", "i have diarrhea", "runny stool"],
    "constipation": ["constipation", "can't poop", "hard stool", "difficult bowel movement", "infrequent bowel movements", "straining at stool"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "tummy ache", "stomach ache", "pain in abdomen", "gut pain", "my stomach hurts", "belly pain", "belly ache"],
    "stomach_pain": ["stomach pain", "pain in stomach", "stomach hurts", "pain in stomach area", "epigastric pain"],
    "bloating": ["bloating", "bloated", "distended abdomen", "stomach swelling", "gassy", "abdominal distension", "feel full"],
    "gas": ["gas", "flatulence", "passing gas", "gassy", "intestinal gas", "excessive gas"],
    "heartburn": ["heartburn", "acid reflux", "burning in chest", "acid indigestion", "gerd", "reflux"],
    "indigestion": ["indigestion", "upset stomach", "dyspepsia", "stomach discomfort", "digestive discomfort"],
    "loss_of_appetite": ["loss of appetite", "not hungry", "don't want to eat", "no appetite", "lost appetite", "i don't feel like eating", "anorexia"],
    "increased_appetite": ["increased appetite", "always hungry", "eating more", "excessive hunger", "can't stop eating", "hyperphagia"],
    "difficulty_swallowing": ["difficulty swallowing", "trouble swallowing", "painful swallowing", "can't swallow", "dysphagia", "food gets stuck"],
    "bloody_stool": ["bloody stool", "blood in stool", "rectal bleeding", "bloody bowel movement", "hematochezia"],
    
    # Musculoskeletal symptoms
    "body_ache": ["body ache", "body pain", "everything hurts", "aching", "my body aches", "aches", "body aches", "general pain", "hurting all over"],
    "muscle_pain": ["muscle pain", "muscle ache", "sore muscles", "muscle soreness", "myalgia", "muscles hurt"],
    "joint_pain": ["joint pain", "painful joints", "joints hurt", "pain in joints", "arthritis pain", "my joints hurt", "joint ache", "arthralgia"],
    "back_pain": ["back pain", "backache", "pain in back", "sore back", "lumbar pain", "back spasm", "my back hurts"],
    "neck_pain": ["neck pain", "sore neck", "stiff neck", "pain in neck", "neck ache", "cervical pain", "my neck hurts"],
    "stiffness": ["stiffness", "stiff", "rigid", "can't bend", "limited movement", "reduced mobility", "restricted movement"],
    "swelling": ["swelling", "swollen", "edema", "puffiness", "bloated", "fluid retention", "inflamed"],
    "weakness": ["weakness", "weak", "no strength", "muscle weakness", "lack of power", "asthenia", "debility"],
    "muscle_cramps": ["muscle cramps", "cramping", "muscle spasm", "charlie horse", "cramp", "involuntary contraction"],
    "muscle_weakness": ["muscle weakness", "weak muscles", "my muscles are weak", "lack of muscle strength", "paresis"],
    
    # General symptoms
    "fatigue": ["fatigue", "tired", "exhausted", "no energy", "weak", "lethargic", "exhaustion", "i feel tired", "i am exhausted", "tiredness", "fatigued", "worn out"],
    "malaise": ["malaise", "feeling unwell", "feeling ill", "general discomfort", "out of sorts", "under the weather"],
    "chills": ["chills", "shivering", "feeling cold", "cold sweats", "rigors", "shaking from cold"],
    "night_sweats": ["night sweats", "sweating at night", "waking up sweating", "sweats during sleep", "nocturnal hyperhidrosis"],
    "weight_loss": ["weight loss", "losing weight", "unexplained weight loss", "getting thinner", "dropping pounds"],
    "weight_gain": ["weight gain", "gaining weight", "unexplained weight gain", "putting on weight", "increased weight"],
    "dehydration": ["dehydration", "dehydrated", "thirsty", "dry mouth", "lack of fluids", "not drinking enough"],
    "excessive_thirst": ["excessive thirst", "very thirsty", "abnormal thirst", "drinking a lot", "polydipsia"],
    "excessive_urination": ["excessive urination", "frequent urination", "peeing a lot", "urinating frequently", "polyuria"],
    "sleep_problems": ["sleep problems", "can't sleep", "difficulty sleeping", "insomnia", "poor sleep", "sleep disturbance"],
    
    # Skin symptoms
    "rash": ["rash", "skin irritation", "red spots", "bumps on skin", "skin outbreak", "hives", "skin rash", "i have a rash", "erythema", "dermatitis"],
    "itching": ["itching", "itchy", "itch", "scratching", "skin irritation", "need to scratch", "my skin itches", "i am itchy", "pruritus"],
    "hives": ["hives", "urticaria", "welts", "itchy bumps", "allergic rash", "raised itchy welts"],
    "skin_lesions": ["skin lesions", "skin sores", "skin ulcers", "open sores", "skin wounds", "skin spots"],
    "bruising": ["bruising", "bruises", "black and blue marks", "contusions", "skin discoloration", "purple spots"],
    "skin_discoloration": ["skin discoloration", "skin color change", "patches of different color", "pigment change", "vitiligo"],
    "dry_skin": ["dry skin", "flaky skin", "skin peeling", "xerosis", "rough skin", "scaly skin"],
    "excessive_sweating": ["excessive sweating", "sweating a lot", "profuse sweating", "hyperhidrosis", "sweating too much"],
    "jaundice": ["jaundice", "yellow skin", "yellowing", "yellow eyes", "yellow sclera", "icterus"],
    
    # Sensory symptoms
    "blurred_vision": ["blurred vision", "blurry vision", "can't see clearly", "fuzzy vision", "vision not clear", "unfocused vision"],
    "double_vision": ["double vision", "seeing double", "diplopia", "two images", "dual vision"],
    "vision_loss": ["vision loss", "can't see", "blindness", "loss of sight", "poor vision", "visual impairment"],
    "eye_pain": ["eye pain", "painful eyes", "sore eyes", "eye discomfort", "ocular pain", "eye ache"],
    "hearing_loss": ["hearing loss", "can't hear", "deafness", "hard of hearing", "reduced hearing", "impaired hearing"],
    "ringing_in_ears": ["ringing in ears", "tinnitus", "ear ringing", "buzzing in ears", "ear noise", "ear buzzing"],
    "ear_pain": ["ear pain", "earache", "painful ear", "ear discomfort", "otalgia", "sore ear"],
    "loss_of_taste": ["loss of taste", "can't taste", "no taste", "food has no flavor", "tasteless", "i can't taste food", "lost my sense of taste", "ageusia"],
    "loss_of_smell": ["loss of smell", "can't smell", "no smell", "unable to smell", "lost sense of smell", "i can't smell", "lost my sense of smell", "anosmia"],
    "altered_taste": ["altered taste", "strange taste", "taste changes", "bad taste", "metallic taste", "dysgeusia"],
    
    # Psychological symptoms
    "anxiety": ["anxiety", "anxious", "worried", "nervous", "on edge", "panicky", "fear", "stress"],
    "depression": ["depression", "depressed", "feeling down", "sad", "hopeless", "despair", "melancholy", "blue"],
    "mood_swings": ["mood swings", "emotional changes", "ups and downs", "emotional instability", "mood changes"],
    "irritability": ["irritability", "irritable", "easily annoyed", "short-tempered", "grouchy", "snappy"],
    "confusion": ["confusion", "disorientation", "confused", "can't think straight", "perplexed", "bewildered"],
    "hallucinations": ["hallucinations", "seeing things", "hearing voices", "false perceptions", "not real sensations"],
    "paranoia": ["paranoia", "suspicious", "mistrust", "feeling watched", "persecutory thoughts", "paranoid"],
    "insomnia": ["insomnia", "can't sleep", "trouble sleeping", "sleeplessness", "difficulty falling asleep", "waking up at night"],
    
    # Cardiovascular symptoms
    "palpitations": ["palpitations", "racing heart", "heart racing", "pounding heart", "fluttering heart", "heartbeat sensation"],
    "irregular_heartbeat": ["irregular heartbeat", "arrhythmia", "skipped beats", "heart rhythm problem", "irregular pulse"],
    "rapid_heartbeat": ["rapid heartbeat", "fast heart rate", "tachycardia", "heart beating fast", "pulse racing"],
    "slow_heartbeat": ["slow heartbeat", "slow pulse", "bradycardia", "heart beating slowly", "slow heart rate"],
    "high_blood_pressure": ["high blood pressure", "hypertension", "elevated blood pressure", "high bp", "high pressure"],
    "low_blood_pressure": ["low blood pressure", "hypotension", "decreased blood pressure", "low bp", "low pressure"],
    "fainting": ["fainting", "passed out", "syncope", "loss of consciousness", "blackout", "collapsed"],
    "swelling_of_extremities": ["swelling of extremities", "swollen ankles", "swollen legs", "swollen feet", "edema", "puffy legs"],
    
    # Reproductive and urinary symptoms
    "menstrual_changes": ["menstrual changes", "period changes", "irregular periods", "heavy periods", "menstrual irregularity"],
    "vaginal_discharge": ["vaginal discharge", "discharge", "abnormal discharge", "leukorrhea", "vaginal secretion"],
    "erectile_dysfunction": ["erectile dysfunction", "impotence", "can't get erection", "can't maintain erection", "ed"],
    "urinary_frequency": ["urinary frequency", "frequent urination", "peeing often", "bathroom frequently", "urinating a lot"],
    "urinary_urgency": ["urinary urgency", "urgent need to urinate", "sudden urge to pee", "can't hold urine", "urgent urination"],
    "painful_urination": ["painful urination", "burning urination", "pain when peeing", "dysuria", "urination pain"],
    "blood_in_urine": ["blood in urine", "bloody urine", "red urine", "pink urine", "hematuria"],
    "urinary_incontinence": ["urinary incontinence", "urine leakage", "can't control bladder", "bladder leakage", "wetting myself"],
    
    # Respiratory conditions
    "asthma": ["asthma", "asthma attack", "asthmatic", "bronchial asthma", "reactive airway"],
    "bronchitis": ["bronchitis", "chest infection", "bronchial infection", "inflamed airways", "bronchial inflammation"],
    "pneumonia": ["pneumonia", "lung infection", "chest infection", "lung inflammation", "pneumonitis"],
    "copd": ["copd", "chronic bronchitis", "emphysema", "chronic obstructive pulmonary disease", "lung disease"],
    "tuberculosis": ["tuberculosis", "tb", "consumption", "koch's disease", "pulmonary tuberculosis"],
    
    # Immune system symptoms
    "frequent_infections": ["frequent infections", "getting sick often", "recurrent infections", "always sick", "weak immune system"],
    "allergic_reaction": ["allergic reaction", "allergy", "allergies", "allergic", "hypersensitivity reaction"],
    "swollen_lymph_nodes": ["swollen lymph nodes", "swollen glands", "enlarged lymph nodes", "lymphadenopathy", "swollen nodes"],
    "autoimmune_symptoms": ["autoimmune symptoms", "autoimmune disease", "immune system attacking body", "autoimmunity", "immune disorder"]
}

def get_symptom_descriptions(symptom_list):
    """
    Get descriptions for a list of symptoms
    
    Args:
        symptom_list: List of symptom keys
        
    Returns:
        dict: Symptoms with their descriptions
    """
    return {symptom: common_symptoms[symptom] for symptom in symptom_list if symptom in common_symptoms}

import streamlit as st
import os
import tempfile
from gtts import gTTS
import base64
import time
from utils import transcribe_audio, detect_language, translate_text
from medical_rules import diagnose_symptoms
from symptoms_db import common_symptoms, get_symptom_descriptions
from database import save_consultation, initialize_medical_data
from serious_condition_analyzer import generate_serious_condition_analysis
from treatment_db import get_treatment_recommendations
from advanced_diagnosis_system import get_advanced_diagnosis

# Set page configuration
st.set_page_config(
    page_title="Multilingual Medical Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    div.stMarkdown h1 {
        color: #2196F3;
        font-size: 2em !important;
        font-weight: 700;
        margin-bottom: 0px;
        text-align: center;
    }
    div.stMarkdown h2 {
        color: #4CAF50;
        font-size: 1.3em !important;
        margin-top: 0px;
        text-align: center;
    }
    .stButton>button {
        background-color: #E53935 !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    .stButton>button:hover {
        background-color: #C62828 !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    .error-box {
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .stAlert {
        border-radius: 10px !important;
        padding: 12px 15px !important;
    }
    .footer-love {
        text-align: center !important; 
        color: #7F7F7F !important; 
        font-size: 14px !important; 
        margin-top: 20px !important;
    }
    div.stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        padding: 5px 10px;
    }
    div.stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f5f5f5;
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        font-weight: 500;
    }
    div.stTabs [aria-selected="true"] {
        background-color: #E53935 !important;
        color: white !important;
    }
    .main-content {
        max-width: 95%;
        margin: 0 auto;
        padding: 10px;
    }
    .center-img {
        display: block;
        margin: 0 auto;
        max-width: 80%;
    }
    @media (max-width: 768px) {
        div.stMarkdown h1 {
            font-size: 1.6em !important;
            padding: 0 5px;
        }
        div.stMarkdown h2 {
            font-size: 1.1em !important;
        }
        div.stTabs [data-baseweb="tab"] {
            padding: 0 10px;
            font-size: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# No need to check for an API key as we're using a free AI diagnosis implementation

# Initialize medical data in database
initialize_medical_data(common_symptoms)

# Initialize session state variables if they don't exist
if 'language' not in st.session_state:
    st.session_state.language = "english"
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = ""
if 'english_transcript' not in st.session_state:
    st.session_state.english_transcript = ""
if 'detected_symptoms' not in st.session_state:
    st.session_state.detected_symptoms = []
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'diagnosis_audio' not in st.session_state:
    st.session_state.diagnosis_audio = None
if 'serious_condition_analysis' not in st.session_state:
    st.session_state.serious_condition_analysis = ""
if 'use_advanced_diagnosis' not in st.session_state:
    st.session_state.use_advanced_diagnosis = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = "age"
if 'age' not in st.session_state:
    st.session_state.age = None
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""

# Initialize variables that will be used across different scopes
text_input = ""
audio_file = None
process_diagnosis = False  # Initialize process_diagnosis variable

# Function to autoplay audio
def autoplay_audio(audio_bytes):
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}"></audio>'
    st.markdown(audio_tag, unsafe_allow_html=True)

# Custom header with logo - centered for mobile
st.markdown("<div style='text-align: center; margin-bottom: 10px;'><img src='hospital_logo.svg' width='100'/></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #000000; font-weight: 700; font-size: 2em;'>Multilingual Medical Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #9C27B0; font-weight: 500; font-size: 1.3em;'>Advanced AI-powered diagnosis in multiple languages</h2>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #E91E63; font-style: italic; margin-top: -10px;'>❤️ Crafted with love by Aswath</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Added spacing

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px; padding: 0 15px;'>
    Describe your symptoms through voice in <b>English</b>, <b>Tamil</b>, or <b>Hindi</b> 
    and receive a comprehensive medical diagnosis with treatment options.
    </div>
""", unsafe_allow_html=True)

# Language selector
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("English", use_container_width=True):
        st.session_state.language = "english"
        st.rerun()
with col2:
    if st.button("தமிழ் (Tamil)", use_container_width=True):
        st.session_state.language = "tamil"
        st.rerun()
with col3:
    if st.button("हिंदी (Hindi)", use_container_width=True):
        st.session_state.language = "hindi"
        st.rerun()

# Display current language
current_lang_display = {
    "english": "English",
    "tamil": "தமிழ் (Tamil)",
    "hindi": "हिंदी (Hindi)"
}
st.info(f"Current language: {current_lang_display[st.session_state.language]}")

# Multi-step flow based on current step
if st.session_state.current_step == "age":
    # Age input section
    st.subheader("What is your age?")
    
    # Instructions for the age step
    st.markdown("""
        **Please enter your age:**
        
        Your age helps us provide a more accurate diagnosis as certain conditions are more 
        common in specific age groups.
    """)
    
    # Mobile-friendly centered design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        age = st.number_input("Age", min_value=1, max_value=120, step=1, 
                           help="Enter your age in years")
        
        # Next button to proceed to gender
        if st.button("Next", type="primary", use_container_width=True):
            if age > 0:
                st.session_state.age = int(age)
                st.session_state.current_step = "gender"
                st.rerun()
            else:
                st.error("Please enter a valid age.")

elif st.session_state.current_step == "gender":
    # Gender input section
    st.subheader("What is your gender?")
    
    # Instructions for the gender step
    st.markdown("""
        **Please select your gender:**
        
        Gender information helps us tailor the diagnosis as certain conditions are more 
        prevalent in specific genders.
    """)
    
    # Mobile-friendly centered design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        gender_options = ["Male", "Female", "Other"]
        gender_index = st.selectbox("Gender", 
                                  options=range(len(gender_options)),
                                  format_func=lambda x: gender_options[x],
                                  help="Select your gender")
        
        selected_gender = gender_options[gender_index]
        
        # Next button to proceed to symptoms
        if st.button("Next", type="primary", use_container_width=True):
            st.session_state.gender = selected_gender
            st.session_state.current_step = "symptoms"
            st.rerun()
        
        # Back button to return to age
        if st.button("Back", use_container_width=True):
            st.session_state.current_step = "age"
            st.rerun()

else:  # symptoms step
    # Voice input section
    st.subheader("Describe Your Symptoms")
    
    # Display patient information
    st.info(f"Patient Information: Age {st.session_state.age}, Gender: {st.session_state.gender}")
    
    # Instructions for users
    st.markdown("""
        **Instructions:**
        1. Select your preferred language above
        2. Either type your symptoms in the text area or upload an audio recording
        3. Click the button to analyze your input
        4. View your diagnosis and listen to the audio response
    """)
    
    # Display info message about audio recording
    st.info("You can use your phone or computer's voice recorder app to record your symptoms and upload the file here.")
    
    # Always use advanced diagnosis
    st.session_state.use_advanced_diagnosis = True
    
    # Text input for symptoms (alternative to voice)
    st.session_state.text_input = st.text_area("Type your symptoms here:", 
                                placeholder="Example: I have a headache, fever, and body aches...",
                                help="Describe your symptoms in detail")
    
    # File uploader for audio input
    audio_file = st.file_uploader("Upload an audio recording of your symptoms (MP3, WAV, or M4A)", 
                                 type=["mp3", "wav", "m4a"], 
                                 help="Record your voice describing your symptoms and upload the file")
    
    # Single "Get Comprehensive Medical Diagnosis" button
    if st.button("Get Comprehensive Medical Diagnosis", type="primary", key="diagnose_button", use_container_width=True):
        process_diagnosis = True
    else:
        process_diagnosis = False
    
    # Back button to return to gender
    if st.button("◀ Change Information", use_container_width=True):
        st.session_state.current_step = "age"
        st.rerun()

# Process text input (only in symptoms step)
if st.session_state.current_step == "symptoms" and process_diagnosis:
    with st.spinner("Processing your symptoms for comprehensive diagnosis..."):
        # Detect language
        detected_lang = detect_language(st.session_state.text_input)
        
        # Store original transcript
        st.session_state.transcript = st.session_state.text_input
        
        # If not English, translate to English for symptom analysis
        if detected_lang != 'en':
            st.session_state.english_transcript = translate_text(st.session_state.text_input, detected_lang, 'en')
        else:
            st.session_state.english_transcript = st.session_state.text_input
            
        # Extract symptoms and diagnose
        detected_symptoms, diagnosis = diagnose_symptoms(st.session_state.english_transcript)
        st.session_state.detected_symptoms = detected_symptoms
        
        # Use advanced diagnosis if enabled
        lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
        if st.session_state.use_advanced_diagnosis:
            primary_condition, advanced_diagnosis, confidence, additional_conditions = get_advanced_diagnosis(
                detected_symptoms, st.session_state.english_transcript, lang_code
            )
            if advanced_diagnosis:
                diagnosis = advanced_diagnosis
        
        # Generate serious condition analysis
        serious_analysis = generate_serious_condition_analysis(st.session_state.english_transcript, lang_code)
        st.session_state.serious_condition_analysis = serious_analysis
        
        # Translate diagnosis back to original language if needed
        if detected_lang != 'en':
            target_lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
            translated_diagnosis = translate_text(diagnosis, 'en', target_lang_code)
            st.session_state.diagnosis = translated_diagnosis
        else:
            st.session_state.diagnosis = diagnosis
            
        # Save consultation to database with age and gender
        lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
        save_consultation(
            language=lang_code,
            transcript=st.session_state.transcript,
            symptoms_list=detected_symptoms,
            diagnosis=st.session_state.diagnosis,
            age=st.session_state.age,
            gender=st.session_state.gender
        )
            
        # Create audio response for the diagnosis
        tts_lang = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
        tts = gTTS(text=st.session_state.diagnosis, lang=tts_lang, slow=False)
        
        # Save the audio to a temporary file and then read it
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            with open(f.name, 'rb') as audio_file:
                st.session_state.diagnosis_audio = audio_file.read()
            os.unlink(f.name)
            
        st.rerun()

# Process audio file (only in symptoms step)
if st.session_state.current_step == "symptoms" and audio_file is not None and audio_file != st.session_state.audio_bytes:
    st.session_state.audio_bytes = audio_file
    
    # Save uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_file.name.split(".")[-1]}') as tmp_file:
        tmp_file.write(audio_file.getvalue())
        tmp_path = tmp_file.name
    
    with st.spinner("Processing your voice input..."):
        # Transcribe the audio
        transcript = transcribe_audio(tmp_path)
        if transcript:
            # Detect language
            detected_lang = detect_language(transcript)
            
            # Store original transcript
            st.session_state.transcript = transcript
            
            # If not English, translate to English for symptom analysis
            if detected_lang != 'en':
                st.session_state.english_transcript = translate_text(transcript, detected_lang, 'en')
            else:
                st.session_state.english_transcript = transcript
                
            # Clean up temporary file
            os.unlink(tmp_path)
            
            # Extract symptoms and diagnose
            detected_symptoms, diagnosis = diagnose_symptoms(st.session_state.english_transcript)
            st.session_state.detected_symptoms = detected_symptoms
            
            # Use advanced diagnosis if enabled
            lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
            if st.session_state.use_advanced_diagnosis:
                primary_condition, advanced_diagnosis, confidence, additional_conditions = get_advanced_diagnosis(
                    detected_symptoms, st.session_state.english_transcript, lang_code
                )
                if advanced_diagnosis:
                    diagnosis = advanced_diagnosis
            
            # Generate serious condition analysis
            serious_analysis = generate_serious_condition_analysis(st.session_state.english_transcript, lang_code)
            st.session_state.serious_condition_analysis = serious_analysis
            
            # Translate diagnosis back to original language if needed
            if detected_lang != 'en':
                target_lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
                translated_diagnosis = translate_text(diagnosis, 'en', target_lang_code)
                st.session_state.diagnosis = translated_diagnosis
            else:
                st.session_state.diagnosis = diagnosis
                
            # Save consultation to database with age and gender
            lang_code = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
            save_consultation(
                language=lang_code,
                transcript=st.session_state.transcript,
                symptoms_list=detected_symptoms,
                diagnosis=st.session_state.diagnosis,
                age=st.session_state.age,
                gender=st.session_state.gender
            )
                
            # Create audio response for the diagnosis
            tts_lang = {'english': 'en', 'tamil': 'ta', 'hindi': 'hi'}[st.session_state.language]
            tts = gTTS(text=st.session_state.diagnosis, lang=tts_lang, slow=False)
            
            # Save the audio to a temporary file and then read it
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                tts.save(f.name)
                with open(f.name, 'rb') as audio_file:
                    st.session_state.diagnosis_audio = audio_file.read()
                os.unlink(f.name)
                
            st.rerun()
        else:
            st.error("Sorry, I couldn't understand the audio. Please try again with a clearer recording or use the text input.")

# Display transcript if available
if st.session_state.transcript:
    st.subheader("Your described symptoms")
    st.write(st.session_state.transcript)
    
    # Display detected symptoms as boxes
    if st.session_state.detected_symptoms:
        st.subheader("Detected symptoms")
        symptom_descriptions = get_symptom_descriptions(st.session_state.detected_symptoms)
        
        # Create CSS for symptom boxes
        st.markdown("""
        <style>
        .symptom-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
            margin: 15px 0;
        }
        .symptom-box {
            background-color: #FFF9C4;
            border-radius: 8px;
            padding: 12px 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #FBC02D;
        }
        .symptom-title {
            color: #5D4037;
            font-weight: 600;
            font-size: 1.05em;
            margin-bottom: 5px;
        }
        .symptom-desc {
            color: #5D4037;
            font-size: 0.9em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create opening div for grid
        st.markdown('<div class="symptom-grid">', unsafe_allow_html=True)
        
        # Add each symptom as a box
        for symptom, description in symptom_descriptions.items():
            st.markdown(f"""
            <div class="symptom-box">
                <div class="symptom-title">{symptom.replace('_', ' ').title()}</div>
                <div class="symptom-desc">{description}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Close the grid div
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display diagnosis and treatments in tabs
    if st.session_state.diagnosis:
        # Create tabs for different sections
        diagnosis_tab, treatments_tab, when_to_visit_tab = st.tabs(["Diagnosis", "Methods of Cure", "When to Visit Doctor"])
        
        with diagnosis_tab:
            # Extract condition name and reformat the diagnosis text
            import re
            condition_match = re.search(r'\*\*(.*?)\*\*', st.session_state.diagnosis)
            condition_name = condition_match.group(1) if condition_match else "Unknown Condition"
            
            # Create a more aesthetically pleasing diagnosis presentation
            # Fix the text formatting issue by properly replacing the condition name in diagnosis
            diagnosis_text = st.session_state.diagnosis
            diagnosis_text = diagnosis_text.replace(f'**{condition_name}**', '')
            
            # Remove any "you may have" text that might still be present
            diagnosis_text = diagnosis_text.replace("You may have ", "")
            diagnosis_text = diagnosis_text.replace("you may have ", "")
            diagnosis_text = diagnosis_text.replace("You may have.", "")
            diagnosis_text = diagnosis_text.replace("you may have.", "")
            
            st.markdown(f"""
            <div style="background-color:#E8F4FD; padding:20px; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color:#1976D2; margin-top:0; font-weight:600; font-size:1.4em;">{condition_name}</h3>
                <p style="font-size:1.05em; line-height:1.5;">{diagnosis_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display serious condition analysis as part of diagnosis but in smaller format
            if st.session_state.serious_condition_analysis:
                st.markdown("""
                <div style="background-color:#FFF3E0; padding:15px; border-radius:8px; border-left:4px solid #F44336; 
                      margin-top:15px; margin-bottom:15px; font-size:0.9em; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color:#D32F2F; margin-top:0; font-weight:600; font-size:1.1em;">⚠️ Potential Serious Conditions to Consider</h4>
                """, unsafe_allow_html=True)
                
                # Get just the content without the disclaimer
                serious_content = st.session_state.serious_condition_analysis
                if "*This is not a professional diagnosis" in serious_content:
                    serious_content = serious_content.split("*This is not a professional diagnosis")[0]
                
                st.markdown(serious_content, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Play diagnosis audio
            if st.session_state.diagnosis_audio:
                st.subheader("Listen to diagnosis")
                autoplay_audio(st.session_state.diagnosis_audio)
                
                # Offer a download button for the audio
                st.download_button(
                    label="Download diagnosis audio",
                    data=st.session_state.diagnosis_audio,
                    file_name="diagnosis.mp3",
                    mime="audio/mp3"
                )
        
        with treatments_tab:
            # Get treatment recommendations for the condition
            treatments = get_treatment_recommendations(condition_name)
            
            st.subheader(f"Treatment Options for {condition_name}")
            
            # Home remedies with better styling
            st.markdown("""
            <div style="background-color:#E8F5E9; padding:15px; border-radius:10px; margin-bottom:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color:#2E7D32; margin-top:0; display:flex; align-items:center;">
                    <span style="margin-right:8px;">🏠</span> Home Remedies
                </h3>
            """, unsafe_allow_html=True)
            
            if treatments and "home_remedies" in treatments and treatments["home_remedies"]:
                for remedy in treatments["home_remedies"]:
                    st.markdown(f"""<div style="margin-bottom:8px; padding-left:10px; border-left:3px solid #A5D6A7;">
                    • {remedy}</div>""", unsafe_allow_html=True)
            else:
                st.info("No specific home remedies are available for this condition. Please consult a healthcare professional.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Medical treatments with better styling
            st.markdown("""
            <div style="background-color:#E3F2FD; padding:15px; border-radius:10px; margin-bottom:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color:#1565C0; margin-top:0; display:flex; align-items:center;">
                    <span style="margin-right:8px;">🏥</span> Medical Treatments
                </h3>
            """, unsafe_allow_html=True)
            
            if treatments and "medical_treatments" in treatments and treatments["medical_treatments"]:
                for treatment in treatments["medical_treatments"]:
                    st.markdown(f"""<div style="margin-bottom:8px; padding-left:10px; border-left:3px solid #90CAF9;">
                    • {treatment}</div>""", unsafe_allow_html=True)
            else:
                st.info("No specific medical treatments are listed for this condition. Please consult a healthcare professional.")
                
            st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("""
            <div style="background-color:#E3F2FD; padding:15px; border-radius:8px; margin-top:20px; font-style:italic;">
            Note: These treatment options are for informational purposes only and are not a substitute for professional medical advice. 
            Always consult with a qualified healthcare provider before starting any treatment.
            </div>
            """, unsafe_allow_html=True)
        
        with when_to_visit_tab:
            st.subheader("When to Visit a Doctor")
            
            # When to visit recommendations with improved styling
            st.markdown("""
            <div style="background-color:#FFF8E1; padding:15px; border-radius:10px; margin-bottom:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color:#E65100; margin-top:0; display:flex; align-items:center;">
                    <span style="margin-right:8px;">🩺</span> Condition-Specific Guidance
                </h3>
            """, unsafe_allow_html=True)
            
            if treatments and "when_to_visit" in treatments and treatments["when_to_visit"]:
                for visit_recommendation in treatments["when_to_visit"]:
                    if "EMERGENCY" in visit_recommendation or "IMMEDIATE" in visit_recommendation or "911" in visit_recommendation:
                        st.markdown(f"""<div style="margin-bottom:10px; padding:8px; border-radius:6px; background-color:#FFEBEE; 
                        border-left:3px solid #D32F2F; font-weight:bold;">⚠️ {visit_recommendation}</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="margin-bottom:8px; padding-left:10px; border-left:3px solid #FFD54F;">
                        • {visit_recommendation}</div>""", unsafe_allow_html=True)
            else:
                st.info("No specific recommendations are available for when to visit a doctor for this condition. When in doubt, it's always best to consult a healthcare professional.")
                
            st.markdown("</div>", unsafe_allow_html=True)
            
            # General guidance with simplified styling - fix rendering issues
            st.subheader("🚨 General Emergency Guidance")
            st.markdown("*Seek immediate medical attention if you experience any of the following symptoms:*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🫁 Breathing Issues**")
                st.markdown("Difficulty breathing or shortness of breath")
                
                st.markdown("**❤️ Chest Problems**")
                st.markdown("Persistent chest pain or pressure")
                
                st.markdown("**🧠 Mental Changes**")
                st.markdown("New confusion or inability to wake/stay awake")
                
                st.markdown("**💙 Discoloration**")
                st.markdown("Bluish lips or face")
                
            with col2:
                st.markdown("**😖 Severe Pain**")
                st.markdown("Severe, persistent pain anywhere")
                
                st.markdown("**🩸 Bleeding**")
                st.markdown("Uncontrolled bleeding")
                
                st.markdown("**🤕 Sudden Headache**")
                st.markdown("Sudden severe headache with no known cause")
                
                st.markdown("**😰 Numbness/Weakness**")
                st.markdown("Sudden numbness, especially on one side")
            
            st.warning("**Important:** This information is not a substitute for professional medical advice. If you're unsure whether to seek medical care, it's better to err on the side of caution and consult a healthcare provider.")

# Add Book Appointment button after diagnosis is displayed
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Add spacing

# Centered Book Appointment button with enhanced styling
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <h3 style="color: #4CAF50;">Need to speak with a doctor?</h3>
    <p>Connect with qualified healthcare professionals through a teleconsultation</p>
</div>
""", unsafe_allow_html=True)

if st.button("📅 Book a Teleconsultation Appointment", type="primary", key="book_appointment_btn", use_container_width=True):
    st.switch_page("pages/book_appointment.py")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Add spacing



# Disclaimer
st.markdown("---")
st.markdown("""
    <div style="color: #F44336; font-weight: bold;">
    ⚠️ Medical Disclaimer: This is a prototype assistant for educational purposes only. 
    Always consult with a qualified healthcare professional for medical advice, diagnosis, or treatment.
    </div>
""", unsafe_allow_html=True)

# Footer with disclaimer
st.markdown("""
    <div style="text-align: center; color: #7F7F7F; font-size: 14px; margin-top: 20px;">
    © 2023 Multilingual Medical Assistant | Not for actual medical use | Educational purposes only
    </div>
""", unsafe_allow_html=True)
import os
port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)

import streamlit as st
import json
from database import get_recent_consultations, get_consultations_by_symptom
import datetime

# Admin authentication function
def admin_authenticate():
    """
    Function to authenticate admin users
    """
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
        
    if st.session_state.admin_authenticated:
        return True
        
    # Get the admin credentials from secrets
    admin_username = st.secrets["admin"]["username"]
    admin_password = st.secrets["admin"]["password"]
    
    st.title("🔒 Admin Login Required")
    st.markdown("Please enter your admin credentials to access the consultation history.")
    
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Add a login button
    if st.button("Login"):
        if username == admin_username and password == admin_password:
            st.session_state.admin_authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")
    
    # Add a return to main app button
    if st.button("Return to Main App"):
        st.switch_page("app.py")
        
    return False

st.set_page_config(
    page_title="Consultation History - Multilingual Medical Assistant",
    page_icon="🏥",
    layout="wide"
)

# Check if user is authenticated
if not admin_authenticate():
    st.stop()  # Stop execution if not authenticated

st.title("📋 Consultation History")
st.markdown("View past consultations and their diagnoses")

# Search options
st.subheader("Search Consultations")
search_by = st.radio("Search by:", ["Recent", "Symptom"])

if search_by == "Recent":
    # Get recent consultations
    consultations = get_recent_consultations(limit=20)
    
    # Display consultations
    if not consultations:
        st.info("No consultations found in the database.")
    else:
        st.write(f"Found {len(consultations)} consultations")
        
        for consultation in consultations:
            with st.expander(f"Consultation #{consultation.id} - {consultation.created_at.strftime('%Y-%m-%d %H:%M')}"):
                st.markdown(f"**Language**: {consultation.language}")
                st.markdown(f"**Patient Description**: {consultation.transcript}")
                
                # Display symptoms
                symptoms = json.loads(consultation.symptoms)
                st.markdown("**Detected Symptoms**:")
                for symptom in symptoms:
                    st.markdown(f"- {symptom}")
                
                # Display diagnosis
                st.markdown("**Diagnosis**:")
                st.markdown(f'<div style="background-color:#E8F4FD; padding:15px; border-radius:10px;">{consultation.diagnosis}</div>', unsafe_allow_html=True)

elif search_by == "Symptom":
    # Search by symptom
    symptom_search = st.text_input("Enter symptom to search for:", placeholder="e.g., headache, fever, cough")
    
    if symptom_search:
        consultations = get_consultations_by_symptom(symptom_search)
        
        if not consultations:
            st.info(f"No consultations found with symptom '{symptom_search}'.")
        else:
            st.write(f"Found {len(consultations)} consultations with symptom '{symptom_search}'")
            
            for consultation in consultations:
                with st.expander(f"Consultation #{consultation.id} - {consultation.created_at.strftime('%Y-%m-%d %H:%M')}"):
                    st.markdown(f"**Language**: {consultation.language}")
                    st.markdown(f"**Patient Description**: {consultation.transcript}")
                    
                    # Display symptoms
                    symptoms = json.loads(consultation.symptoms)
                    st.markdown("**Detected Symptoms**:")
                    for symptom in symptoms:
                        st.markdown(f"- {symptom}")
                    
                    # Display diagnosis
                    st.markdown("**Diagnosis**:")
                    st.markdown(f'<div style="background-color:#E8F4FD; padding:15px; border-radius:10px;">{consultation.diagnosis}</div>', unsafe_allow_html=True)
    
# Disclaimer
st.markdown("---")
st.markdown("""
    <div style="color: #F44336; font-weight: bold;">
    ⚠️ Medical Disclaimer: This is a prototype assistant for educational purposes only. 
    Always consult with a qualified healthcare professional for medical advice, diagnosis, or treatment.
    </div>
""", unsafe_allow_html=True)
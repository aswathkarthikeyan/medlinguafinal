import streamlit as st
import json
import pandas as pd
import altair as alt
from database import get_recent_consultations
from collections import Counter

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
    st.markdown("Please enter your admin credentials to access the symptom statistics.")
    
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
    page_title="Symptom Statistics - Multilingual Medical Assistant",
    page_icon="📊",
    layout="wide"
)

# Check if user is authenticated
if not admin_authenticate():
    st.stop()  # Stop execution if not authenticated

st.title("📊 Symptom Statistics")
st.markdown("Statistical analysis of symptoms across consultations")

# Get consultations for analysis
consultations = get_recent_consultations(limit=100)

if not consultations:
    st.info("No consultation data available for analysis.")
else:
    # Extract all symptoms from consultations
    all_symptoms = []
    for consultation in consultations:
        symptoms = json.loads(consultation.symptoms)
        all_symptoms.extend(symptoms)
    
    # Count symptom occurrences
    symptom_counts = Counter(all_symptoms)
    
    # Create DataFrame for visualization
    df = pd.DataFrame({
        'Symptom': list(symptom_counts.keys()),
        'Count': list(symptom_counts.values())
    })
    
    # Sort by count descending
    df = df.sort_values('Count', ascending=False).reset_index(drop=True)
    
    # Display total consultations
    st.subheader(f"Total Consultations: {len(consultations)}")
    
    # Display top symptoms
    st.subheader("Most Common Symptoms")
    
    # Bar chart 
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Occurrences'),
        y=alt.Y('Symptom:N', title='Symptom', sort='-x'),
        color=alt.Color('Count:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['Symptom', 'Count']
    ).properties(
        title='Symptom Frequency',
        width=600,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Display as a table
    st.subheader("Symptom Frequency Table")
    st.dataframe(df, use_container_width=True)
    
    # Additional statistics
    if len(consultations) > 1:
        st.subheader("Consultation Language Distribution")
        languages = [c.language for c in consultations]
        language_counts = Counter(languages)
        
        lang_df = pd.DataFrame({
            'Language': list(language_counts.keys()),
            'Count': list(language_counts.values())
        })
        
        # Simple pie chart
        lang_chart = alt.Chart(lang_df).mark_arc().encode(
            theta='Count:Q',
            color='Language:N',
            tooltip=['Language', 'Count']
        ).properties(
            title='Consultations by Language',
            width=400,
            height=400
        )
        
        st.altair_chart(lang_chart, use_container_width=True)

# Disclaimer
st.markdown("---")
st.markdown("""
    <div style="color: #F44336; font-weight: bold;">
    ⚠️ Medical Disclaimer: This is a prototype assistant for educational purposes only. 
    The statistical data shown here is based on the consultations performed with this app and should not be used for medical research or professional diagnosis.
    </div>
""", unsafe_allow_html=True)
import streamlit as st
from datetime import datetime, timedelta
import json
import os
import uuid
import sys

# Add parent directory to path to import email_utils
sys.path.append(".")

# Set page configuration
st.set_page_config(
    page_title="Book Doctor Appointment - Multilingual Medical Assistant",
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
    .appointment-card {
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .calendar-day {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        cursor: pointer;
    }
    .calendar-day:hover {
        background-color: #E8F5E9;
        border-color: #4CAF50;
    }
    .calendar-day.selected {
        background-color: #4CAF50;
        color: white;
        border-color: #2E7D32;
    }
    .time-slot {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        cursor: pointer;
    }
    .time-slot:hover {
        background-color: #E3F2FD;
        border-color: #2196F3;
    }
    .time-slot.selected {
        background-color: #2196F3;
        color: white;
        border-color: #1565C0;
    }
    .time-slot.unavailable {
        background-color: #EEEEEE;
        color: #9E9E9E;
        cursor: not-allowed;
    }
    .success-message {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize appointments file path
APPOINTMENTS_FILE = "data/appointments.json"
os.makedirs("data", exist_ok=True)

# Initialize appointments data structure if it doesn't exist
if not os.path.exists(APPOINTMENTS_FILE):
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump([], f)

# Function to load appointments
def load_appointments():
    try:
        with open(APPOINTMENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Function to save appointments
def save_appointment(appointment_data):
    appointments = load_appointments()
    appointment_data["id"] = str(uuid.uuid4())
    appointments.append(appointment_data)
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=4)
    return appointment_data["id"]

# Function to check if a time slot is available
def is_slot_available(date, time_slot):
    appointments = load_appointments()
    for appointment in appointments:
        if appointment["date"] == date and appointment["time_slot"] == time_slot:
            return False
    return True

# Page header
st.markdown("<div style='text-align: center; margin-bottom: 10px;'><img src='hospital_logo.svg' width='100'/></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #000000; font-weight: 700; font-size: 2em;'>Book a Teleconsultation</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #9C27B0; font-weight: 500; font-size: 1.3em;'>Connect with qualified medical professionals</h2>", unsafe_allow_html=True)

# Initialize session state for multi-step form
if "appointment_step" not in st.session_state:
    st.session_state.appointment_step = 1

if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

if "appointment_date" not in st.session_state:
    st.session_state.appointment_date = None

if "appointment_time" not in st.session_state:
    st.session_state.appointment_time = None

# Step 1: Collect Patient Information
if st.session_state.appointment_step == 1:
    st.markdown("### 📋 Patient Information")
    st.markdown("Please provide your personal details for the teleconsultation.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*", 
                            help="Enter your full name as it appears on official documents")
        email = st.text_input("Email Address*", 
                            help="We'll send appointment confirmation and teleconsultation link to this email")
        phone = st.text_input("Phone Number*", 
                            help="Enter a valid mobile number for appointment reminders")
        age = st.number_input("Age*", min_value=1, max_value=120, value=30,
                            help="Your current age in years")
    
    with col2:
        gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other"],
                            help="Select your gender")
        height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170,
                                help="Your height in centimeters")
        weight = st.number_input("Weight (kg)", min_value=1, max_value=300, value=70,
                                help="Your weight in kilograms")
        existing_conditions = st.text_area("Existing Medical Conditions", 
                                        help="Any chronic illnesses, allergies, or ongoing treatments")
    
    additional_notes = st.text_area("Additional Notes for the Doctor", 
                                  help="Any specific concerns you'd like to discuss during the appointment")
    
    st.markdown("**Fields marked with * are required**")
    
    # Validation and next step
    if st.button("Next: Select Appointment Date & Time", use_container_width=True):
        # Basic validation
        if not name or not email or not phone or gender == "Select":
            st.error("Please fill in all required fields.")
        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")
        elif len(phone) < 10:
            st.error("Please enter a valid phone number.")
        else:
            # Save to session state
            st.session_state.patient_info = {
                "name": name,
                "email": email,
                "phone": phone,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "existing_conditions": existing_conditions,
                "additional_notes": additional_notes
            }
            st.session_state.appointment_step = 2
            st.rerun()
    
    # Return to main app
    if st.button("◀ Back to Diagnosis", use_container_width=True):
        st.switch_page("app.py")

# Step 2: Select Appointment Date and Time
elif st.session_state.appointment_step == 2:
    st.markdown("### 📅 Select Appointment Date")
    
    # Show patient info summary
    st.markdown(f"""
    <div class="appointment-card">
        <h3>Patient Information</h3>
        <p><strong>Name:</strong> {st.session_state.patient_info.get('name')}</p>
        <p><strong>Email:</strong> {st.session_state.patient_info.get('email')}</p>
        <p><strong>Phone:</strong> {st.session_state.patient_info.get('phone')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Date selection
    today = datetime.now().date()
    dates = [(today + timedelta(days=i)) for i in range(1, 15)]  # Next 14 days
    
    # Create a calendar-like display for dates
    st.markdown("**Select a date for your appointment:**")
    
    # Group dates into rows of 7 (weekly calendar view)
    date_rows = [dates[i:i+7] for i in range(0, len(dates), 7)]
    
    for row in date_rows:
        cols = st.columns(len(row))
        for i, date in enumerate(row):
            with cols[i]:
                date_str = date.strftime("%Y-%m-%d")
                day_name = date.strftime("%a")
                day_num = date.strftime("%d")
                month = date.strftime("%b")
                
                # Check if this date is selected
                is_selected = st.session_state.appointment_date == date_str
                
                # Create the clickable date card
                if st.button(
                    f"{day_name}\n{day_num} {month}", 
                    key=f"date_{date_str}",
                    use_container_width=True
                ):
                    st.session_state.appointment_date = date_str
                    st.session_state.appointment_time = None  # Reset time when date changes
                    st.rerun()
    
    # Time slot selection (only show if a date is selected)
    if st.session_state.appointment_date:
        st.markdown(f"### 🕒 Select Time Slot for {st.session_state.appointment_date}")
        
        # Morning slots (10 AM - 1 PM)
        st.markdown("**Morning Slots:**")
        morning_slots = ["10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM"]
        morning_cols = st.columns(len(morning_slots))
        
        for i, time_slot in enumerate(morning_slots):
            with morning_cols[i]:
                available = is_slot_available(st.session_state.appointment_date, time_slot)
                if available:
                    if st.button(time_slot, key=f"morning_{time_slot}", use_container_width=True):
                        st.session_state.appointment_time = time_slot
                        st.rerun()
                else:
                    st.button(time_slot, key=f"morning_{time_slot}", use_container_width=True, disabled=True)
        
        # Lunch break
        st.markdown("**Lunch Break (1:00 PM - 2:00 PM)**")
        
        # Afternoon slots (2 PM - 6 PM)
        st.markdown("**Afternoon Slots:**")
        afternoon_slots = ["2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"]
        
        # Create two rows for afternoon slots
        afternoon_row1 = afternoon_slots[:4]
        afternoon_row2 = afternoon_slots[4:]
        
        afternoon_cols1 = st.columns(len(afternoon_row1))
        for i, time_slot in enumerate(afternoon_row1):
            with afternoon_cols1[i]:
                available = is_slot_available(st.session_state.appointment_date, time_slot)
                if available:
                    if st.button(time_slot, key=f"afternoon1_{time_slot}", use_container_width=True):
                        st.session_state.appointment_time = time_slot
                        st.rerun()
                else:
                    st.button(time_slot, key=f"afternoon1_{time_slot}", use_container_width=True, disabled=True)
        
        afternoon_cols2 = st.columns(len(afternoon_row2))
        for i, time_slot in enumerate(afternoon_row2):
            with afternoon_cols2[i]:
                available = is_slot_available(st.session_state.appointment_date, time_slot)
                if available:
                    if st.button(time_slot, key=f"afternoon2_{time_slot}", use_container_width=True):
                        st.session_state.appointment_time = time_slot
                        st.rerun()
                else:
                    st.button(time_slot, key=f"afternoon2_{time_slot}", use_container_width=True, disabled=True)
        
        # Dinner break
        st.markdown("**Dinner Break (6:00 PM - 7:00 PM)**")
        
        # Evening slots (7 PM - 10 PM)
        st.markdown("**Evening Slots:**")
        evening_slots = ["7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM", "9:30 PM"]
        evening_cols = st.columns(len(evening_slots))
        
        for i, time_slot in enumerate(evening_slots):
            with evening_cols[i]:
                available = is_slot_available(st.session_state.appointment_date, time_slot)
                if available:
                    if st.button(time_slot, key=f"evening_{time_slot}", use_container_width=True):
                        st.session_state.appointment_time = time_slot
                        st.rerun()
                else:
                    st.button(time_slot, key=f"evening_{time_slot}", use_container_width=True, disabled=True)
    
    # Show the currently selected time and confirm button
    if st.session_state.appointment_time:
        st.success(f"Selected time: {st.session_state.appointment_time} on {st.session_state.appointment_date}")
        
        if st.button("Confirm Appointment", type="primary", use_container_width=True):
            st.session_state.appointment_step = 3
            st.rerun()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀ Back to Patient Information", use_container_width=True):
            st.session_state.appointment_step = 1
            st.rerun()
    with col2:
        if st.button("Cancel and Return to Diagnosis", use_container_width=True):
            st.switch_page("app.py")

# Step 3: Confirmation
elif st.session_state.appointment_step == 3:
    st.markdown("### ✅ Appointment Confirmation")
    
    # Check if we've already processed this confirmation
    if "appointment_processed" not in st.session_state or not st.session_state.appointment_processed:
        # Save the appointment
        appointment_data = {
            "patient_name": st.session_state.patient_info.get("name"),
            "email": st.session_state.patient_info.get("email"),
            "phone": st.session_state.patient_info.get("phone"),
            "age": st.session_state.patient_info.get("age"),
            "gender": st.session_state.patient_info.get("gender"),
            "height": st.session_state.patient_info.get("height"),
            "weight": st.session_state.patient_info.get("weight"),
            "existing_conditions": st.session_state.patient_info.get("existing_conditions"),
            "additional_notes": st.session_state.patient_info.get("additional_notes"),
            "date": st.session_state.appointment_date,
            "time_slot": st.session_state.appointment_time,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "confirmed"
        }
        
        # Save and get appointment ID
        appointment_id = save_appointment(appointment_data)
        appointment_data["id"] = appointment_id
        
        # Save the appointment ID to session state
        st.session_state.appointment_id = appointment_id
        
        # Generate email templates for display
        from email_utils import format_appointment_email, format_payment_email
        
        # Store the formatted emails in session state
        st.session_state.confirmation_email = format_appointment_email(appointment_data)
        st.session_state.payment_email = format_payment_email(appointment_data)
        
        # Set a flag to indicate we've processed this appointment
        st.session_state.appointment_processed = True
    else:
        # Retrieve appointment ID from session state
        appointment_id = st.session_state.appointment_id
    
    # Display confirmation message
    st.markdown(f"""
    <div class="success-message">
        <h3>✅ Your appointment has been confirmed!</h3>
        <p>Thank you for booking a teleconsultation with our medical professionals.</p>
        <p><strong>Appointment ID:</strong> {appointment_id}</p>
        <p><strong>Date:</strong> {st.session_state.appointment_date}</p>
        <p><strong>Time:</strong> {st.session_state.appointment_time}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show a preview of what's coming next
    st.markdown("""
    <div style="background-color:#E3F2FD; padding:15px; border-radius:8px; margin-top:20px;">
        <h4>What's Next?</h4>
        <ol>
            <li>You will receive a confirmation email with your appointment details (preview below).</li>
            <li>A payment link will be sent to complete your consultation fee.</li>
            <li>Once payment is confirmed, you will receive a teleconsultation link for your appointment.</li>
            <li>Please join 5 minutes before your scheduled time.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Display email previews in expandable sections
    if "confirmation_email" in st.session_state:
        with st.expander("📧 Preview: Appointment Confirmation Email", expanded=False):
            st.markdown(st.session_state.confirmation_email, unsafe_allow_html=True)
    
    if "payment_email" in st.session_state:
        with st.expander("💳 Preview: Payment Link Email", expanded=False):
            st.markdown(st.session_state.payment_email, unsafe_allow_html=True)
    
    # Offer options to return to app
    if st.button("Return to Home", type="primary", use_container_width=True):
        # Reset appointment state and go back to main page
        st.session_state.appointment_step = 1
        st.session_state.patient_info = {}
        st.session_state.appointment_date = None
        st.session_state.appointment_time = None
        st.session_state.appointment_processed = False
        if "appointment_id" in st.session_state:
            del st.session_state.appointment_id
        st.switch_page("app.py")

# Footer with disclaimer
st.markdown("---")
st.markdown("""
    <div style="color: #F44336; font-weight: bold;">
    ⚠️ Medical Disclaimer: This is a teleconsultation booking system. Please ensure all information is accurate.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #7F7F7F; font-size: 14px; margin-top: 20px;">
    © 2023 Multilingual Medical Assistant | Not for actual medical use | Educational purposes only
    </div>
""", unsafe_allow_html=True)
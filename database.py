import datetime
import json
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLite database
DATABASE_URL = "sqlite:///medical_assistant.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define data models
class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(10), nullable=False)
    transcript = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=False)  # JSON string of symptoms
    diagnosis = Column(Text, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    @property
    def symptoms_list(self):
        """Convert symptoms JSON string to list"""
        if self.symptoms:
            return json.loads(self.symptoms)
        return []

class MedicalData(Base):
    __tablename__ = "medical_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symptom_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    severity_level = Column(Integer, default=1)  # 1-5 scale
    common = Column(Boolean, default=True)
    treatments = Column(Text)  # JSON string of treatment options

# Create tables
Base.metadata.create_all(bind=engine)

# Database operations
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def save_consultation(language, transcript, symptoms_list, diagnosis, age=None, gender=None):
    """
    Save a consultation to the database
    
    Args:
        language (str): Language of the consultation
        transcript (str): User's symptom description
        symptoms_list (list): List of detected symptoms
        diagnosis (str): The diagnosis provided
        age (int, optional): Age of the patient
        gender (str, optional): Gender of the patient
    
    Returns:
        int: ID of the saved consultation
    """
    symptoms_json = json.dumps(symptoms_list)
    db = get_db()
    
    consultation = Consultation(
        language=language,
        transcript=transcript,
        symptoms=symptoms_json,
        diagnosis=diagnosis,
        age=age,
        gender=gender
    )
    
    try:
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        return consultation.id
    except Exception as e:
        db.rollback()
        print(f"Error saving consultation: {e}")
        return None
    finally:
        db.close()

def get_recent_consultations(limit=10):
    """
    Get most recent consultations
    
    Args:
        limit (int): Maximum number of records to return
    
    Returns:
        list: List of Consultation objects
    """
    db = get_db()
    try:
        return db.query(Consultation).order_by(Consultation.created_at.desc()).limit(limit).all()
    finally:
        db.close()

def get_consultation_by_id(consultation_id):
    """
    Get a consultation by ID
    
    Args:
        consultation_id (int): ID of the consultation
    
    Returns:
        Consultation: The consultation object or None
    """
    db = get_db()
    try:
        return db.query(Consultation).filter(Consultation.id == consultation_id).first()
    finally:
        db.close()

def get_consultations_by_symptom(symptom):
    """
    Get consultations containing a specific symptom
    
    Args:
        symptom (str): Symptom to search for
    
    Returns:
        list: List of Consultation objects
    """
    db = get_db()
    try:
        # This is inefficient but works for a simple SQLite database
        consultations = db.query(Consultation).all()
        return [c for c in consultations if symptom in c.symptoms_list]
    finally:
        db.close()

def initialize_medical_data(symptoms_data):
    """
    Initialize medical data in the database
    
    Args:
        symptoms_data (dict): Dictionary of symptom data
    """
    db = get_db()
    try:
        # Check if data already exists
        if db.query(MedicalData).count() > 0:
            return
        
        # Add each symptom to the database
        for symptom_name, description in symptoms_data.items():
            data = MedicalData(
                symptom_name=symptom_name,
                description=description,
                treatments=json.dumps(["Rest", "Hydration", "Consult doctor if persistent"])
            )
            db.add(data)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing medical data: {e}")
    finally:
        db.close()
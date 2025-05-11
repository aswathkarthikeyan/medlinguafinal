import streamlit as st
from datetime import datetime

def format_appointment_email(appointment_data):
    """
    Format appointment confirmation email content
    
    Args:
        appointment_data (dict): Dictionary containing appointment details
    
    Returns:
        str: HTML formatted email content
    """
    # Format appointment date/time for display
    appointment_date = datetime.strptime(appointment_data["date"], "%Y-%m-%d").strftime("%A, %B %d, %Y")
    appointment_time = appointment_data["time_slot"]
    
    # Email body with HTML formatting
    email_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
        <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">Appointment Confirmation</h1>
        </div>
        <div style="padding: 20px; background-color: #f9f9f9;">
            <p>Dear {appointment_data["patient_name"]},</p>
            
            <p>Thank you for booking a teleconsultation with our medical professionals. Your appointment has been confirmed.</p>
            
            <div style="background-color: #f0f0f0; padding: 15px; border-left: 4px solid #4CAF50; margin: 15px 0;">
                <h3>Appointment Details:</h3>
                <p><strong>Appointment ID:</strong> {appointment_data["id"]}</p>
                <p><strong>Date:</strong> {appointment_date}</p>
                <p><strong>Time:</strong> {appointment_time}</p>
            </div>
            
            <h3>What to Expect:</h3>
            <p>A payment link will be sent to you separately. After your payment is confirmed, you will receive a secure link to join the teleconsultation.</p>
            
            <h3>Preparation Tips:</h3>
            <ul>
                <li>Join the consultation 5 minutes before your scheduled time</li>
                <li>Ensure you have a stable internet connection</li>
                <li>Be in a quiet, well-lit place for better communication</li>
                <li>Have a list of your current medications ready</li>
                <li>Write down any questions or concerns you want to discuss</li>
            </ul>
            
            <p>If you need to reschedule or cancel your appointment, please contact us at least 24 hours before your appointment time.</p>
            
            <p>We look forward to providing you with excellent care!</p>
            
            <p>Best regards,<br>
            Medical Consultation Team</p>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f5f5f5; color: #777; font-size: 12px; border-radius: 0 0 10px 10px;">
            <p>This is an automated message.</p>
            <p>© 2025 Multilingual Medical Assistant | All rights reserved</p>
        </div>
    </div>
    """
    
    return email_content

def format_payment_email(appointment_data):
    """
    Format payment link email content
    
    Args:
        appointment_data (dict): Dictionary containing appointment details
    
    Returns:
        str: HTML formatted email content
    """
    # Format appointment date for payment email
    appointment_date = datetime.strptime(appointment_data["date"], "%Y-%m-%d").strftime("%A, %B %d, %Y")
    
    # Payment link (in a real scenario, this would be a link to a payment gateway)
    payment_link = f"#payment-link-{appointment_data['id']}"
    
    # Email body with HTML formatting
    email_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
        <div style="background-color: #2196F3; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0;">Complete Your Payment</h1>
        </div>
        <div style="padding: 20px; background-color: #f9f9f9;">
            <p>Dear {appointment_data["patient_name"]},</p>
            
            <p>Thank you for booking your teleconsultation. To confirm your appointment, please complete the payment using the secure link below.</p>
            
            <div style="background-color: #f0f0f0; padding: 15px; border-left: 4px solid #2196F3; margin: 15px 0;">
                <h3>Payment Details:</h3>
                <p><strong>Appointment ID:</strong> {appointment_data["id"]}</p>
                <p><strong>Date:</strong> {appointment_date}</p>
                <p><strong>Time:</strong> {appointment_data["time_slot"]}</p>
                
                <div style="font-size: 24px; font-weight: bold; color: #333; text-align: center; margin: 20px 0;">
                    Amount: $50.00
                </div>
            </div>
            
            <p style="text-align: center;">
                <a href="{payment_link}" style="display: inline-block; background-color: #2196F3; color: white; padding: 12px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 15px;">Complete Payment</a>
            </p>
            
            <p><strong>Why payment is required:</strong> Your payment confirms your appointment slot and helps us maintain our teleconsultation services.</p>
            
            <p><strong>What happens next:</strong> After your payment is confirmed, you will receive a separate email with a secure link to join your teleconsultation at the scheduled time.</p>
            
            <p>If you have any questions about the payment process, please contact our support team.</p>
            
            <p>Best regards,<br>
            Medical Consultation Team</p>
        </div>
        <div style="text-align: center; padding: 10px; background-color: #f5f5f5; color: #777; font-size: 12px; border-radius: 0 0 10px 10px;">
            <p>This is an automated message.</p>
            <p>© 2025 Multilingual Medical Assistant | All rights reserved</p>
        </div>
    </div>
    """
    
    return email_content
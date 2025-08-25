import streamlit as st
import re
import time
import random
import pandas as pd
from datetime import datetime, date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import json

# Configure the page
st.set_page_config(
    page_title="LGL Employee Helper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple CSS styling - basic version
st.markdown("""
<style>
    .main-header {
        background-color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Employee Database - Sample Data for Leave Tracking
EMPLOYEE_DATA = {
    'loyed': {
        'name': 'Loyed',
        'department': 'Logistics',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP001',
        'join_date': '2023-01-15',
        'contract_type': 'Unlimited',
        'position': 'Logistics Coordinator',
        'annual_leave_taken': 10,
        'sick_leave_taken': 2,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 1.8
    },
    'eva': {
        'name': 'Eva',
        'department': 'Commercial Services',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP002',
        'join_date': '2022-08-10',
        'contract_type': 'Unlimited',
        'position': 'Commercial Services Specialist',
        'annual_leave_taken': 12,
        'sick_leave_taken': 3,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 2.3
    },
    'jaq': {
        'name': 'Jaq',
        'department': 'Commercial Sales',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP003',
        'join_date': '2024-01-20',
        'contract_type': 'Limited',
        'position': 'Sales Executive',
        'annual_leave_taken': 5,
        'sick_leave_taken': 7,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 0.7
    },
    'rajeev': {
        'name': 'Rajeev',
        'department': 'Vessel Operations',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP004',
        'join_date': '2021-05-03',
        'contract_type': 'Unlimited',
        'position': 'Operations Manager',
        'annual_leave_taken': 4,
        'sick_leave_taken': 6,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 5,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 3.6
    },
    'sarah': {
        'name': 'Sarah',
        'department': 'Human Resources',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP005',
        'join_date': '2020-11-12',
        'contract_type': 'Unlimited',
        'position': 'HR Manager',
        'annual_leave_taken': 8,
        'sick_leave_taken': 1,
        'maternity_leave_taken': 45,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 3,
        'probation_completed': True,
        'years_of_service': 4.1
    },
    'ahmed': {
        'name': 'Ahmed',
        'department': 'Finance',
        'approval_manager': 'Alistar Concessio',
        'employee_id': 'EMP006',
        'join_date': '2023-09-01',
        'contract_type': 'Limited',
        'position': 'Financial Analyst',
        'annual_leave_taken': 6,
        'sick_leave_taken': 0,
        'maternity_leave_taken': 0,
        'parental_leave_taken': 0,
        'bereavement_leave_taken': 0,
        'probation_completed': True,
        'years_of_service': 1.3
    }
}

def calculate_leave_entitlements(employee_data):
    """Calculate leave entitlements based on employee data and handbook policies"""
    years_of_service = employee_data['years_of_service']
    probation_completed = employee_data['probation_completed']
    
    # Annual Leave Calculation
    if years_of_service >= 1:
        annual_leave_entitlement = 22  # Subsequent years
    else:
        annual_leave_entitlement = 20  # First year
    
    # Sick Leave Calculation (only after probation)
    if probation_completed:
        sick_leave_entitlement = 90  # 90 calendar days per year
    else:
        sick_leave_entitlement = 0
    
    # Other leave entitlements
    maternity_leave_entitlement = 60
    parental_leave_entitlement = 5
    bereavement_leave_entitlement = 5
    
    return {
        'annual_leave': {
            'entitlement': annual_leave_entitlement,
            'taken': employee_data['annual_leave_taken'],
            'remaining': annual_leave_entitlement - employee_data['annual_leave_taken']
        },
        'sick_leave': {
            'entitlement': sick_leave_entitlement,
            'taken': employee_data['sick_leave_taken'],
            'remaining': sick_leave_entitlement - employee_data['sick_leave_taken']
        },
        'maternity_leave': {
            'entitlement': maternity_leave_entitlement,
            'taken': employee_data['maternity_leave_taken'],
            'remaining': maternity_leave_entitlement - employee_data['maternity_leave_taken']
        },
        'parental_leave': {
            'entitlement': parental_leave_entitlement,
            'taken': employee_data['parental_leave_taken'],
            'remaining': parental_leave_entitlement - employee_data['parental_leave_taken']
        },
        'bereavement_leave': {
            'entitlement': bereavement_leave_entitlement,
            'taken': employee_data['bereavement_leave_taken'],
            'remaining': bereavement_leave_entitlement - employee_data['bereavement_leave_taken']
        }
    }

def generate_email_alternatives(form_type, employee_name, manager_name, form_data):
    """Generate multiple email alternatives for form submission"""
    email_subject = f"{form_type} Request - {employee_name}"
    
    # Simple text email for copying
    text_email = f"""Subject: {email_subject}
To: concessioac@gmail.com

Dear {manager_name},

I would like to submit a {form_type} request with the following details:

📋 REQUEST DETAILS:
• Employee: {employee_name}
• Request Type: {form_type}
• Date Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
• Status: Pending Approval
"""
    
    # Add form-specific details
    for key, value in form_data.items():
        if key not in ['employee_name', 'manager_name', 'form_type']:
            formatted_key = key.replace('_', ' ').title()
            text_email += f"• {formatted_key}: {value}\n"
    
    text_email += f"""

Please review this request and let me know your decision.

Best regards,
{employee_name}

---
This request was generated by the LGL Employee Helper System
Alistar Personnel | 605, Park Avenue, Dubai Silicon Oasis
HR Contact: concessioac@gmail.com"""
    
    return {
        'subject': email_subject,
        'text_email': text_email,
        'manager_email': 'concessioac@gmail.com'
    }

# Main header - simple version
st.title("🤖 LGL Employee Helper")
st.subheader("Alistar's Personnel Employee Handbook")

# Employee Login Section
st.sidebar.title("👥 Employee Login")
st.sidebar.markdown("Select your name to access personalized features:")

employee_names = ['Select Employee'] + [emp_data['name'] for emp_data in EMPLOYEE_DATA.values()]
selected_employee = st.sidebar.selectbox(
    "Choose your name:",
    employee_names,
    index=0
)

if selected_employee != 'Select Employee':
    # Find employee data
    employee_key = None
    for key, data in EMPLOYEE_DATA.items():
        if data['name'] == selected_employee:
            employee_key = key
            break
    
    if employee_key:
        st.session_state.current_employee = employee_key
        st.session_state.employee_data = EMPLOYEE_DATA[employee_key]
        
        # Show employee info in sidebar
        emp_data = st.session_state.employee_data
        leave_balances = calculate_leave_entitlements(emp_data)
        
        st.sidebar.success(f"Welcome, {emp_data['name']}!")
        st.sidebar.markdown(f"""
        **💼 Employee Details:**
        • Department: {emp_data['department']}
        • Position: {emp_data['position']}
        • Manager: {emp_data['approval_manager']}
        • Service: {emp_data['years_of_service']} years
        
        **📅 Leave Balances:**
        • Annual: {leave_balances['annual_leave']['remaining']} days
        • Sick: {leave_balances['sick_leave']['remaining']} days
        """)
        
        # Quick leave request button
        st.sidebar.markdown("---")
        if st.sidebar.button("📧 Submit Leave Request", use_container_width=True):
            st.session_state.show_leave_form = True
else:
    st.session_state.current_employee = None
    st.session_state.employee_data = None
    st.sidebar.info("Please select your name to access personalized features.")

# Main content area
st.markdown("### 🚀 Quick Topics:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏖️ Annual Leave", help="Learn about annual leave policies"):
        st.markdown("### 📅 Annual Leave Policy")
        st.markdown("""
        **Annual Leave Entitlement:**
        • First Year: 20 working days (after probation)
        • Subsequent Years: 22 working days
        • Notice Required: Minimum twice the duration requested
        """)

with col2:
    if st.button("🏥 Sick Leave", help="Learn about sick leave policies"):
        st.markdown("### 🏥 Sick Leave Policy")
        st.markdown("""
        **Sick Leave Entitlement:**
        • Total: 90 calendar days after probation
        • Full Pay: First 15 days
        • Half Pay: Next 30 days
        • No Pay: Next 45 days
        """)

with col3:
    if st.button("⏰ Working Hours", help="Learn about working schedules"):
        st.markdown("### ⏰ Working Hours")
        st.markdown("""
        **Administrative Staff:**
        • Days: Monday – Friday
        • Hours: 9:00am – 6:00pm
        
        **Academic Staff:**
        • Flexible scheduling based on demand
        """)

# Leave request form
if 'show_leave_form' in st.session_state and st.session_state.show_leave_form and 'current_employee' in st.session_state:
    st.markdown("---")
    st.markdown("### 📧 Leave Request Form")
    
    emp_data = st.session_state.employee_data
    leave_balances = calculate_leave_entitlements(emp_data)
    
    with st.form("leave_request_form"):
        st.markdown(f"**Current Leave Balances:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Leave", f"{leave_balances['annual_leave']['remaining']} days")
        with col2:
            st.metric("Sick Leave", f"{leave_balances['sick_leave']['remaining']} days")
        with col3:
            st.metric("Maternity Leave", f"{leave_balances['maternity_leave']['remaining']} days")
        
        col1, col2 = st.columns(2)
        with col1:
            leave_type = st.selectbox("Leave Type:", 
                ['Annual Leave', 'Sick Leave', 'Maternity Leave', 'Parental Leave', 'Bereavement Leave'])
            start_date = st.date_input("Start Date:", min_value=date.today())
        
        with col2:
            end_date = st.date_input("End Date:", min_value=date.today())
            emergency_contact = st.text_input("Emergency Contact:", placeholder="Name and phone number")
        
        reason = st.text_area("Reason for Leave:", placeholder="Please provide a brief reason...")
        
        if st.form_submit_button("📧 Submit Leave Request", use_container_width=True):
            form_data = {
                'leave_type': leave_type,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days_requested': (end_date - start_date).days + 1,
                'reason': reason,
                'emergency_contact': emergency_contact
            }
            
            # Generate email
            email_options = generate_email_alternatives(
                "Leave Request",
                emp_data['name'],
                emp_data['approval_manager'],
                form_data
            )
            
            st.success("✅ Leave Request prepared successfully!")
            
            # Show email options
            st.markdown("### 📧 Send Your Request:")
            
            # Gmail link
            gmail_url = f"https://mail.google.com/mail/?view=cm&to={email_options['manager_email']}&subject={email_options['subject']}&body={urllib.parse.quote(email_options['text_email'])}"
            st.markdown(f'[📧 Send via Gmail]({gmail_url})')
            
            # Copy-paste option
            with st.expander("📋 Copy Email Content"):
                st.code(email_options['text_email'], language=None)
                st.info("Copy the text above and paste it into your email client.")

    if st.button("Close Form"):
        st.session_state.show_leave_form = False
        st.rerun()
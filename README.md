# LGL Employee Helper

A Streamlit-based employee handbook and leave management system for Alistar Personnel.

## Features

- **Employee Portal**: Personalized login system with employee data
- **Leave Management**: View leave balances and submit leave requests
- **Email Integration**: Generate and send leave requests via email
- **Handbook Information**: Quick access to company policies
- **User-Friendly Interface**: Simple, clean design for easy navigation

## Employee Database

The system includes sample data for 6 employees:
- Loyed (Logistics)
- Eva (Commercial Services)
- Jaq (Commercial Sales)
- Rajeev (Vessel Operations)
- Sarah (Human Resources)
- Ahmed (Finance)

## Leave Types Supported

- Annual Leave (20-22 days based on service)
- Sick Leave (90 days after probation)
- Maternity Leave (60 days)
- Parental Leave (5 days)
- Bereavement Leave (5 days)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lgl-HELPER
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. Push the code to a public GitHub repository
2. Connect your GitHub account to Streamlit Cloud
3. Deploy the app by selecting the repository and main file (app.py)
4. The app will be automatically deployed and accessible via a public URL

## File Structure

```
lgl-HELPER/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

1. **Select Employee**: Choose your name from the sidebar dropdown
2. **View Information**: See your leave balances and employee details
3. **Submit Requests**: Click "Submit Leave Request" to create a new request
4. **Send Email**: Use the generated email links to send your request to management

## Email System

The system generates properly formatted emails that can be sent via:
- Gmail (direct link)
- Copy & paste to any email client
- All emails are addressed to: concessioac@gmail.com

## System Requirements

- Python 3.7+
- Streamlit 1.28.0+
- Pandas 1.5.0+

## Support

For technical support or questions about the employee handbook, contact:
- HR Manager: concessioac@gmail.com
- System Administrator: [Your contact information]

---

**Alistar Personnel**  
605, Park Avenue, Dubai Silicon Oasis  
Employee Helper System v1.0
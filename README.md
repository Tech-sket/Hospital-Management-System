#  Hospital Management System
A Django-based Hospital Management System integrated with a serverless email service and Google Calendar API for real-time appointment scheduling and notifications.

## Setup and Run

1. create the repository
```bash
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system

2. Create virtual environment
python -m venv venv

Activate:

 for Windows

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables
Create .env file: and add 
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password

5. Apply migrations
python manage.py makemigrations
python manage.py migrate

6. Run Django server
python manage.py runserver

7. Run serverless email service (separate terminal)
cd email_service
serverless offline

8. Google Calendar setup
Enable Google Calendar API
Configure OAuth consent screen
Download credentials.json
Place it in project root

System Architecture

The system is built using a modular architecture consisting of three core components:

1. Django Application

The main backend handles:

User authentication and role management (Doctor / Patient)
Appointment booking system
Doctor availability slot management
Database operations using Django ORM

Role-based access control:

Doctors can manage availability slots and view appointments
Patients can view doctors and book appointments

2. Serverless Email Service
A separate microservice handles all email notifications.

Flow:

Django sends HTTP request to serverless API
Serverless function processes request
SMTP (Gmail) sends email

Responsibilities:
Signup welcome emails
Appointment confirmation emails

This separation ensures the main Django server is not blocked by email processing.

3. Google Calendar Integration

Google Calendar is integrated using OAuth 2.0.

Flow:

Doctor connects Google account via OAuth
Access and refresh tokens are stored
When appointment is booked:
Calendar event is automatically created
Event contains doctor, patient, date, and time

This ensures real-time synchronization between hospital system and Google Calendar.


*The Design Decision

Decision: Serverless Email Service vs Direct Django Email (SMTP)

Option 1: Django SMTP Integration
Email sent directly from Django using SMTP
Simple implementation
Tightly coupled with backend

Option 2: Serverless Email Service (Chosen)
Email handled by separate serverless function
Django communicates via HTTP API

Reason for Choosing Serverless Approach:

1)Decouples email system from core backend
2)Prevents request blocking in Django
3)Allows independent scaling of email service
4)Improves system modularity
5)Mimics real-world microservice architecture

Limitations
1. Google OAuth is in testing mode
Only approved test users can log in
Requires manual configuration in Google Cloud Console

2. Email service is not production-grade
Uses SMTP (Gmail) with basic setup
No retry mechanism for failed emails
No queue or background worker system

3. No asynchronous task handling
Email and calendar requests are synchronous
Can cause delay under heavy load

4. Limited scalability
Single database design (no multi-hospital support)
No tenant-based architecture

5. No monitoring or logging system
Email delivery status is not tracked in database
No analytics for system performance

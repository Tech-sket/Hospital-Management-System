import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email, subject, body):
    """Send email via Gmail SMTP"""

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        raise Exception("SMTP credentials not set in environment variables")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = None
    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

        print(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        raise Exception("SMTP Authentication failed. Use Gmail App Password.")

    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error: {str(e)}")

    finally:
        if server:
            try:
                server.quit()
            except:
                pass


def send_email_handler(event, context):
    """Serverless entry point"""

    try:
        body = json.loads(event.get("body", "{}"))

        email_type = body.get("type")
        recipient = body.get("email")
        name = body.get("name", "")


        if not recipient:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Email is required"
                })
            }

        # SIGNUP EMAIL
        if email_type == "SIGNUP_WELCOME":
            subject = "Welcome to Hospital Manager"
            message = f"""
Hello {name},

Welcome to our Hospital Management System.
You can now log in and manage appointments.

Thank you,
Hospital Team
"""
            send_email(recipient, subject, message)

        # BOOKING EMAIL
        elif email_type == "BOOKING_CONFIRMATION":
            doctor_name = body.get("doctor_name", "Doctor")
            date = body.get("date", "Unknown date")
            time = body.get("time", "Unknown time")

            subject = f"Appointment Confirmed with Dr. {doctor_name}"
            message = f"""
Hello {name},

Your appointment is confirmed:

Doctor: {doctor_name}
Date: {date}
Time: {time}

Thank you,
Hospital Team
"""
            send_email(recipient, subject, message)

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": f"Unknown email type: {email_type}"
                })
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully"
            })
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid JSON in request body"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
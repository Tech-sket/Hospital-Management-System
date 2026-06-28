import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your credentials
SMTP_EMAIL ="siddheshp749@gmail.com"
SMTP_PASSWORD = "taycjppozgdvpbrx"

msg = MIMEMultipart()
msg["From"] = SMTP_EMAIL
msg["To"] = "siddpatel933@gmail.com"  # send to yourself
msg["Subject"] = "Test from Hospital Manager"
msg.attach(MIMEText("This is a test email.", "plain"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ SMTP Error: {e}")

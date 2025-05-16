# Importing necessary libraries
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

# List of recipient email addresses
recipient_emails = [
    "vickykawadkar779@gmail.com"
]

# Email subject and body
subject = "Test Email from Python"
body = "Hello, this is a test email from Python!"

# Creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# Start TLS for security
s.starttls()

try:
    # Authentication
    s.login(sender_email, password)

    # Message format
    message = f"Subject: {subject}\n\n{body}"

    # Sending the mail to multiple recipients
    for recipient in recipient_emails:
        s.sendmail(sender_email, recipient, message)
        print(f"Email sent to {recipient}")

    print("All emails sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Terminating the session
    s.quit()

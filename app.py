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

# Email subject and enhanced HTML body
subject = "Get a Project Collaboration"
body = '''
<html>
<head>
<style>
    .btn {
        background-color: #FF5722;
        color: white;
        padding: 14px 28px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 10px;
        margin-top: 15px;
        transition: background-color 0.3s ease;
        font-size: 16px;
        font-weight: bold;
    }
    .btn:hover {
        background-color: #E64A19;
    }
    .container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
        max-width: 600px;
        margin: auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h2 {
        color: #FF5722;
    }
</style>
</head>
<body>
<div class="container">
    <h2>Get a Project Collaboration</h2>
    <p>Hello,<br><br>I hope this message finds you well. I am reaching out to discuss potential project collaboration opportunities. I believe that with my skills and experience, we could work together to achieve great results. Please let me know if you would be open to discussing this further.</p>
    <p>Looking forward to your response.<br>Best regards,<br>[Your Name]</p>
    <img src="https://img.freepik.com/free-vector/night-ocean-landscape-full-moon-stars-shine_107791-7397.jpg" alt="Profile Picture" style="border-radius: 50%; width: 100px; height: 100px;">
    <br>
    <a href="https://www.example.com" class="btn">View My Portfolio</a>
</div>
</body>
</html>
'''

# Creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# Start TLS for security
s.starttls()

try:
    # Authentication
    s.login(sender_email, password)

    # Message format
    message = f"Subject: {subject}\nContent-Type: text/html\n\n{body}"

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

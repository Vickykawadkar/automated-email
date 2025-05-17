import streamlit as st
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Load environment variables
load_dotenv()

# Get email credentials from environment variables
sender_email = os.getenv("SENDER_EMAIL")

# Custom CSS for modern and impactful UI
st.markdown(
    '''
    <style>
    .main {
        background-color: #121212;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 40px;
    }
    .btn-confirm {
        background-color: #ff5722;
        color: white;
        font-size: 22px;
        font-weight: 900;
        padding: 15px 0;
        width: 100%;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 20px;
    }
    .btn-confirm:hover {
        background-color: #e64a19;
    }
    .portfolio-btn {
        background-color: #ff5722;
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 20px 0;
        font-size: 18px;
    }
    .portfolio-btn:hover {
        background-color: #e64a19;
    }
    </style>
    ''',
    unsafe_allow_html=True,
)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("Automated Email Sender")

# Display sender email
st.text_input("Sender Email", value=sender_email or "", disabled=True)

# Input multiple email addresses
recipient_emails = st.text_area("Enter Recipient Emails (comma-separated)")
recipients = [email.strip() for email in recipient_emails.split(",") if email.strip()]

# GitHub portfolio link
portfolio_link = st.text_input("Enter GitHub Portfolio Link")

# Upload an image for the email
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if st.button("SEND EMAILS", key="send_btn", help="Click to send emails"):
    if not sender_email:
        st.error("Sender email not set in .env file")
    elif not recipients:
        st.error("No recipients to send emails")
    else:
        try:
            for r in recipients:
                # Create message container
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = r
                msg['Subject'] = "Exciting Project Collaboration"

                # Email body
                body = f'''<html>
<body style='font-family:Segoe UI; color:#333;'>
<h2 style='color:#ff5722; font-size:28px;'>Exciting Project Collaboration</h2>
<p><b>Hello,</b><br><br><b>I hope this message finds you well. I am reaching out to discuss potential project collaboration opportunities. I believe that with my skills and experience, we could work together to achieve great results. Please let me know if you would be open to discussing this further.</b></p>
<p><b>Looking forward to your response.<br>Best regards,<br>[Your Name]</b></p>'''

                # Add portfolio link if provided
                if portfolio_link:
                    body += f'''<br><a href='{portfolio_link}' class='portfolio-btn'>View My Portfolio</a>'''

                # Attach the HTML body
                msg.attach(MIMEText(body, 'html'))

                # Attach image if uploaded
                if uploaded_image is not None:
                    image_data = uploaded_image.read()
                    image = MIMEImage(image_data)
                    image.add_header('Content-Disposition', 'attachment', filename=uploaded_image.name)
                    msg.attach(image)

                # SMTP session
                with smtplib.SMTP('smtp.gmail.com', 587) as s:
                    s.starttls()
                    s.login(sender_email, os.getenv("PASSWORD"))
                    s.send_message(msg)
                    st.success(f"Email sent to {r}")

            st.success("All emails sent successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get email credentials from environment variables
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

# Load recipients from file automatically
def load_recipients():
    recipients = []
    try:
        with open("recipients.txt", "r") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        recipients = []
    return recipients

recipients = load_recipients()

# Custom CSS for strong background and bold text
st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 40px;
    }
    .stTextInput>div>div>input[readonly] {
        background-color: #333 !important;
        color: #eee !important;
        font-weight: bold;
    }
    .recipients {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        max-height: 200px;
        overflow-y: auto;
        font-weight: bold;
        font-size: 16px;
    }
    .btn-confirm {
        background-color: #ff5722;
        color: white;
        font-size: 20px;
        font-weight: 900;
        padding: 15px 0;
        width: 100%;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .btn-confirm:hover {
        background-color: #e64a19;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("Automated Email Sender")

# Show sender email and password readonly
st.text_input("Sender Email", value=sender_email or "", disabled=True)
st.text_input("Password", value=password or "", disabled=True, type="password")

st.markdown("### Recipient Emails")
if recipients:
    st.markdown(f'<div class="recipients">{"<br>".join(recipients)}</div>', unsafe_allow_html=True)
else:
    st.warning("No recipients found in recipients.txt")

if st.button("CONFIRM & SEND", key="send_btn", help="Click to send emails"):
    if not sender_email or not password:
        st.error("Sender email or password not set in .env file")
    elif not recipients:
        st.error("No recipients to send emails")
    else:
        try:
            # Email details
            subject = "Get a Project Collaboration"
            body = """
            <html>
            <body style='font-family:Segoe UI; color:#333;'>
            <h2 style='color:#ff5722;'>Get a Project Collaboration</h2>
            <p>Hello,<br><br>I hope this message finds you well. I am reaching out to discuss potential project collaboration opportunities. I believe that with my skills and experience, we could work together to achieve great results. Please let me know if you would be open to discussing this further.</p>
            <p>Looking forward to your response.<br>Best regards,<br>[Your Name]</p>
            <img src='https://img.freepik.com/free-vector/night-ocean-landscape-full-moon-stars-shine_107791-7397.jpg' alt='Profile Picture' style='border-radius: 50%; width: 100px; height: 100px;'>
            <br>
            <a href='https://www.example.com' style='
                background-color:#ff5722; color:white; padding:10px 20px; border-radius:10px; text-decoration:none; font-weight:bold;'>View My Portfolio</a>
            </body>
            </html>
            """
            message = f"Subject: {subject}\nContent-Type: text/html\n\n{body}"

            # SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_email, password)

            for r in recipients:
                s.sendmail(sender_email, r, message)
                st.success(f"Email sent to {r}")

            s.quit()
            st.success("All emails sent successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

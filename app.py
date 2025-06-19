import streamlit as st
import pandas as pd
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Load credentials
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")

# Custom CSS for premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, .main {
        background-color: #0f0f0f;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        animation: fadeIn 1.5s ease;
    }

    h1 {
        color: #ff5722;
        font-size: 42px;
        margin-bottom: 30px;
        font-weight: 800;
    }

    .stTextArea label,
    .stFileUploader label {
        font-size: 18px;
        font-weight: 600;
        color: #e0e0e0;
    }

    .stTextArea textarea,
    .stFileUploader input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px;
    }

    .stButton button {
        background-color: #ff5722;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 30px;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #e64a19;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
</style>
""", unsafe_allow_html=True)

st.title("📧 Bulk Email Sender")

# Upload Excel
excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Message box
custom_message = st.text_area("Write Your Message", height=200)

# Optional image
uploaded_image = st.file_uploader("Upload an Image (optional)", type=["jpg", "jpeg", "png"])

# Send button
if st.button("📨 Send Emails"):
    if not sender_email or not password:
        st.error("Sender email or password missing in .env")
    elif not excel_file:
        st.error("Please upload an Excel file")
    elif not custom_message.strip():
        st.error("Please enter a message to send")
    else:
        try:
            df = pd.read_excel(excel_file)

            if 'Name' not in df.columns or 'Email' not in df.columns:
                st.error("Excel must have 'Name' and 'Email' columns")
            else:
                success_count = 0
                with smtplib.SMTP('smtp.gmail.com', 587) as s:
                    s.starttls()
                    s.login(sender_email, password)

                    for _, row in df.iterrows():
                        name = str(row['Name'])
                        receiver_email = str(row['Email'])

                        # Replace [Name] and add signature
                        personalized_msg = custom_message.replace("[Name]", name)
                        personalized_msg += "<br><br><b>Best regards,<br>Vicky Kawadkar</b>"

                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = "Exciting Project Collaboration"

                        msg.attach(MIMEText(personalized_msg, 'html'))

                        if uploaded_image:
                            image_data = uploaded_image.read()
                            image = MIMEImage(image_data)
                            image.add_header('Content-Disposition', 'attachment', filename=uploaded_image.name)
                            msg.attach(image)

                        s.send_message(msg)
                        success_count += 1
                        st.success(f"✅ Sent to {name} ({receiver_email})")

                st.success(f"🎉 All {success_count} emails sent successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

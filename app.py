import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import mimetypes

# ---------------- Custom CSS ----------------
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
        color: #E5315F;
        font-size: 42px;
        margin-bottom: 30px;
        font-weight: 800;
    }

    .stTextArea label,
    .stFileUploader label,
    .stTextInput label {
        font-size: 18px;
        font-weight: 600;
        color: #e0e0e0;
    }

    .stTextArea textarea,
    .stFileUploader input,
    .stTextInput input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px;
    }

    .stButton button {
        background-color: #E5315F !important;
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 30px;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
    }

    /* Eye button in sidebar password input */
    section[data-testid="stSidebar"] input[type="password"] + div button {
        background-color: #E5315F !important;
        color: white !important;
        border: none !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        margin-left: 10px !important;
        margin-top: 1px !important;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.header("📨 Sender Credentials")
sender_email = st.sidebar.text_input("Sender Email")
password = st.sidebar.text_input("App Password", type="password")

# ---------------- Title ----------------
st.markdown("""
<h1 style='text-align: center; color: #E5315F; font-size: 48px; font-weight: 800;'>
📧 Bulk Email Sender
</h1>
""", unsafe_allow_html=True)

# ---------------- Main Inputs ----------------
excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])
subject = st.text_input("Enter Email Subject", value="")
custom_message = st.text_area("Write Your Message", height=200)
uploaded_image = st.file_uploader("Upload an Image (optional)", type=["jpg", "jpeg", "png"])
uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

# ---------------- Email Sending Logic ----------------
if st.button("📨 Send Emails"):
    if not sender_email or not password:
        st.error("Please enter sender email and password in the sidebar.")
    elif not excel_file:
        st.error("Please upload an Excel file")
    elif not subject.strip():
        st.error("Please enter a subject")
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

                        # Preserve spacing and line breaks
                        msg_raw = custom_message.replace("[Name]", name)
                        msg_html = msg_raw.replace("  ", "&nbsp;&nbsp;").replace("\n", "<br>")

                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(msg_html, 'html'))

                        # Attach image if provided
                        if uploaded_image:
                            uploaded_image.seek(0)
                            image_data = uploaded_image.read()
                            mime_type, _ = mimetypes.guess_type(uploaded_image.name)
                            if mime_type and mime_type.startswith("image/"):
                                subtype = mime_type.split("/")[1]
                                image = MIMEImage(image_data, _subtype=subtype)
                                image.add_header('Content-Disposition', 'attachment', filename=uploaded_image.name)
                                msg.attach(image)
                            else:
                                st.warning(f"⚠️ Skipping image: Could not determine image type for {uploaded_image.name}")

                        # Attach resume PDF if provided
                        if uploaded_resume:
                            uploaded_resume.seek(0)
                            resume_data = uploaded_resume.read()
                            resume = MIMEApplication(resume_data, _subtype='pdf')
                            resume.add_header('Content-Disposition', 'attachment', filename=uploaded_resume.name)
                            msg.attach(resume)

                        s.send_message(msg)
                        success_count += 1
                        st.success(f"✅ Sent to {name} ({receiver_email})")

                st.success(f"🎉 All {success_count} emails sent successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

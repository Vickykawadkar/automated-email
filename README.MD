
# 📧 Bulk Email Sender App

A modern, customizable bulk email sender built with **Streamlit**. It supports dynamic message personalization, attachments (image & PDF), and is styled with a sleek dark UI. Ideal for outreach campaigns, resumes, and announcements.

---

## 🚀 Features

- ✅ Upload Excel with names and emails
- ✍️ Personalize messages using `[Name]` placeholder
- 📎 Attach image and resume files
- 🎨 Premium UI (dark theme, custom font, animations)
- 📬 Send via Gmail using SMTP
- ☁️ Deploy on **Render** (free or paid)


---

## 📁 Project Structure

```

email-sender-app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # (Optional) Local credentials file

````

---

## 🛠️ Setup Locally

### 1. Clone the Repo

```bash
git clone https://github.com/Vickykawadkar/automated-email
cd automated-email
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

```env
SENDER_EMAIL=your_email@gmail.com
PASSWORD=your_app_password
```

> Make sure to generate an **App Password** if you're using Gmail with 2FA.

### 4. Run App

```bash
streamlit run app.py
```

---

## ☁️ Deployment on Render

1. Push this project to GitHub.
2. Go to [https://render.com](https://render.com) → New Web Service
3. Connect your GitHub repo.
4. Configure:

   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add Environment Variables:

   * `SENDER_EMAIL`
   * `PASSWORD`

---

## 📌 Excel Format

Your uploaded `.xlsx` file should have:

| Name     | Email                                                     |
| -------- | --------------------------------------------------------- |
| Vicky    | [vickykawadkar@gmail.com](mailto:vickykawadkar@gmail.com) |
| John Doe | [johndoe@example.com](mailto:johndoe@example.com)         |

---

## 💡 Message Personalization

Use `[Name]` inside your message box. Example:

```text
Hello [Name],

Hope you're doing well. Here's my resume for your reference.

Regards,  
Vicky Kawadkar
```

---

## 🔐 Security Notes

* Never expose `.env` or real credentials in public repositories.
* Use Gmail **App Passwords** instead of regular ones.
* Always validate email lists before sending.

---

## 📃 License

MIT License – free to use, modify, and distribute.

---

## 👨‍💻 Author

**Vicky Kawadkar**
[Portfolio](https://github.com/Vickykawadkar)





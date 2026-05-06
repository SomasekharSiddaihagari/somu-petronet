# def send_email(to_email: str, subject: str, body: str):
#     """
#     Generic reusable email sender.
#     Configure your SMTP credentials in .env
#     """
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()

#     import smtplib
#     from email.mime.text import MIMEText
#     from email.mime.multipart import MIMEMultipart

#     SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
#     SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
#     SMTP_USER = os.getenv("SMTP_USER")
#     SMTP_PASS = os.getenv("SMTP_PASS")
#     SMTP_EMAIL = os.getenv("SMTP_EMAIL")


#     try:
#         msg = MIMEMultipart()
#         msg["From"] = SMTP_EMAIL
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         #  Use plain text (safer)
#         msg.attach(MIMEText(body, "plain"))
#         print("reached here bro")
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASS)
#             server.send_message(msg)

#         print(f"📧 Email sent to {to_email}: {subject}")

#     except Exception as e:
#         print(f" Failed to send email to {to_email}: {e}")


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_name: str | None = None,   # ✅ optional, backward compatible
):
    import os
    from dotenv import load_dotenv
    load_dotenv()

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import formataddr

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")

    try:
        msg = MIMEMultipart()

        # ✅ Preserve old logic + add flexibility
        sender_name = from_name or "Petronet"
        sender_email = SMTP_EMAIL or SMTP_USER

        msg["From"] = formataddr((sender_name, sender_email))
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        print(f"📧 Email sent to {to_email}: {subject}")

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
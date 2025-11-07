import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  # expects .env in project root

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASSWORD")

class EmailSender:
    def __init__(self):
        self.host = SMTP_HOST
        self.port = SMTP_PORT
        self.user = SMTP_USER
        self.password = SMTP_PASS

    def send_email(self, to_email, subject, body, attachments=[]):
        msg = EmailMessage()
        msg["From"] = self.user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        for path in attachments:
            if not path or not os.path.exists(path):
                continue
            with open(path, "rb") as f:
                data = f.read()
                import mimetypes
                mtype, _ = mimetypes.guess_type(path)
                if mtype:
                    maintype, subtype = mtype.split("/", 1)
                else:
                    maintype, subtype = ("application", "octet-stream")
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))

        with smtplib.SMTP_SSL(self.host, self.port) as s:
            s.login(self.user, self.password)
            s.send_message(msg)
        print("Email sent to", to_email)

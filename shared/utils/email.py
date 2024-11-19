import resend
from decouple import config

resend.api_key = config("RESEND_API_KEY")


def send_resend_email(subject: str, recipient: str, html: str):
    params: resend.Emails.SendParams = {
        "from": config("RESEND_HOST"),
        "to": [recipient],
        "subject": subject,
        "html": html,
    }
    resend.Emails.send(params)

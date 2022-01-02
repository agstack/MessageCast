import smtplib
import ssl

from AgStackRegistry.local_settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SSL_PORT


def send_email(message: str, user):
    receiver_email = user.email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, SSL_PORT, context=context) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, receiver_email, message)

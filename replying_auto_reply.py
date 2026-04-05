from gmail_auth import get_gmail_service
import base64
from email.mime.text import MIMEText

def send_email_reply(receiver_email: str, subject: str, reply_body: str, thread_id: str, message_id: str = None):
    service = get_gmail_service()

    # Construct the email
    message = MIMEText(reply_body)
    message['to'] = receiver_email
    message['subject'] = f"Re: {subject}"
    if message_id:
        message['In-Reply-To'] = message_id
        message['References'] = message_id

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message_data = {
        'raw': raw_message,
        'threadId': thread_id
    }

    try:
        sent_message = service.users().messages().send(userId='me', body=message_data).execute()
        print(f"✅ Reply sent to {receiver_email} in thread {thread_id}")
        return sent_message
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None

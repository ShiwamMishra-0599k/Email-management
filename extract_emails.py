from gmail_auth import get_gmail_service
import base64

def decode_base64(data):
    try:
        return base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
    except Exception as e:
        return ""

def extract_body(payload):
    
    if payload.get('mimeType') == 'text/plain' and payload.get('body', {}).get('data'):
        return decode_base64(payload['body']['data'])

    if 'parts' in payload:
        for part in payload['parts']:
            result = extract_body(part)
            if result:
                return result
    return ""

def get_full_email_content():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])

    email_list = []

    for msg in messages:
        msg_id = msg['id']
        full_msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        payload = full_msg.get('payload', {})
        headers = payload.get('headers', [])

        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '(Unknown Sender)')
        message_id = next((h['value'] for h in headers if h['name'].lower() == 'message-id'), None)
        thread_id = full_msg.get("threadId", None)

        body = extract_body(payload).strip()

        email_list.append({
            'email_id': msg_id,           
            'thread_id': thread_id,        
            'message_id': message_id,      
            'from': sender,
            'subject': subject,
            'body': body
        })

    return email_list

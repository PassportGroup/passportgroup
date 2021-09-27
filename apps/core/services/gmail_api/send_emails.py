# for getting full paths to attachements
import os
# for encoding messages in base64
from base64 import urlsafe_b64encode
# for dealing with attachments MIME types
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type


# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


def build_message(message_data):

    template = """
שלום רב,    
מוגשת לכם בזאת בקשה לקבלת תעודת צאצא בשם    
בכל שאלה או הבהרה ניתן לפנות אליי.    
בכבוד רב ובברכה,    
    """

    message = MIMEMultipart()
    message['to'] = message_data['to']
    message['from'] = message_data['from']
    message.attach(MIMEText(template))
    message['In-Reply-To'] = message_data['message_id']
    message['References'] = message_data['message_id']
    message['threadId'] = message_data['thread_id']
    message['subject'] = message_data['subject']

    if message_data['attachments'] and isinstance(message_data['attachments'], dict):
        for file in message_data['attachments']:
            add_attachment(message, message_data['attachments'][file])

    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, message_data):
    return service.users().messages().send(userId="me", body=build_message(message_data)).execute()

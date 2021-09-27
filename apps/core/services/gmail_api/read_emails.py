def process_message(message, is_approved):
    thread_id = message["threadId"]
    payload = message['payload']
    headers = payload.get("headers")
    message_data = {
        'thread_id': thread_id,
        'snippet': message["snippet"],
        'is_approved': is_approved,
    }
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == "message-id":
                message_data['message_id'] = value
            if name.lower() == "subject":
                message_data['subject'] = value
            if name.lower() == "date":
                message_data['date'] = value

    return message_data


def read_message(service, message_id):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Reads the content of the email, mostly the snippet, headers and returns them as a dictionary
    """
    message = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
    snippet = message["snippet"]
    is_approved = False
    if snippet and "security" in snippet or "access" in snippet:
        is_approved = True
    return process_message(message, is_approved)



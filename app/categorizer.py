def detect_category(text: str):

    text = text.lower()

    if "meeting" in text or "schedule" in text:
        return "Meeting"

    elif "urgent" in text or "asap" in text:
        return "Urgent"

    elif "complaint" in text or "issue" in text or "problem" in text:
        return "Complaint"

    elif "request" in text or "please" in text:
        return "Request"

    elif "job" in text or "internship" in text:
        return "Career"

    else:
        return "General"
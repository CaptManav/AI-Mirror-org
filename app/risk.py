import re

MONEY_WORDS = [
    "pay", "payment", "invoice", "refund", "transfer",
    "upi", "bank", "account", "price", "cost", "charge"
]

LEGAL_WORDS = [
    "contract", "agreement", "legal", "lawyer",
    "court", "liability", "terms", "lawsuit"
]

PROMISE_WORDS = [
    "guarantee", "definitely", "surely",
    "will deliver", "100%", "no problem"
]


def keyword_score(text, words, weight):
    score = 0
    t = text.lower()
    for w in words:
        if w in t:
            score += weight
    return score


def compute_risk(message):

    risk = 0

    risk += keyword_score(message, MONEY_WORDS, 3)
    risk += keyword_score(message, LEGAL_WORDS, 4)
    risk += keyword_score(message, PROMISE_WORDS, 2)

    # caps shouting signal
    if re.search(r"[A-Z]{6,}", message):
        risk += 2

    # question with deadline pressure
    if "urgent" in message.lower():
        risk += 2

    if risk >= 7:
        level = "HIGH"
    elif risk >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return risk, level

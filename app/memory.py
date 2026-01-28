from datetime import datetime

conversation_store = {}

def get_conversation(conversation_id: str):
    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = {
            "state": "LISTENING",
            "messages": [],
            "turns": 0,
            "start_time": datetime.utcnow(),
            "extracted": {
                "upi_ids": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "phishing_links": []
            }
        }
    return conversation_store[conversation_id]

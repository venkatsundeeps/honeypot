import re

def extract_intelligence(text: str, store: dict):
    upi_ids = re.findall(r"[\w.-]+@[\w]+", text)
    urls = re.findall(r"https?://[^\s]+", text)
    accounts = re.findall(r"\b\d{9,18}\b", text)
    ifsc_codes = re.findall(r"[A-Z]{4}0[A-Z0-9]{6}", text)

    for item in upi_ids:
        if item not in store["upi_ids"]:
            store["upi_ids"].append(item)

    for item in urls:
        if item not in store["phishing_links"]:
            store["phishing_links"].append(item)

    for item in accounts:
        if item not in store["bank_accounts"]:
            store["bank_accounts"].append(item)

    for item in ifsc_codes:
        if item not in store["ifsc_codes"]:
            store["ifsc_codes"].append(item)

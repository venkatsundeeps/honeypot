from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime

from app.security import verify_api_key
from app.memory import get_conversation
from app.scam_detector import detect_scam
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence

app = FastAPI(title="Agentic Honey-Pot API")


@app.post("/honeypot")
async def honeypot(payload: dict, auth=Depends(verify_api_key)):
    # Accept flexible input formats
    conversation_id = (
        payload.get("conversation_id")
        or payload.get("conversationId")
        or "default-conversation"
    )

    message = (
        payload.get("message")
        or payload.get("text")
        or payload.get("content")
    )

    # 🔥 IMPORTANT: Never reject the request body
    if not message:
        message = ""


    convo = get_conversation(conversation_id)
    convo["turns"] += 1

    # Scam detection
    is_scam, confidence = detect_scam(message)

    if is_scam:
        convo["state"] = "AGENT_ACTIVE"

    agent_reply = ""
    if convo["state"] == "AGENT_ACTIVE":
        agent_reply = generate_agent_reply(convo["messages"], message)

    # Update history
    convo["messages"].append({"role": "user", "content": message})
    if agent_reply:
        convo["messages"].append({"role": "assistant", "content": agent_reply})

    # Extract intelligence
    extract_intelligence(message, convo["extracted"])

    duration = (datetime.utcnow() - convo["start_time"]).seconds

    return {
        "conversation_id": conversation_id,
        "scam_detected": is_scam,
        "scam_confidence": confidence,
        "agent_active": convo["state"] == "AGENT_ACTIVE",
        "agent_reply": agent_reply,
        "engagement": {
            "turns": convo["turns"],
            "duration_seconds": duration
        },
        "extracted_intelligence": convo["extracted"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}

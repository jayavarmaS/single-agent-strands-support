import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from strands import Agent, tool
from strands.models import BedrockModel

import re

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
)

os.environ.setdefault("OTEL_SDK_DISABLED", "true")

BASE_DIR = Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "ui.html"

# -------------------------
# Bedrock model (Claude)
# -------------------------
bedrock_model = BedrockModel(
    model_id=BEDROCK_MODEL_ID,
    region_name=AWS_REGION,
    temperature=0.3,
    max_tokens=2048,
)

# =============================================
# TOOLS — These make the agent smart & reliable
# =============================================

@tool
def is_support_related(message: str) -> bool:
    """Determine if the message is about customer support topics."""
    support_keywords = [
        "login", "password", "account", "billing", "payment", "subscription",
        "order", "tracking", "refund", "cancel", "charge", "error", "bug",
        "can't access", "not working", "help", "support", "issue", "problem"
    ]
    msg = message.lower()
    return any(keyword in msg for keyword in support_keywords)


@tool
def get_faq_answer(query: str) -> str:
    """Return exact FAQ answer if matched, otherwise 'no_match'."""
    faqs = {
        "return policy": "You have 30 days to return items. Must be unused with tags. Free return label provided.",
        "shipping time": "Standard: 5-7 business days. Express: 2-3 days. Free over $50.",
        "cancel order": "You can cancel within 1 hour of purchase. After that, contact support.",
        "payment methods": "We accept credit cards, PayPal, Apple Pay, Google Pay, and Klarna.",
        "track order": "Check your confirmation email or log in → Orders → Track Package.",
        "change password": "Go to Account → Security → Change Password. We'll send a reset link.",
        "subscription cancel": "Go to Account → Subscriptions → Manage → Cancel. No fees.",
        "refund status": "Refunds take 3-7 business days to appear after processing."
    }
    
    q = query.lower()
    for key, answer in faqs.items():
        if key in q or any(word in q for word in key.split()):
            return f"Yes! {answer}"
    return "no_match"


@tool
def extract_order_id(message: str) -> str:
    """Extract order number like #ABC123 or ORD-45678"""
    match = re.search(r"(?:order|#)\s*#?([A-Z0-9]{4,})", message, re.IGNORECASE)
    return match.group(1) if match else "none"


@tool
def detect_urgency_and_tone(message: str) -> dict:
    """Detect urgency and negative tone"""
    msg = message.lower()
    urgent_words = ["now", "urgent", "asap", "immediately", "today", "right now"]
    negative_words = ["angry", "furious", "unacceptable", "hate", "terrible", "worst"]
    profanity = bool(re.search(r"\b(fuck|shit|bitch|damn|crap|ass)\b", msg, re.IGNORECASE))
    
    urgency = "high" if any(w in msg for w in urgent_words) else "medium"
    tone = "negative" if any(w in msg for w in negative_words) or profanity else "neutral"
    
    return {"urgency": urgency, "tone": tone, "profanity": profanity}


# =============================================
# SINGLE AGENT WITH TOOLS + IMPROVED PROMPT
# =============================================

SUPPORT_SYSTEM_PROMPT = """
You are a helpful Customer Support Agent.

Allowed topics:
- Login / password / account access
- Billing, payments, refunds
- Orders, shipping, tracking
- Subscriptions
- Technical issues

If the user asks about anything else (math, programming, history, jokes, general knowledge), 
politely say: "I'm sorry, I can only help with customer support questions."

Use your tools FIRST to gather facts:
- Always call is_support_related()
- If relevant, call get_faq_answer(), extract_order_id(), detect_urgency_and_tone()

Then respond clearly and helpfully.

Response rules:
- Be friendly and professional
- Use the customer's order number if found
- Give short, numbered steps when troubleshooting
- Escalate urgent/angry cases: "I'll escalate this to a senior agent right away."
- End with: "Is there anything else I can help with?"

Output ONLY the final customer message — no internal notes.
"""

support_agent = Agent(
    name="customer_support_agent",
    system_prompt=SUPPORT_SYSTEM_PROMPT,
    model=bedrock_model,
    tools=[
        is_support_related,
        get_faq_answer,
        extract_order_id,
        detect_urgency_and_tone
    ]
)

# -------------------------
# FastAPI app
# -------------------------
class SupportRequest(BaseModel):
    message: str

class SupportResponse(BaseModel):
    answer: str

app = FastAPI(title="Tool-Enhanced Single-Agent Support Desk", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui_root():
    return FileResponse(str(UI_FILE))

@app.get("/ui")
def serve_ui():
    return FileResponse(str(UI_FILE))

@app.post("/support", response_model=SupportResponse)
def support_endpoint(req: SupportRequest):
    response = support_agent(req.message)
    answer = str(response.content) if hasattr(response, 'content') else str(response)
    return SupportResponse(answer=answer.strip())

# -------------------------
# Auto-run with browser open
# -------------------------
if __name__ == "__main__":
    import uvicorn
    import webbrowser
    url = "http://127.0.0.1:8000/"
    print(f"Starting server and opening browser at {url}")
    webbrowser.open(url)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
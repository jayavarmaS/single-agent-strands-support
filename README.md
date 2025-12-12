single-agent-support-desk
Repository Description:
A lightweight, tool-enhanced customer support agent powered by AWS Bedrock and Claude 3.5 Sonnet. Uses a single intelligent agent with specialized tools for FAQ lookup, order extraction, urgency/tone detection, and topic filtering. Includes a clean web UI with auto-browser launch.
Visibility: Public (recommended for portfolio/showcase)

Full README.md Content
Copy and paste this entire content into your README.md file:
Markdown# Single-Agent Customer Support Desk

A smart, focused, and reliable **single-agent customer support system** built with **AWS Bedrock**, **Claude 3.5 Sonnet**, and the **Strands Agents** framework.

Unlike complex multi-agent systems, this project demonstrates the power of **one well-designed agent** equipped with **targeted tools** to handle real-world support scenarios efficiently.

![Demo Preview](https://via.placeholder.com/1200x600?text=Single+Agent+Support+Desk+UI)  
*(Live chat interface with real-time responses)*

## ✨ Features

- **Topic Guardrails** — Politely declines non-support questions
- **Smart FAQ Matching** — Instant answers for common queries
- **Order ID Extraction** — Automatically detects order numbers
- **Urgency & Tone Detection** — Identifies angry/urgent customers (including profanity)
- **Professional Responses** — Clear, empathetic, step-by-step help
- **Clean Web UI** — Simple HTML interface served via FastAPI
- **Auto Browser Launch** — Opens UI automatically on start
- **CORS Enabled** — Ready for frontend integration

## 🛠️ Tech Stack

- **Framework**: Strands Agents SDK
- **LLM**: Anthropic Claude 3.5 Sonnet via AWS Bedrock
- **Backend**: FastAPI + Uvicorn (with auto-reload)
- **Tools**: Custom Python functions with `@tool` decorator
- **Frontend**: Pure HTML (`ui.html`) — easy to customize
- **Config**: `.env` file for credentials

## 📋 Prerequisites

- Python 3.10+
- AWS account with Bedrock access
- IAM user with `bedrock:InvokeModel` permission
- Ports: 8000 available

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/single-agent-support-desk.git
cd single-agent-support-desk
2. Set Up Virtual Environment
Bashpython -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
3. Install Dependencies
Bashpip install strands-agents fastapi uvicorn python-dotenv
4. Configure AWS Credentials
Create a .env file in the project root:
envAWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
5. Run the Application
Bashpython main.py
→ Automatically opens your browser at http://127.0.0.1:8000
Start typing support questions! Try examples like:

"I forgot my password"
"Where is my order #ABC12345?"
"This is urgent — I was charged twice!"
"Tell me a joke" → (Agent politely declines)

🔧 How It Works
The agent uses four powerful tools before responding:

























ToolPurposeis_support_related()Filters out off-topic questionsget_faq_answer()Provides instant answers to common queriesextract_order_id()Finds order numbers in messagesdetect_urgency_and_tone()Detects urgency, negativity, and profanity
The system prompt enforces professional behavior and escalation when needed.
Response Rules (enforced via prompt):

Only answer support-related questions
Use order numbers when available
Escalate high-urgency or negative cases
End with offer for more help

📁 Project Structure
textsingle-agent-support-desk/
├── main.py                  # Core agent + FastAPI server
├── ui.html                  # Simple chat interface
├── .env                     # Your credentials (git ignored)
├── .env.example             # Template (include this in repo)
├── requirements.txt         # Dependencies
├── README.md                # This file
└── .gitignore
🔒 AWS Bedrock Setup

Go to AWS Console → Bedrock → Model access
Enable Anthropic Claude 3.5 Sonnet
Create IAM policy:

JSON{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "*"
    }
  ]
}

Generate access keys and add to .env

🛡️ Security Best Practices

Never commit .env with real keys
.env is in .gitignore
Use least-privilege IAM permissions
Rotate keys regularly

🤝 Contributing
Contributions welcome! Feel free to:

Improve the UI
Add more FAQs
Enhance tools
Submit pull requests

📄 License
MIT License — feel free to use, modify, and deploy.
🙏 Acknowledgments

Built with Strands Agents
Powered by Anthropic Claude via AWS Bedrock
FastAPI for modern Python web


Simple. Smart. Support-Focused.
Built in December 2025 — a clean alternative to complex multi-agent systems when one great agent is all you need.
🌟 Star this repo if you like focused, tool-enhanced agents!
text---

### Next Steps for GitHub

1. Create the repository: **single-agent-support-desk**
2. Upload these files:
   - `main.py` (your code)
   - `ui.html` (your chat interface)
   - `README.md` (above content)
   - `.env.example` (copy from `.env` but remove real keys)
   - `requirements.txt` with:
strands-agents
fastapi
uvicorn
python-dotenv

# Proposal Intelligence Agent

An offline AI-powered chatbot that turns a static proposal document into an interactive, conversational briefing experience. Built for enterprise pre-engagement scenarios where stakeholders need to interrogate a complex proposal live — without waiting for the engagement team to be in the room.

## The Problem It Solves

Enterprise AI proposals are long, dense documents. Stakeholders receiving them rarely read them cover to cover before a meeting — and when they have questions, they have to wait for the right person to be available.

This agent lets any stakeholder ask natural language questions about a proposal and receive instant, accurate answers — bounded by the proposal content. If a question falls outside the proposal scope, the agent says so clearly rather than guessing.

## How It Works

```
User Question
     │
     ▼
Query Normalisation (lowercase, strip punctuation)
     │
     ▼
Keyword + Content Scoring (TF-IDF style matching)
     │
     ▼
Confidence Threshold Check
     │
     ├── High confidence → Answer from matched section
     └── Low confidence  → Out-of-scope response
```

- **No LLM required** — fully offline, deterministic, auditable
- **No hallucinations** — every answer traces directly to the source document
- **Bounded responses** — out-of-scope questions receive a graceful redirect
- **Typing animation** — responses appear progressively, simulating a live agent

## Demo Content

The included knowledge base contains a fictional AI Assurance & Deployment proposal for a fictional European bank (EuroBank NV). It covers:

- Executive summary and programme objectives
- Problem statement and blockers being addressed
- Solution approach across 3 phases
- AI Assurance framework (guardrails, bias, hallucinations, explainability)
- Team structure and roles
- 12-month timeline and milestones
- Investment (€2.4M) and ROI model (340% over 3 years)
- Technology stack
- Risk management approach
- Why the vendor credentials
- Next steps

## Running Locally

```bash
# Clone the repo
git clone https://github.com/arvindsundar-svg/proposal-chatbot
cd proposal-chatbot

# Install dependencies (Flask only)
pip install -r requirements.txt

# Run
python app.py

# Open browser
http://localhost:5000
```

## Deploying to Render (free)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python app.py`
6. Deploy — you get a free `https://your-app.onrender.com` URL

## Adapting for Your Own Proposal

Replace `knowledge_base.json` with your own proposal content. Each section needs:

```json
{
  "id": "unique_id",
  "title": "Section Title",
  "keywords": ["keyword1", "keyword2", "phrase that triggers this section"],
  "content": "The answer text shown when this section is matched."
}
```

The more specific and varied your keywords, the better the matching.

## Architecture

```
proposal-chatbot/
├── app.py              # Flask web server
├── matcher.py          # Query matching engine
├── knowledge_base.json # Proposal content store
├── requirements.txt    # Flask only — no LLM dependencies
├── Procfile            # For Render deployment
└── templates/
    └── index.html      # Chat UI with typing animation
```

## Built By

Arvind Sundarraman — FDE Engagement Manager, AI Assurance & Deployment Practice  
[linkedin.com/in/arvind-sundarraman-65ab29a9](https://linkedin.com/in/arvind-sundarraman-65ab29a9)  
[github.com/arvindsundar-svg](https://github.com/arvindsundar-svg)

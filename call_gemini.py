from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import re

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Organisation name used in AI replies. Set ASSISTANT_ORG_NAME in .env.
ORG_NAME = os.getenv("ASSISTANT_ORG_NAME", "our team")


model = genai.GenerativeModel("gemini-2.5-flash")


# Function to summarize email text using Gemini AI
def summarize_email_text(email_body: str) -> str:

    if not email_body.strip():
        return "(Empty email)"

    prompt = f"""
    Read the following email and give a short, human-style explanation of what it's about — like what you’d write in a to-do list or summary feed in about 20-30 words.

    Make it sound like: "email about..." or "reminder to..." — not a formal summary.

    Only include the explanation.

    Email:
    {email_body}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"(Error summarizing: {e})"


#Email classification function using Gemini AI
def classify_email(summary: str) -> dict:
    if not summary.strip():
        return {
            "urgency": "low",
            "intent": "FYI",
            "topic": "personal",
            "action_flag": "no_reply_needed"
        }

    prompt = f"""
    Classify the following email into four categories based on the *summary* provided.

    Categories:

    Urgency:
    - urgent: time-sensitive, requires immediate attention
    - normal: routine communication or task
    - low: not time-sensitive, no immediate action needed

    Intent:
    - meeting_request: scheduling or requesting a meeting
    - notification: automated update, alert, or system message
    - action_required: requires the user to take some action or respond
    - FYI: just informational, no action or response expected

    Topic:
    - security: login alerts, password issues, suspicious activity
    - events: webinars, launches, invitations, meetups
    - project: team updates, assignments, progress reports
    - personal: casual or non-work-related messages

    Action Flag:
    - manual_review: urgent or sensitive emails that require human oversight
    - auto_reply: safe and straightforward emails that can be replied to by an AI
    - optional_reply: low-priority or friendly messages that could be replied to
    - no_reply_needed: purely informational or irrelevant emails that do not need a reply

    Choose the action_flag based on the urgency, intent, and topic. If the message is high-risk, highly sensitive, or urgent, prefer "manual_review". If it's clearly routine and safe, use "auto_reply". Use the others as needed.

    Respond strictly in the following JSON format:
    {{
      "urgency": "...",
      "intent": "...",
      "topic": "...",
      "action_flag": "..."
    }}

    Email Summary:
    \"\"\"{summary}\"\"\"
    """

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        match = re.search(r"\{.*?\}", raw_output, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("No valid JSON block found in Gemini response.")

    except Exception as e:
        return {
            "urgency": "normal",
            "intent": "FYI",
            "topic": "personal",
            "action_flag": "no_reply_needed",
            "error": str(e)
        }


def generate_ai_reply_from_body(email_body, sender, context_reply=None):
    context_part = f"Relevant previous reply to guide your tone and structure:\n{context_reply}\n\n" if context_reply else ""

    prompt = f"""
        You are an AI email assistant for {ORG_NAME}. Based on the email body below, generate a professional and concise reply.

        Sender: {sender}

        {context_part}
        Email Body:
        \"\"\"
        {email_body}
        \"\"\"

        Write your reply in full email format (greeting, body, closing).
        Do not hallucinate any information. Keep it polite and helpful.
        """


    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating reply: {str(e)}"
    
    

def get_sentiment_from_email(email_body: str) -> str:

    prompt = f"""
    You are an email sentiment analysis assistant. 

    Based on the email content below, classify the overall sentiment into **one** of the following categories:

    - appreciative  
    - neutral  
    - confused  
    - frustrated  
    - urgent  
    - negative  
    - positive  
    - concerned  

    Return the sentiment with a confidence percentage. Format:  
    **Sentiment (Confidence%)**  
    Example: frustrated (82%)

    Only return one best-fit sentiment.

    ---

    Email Content:
    \"\"\"
    {email_body}
    \"\"\"
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip().lower()
    except Exception as e:
        print(f"Error getting sentiment: {e}")
        return "neutral"  

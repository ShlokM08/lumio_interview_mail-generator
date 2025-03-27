import os
from dotenv import load_dotenv  # Add this line
load_dotenv()  # Load environment variables from .env file

import re
import smtplib
import ssl
import requests
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

###############################################################################
# CONFIGURATION
###############################################################################

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Environment variables SENDER_EMAIL or SENDER_PASSWORD are not set.")

# Debugging environment variables
print("SENDER_EMAIL:", SENDER_EMAIL)
print("SENDER_PASSWORD:", SENDER_PASSWORD)

# In-memory storage instead of SQLite
email_store = []

###############################################################################
# FLASK SETUP
###############################################################################
app = Flask(__name__)

###############################################################################
# EMAIL STORAGE HELPERS
###############################################################################
def log_email(recipient, subject, body, status):
    """Store email in memory instead of database."""
    email_store.append({
        "id": len(email_store) + 1,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "status": status,
        "created_at": datetime.now().isoformat()
    })
    # Keep only the last 100 emails to prevent memory issues
    if len(email_store) > 100:
        email_store.pop(0)

###############################################################################
# ROUTES
###############################################################################

@app.route("/", methods=["GET"])
def home():
    return "Flask App is Running on Vercel!"

@app.route("/send_email", methods=["POST"])
def send_email():
    """API endpoint to send an email via SMTP."""
    data = request.json
    recipient = data.get("recipient")
    subject = data.get("subject", "Generated Email")
    body = data.get("body", "")

    if not recipient or not body:
        return jsonify({"success": False, "error": "Missing recipient or body"}), 400

    success = send_email_smtp(recipient, subject, body)
    if success:
        log_email(recipient, subject, body, "SENT")
        return jsonify({"success": True, "message": "Email sent successfully!"})
    else:
        log_email(recipient, subject, body, "FAILED")
        return jsonify({"success": False, "error": "Failed to send email"}), 500

@app.route("/email_history", methods=["GET"])
def get_email_history():
    """Get the history of sent emails (in-memory)."""
    return jsonify({"emails": email_store})

###############################################################################
# SMTP SENDING
###############################################################################
def send_email_smtp(recipient, subject, body):
    """Send email via Gmail SMTP with SSL."""
    try:
        if not SENDER_EMAIL or SENDER_EMAIL == "default@example.com" or not SENDER_PASSWORD:
            print("Error: Email credentials not properly configured")
            return False
            
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            message = f"""From: {SENDER_EMAIL}
To: {recipient}
Subject: {subject}

{body}
"""
            server.sendmail(SENDER_EMAIL, recipient, message)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

###############################################################################
# HANDLER FOR VERCEL SERVERLESS FUNCTION
###############################################################################
def handler(event, context):
    return app(event, context)

###############################################################################
# MAIN (For Local Testing)
###############################################################################
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

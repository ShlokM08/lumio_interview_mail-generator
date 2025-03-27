# Flask Email App on Vercel

This is a simple Flask-based email sending app that runs on Vercel.

## 🚀 Features
- Generates and sends emails using SMTP (Gmail).
- Logs email status in memory (serverless-compatible).
- Deployed as a serverless function on Vercel.

## 🛠 Installation

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## 🚀 Deployment to Vercel

1. Fork or clone this repository
2. Set up environment variables in Vercel:
   - SENDER_EMAIL: Your Gmail address
   - SENDER_PASSWORD: Your Gmail app password
3. Deploy to Vercel

### Important Notes
- This app uses in-memory storage for email logs as Vercel serverless functions don't support file-based databases like SQLite
- Make sure to set up environment variables in Vercel's dashboard

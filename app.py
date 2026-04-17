import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()


# ---------------- BOT CLASS ---------------- #

class OpenClawBot:

    def __init__(self, sheet_id):

        # 🔐 API setup
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env")

        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        self.client = Groq(api_key=self.api_key)

        # 📊 Google Sheets
        self.sheet_id = sheet_id
        self.sheets = self.init_sheets()

    def init_sheets(self):
        try:
            creds = Credentials.from_service_account_file(
                "credentials.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            return build("sheets", "v4", credentials=creds)
        except Exception as e:
            st.error(f"Google Sheets Error: {e}")
            return None

    def save_to_sheets(self, data):

        if not self.sheets:
            st.warning("Google Sheets not connected")
            return

        rows = []

        for item in data:
            rows.append([
                item.get("date", ""),
                item.get("topic", ""),
                item.get("hook", ""),
                item.get("script", ""),
                item.get("cta", "")
            ])

        body = {"values": rows}

        try:
            self.sheets.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body=body
            ).execute()

            st.success("✅ Saved to Google Sheets")

        except Exception as e:
            st.error(f"Error saving to sheets: {e}")

    # ---------------- CORE LOGIC ---------------- #

    def get_hooks(self, topic):

        hooks_db = {
            "skincare": [
                "You're destroying your skin without knowing it",
                "Dermatologists won't tell you this secret",
                "This one mistake is causing your acne"
            ],
            "fitness": [
                "You're wasting hours in the gym",
                "This mistake is killing your gains",
                "Trainers don't want you to know this"
            ],
            "default": [
                "This changed everything for me",
                "You're doing this wrong",
                "No one talks about this"
            ]
        }

        return hooks_db.get(topic.lower(), hooks_db["default"])

    def generate_script(self, topic, hook):

        system_prompt = """You are a high-converting ad copywriter.

Return ONLY valid JSON:
{
    "hook": "",
    "script": "",
    "cta": ""
}

Rules:
- Script must be 15-20 seconds
- Highly engaging
- Short and punchy
"""

        user_prompt = f"Topic: {topic}\nHook: {hook}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            text = response.choices[0].message.content

        except Exception as e:
            return {
                "hook": hook,
                "script": f"Error: {e}",
                "cta": "Try again"
            }

        try:
            return json.loads(text)
        except:
            return {
                "hook": hook,
                "script": text,
                "cta": "Learn more"
            }

    def run(self, topic, num, custom_hooks=None):

        if custom_hooks:
            hooks = custom_hooks
        else:
            hooks = self.get_hooks(topic)[:num]

        results = []

        for hook in hooks:
            data = self.generate_script(topic, hook)
            data["topic"] = topic
            data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append(data)

        return results


# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(page_title="OpenClaw AI", layout="wide")

st.title("🦾 OpenClaw AI Ad Generator")

st.markdown("Generate viral ad scripts and save them directly to Google Sheets 🚀")

# Inputs
sheet_id = st.text_input("📊 Google Sheet ID")
topic = st.text_input("🧠 Topic (e.g. Skincare)")
num = st.slider("📈 Number of Scripts", 1, 10, 3)

use_custom = st.checkbox("✍️ Use Custom Hooks")

custom_hooks = None
if use_custom:
    custom_hooks = []
    for i in range(num):
        hook = st.text_input(f"Hook {i+1}")
        if hook:
            custom_hooks.append(hook)

# Button
if st.button("🚀 Generate"):

    if not sheet_id:
        st.error("Please enter Google Sheet ID")
    elif not topic:
        st.error("Please enter topic")
    else:

        bot = OpenClawBot(sheet_id)

        with st.spinner("Generating scripts..."):
            results = bot.run(topic, num, custom_hooks)
            bot.save_to_sheets(results)

        st.success("✅ Done!")

        for r in results:
            st.markdown(f"### 🔥 Hook: {r['hook']}")
            st.write(f"📝 {r['script']}")
            st.write(f"📢 CTA: {r['cta']}")
            st.markdown("---")
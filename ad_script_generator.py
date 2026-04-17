import json
import os
from datetime import datetime
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

# Google Sheets imports
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load env variables
load_dotenv()


class AdScriptGenerator:

    def __init__(self, google_sheet_id: Optional[str] = None):

        
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(" GROQ_API_KEY not found in .env")

        # Load Model
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        # Initialize Groq
        self.client = Groq(api_key=self.api_key)

        # Google Sheets setup
        self.google_sheet_id = google_sheet_id
        self.sheets_client = None

        if google_sheet_id:
            self.init_google_sheets()

    # GOOGLE SHEETS 

    def init_google_sheets(self):
        try:
            credentials = Credentials.from_service_account_file(
                "credentials.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )

            self.sheets_client = build("sheets", "v4", credentials=credentials)
            print(" Google Sheets Connected")

        except Exception as e:
            print(f" Google Sheets Error: {e}")

    def save_to_google_sheets(self, scripts):

        if not self.sheets_client:
            print("⚠ Google Sheets not initialized")
            return

        rows = []

        # Header
        rows.append([
            "Date", "Topic", "Hook", "Problem",
            "Solution", "CTA", "Full Script", "Platform"
        ])

        for script in scripts:
            rows.append([
                script.get("date", ""),
                script.get("topic", ""),
                script.get("hook", ""),
                script.get("problem_statement", ""),
                script.get("solution", ""),
                script.get("cta", ""),
                script.get("full_script", ""),
                script.get("platform", "")
            ])

        body = {"values": rows}

        try:
            self.sheets_client.spreadsheets().values().append(
                spreadsheetId=self.google_sheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body=body
            ).execute()

            print(" Data saved to Google Sheets")

        except Exception as e:
            print(f" Error saving to sheets: {e}")

    # CORE LOGIC 

    def get_viral_hooks(self, topic: str):
        trending_hooks_db = {
            "skincare": [
                {"hook": "POV: You've been using the wrong skincare routine"},
                {"hook": "Dermatologists HATE this one simple trick"},
                {"hook": "Your skin at 25 vs. 35 (here's what I changed)"}
            ],
            "default": [
                {"hook": "You've been doing this wrong your whole life"},
                {"hook": "This changed everything for me"},
                {"hook": "POV: You just discovered the solution"}
            ]
        }

        return trending_hooks_db.get(topic.lower(), trending_hooks_db["default"])

    def generate_ad_script(self, topic: str, hook: str):

        system_prompt = """You are a world-class ad copywriter.

Return ONLY valid JSON:
{
    "hook": "",
    "problem_statement": "",
    "solution": "",
    "cta": "",
    "full_script": "",
    "platform": "Instagram Reels",
    "estimated_duration": "15-20 seconds"
}
"""

        user_prompt = f"""
Topic: {topic}
Hook: {hook}

Generate a high-converting 15-20 second ad script.
"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )

            response_text = completion.choices[0].message.content

        except Exception as e:
            print(f" API Error: {e}")
            return {"error": str(e)}

        try:
            return json.loads(response_text)
        except:
            return {
                "hook": hook,
                "full_script": response_text,
                "platform": "Instagram Reels"
            }

    def create_workflow(self, topic: str, num_scripts: int = 3):

        print(f"\n Starting Workflow for: {topic}")

        hooks = self.get_viral_hooks(topic)[:num_scripts]
        scripts = []

        for i, item in enumerate(hooks, 1):
            hook = item["hook"]

            print(f"Generating script {i}/{num_scripts}...")

            script = self.generate_ad_script(topic, hook)

            script["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            script["topic"] = topic
            script["script_number"] = i

            scripts.append(script)

        return scripts


# MAIN 

def main():

    # PUT YOUR GOOGLE SHEET ID HERE
    GOOGLE_SHEET_ID = "1vFd57steELygi3bHs7KLzGaw4k0z4DxgJMwcuLU52QE"

    generator = AdScriptGenerator(google_sheet_id=GOOGLE_SHEET_ID)

    scripts = generator.create_workflow("Skincare", 3)

    # Save to Google Sheets
    generator.save_to_google_sheets(scripts)

    print("\n========== GENERATED SCRIPTS ==========\n")

    for script in scripts:
        print(json.dumps(script, indent=2))
        print("\n--------------------------------------\n")


if __name__ == "__main__":
    main()

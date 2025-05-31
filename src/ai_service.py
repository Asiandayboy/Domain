import google.generativeai as genai
from dotenv import load_dotenv
import os
import markdown

load_dotenv()
genai.configure(api_key=os.getenv("GG_API_KEY"))


model = genai.GenerativeModel("gemini-1.5-flash-002")


def get_ai_response(prompt):
    response = model.generate_content(prompt)
    html_response = markdown.markdown(response.text)
    return html_response
import google.generativeai as genai
from dotenv import load_dotenv
import os
import markdown

load_dotenv()
genai.configure(api_key=os.getenv("GG_API_KEY"))


model = genai.GenerativeModel("gemini-1.5-flash-002")


AI_INSTRUCTION = (
    "You are an expert in embedded systems and IoT."
    "You provide technical and helpful responses."
    "Use traffic dataset trends when applicable."
)

def get_ai_response(prompt):
    response = model.generate_content(
        [AI_INSTRUCTION, prompt]
    )
    html_response = markdown.markdown(response.text)
    return html_response
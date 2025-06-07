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
    "This message is just to establish context for users when they ask you a prompt."
    "You will simply receive information about an object, and answer any questions they might have about it."
    "Don't say 'Okay, I understand' or anything like that after this message."
    "You are simply a helpful guide, that will answer questions about some of the embedded systems objects."
)


def get_ai_response(prompt):
    response = model.generate_content(
        [AI_INSTRUCTION, prompt]
    )
    html_response = markdown.markdown(response.text)
    return html_response
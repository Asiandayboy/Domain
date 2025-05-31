from flask import Blueprint, request, jsonify
from ai_service import get_ai_response
from cache import get_cached_response, set_cached_response
from flasgger import swag_from

ai_bp = Blueprint("ai", __name__)



@ai_bp.route("/ask", methods=["POST"])
@swag_from({
    "parameters": [
        {
            "name": "prompt",
        }
    ],
    "responses": {
        "200": {
            "description": "AI response",
            "examples": {
                "application/json": {
                    "response": "AI-generated text here",
                    "cached": False
                }
            }
        },
        "400": {
            "description": "Bad request",
            "examples": {
                "application/json": {
                    "error": "No prompt provided"
                }
            }
        }
    }
})
def ask():
    """
    Get a response from the AI model based on the provided prompt.
    ---
    """
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({ "error": "No prompt provided" }), 400
    
    # check if prompt is cahced
    cached = get_cached_response(prompt)
    if cached:
        return jsonify({ 
            "response": cached,
            "cached": True
        })
    
    response = get_ai_response(prompt)
    set_cached_response(prompt, response)

    return jsonify({ 
            "response": response, 
            "cached": False 
        })
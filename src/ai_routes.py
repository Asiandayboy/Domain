from flask import Blueprint, request, jsonify
from ai_service import get_ai_response
from cache import get_cached_response, set_cached_response
from flasgger import swag_from
from uids_routes import MODEL_INFO

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
    model_id = data.get("model_id")

    if not prompt:
        return jsonify({ "error": "No prompt provided" }), 400
    
    if model_id and model_id in MODEL_INFO:
        context = MODEL_INFO[model_id]
        model_name = context.get("name", "")
        model_desc = context.get("description", "")
        model_ctx = context.get("embedded_context", "")
        prompt = f"This question is about {model_name}. {model_desc}. Some context: {model_ctx}.\n\nPrompt: {prompt}"
    
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
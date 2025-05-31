from flask import Flask, render_template, request, jsonify
from ai_routes import ai_bp
from uids_routes import uids_bp
from cache import init_db
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(uids_bp, url_prefix="/api")

swagger = Swagger(app)


@app.route("/")
def index():
    """
    Serves the root page.
    ---

    responses:
        200:
            description: Rendered index.html page
            content:
                text/html
    """
    return render_template("index.html")



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
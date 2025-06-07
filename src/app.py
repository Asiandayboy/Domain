from flask import Flask, render_template, request, jsonify, Response
from ai_routes import ai_bp
from uids_routes import uids_bp
from cache import init_db
from flasgger import Swagger
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(uids_bp, url_prefix="/api")
swagger = Swagger(app)


REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])


@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()



@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



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
    app.run(debug=True, port=5000, host="0.0.0.0")
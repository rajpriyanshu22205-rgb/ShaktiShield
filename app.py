from flask import Flask
from routes.sos_routes import sos_bp
from routes.user_routes import user_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "shakti_shield_secret_key"

app.register_blueprint(sos_bp, url_prefix="/api/sos")
app.register_blueprint(user_bp, url_prefix="/api/user")

@app.route("/")
def home():
    return "Shakti Shield Backend Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)
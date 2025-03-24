from flask import Flask, jsonify

from src.api.routes.tournaments import tournaments_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(tournaments_bp)

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Esports API!"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_cors import CORS

from blueprints import betise_bp, recette_bp, couture_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
app.register_blueprint(betise_bp, url_prefix='/api/betise')
app.register_blueprint(recette_bp, url_prefix='/api/recette')
app.register_blueprint(couture_bp, url_prefix='/api/couture')


if __name__ == '__main__':
    app.run()

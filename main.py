from flask import Flask
from flask_cors import CORS

from blueprints import main_bp, galerie_bp, nendoroids_bp, user_bp, carton_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://localhost:3000"]}})
# app.register_blueprint(betise_bp, url_prefix='/api/betise')
# app.register_blueprint(recette_bp, url_prefix='/api/recette')
# app.register_blueprint(couture_bp, url_prefix='/api/couture')
app.register_blueprint(main_bp, url_prefix='/api/collection')
app.register_blueprint(carton_bp, url_prefix='/api/carton')
app.register_blueprint(galerie_bp, url_prefix='/api/galerie')
app.register_blueprint(nendoroids_bp, url_prefix='/api/nendoroids')
app.register_blueprint(user_bp, url_prefix='/api/user')


if __name__ == '__main__':
    app.run()

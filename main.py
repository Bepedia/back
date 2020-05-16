from flask import Flask
from blueprints import betise_bp, recette_bp, couture_bp

app = Flask(__name__)
app.register_blueprint(betise_bp, url_prefix='/api/betise')
app.register_blueprint(recette_bp, url_prefix='/api/recette')
app.register_blueprint(couture_bp, url_prefix='/api/couture')


if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_cors import CORS
from routes.cnpj_routes import cnpj_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(cnpj_bp, url_prefix='/cnpj')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
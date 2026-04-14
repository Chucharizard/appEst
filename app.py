from flask import Flask
import math

from modules.tablas import tablas_bp
from modules.graficos import graficos_bp

app = Flask(__name__)

# Filtro Jinja2 para mostrar log10 en el template
app.jinja_env.filters["log10"] = math.log10

# Registrar Blueprints
app.register_blueprint(tablas_bp)
app.register_blueprint(graficos_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5050)

# Guía para Añadir Nuevos Módulos a AppEst 🧩

La arquitectura de AppEst está implementada mediante el patrón **Modular Monolith** (Monolito Modular) apoyado nativamente por la tecnología **Flask Blueprints**. Esto permite que la aplicación aguante decenas de paquetes diferentes (Ej: Probabilidad, Regresión Lineal) sin que el código jamás reviente.

Sigue estos 4 pasos para agregar un "Tercer Módulo" al sistema.

## Paso 1: Crear la Carpeta del Módulo
Ve a la carpeta `/modules/` y crea una carpeta con el nombre de tu nuevo módulo, por ejemplo: `/modules/probabilidad/`.

Dentro de esa carpeta, debes crear **estrictamente estos 3 archivos**:
1. `__init__.py`
2. `routes.py`
3. `services.py`

## Paso 2: Programar los 3 Archivos de tu Módulo

### A) El Inicializador (`__init__.py`)
Este archivo le dice a Python que esta carpeta funciona como un Blueprint independiente. Pega esto:
```python
from flask import Blueprint

# Declaramos el nombre del plano y el sufijo URL (Opcional)
probabilidad_bp = Blueprint('probabilidad', __name__)

from . import routes
```

### B) El Controlador Web (`routes.py`)
Aquí recibimos las peticiones web. Las rutas aquí usan `@ombrenombre_bp.route`, no usamos el clásico `@app`.
```python
from flask import render_template, request
from . import probabilidad_bp
from .services import hacer_matematica

@probabilidad_bp.route('/probabilidades', methods=['GET', 'POST'])
def view_probabilidad():
    resultados = None
    if request.method == 'POST':
        datos = request.form.get('mis_datos')
        resultados = hacer_matematica(datos)
        
    return render_template('probabilidades/index.html', resultados=resultados)
```

### C) El Motor Matemático (`services.py`)
Aquí no va nada web, solo Python matemático puro.
```python
def hacer_matematica(datos):
    # Lógica de probabilidad aquí
    return "Éxito al calcular"
```

## Paso 3: Conectar el Módulo a la Central (`app.py`)
Abre tu archivo general principal `app.py` que está en la raíz del proyecto.
Importa tu Blueprint inventado y regístralo:
```python
# Importa tu nuevo Blueprint
from modules.probabilidad import probabilidad_bp

# Registra
app.register_blueprint(probabilidad_bp)
```

## Paso 4: Añadir la Pestaña Visual (HTML)
1. En tu carpeta `/templates/`, crea una subcarpeta `/templates/probabilidades/` y mete ahí tu diseño web visual (`index.html`) asegurándote de usar `{% extends "base.html" %}` para heredar el menú y fondo.
2. Finalmente, abre `/templates/base.html` y añade un nuevo enlace en el sector de `<nav>` para que aparezca un tercer botón en la superio:
```html
<a href="/probabilidades" class="nav-item {% if request.path == '/probabilidades' %}active{% endif %}">🎲 Mis Probabilidades</a>
```

¡Listo! Así puedes escalar AppEst hasta donde necesites.

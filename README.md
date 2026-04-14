<div align="center">

# ∑ EstaDística

### Calculadora de Estadística Descriptiva · Visualización Interactiva de Datos

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://chartjs.org)
[![Tesseract.js](https://img.shields.io/badge/Tesseract.js-5.x-4A90D9?style=for-the-badge)](https://tesseract.projectnaptha.com)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-22d3ee?style=for-the-badge)](LICENSE)

**Resuelve ejercicios completos de estadística descriptiva en segundos.**  
Tablas de frecuencias, medidas estadísticas, gráficos interactivos y reconocimiento OCR de imágenes — todo en una sola app.

[Ver Demo](#demo) · [Instalación rápida](#instalación) · [Estructura del proyecto](#estructura)

</div>

---

## Características

### Tablas Estadísticas
- **Tabla de frecuencias completa** — Genera automáticamente Li, Ls, xi, fi, hi, pi, Fi, Hi, Pi
- **Método de Sturges** — k = 1 + 3.3 · log₁₀(n), con corrección de límites automática
- **Método arbitrario** — Define tú mismo el número de clases k
- **Ajuste de sobrante** — Distribuye el excedente entre límite inferior y superior
- **Fórmulas paso a paso** — Cada cálculo se explica con sustitución numérica

### Medidas Estadísticas
| Categoría | Medidas |
|-----------|---------|
| **Tendencia central** | Media aritmética, Mediana, Moda (método Czuber) |
| **Posición** | Cuartiles Q₁–Q₃, Deciles D₁–D₉, Percentil Pₖ personalizado |
| **Interpretación** | Cada medida incluye su explicación en lenguaje natural |

### Gráficos Interactivos (Chart.js)
10 tipos de visualización disponibles:

| Gráfico | Descripción |
|---------|-------------|
| Columnas simples | Distribución por categorías |
| Columnas compuestas | Comparación apilada de dos grupos |
| Barras horizontales | Ideal para etiquetas largas |
| Bastones | Datos discretos con línea punteada |
| Lineal | Tendencias y series temporales |
| Área | Variación continua con relleno |
| Dispersión de puntos | Correlación entre variables |
| Burbujas | Visualización 3D (x, y, tamaño) |
| Circular / Pastel | Proporciones de un total |
| Dona | Pastel con espacio central para KPIs |

### OCR — Extracción desde imágenes
- **Tomar foto** directamente desde la cámara del dispositivo
- **Subir archivo** de imagen (JPG, PNG, WebP)
- Reconocimiento en inglés y español con **Tesseract.js v5**
- Extrae automáticamente todos los valores numéricos detectados
- Soporte para decimales con punto (.) y coma (,)

### Diseño y UX
- Tema oscuro con paleta **morado · cian · rosa**
- **Totalmente responsivo** — Optimizado para móvil, tablet y escritorio
- Navbar con menú hamburguesa en pantallas pequeñas
- Animaciones suaves y notificaciones inline
- Sin dependencias de JavaScript externas (excepto Chart.js y Tesseract.js vía CDN)

---

## Demo

> Ingresa tu conjunto de datos, selecciona qué calcular y obtén resultados en menos de un segundo.

```
Datos de entrada:
12 13 9.5 10 8 10 9 8 8.5 9
10.1 9.2 8.1 8.2 8.1 8.3 8.1 9.2 9.4 10
10 9 8.5 12 8.1 8 8.3 9.3 14 14.5

Resultado → n=30, k=6 (Sturges), t=1.125
Tabla de 6 clases con todas las frecuencias
Media: 9.99 | Mediana: 9.61 | Moda: 8.36
Q₁: 8.55 · Q₂: 9.61 · Q₃: 10.38
```

---

## Instalación

### Requisitos previos
- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/appEst.git
cd appEst

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

Abre tu navegador en `http://localhost:5050`

### Dependencias
```
flask>=3.0.0
```
El frontend usa CDN — no necesitas Node.js ni npm.

---

## Uso

### Tablas Estadísticas (`/`)
1. Ingresa tu dataset en el campo de texto (espacios, comas o saltos de línea)
2. Elige el método: **Sturges** (automático) o **Arbitrario** (defines k)
3. Selecciona qué calcular con los chips interactivos
4. Haz clic en **Calcular**

**Atajos de entrada:**
- `✦ Cargar ejemplo` — Carga un dataset de muestra
- `📸 Tomar Foto` — Usa la cámara para capturar datos impresos
- `🖼️ Subir Archivo` — Sube una imagen y extrae los números con OCR

### Gráficos (`/graficos`)
1. Selecciona el tipo de gráfico
2. Ingresa las categorías (Ej: `Enero, Febrero, Marzo`)
3. Ingresa los valores del Grupo 1 (Ej: `120, 95, 140`)
4. Opcionalmente, agrega un Grupo 2 para gráficos comparativos
5. Haz clic en **Generar Gráfico**

---

## Estructura

```
appEst/
│
├── app.py                      # Punto de entrada Flask — registra blueprints
├── requirements.txt
│
├── modules/
│   ├── tablas/                 # Módulo de tablas estadísticas
│   │   ├── __init__.py         # Blueprint: tablas_bp
│   │   ├── routes.py           # GET/POST /
│   │   ├── parser.py           # Normalización del input (punto/coma, formatos)
│   │   ├── tables.py           # Algoritmo de tabla de frecuencias (Sturges)
│   │   └── measures.py         # Media, Mediana, Moda, Cuartiles, Deciles, Percentiles
│   │
│   └── graficos/               # Módulo de visualización
│       ├── __init__.py         # Blueprint: graficos_bp
│       ├── routes.py           # GET/POST /graficos
│       └── charts.py           # Transformación de datos para Chart.js
│
├── templates/
│   ├── base.html               # Layout base — navbar, CDN imports
│   ├── tablas_index.html       # Interfaz de tablas
│   └── graficos_index.html     # Interfaz de gráficos
│
├── static/
│   ├── css/style.css           # Tema oscuro — variables CSS, responsive
│   └── js/main.js              # OCR, spinner, auto-scroll, notificaciones
│
└── guia/
    └── COMO_AGREGAR_MODULOS.md # Guía para extender la app con nuevos módulos
```

---

## Arquitectura

La app sigue el patrón **Monolito Modular** con Flask Blueprints:

```
HTTP Request
     │
     ▼
  app.py  ──── registra blueprints
     │
     ├──► tablas_bp (/):
     │       routes.py → parser.py → tables.py → measures.py → Jinja2
     │
     └──► graficos_bp (/graficos):
              routes.py → charts.py → Jinja2 → Chart.js
```

Para agregar un nuevo módulo (ej: Probabilidad):

```bash
mkdir modules/probabilidad
touch modules/probabilidad/__init__.py
touch modules/probabilidad/routes.py
touch modules/probabilidad/services.py
```

Ver la guía completa en [`guia/COMO_AGREGAR_MODULOS.md`](guia/COMO_AGREGAR_MODULOS.md).

---

## Algoritmos implementados

### Tabla de frecuencias — Regla de Sturges
```
k  = ⌈ 1 + 3.3 · log₁₀(n) ⌉
la = Xmáx − Xmín + unidad
t  = la / k  (ajustado para que t·k ≥ la)
```
El sobrante se reparte equitativamente entre el límite inferior y superior para centrar los datos.

### Mediana
```
Md = Lᵢ + ( (n/2 − Fₐ₋₁) / fᵢ ) · t
```

### Moda — Método de Czuber
```
Mo = Lᵢ + ( d₁ / (d₁ + d₂) ) · t

donde:
  d₁ = fᵢ − fᵢ₋₁   (diferencia con clase anterior)
  d₂ = fᵢ − fᵢ₊₁   (diferencia con clase siguiente)
```

### Percentiles / Cuartiles / Deciles
```
Pₖ = Lᵢ + ( ( (k·n)/100 − Fₐ₋₁ ) / fᵢ ) · t
```
Q₁ = P₂₅ · Q₂ = P₅₀ · Q₃ = P₇₅  
D₁ = P₁₀ · D₂ = P₂₀ · … · D₉ = P₉₀

---

## Stack tecnológico

| Capa | Tecnología | Rol |
|------|-----------|-----|
| Backend | Python + Flask 3.0 | Servidor web y lógica estadística |
| Templating | Jinja2 | Renderizado HTML server-side |
| Gráficos | Chart.js 4 | Visualizaciones interactivas en canvas |
| OCR | Tesseract.js 5 | Reconocimiento de texto en imágenes |
| Fuentes | Google Fonts (Inter + JetBrains Mono) | Tipografía |
| Estilos | CSS custom con variables | Tema oscuro, responsive |

---

## Responsive Design

La app está optimizada para todos los dispositivos:

| Dispositivo | Ancho | Comportamiento |
|-------------|-------|----------------|
| Desktop | > 1024px | Layout completo, grillas multi-columna |
| Tablet | 601–1024px | Grillas adaptadas |
| Móvil | 481–600px | Columna única, botones apilados |
| Móvil pequeño | ≤ 480px | Navbar hamburguesa, padding mínimo |

---

## Contribuir

Las contribuciones son bienvenidas. El proyecto está diseñado para ser extendido fácilmente:

1. Haz fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcion`
3. Implementa tu módulo siguiendo la guía en `guia/`
4. Abre un Pull Request

**Ideas para contribuir:**
- Módulo de estadística inferencial (intervalos de confianza, pruebas de hipótesis)
- Módulo de regresión y correlación
- Exportar tabla a PDF o Excel
- Soporte para datasets CSV

---

## Licencia

Distribuido bajo la licencia MIT. Ver [`LICENSE`](LICENSE) para más información.

---

<div align="center">

Hecho con Flask · Chart.js · Tesseract.js

</div>

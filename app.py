from flask import Flask, render_template, request, jsonify
import math
import statistics
from collections import Counter

app = Flask(__name__)

# Filtro Jinja2 para mostrar log10 en el template
app.jinja_env.filters["log10"] = math.log10


# ─────────────────────────────────────────────
# ESTADÍSTICA DESCRIPTIVA – LÓGICA CENTRAL
# ─────────────────────────────────────────────

def parse_data(raw: str) -> tuple[list[float], int]:
    """Convierte texto en lista de floats y retorna la cantidad máx de decimales.
    Permite coma como decimal si no está seguida de un espacio."""
    import re
    # Soporta coma como decimal (ej 1,64 -> 1.64)
    raw_normalized = re.sub(r"(\d),(\d)", r"\1.\2", raw)
    
    tokens = re.split(r"[^\d.-]+", raw_normalized.strip())
    
    data = []
    max_dec = 0
    for t in tokens:
        if not t: continue
        try:
            val = float(t)
            data.append(val)
            if "." in t:
                dec = len(t.split(".")[1])
                if dec > max_dec:
                    max_dec = dec
        except ValueError:
            pass
            
    return sorted(data), max_dec


def sturges(n: int) -> int:
    """Número de clases por la regla de Sturges (coef. 3.3)."""
    return round(1 + 3.3 * math.log10(n))


def build_frequency_table(data: list[float], max_dec: int):
    """
    Construye la tabla estadística adaptando la precisión (unidad de medida).
    """
    n = len(data)
    d  = min(data)          # mínimo
    D  = max(data)          # máximo
    
    unit = 10 ** -max_dec if max_dec > 0 else 1
    la = round(D - d + unit, 10)   # longitud de alcance
    k  = sturges(n)

    # Tamaño de clase inicial ajustado a la precisión
    t_raw = la / k
    t = round(t_raw, max_dec)
    if t < t_raw:                   # si se redondeó hacia abajo
        t = round(t + unit, max_dec)

    # Corrección: verificar que t*k cubre la longitud de alcance
    t_k_inicial = round(t * k, 10)
    correction_applied = False
    while round(t * k, 10) < la:
        t = round(t + unit, max_dec)
        correction_applied = True

    t_k_final = round(t * k, 10)

    # Cálculo y reparto del sobrante
    sobrante = round(t_k_final - la, 10)
    unidades_sobra = int(round(sobrante / unit))
    mitad_inf = unidades_sobra // 2
    mitad_sup = unidades_sobra - mitad_inf

    nuevo_d = round(d - mitad_inf * unit, max_dec)
    nuevo_D = round(D + mitad_sup * unit, max_dec)

    # Construcción de clases
    clases = []
    li = nuevo_d  # Empieza con el límite inferior corregido
    fa_acum = 0
    hi_acum = 0.0

    for i in range(k):
        ls = round(li + t, 10)
        # La última clase incluye el límite superior
        if i == k - 1:
            fi = sum(1 for x in data if li <= x <= ls + 1e-9)
        else:
            fi = sum(1 for x in data if li <= x < ls)

        marca = round((li + ls) / 2, 4)
        hi = round(fi / n, 4)
        pi = round(hi * 100, 2)
        fa_acum += fi
        hi_acum = round(hi_acum + hi, 4)
        Pi_val = round(hi_acum * 100, 2)

        clases.append({
            "clase": i + 1,
            "li": round(li, 4),
            "ls": round(ls, 4),
            "marca": marca,
            "fi": fi,
            "hi": hi,
            "pi": pi,
            "Fi": fa_acum,
            "Hi": hi_acum,
            "Pi": Pi_val,
            # Mantener compatibilidad interna
            "fr": hi,
            "fa": fa_acum,
            "frl": hi_acum,
        })
        li = ls

    meta = {
        "n": n,
        "d": d,
        "D": D,
        "unidad": unit,
        "la": round(la, 4),
        "k": k,
        "k_exacto": round(1 + 3.3 * math.log10(n), 4),
        "t_inicial": t_k_inicial / k if k else t,   # t antes de corrección
        "t": t,
        "t_k": t_k_final,
        "correction_applied": correction_applied,
        "sobrante": sobrante,
        "unidades_sobra": unidades_sobra,
        "mitad_inf": mitad_inf,
        "mitad_sup": mitad_sup,
        "nuevo_d": nuevo_d,
        "nuevo_D": nuevo_D,
    }
    return clases, meta


def calc_media(clases, n):
    return round(sum(c["marca"] * c["fi"] for c in clases) / n, 4)


def calc_mediana(clases, n):
    mitad = n / 2
    fa_ant = 0
    for c in clases:
        if c["fa"] >= mitad:
            li = c["li"]
            fi = c["fi"]
            amp = c["ls"] - c["li"]
            med = li + ((mitad - fa_ant) / fi) * amp
            return round(med, 4), c["clase"]
        fa_ant = c["fa"]
    return None, None


def calc_moda(clases):
    max_fi = max(c["fi"] for c in clases)
    modales = [c for c in clases if c["fi"] == max_fi]
    resultados = []
    for c in modales:
        idx = clases.index(c)
        d1 = c["fi"] - (clases[idx - 1]["fi"] if idx > 0 else 0)
        d2 = c["fi"] - (clases[idx + 1]["fi"] if idx < len(clases) - 1 else 0)
        denom = d1 + d2
        amp = c["ls"] - c["li"]
        moda = c["li"] + (d1 / denom * amp) if denom != 0 else c["marca"]
        resultados.append({"moda": round(moda, 4), "clase": c["clase"]})
    return resultados


def calc_percentil_detail(clases, n, p, t):
    """Calcula el percentil Pp y retorna un dict con detalles para mostrar paso a paso."""
    pos = (p / 100) * n
    fa_ant = 0
    for c in clases:
        if c["Fi"] >= pos:
            li = c["li"]
            fi = c["fi"]
            val = li + ((pos - fa_ant) / fi) * t
            return {
                "valor": round(val, 4),
                "clase": c["clase"],
                "li": li,
                "ls": c["ls"],
                "fi": fi,
                "fa_ant": fa_ant,
                "pos": pos,
                "p": p,
                "t": t
            }
        fa_ant = c["Fi"]
    return None


def interpret_media(media, min_val, max_val):
    return (f"La media aritmética es {media}. Esto significa que el promedio de los puntajes "
            f"obtenidos en el examen de suficiencia es de {media} puntos (escala {min_val}–{max_val}).")


def interpret_mediana(mediana, n):
    return (f"La mediana es {mediana}. El 50% de los {n} estudiantes obtuvo un puntaje "
            f"menor o igual a {mediana} puntos, y el otro 50% obtuvo más de {mediana} puntos.")


def interpret_moda(modas):
    if len(modas) == 1:
        return (f"La moda es {modas[0]['moda']}. Es el valor que aparece con mayor frecuencia "
                f"en la distribución (clase {modas[0]['clase']}).")
    vals = ", ".join(str(m["moda"]) for m in modas)
    return f"La distribución es bimodal/multimodal con modas en: {vals}."


def interpret_percentil(nombre, valor, p, n):
    return (f"El {nombre} ({p}° percentil) es {valor}. "
            f"Esto indica que el {p}% de los {n} estudiantes obtuvo un puntaje "
            f"menor o igual a {valor} puntos.")


# ─────────────────────────────────────────────
# RUTAS FLASK
# ─────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None
    raw_data = ""

    if request.method == "POST":
        raw_data = request.form.get("datos", "").strip()
        calcular = {
            "tabla":       "tabla"       in request.form,
            "media":       "media"       in request.form,
            "mediana":     "mediana"     in request.form,
            "moda":        "moda"        in request.form,
            "cuartiles":   "cuartiles"   in request.form,
            "deciles":     "deciles"     in request.form,
        }

        pk_request = request.form.get("percentil_k", "").strip()
        if pk_request.isdigit():
            calcular["percentil_k"] = int(pk_request)
        else:
            calcular["percentil_k"] = None

        try:
            data, max_dec = parse_data(raw_data)
            n = len(data)
            if n < 5:
                raise ValueError("Se necesitan al menos 5 datos.")

            clases, meta = build_frequency_table(data, max_dec)

            resultado = {
                # pasos del método
                "n":                 meta["n"],
                "d":                 meta["d"],
                "D":                 meta["D"],
                "unidad":            meta["unidad"],
                "la":                meta["la"],
                "k":                 meta["k"],
                "k_exacto":          meta["k_exacto"],
                "t_inicial":         round(meta["t_inicial"], max_dec + 1),
                "t":                 meta["t"],
                "t_k":               round(meta["t_k"], 4),
                "correction_applied": meta["correction_applied"],
                "sobrante":          meta.get("sobrante", 0),
                "unidades_sobra":    meta.get("unidades_sobra", 0),
                "mitad_inf":         meta.get("mitad_inf", 0),
                "mitad_sup":         meta.get("mitad_sup", 0),
                "nuevo_d":           meta.get("nuevo_d", meta["d"]),
                "nuevo_D":           meta.get("nuevo_D", meta["D"]),
                # tabla
                "clases":   clases,
                "calcular": calcular,
            }

            if calcular["media"] or calcular["mediana"] or calcular["moda"]:
                media = calc_media(clases, n)
                mediana, cls_med = calc_mediana(clases, n)
                modas = calc_moda(clases)

                resultado["media"]         = media
                resultado["media_interp"]  = interpret_media(media, meta["d"], meta["D"])
                resultado["mediana"]       = mediana
                resultado["mediana_clase"] = cls_med
                resultado["mediana_interp"]= interpret_mediana(mediana, n)
                resultado["modas"]         = modas
                resultado["moda_interp"]   = interpret_moda(modas)

            if calcular["cuartiles"]:
                resultado["cuartiles_lista"] = []
                for k in range(1, 4):
                    p = k * 25
                    res = calc_percentil_detail(clases, n, p, meta["t"])
                    if res:
                        resultado["cuartiles_lista"].append(res)
                        
            if calcular["deciles"]:
                resultado["deciles_lista"] = []
                for k in range(1, 10):
                    p = k * 10
                    res = calc_percentil_detail(clases, n, p, meta["t"])
                    if res:
                        resultado["deciles_lista"].append(res)

            if calcular["percentil_k"] is not None:
                p = calcular["percentil_k"]
                if 1 <= p <= 99:
                    res = calc_percentil_detail(clases, n, p, meta["t"])
                    resultado["percentil_detalle"] = res

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Error inesperado: {e}"

    return render_template("index.html", resultado=resultado, error=error, raw_data=raw_data)


if __name__ == "__main__":
    app.run(debug=True, port=5050)


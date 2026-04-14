from flask import Blueprint, render_template, request
from .parser import parse_data
from .tables import build_frequency_table
from .measures import (
    calc_media, calc_mediana, calc_moda, calc_percentil_detail,
    interpret_media, interpret_mediana, interpret_moda, interpret_percentil
)

from . import tablas_bp

@tablas_bp.route("/", methods=["GET", "POST"])
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
            
        metodo = request.form.get("metodo", "sturges")
        k_arbitrario = None
        if metodo == "arbitrario":
            k_arb_str = request.form.get("k_arbitrario", "").strip()
            if k_arb_str.isdigit():
                k_arbitrario = int(k_arb_str)

        try:
            data, max_dec = parse_data(raw_data)
            n = len(data)
            if n < 5:
                raise ValueError("Se necesitan al menos 5 datos.")

            clases, meta = build_frequency_table(data, max_dec, method=metodo, custom_k=k_arbitrario)

            resultado = {
                "n":                 meta["n"],
                "d":                 meta["d"],
                "D":                 meta["D"],
                "unidad":            meta["unidad"],
                "la":                meta["la"],
                "k":                 meta["k"],
                "k_exacto":          meta["k_exacto"],
                "metodo":            meta["metodo"],
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
            error = f"Error inesperado: {str(e)}"

    return render_template("tablas_index.html", resultado=resultado, error=error, raw_data=raw_data)

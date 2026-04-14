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

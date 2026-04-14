import math

def sturges(n: int) -> int:
    """Número de clases por la regla de Sturges (coef. 3.3)."""
    return round(1 + 3.3 * math.log10(n))

def build_frequency_table(data: list[float], max_dec: int, method: str = "sturges", custom_k: int = None):
    """
    Construye la tabla estadística adaptando la precisión (unidad de medida)
    pudiendo utilizar Sturges o un método Arbitrario (k dado).
    """
    n = len(data)
    d  = min(data)          # mínimo
    D  = max(data)          # máximo
    
    unit = 10 ** -max_dec if max_dec > 0 else 1
    la = round(D - d + unit, 10)   # longitud de alcance
    
    if method == "arbitrario" and custom_k is not None and custom_k > 0:
        k = custom_k
    else:
        k = sturges(n)

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
        "k_exacto": round(1 + 3.3 * math.log10(n), 4) if method != "arbitrario" else None,
        "metodo": method,
        "t_inicial": t_k_inicial / k if k else t,
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

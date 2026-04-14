import re

def parse_data(raw: str) -> tuple[list[float], int]:
    """Convierte texto en lista de floats y retorna la cantidad máx de decimales.
    Permite coma como decimal si no está seguida de un espacio."""
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

microrreductor = {
    "MALVIN FORCE": {
        "Trifásico": {
            "Potencia": [60, 90, 120],
            "Ratio": [5, 7.5, 10, 15, 20, 30, 40, 60, 90, 100],
        },
        "Monofásico": {
            "Fija": {
                "Potencia": [6, 15, 25, 40, 60, 90, 120, 140, 160, 180, 250],
                "Ratio": [5, 7.5, 10, 15, 20, 30, 40, 60, 90, 100],
            },
            "Variable": {
                "Potencia": [25, 40, 60, 90, 120, 180],
                "Ratio": [5, 7.5, 10, 15, 20, 30, 40, 60, 90, 100],
            },
        },
    },
    "K-VIN": {"Monofásico": {"Potencia": [60], "Ratio": [3]}},
}


def _fmt_size(val):
    try:
        return f"{int(float(val))}"
    except Exception:
        return str(val)


def _fmt_potencia(val):
    try:
        return f"{int(float(val))} W"
    except Exception:
        return str(val)


def _fmt_ratio(val):
    try:
        return f"{float(val)}:1"
    except Exception:
        return str(val)


def _filter_fmt_size(val):
    try:
        return int(val.strip())
    except Exception:
        return str(val)


def _filter_fmt_potencia(val):
    try:
        new_val = int(val.replace(" W", "").strip())
        print(new_val, type(new_val), sep=" ")
        return new_val
    except Exception:
        print("Can't convert to int")
        return str(val)


def _filter_fmt_ratio(val):
    try:
        return float(val.replace(":1", "").strip())
    except Exception:
        return str(val)

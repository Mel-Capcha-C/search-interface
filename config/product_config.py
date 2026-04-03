import microrreductor_config as mi
import reductor_sinfin_config

# ComboBox selection features
config = {
    "Microrreductor": {
        "Marca": {
            "cb_label": "Marca",
            "cb_format": str,
            "filter_format": str,
        },
        "Conexión": {
            "cb_label": "Conexión",
            "cb_format": str,
            "filter_format": str,
        },
        "Size": {
            "cb_label": "Tamaño",
            "cb_format": mi._fmt_size,
            "filter_format": mi._filter_fmt_size,
        },
        "Tipo Motor": {
            "cb_label": "Tipo Motor",
            "cb_format": str,
            "filter_format": str,
        },
        "Potencia": {
            "cb_label": "Potencia",
            "cb_format": mi._fmt_potencia,
            "filter_format": mi._filter_fmt_potencia,
        },
        "Ratio": {
            "cb_label": "Ratio",
            "cb_format": mi._fmt_ratio,
            "filter_format": mi._filter_fmt_ratio,
        },
    },
    # "Reductor Sinfín": {
    #     "features": ["Marca", "Conexión", "Velocidad", "Potencia", "Ratio"],
    #     "data": reductor_sinfin,
    # },
}

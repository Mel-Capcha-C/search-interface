from microrreductor_config import microrreductor
from reductor_sinfin_config import reductor_sinfin

config = {
    "Microrreductor": {
        "features": ["Marca", "Conexión", "Tipo Velocidad", "Potencia", "Ratio"],
        "data": microrreductor,
    },
    "Reductor Sinfín": {
        "features": ["Marca", "Conexión", "Velocidad", "Potencia", "Ratio"],
        "data": reductor_sinfin,
    },
}

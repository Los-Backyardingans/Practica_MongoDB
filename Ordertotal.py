from conexion import conectar_mongodb
from bson.decimal128 import Decimal128

conexion = conectar_mongodb()
db = conexion[1] if isinstance(conexion, tuple) else conexion


def num(v):
    if v is None:
        return 0.0
    if isinstance(v, Decimal128):
        return float(v.to_decimal())
    return float(v)


def sin_id(doc):
    if doc is None:
        return {}
    return {k: v for k, v in doc.items() if k != "_id"}

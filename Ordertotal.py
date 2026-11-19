
from conexion import conectar_mongodb
from decimal import Decimal
from bson.decimal128 import Decimal128


# ==========================================================
# FUNCIÓN: limpiar_documento
# ==========================================================

def limpiar_documento(documento):

    if documento is None:
        return None

    return {
        clave: valor
        for clave, valor in documento.items()
        if clave != "_id"
    }


# ==========================================================
# FUNCIÓN: convertir_decimal
# ==========================================================

def convertir_decimal(valor):

    if isinstance(valor, Decimal128):
        return valor.to_decimal()

    if isinstance(valor, Decimal):
        return valor

    if valor is None:
        return Decimal("0")

    return Decimal(str(valor))


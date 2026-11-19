from conexion import conectar_mongodb
from decimal import Decimal
from bson.decimal128 import Decimal128

# =============================
# CONEXIÓN Y UTILIDADES
# =============================

def obtener_base_datos():
    conexion = conectar_mongodb()

    if isinstance(conexion, tuple):
        cliente, db = conexion
    else:
        # Si devuelve directamente la base de datos.
        if hasattr(conexion, "list_collection_names"):
            db = conexion
            cliente = None
        else:
            # Si devuelve, solamente el cliente MongoDB.
            cliente = conexion
            db = cliente["Northwind"]

    return cliente, db

def convertir_decimal(valor):
    if isinstance(valor, Decimal128):
        return valor.to_decimal()

    if isinstance(valor, Decimal):
        return valor

    if valor is None:
        return Decimal("0")

    return Decimal(str(valor))


def mostrar_documento(documento):

    if documento is None:
        print("No hay información disponible.")
        return

    for campo, valor in documento.items():
        if campo != "_id":
            print(f"{campo}: {valor}")

# ==========================================================
# Archivo: migracion.py
# Descripción:
# Migrar todas las tablas de MySQL hacia colecciones
# equivalentes en MongoDB.
#
# También convierte los valores Decimal de MySQL a
# Decimal128 para conservar la precisión de los datos.
# ==========================================================


# Importamos las funciones de conexión
from conexion import conectar_mysql, conectar_mongodb

# Importamos Decimal para identificar valores decimales
from decimal import Decimal

# Importamos Decimal128 para almacenar decimales en MongoDB
from bson.decimal128 import Decimal128


# ==========================================================
# FUNCIÓN: convertir_valores
# ==========================================================

def convertir_valores(registro):
    """
    Convierte los valores Decimal de MySQL a Decimal128,
    formato compatible con MongoDB.

    Recibe:
        registro: diccionario con los datos de una fila.

    Retorna:
        Un diccionario con los valores preparados para MongoDB.
    """

    documento = {}

    for columna, valor in registro.items():

        # Comprobar si el valor es de tipo Decimal
        if isinstance(valor, Decimal):

            # Convertir Decimal a Decimal128
            documento[columna] = Decimal128(valor)

        else:

            # Mantener los demás valores sin modificaciones
            documento[columna] = valor

    return documento


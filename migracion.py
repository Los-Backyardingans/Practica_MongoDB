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


# ==========================================================
# FUNCIÓN PRINCIPAL: migrar_datos
# ==========================================================

def migrar_datos():
    """
    Obtiene todas las tablas físicas de MySQL y migra
    sus registros a colecciones de MongoDB.
    """

    # Inicializar las variables de conexión
    conexion_mysql = None
    cursor = None
    cliente_mongo = None

    try:

        # ==================================================
        # 1. CONECTAR CON MYSQL
        # ==================================================

        conexion_mysql = conectar_mysql()

        if conexion_mysql is None:
            print("No fue posible conectar con MySQL.")
            return

        # ==================================================
        # 2. CONECTAR CON MONGODB
        # ==================================================

        cliente_mongo, base_datos = conectar_mongodb()

        if cliente_mongo is None or base_datos is None:
            print("No fue posible conectar con MongoDB.")
            return

        # ==================================================
        # 3. CREAR CURSOR MYSQL
        # ==================================================

        cursor = conexion_mysql.cursor()

        # ==================================================
        # 4. OBTENER TODAS LAS TABLAS FÍSICAS DE MYSQL
        # ==================================================

        cursor.execute(
            "SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'"
        )

        tablas = cursor.fetchall()

        print("\n==========================================")
        print("       MIGRACIÓN DE DATOS NORTHWIND")
        print("==========================================")

        # Verificar que existan tablas
        if not tablas:
            print("No se encontraron tablas en MySQL.")
            return

        # Variables para contabilizar los resultados
        total_tablas = 0
        total_registros = 0

        # ==================================================
        # 5. RECORRER TODAS LAS TABLAS
        # ==================================================

        for tabla in tablas:

            # Obtener el nombre de la tabla
            nombre_tabla = tabla[0]

            print(f"\nMigrando tabla: {nombre_tabla}")

            # ==================================================
            # 6. CONSULTAR LOS REGISTROS DE MYSQL
            # ==================================================

            cursor.execute(f"SELECT * FROM `{nombre_tabla}`")

            registros = cursor.fetchall()

            # Obtener los nombres de las columnas
            columnas = cursor.column_names

            # ==================================================
            # 7. CONVERTIR LOS REGISTROS EN DOCUMENTOS
            # ==================================================

            documentos = []



# ==========================================================
# Practica MongoDB - PROGRAMACIÓN II
# Archivo: conexion.py
# Descripción:
# Este permite conectar Python con MySQL y MongoDB.
# ==========================================================

import mysql.connector
from pymongo import MongoClient

# 1. CONEXIÓN CON MYSQL
def conectar_mysql():
    """
    Establece una conexión con la base de datos NorthWind
    almacenada en el servidor MySQL.
    """

    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="parda99*",
            database="NorthWind"
        )

        if conexion.is_connected():
            print("Conexión con MySQL exitosa.")

        return conexion

    except mysql.connector.Error as error:
        print("Error al conectar con MySQL:", error)
        return None

# 2. CONEXIÓN CON MONGODB
def conectar_mongodb():
    """
    Establece una conexión con el servidor MongoDB
    y selecciona la base de datos Northwind.
    """

    try:
        cliente = MongoClient(
            "mongodb://admin:parda99*@127.0.0.1:27017/?authSource=admin",
            serverSelectionTimeoutMS=5000
        )

        # Comprobar que MongoDB responde
        cliente.admin.command("ping")

        # Seleccionar la base de datos
        db = cliente["Northwind"]

        print("Conexión con MongoDB exitosa.")

        return cliente, db

    except Exception as error:
        print("Error al conectar con MongoDB:", error)
        return None, None

# 3. PROGRAMA PRINCIPAL DE PRUEBA
if __name__ == "__main__":

    print("CONEXIONES DEL PRACTICA NORTHWIND MDB ")

    mysql = conectar_mysql()

    mongo_cliente, mongo_db = conectar_mongodb()

    # Cerrar las conexiones al finalizar la prueba
    if mysql is not None:
        mysql.close()
        print("Conexión MySQL cerrada.")

    if mongo_cliente is not None:
        mongo_cliente.close()
        print("Conexión MongoDB cerrada.")

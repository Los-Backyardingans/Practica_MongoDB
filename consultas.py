from conexion import conectar_mongodb


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


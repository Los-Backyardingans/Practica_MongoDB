
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

# ==============================================
# CONSULTA 1: LISTAR CATEGORÍAS Y SUS PRODUCTOS
# ==============================================

def listar_categorias_productos():
    #Consulta las colecciones categories y products.

    cliente, db = obtener_base_datos()

    try:
        categorias = db["categories"]
        productos = db["products"]

        print("\n=========================================")
        print("       CATEGORÍAS Y SUS PRODUCTOS")
        print("==========================================")

        # Obtener todas las categorías.
        lista_categorias = categorias.find().sort("CategoryID", 1)

        for categoria in lista_categorias:

            category_id = categoria.get("CategoryID")
            category_name = categoria.get("CategoryName")

            print(f"\nCategoría: {category_id} - {category_name}")
            print("-" * 55)

            # Buscar los productos que pertenecen a la categoría.
            lista_productos = productos.find(
                {"CategoryID": category_id}
            ).sort("ProductID", 1)

            encontrados = 0

            for producto in lista_productos:

                print(
                    f"Código: {producto.get('ProductID')} | "
                    f"Producto: {producto.get('ProductName')}"
                )

                encontrados += 1

            if encontrados == 0:
                print("Esta categoría no tiene productos.")

        print("\nConsulta finalizada.")

    finally:
        if cliente is not None:
            cliente.close()

            # ==============================================
            # CONSULTA 2: INVENTARIO POR CATEGORÍA
            # ==============================================

            def consultar_inventario():

                cliente, db = obtener_base_datos()

                try:
                    categorias = db["categories"]
                    productos = db["products"]

                    category_id = int(input("Digite el código de la categoría: "))

                    categoria = categorias.find_one({"CategoryID": category_id})

                    if categoria is None:
                        print("Categoría no encontrada.")
                        return

                    print("\nCategoría:", categoria.get("CategoryName"))
                    print("-" * 75)
                    print("Código    Producto                  Precio    Existencia    Total")

                    total_categoria = 0

                    lista_productos = productos.find({"CategoryID": category_id})

                    for producto in lista_productos:
                        codigo = producto.get("ProductID")
                        nombre = producto.get("ProductName")
                        precio = convertir_decimal(producto.get("UnitPrice"))
                        existencia = producto.get("UnitsInStock") or 0

                        total = precio * existencia
                        total_categoria += total

                        print(codigo, nombre, precio, existencia, total)

                    print("-" * 75)
                    print("TOTAL DE LA CATEGORÍA:", total_categoria)

                finally:
                    if cliente is not None:
                        cliente.close()


# ==============================================
# CONSULTA 3: FACTURA COMPLETA
# ==============================================

def consultar_factura():

    cliente, db = obtener_base_datos()

    try:
        ordertotal = db["Ordertotal"]

        order_id = int(input("Digite el número del pedido: "))

        pipeline = [
            {"$match": {"OrderID": order_id}}
        ]

        factura = list(ordertotal.aggregate(pipeline))

        if len(factura) == 0:
            print("No se encontró la factura.")
            return

        factura = factura[0]

        print("\n========== FACTURA ==========")

        print("Número de pedido:", factura.get("OrderID"))

        print("\n--- CLIENTE ---")
        mostrar_documento(factura.get("Customer"))

        print("\n--- EMPLEADO ---")
        mostrar_documento(factura.get("Employee"))

        print("\n--- PRODUCTOS ---")

        for detalle in factura.get("Details", []):

            mostrar_documento(detalle.get("Product"))

            print("Cantidad:", detalle.get("Quantity"))
            print("Precio:", detalle.get("UnitPrice"))
            print("Descuento:", detalle.get("Discount"))
            print("Total:", detalle.get("LineTotal"))
            print("--------------------------")

        print("\nTOTAL DE LA FACTURA:", factura.get("InvoiceTotal"))

    finally:
        if cliente is not None:
            cliente.close()


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


# ==========================================================
# FUNCIÓN PRINCIPAL: crear_ordertotal
# ==========================================================

def crear_ordertotal():

    cliente_mongo = None

    try:

        cliente_mongo, base_datos = conectar_mongodb()

        if cliente_mongo is None or base_datos is None:
            print("No fue posible conectar con MongoDB.")
            return

        print("\n==========================================")
        print("       CONSTRUCCIÓN DE ORDERTOTAL")
        print("==========================================")

        pedidos = list(base_datos["orders"].find())
        clientes = list(base_datos["customers"].find())
        empleados = list(base_datos["employees"].find())
        transportistas = list(base_datos["shippers"].find())
        productos = list(base_datos["products"].find())
        detalles = list(base_datos["order_details"].find())

        print(f"\nPedidos encontrados: {len(pedidos)}")

        mapa_clientes = {
            cliente["CustomerID"]: cliente
            for cliente in clientes
        }

        mapa_empleados = {
            empleado["EmployeeID"]: empleado
            for empleado in empleados
        }

        mapa_transportistas = {
            transportista["ShipperID"]: transportista
            for transportista in transportistas
        }

        mapa_productos = {
            producto["ProductID"]: producto
            for producto in productos
        }

        detalles_por_pedido = {}

        for detalle in detalles:

            numero_pedido = detalle["OrderID"]

            if numero_pedido not in detalles_por_pedido:
                detalles_por_pedido[numero_pedido] = []

            detalles_por_pedido[numero_pedido].append(detalle)

        documentos_ordertotal = []

        for pedido in pedidos:

            numero_pedido = pedido["OrderID"]
            codigo_cliente = pedido.get("CustomerID")
            codigo_empleado = pedido.get("EmployeeID")
            codigo_transportista = pedido.get("ShipVia")

            cliente = mapa_clientes.get(codigo_cliente)
            empleado = mapa_empleados.get(codigo_empleado)
            transportista = mapa_transportistas.get(
                codigo_transportista
            )

            detalles_pedido = detalles_por_pedido.get(
                numero_pedido, []
            )

            lista_detalles = []

            total_factura = Decimal("0")

            for detalle in detalles_pedido:
                codigo_producto = detalle["ProductID"]

                producto = mapa_productos.get(codigo_producto)

                precio = convertir_decimal(
                    detalle.get("UnitPrice")
                )

                cantidad = detalle.get("Quantity", 0)

                descuento = convertir_decimal(
                    detalle.get("Discount")
                )

                total_linea = (
                        precio
                        * Decimal(str(cantidad))
                        * (Decimal("1") - descuento)
                )

                total_factura += total_linea

                documento_detalle = {

                    "Product": limpiar_documento(producto),

                    "ProductID": codigo_producto,
                    "Quantity": cantidad,
                    "UnitPrice": Decimal128(precio),
                    "Discount": Decimal128(descuento),
                    "LineTotal": Decimal128(total_linea)
                }

                lista_detalles.append(documento_detalle)

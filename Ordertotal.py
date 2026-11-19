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


def crear_ordertotal():
    clientes = {c["CustomerID"]: c for c in db["customers"].find()}
    empleados = {e["EmployeeID"]: e for e in db["employees"].find()}
    shippers = {s["ShipperID"]: s for s in db["shippers"].find()}
    categorias = {c["CategoryID"]: c for c in db["categories"].find()}
    productos = {p["ProductID"]: p for p in db["products"].find()}

    detalles_por_orden = {}
    for d in db["order_details"].find():
        detalles_por_orden.setdefault(d["OrderID"], []).append(d)

    documentos = []
    for o in db["orders"].find():
        lineas = []
        total = 0.0

        for d in detalles_por_orden.get(o["OrderID"], []):
            prod = productos.get(d["ProductID"], {})
            cat = categorias.get(prod.get("CategoryID"), {})

            precio = num(d.get("UnitPrice"))
            cantidad = num(d.get("Quantity"))
            descuento = num(d.get("Discount"))
            linea = round(precio * cantidad * (1 - descuento), 2)
            total += linea

            lineas.append({
                "Product": {
                    "ProductID": prod.get("ProductID"),
                    "ProductName": prod.get("ProductName"),
                    "CategoryID": prod.get("CategoryID"),
                    "CategoryName": cat.get("CategoryName"),
                },
                "UnitPrice": precio,
                "Quantity": cantidad,
                "Discount": descuento,
                "LineTotal": linea,
            })

        doc = sin_id(o)
        doc["Customer"] = sin_id(clientes.get(o.get("CustomerID")))
        doc["Employee"] = sin_id(empleados.get(o.get("EmployeeID")))
        doc["Shipper"] = sin_id(shippers.get(o.get("ShipVia")))
        doc["Details"] = lineas
        doc["InvoiceTotal"] = round(total + num(o.get("Freight")), 2)
        documentos.append(doc)

    db["Ordertotal"].drop()
    if documentos:
        db["Ordertotal"].insert_many(documentos)
    print(f"Ordertotal creada con {len(documentos)} pedidos.")


if __name__ == "__main__":
    crear_ordertotal()
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

# ⬇️ Importamos la "base de datos" desde archivo externo
from eventos import eventos

app = Flask(__name__)


@app.route("/")
def index():
    # Ordenar eventos por fecha ascendente (los más próximos primero)
    eventos_ordenados = sorted(
        eventos,
        key=lambda e: datetime.strptime(e["fecha"], "%Y-%m-%d")
    )

    return render_template("index.html", eventos=eventos_ordenados)


@app.route("/evento/<int:event_id>")
def evento_detalle(event_id):
    # Buscar evento por id
    evento = next((e for e in eventos if e["id"] == event_id), None)
    if not evento:
        return "Evento no encontrado", 404
    return render_template("evento.html", evento=evento)



@app.route("/agregar_evento", methods=["POST"])
def agregar_evento():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    tipo = request.form.get("tipo")
    fecha = request.form.get("fecha")
    hora = request.form.get("hora")
    costo = request.form.get("costo") or "0"

    # LUGAR LARGO PARA MAPS
    lugar = request.form.get("lugar")

    # LUGAR CORTO (visible)
    mapping_corto = {
        "General Alvear Mendoza": "General Alvear",
        "Bowen General Alvear Mendoza": "Bowen",
        "San Pedro del Atuel General Alvear Mendoza": "San Pedro del Atuel",
        "Alvear Oeste General Alvear Mendoza": "Alvear Oeste"
    }
    lugar_corto = mapping_corto.get(lugar, lugar)

    # NUEVO CAMPO
    direccion = request.form.get("direccion")

    imagen = request.form.get("imagen") or \
        "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=400&fit=crop"

    nuevo_evento = {
    "id": len(eventos),  # <-- id único
    "nombre": nombre,
    "descripcion": descripcion,
    "tipo": tipo,
    "fecha": fecha,
    "hora": hora,
    "costo": costo,
    "lugar": lugar,             # largo para Maps
    "lugar_corto": lugar_corto, # corto visible
    "direccion": direccion,     # nuevo
    "imagen": imagen
}


    # Guardamos en la "base de datos"
    eventos.append(nuevo_evento)

    return redirect(url_for("index"))


# En app.py, agrégalo debajo de las otras rutas
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


if __name__ == "__main__":
    app.run(debug=True)

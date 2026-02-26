from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


FastAPI_URL = "http://localhost:5000"

@app.route("/")
def index():
    r = requests.get(f"{FastAPI_URL}/v1/usuarios/")
    usuarios = r.json().get("Usuarios", [])
    return render_template("index.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar():
    nuevo = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    requests.post(f"{FastAPI_URL}/v1/usuarios/", json=nuevo)
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    requests.delete(f"{FastAPI_URL}/v1/usuarios/{id}")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=5010, debug=True)
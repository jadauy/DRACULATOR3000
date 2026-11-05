"""Guardado de donantes en un archivo .txt (una línea por donante, separado por ';')."""

import csv
import os

COLUMNAS = ("rut", "nombre", "fecha_nacimiento", "sexo", "peso", "tipo_sangre", "telefono")
RUTA_POR_DEFECTO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "donantes.txt")


class RepositorioDonantes:
    def __init__(self, ruta=RUTA_POR_DEFECTO):
        self.ruta = ruta

    def listar(self):
        if not os.path.exists(self.ruta):
            return []
        with open(self.ruta, encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo, fieldnames=COLUMNAS, delimiter=";")
            return [dict(fila) for fila in lector if fila.get("rut")]

    def buscar_por_rut(self, rut):
        for donante in self.listar():
            if donante["rut"] == rut:
                return donante
        return None

    def guardar(self, donante):
        carpeta = os.path.dirname(self.ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        with open(self.ruta, "a", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS, delimiter=";")
            escritor.writerow({c: donante[c] for c in COLUMNAS})

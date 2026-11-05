"""Reglas de validación de los datos de un donante (H1 · Registrar donante)."""

import re
from datetime import date, datetime

from .rut import validar_rut

TIPOS_SANGRE = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
SEXOS = ("F", "M")
FORMATO_FECHA = "%d-%m-%Y"  # Ej: 25-12-1990

CAMPOS_OBLIGATORIOS = (
    "rut",
    "nombre",
    "fecha_nacimiento",
    "sexo",
    "peso",
    "tipo_sangre",
    "telefono",
)


def validar_nombre(nombre):
    if len(nombre.strip()) < 2:
        return "El nombre debe tener al menos 2 caracteres."
    if any(c.isdigit() for c in nombre):
        return "El nombre no puede contener números."
    return None


def parsear_fecha(texto):
    return datetime.strptime(texto.strip(), FORMATO_FECHA).date()


def validar_fecha_nacimiento(texto, hoy=None):
    hoy = hoy or date.today()
    try:
        fecha = parsear_fecha(texto)
    except ValueError:
        return "Fecha inválida, use el formato DD-MM-AAAA."
    if fecha > hoy:
        return "La fecha de nacimiento no puede ser futura."
    return None


def validar_sexo(sexo):
    if sexo.strip().upper() not in SEXOS:
        return "El sexo debe ser F o M."
    return None


def validar_peso(texto):
    try:
        peso = float(str(texto).replace(",", "."))
    except ValueError:
        return "El peso debe ser un número."
    if peso <= 0:
        return "El peso debe ser un número positivo."
    return None


def normalizar_tipo_sangre(tipo):
    # Acepta también el signo menos tipográfico (−) además del guion normal.
    return tipo.strip().upper().replace("−", "-")


def validar_tipo_sangre(tipo):
    if normalizar_tipo_sangre(tipo) not in TIPOS_SANGRE:
        return "Tipo de sangre inválido. Opciones: " + ", ".join(TIPOS_SANGRE)
    return None


def limpiar_telefono(telefono):
    return re.sub(r"[\s\-()]", "", telefono)


def validar_telefono(telefono):
    """Celular chileno: 9 dígitos que empiezan con 9, con o sin +56."""
    limpio = limpiar_telefono(telefono)
    if not re.fullmatch(r"(\+?56)?9\d{8}", limpio):
        return "Teléfono inválido (ej: +56 9 1234 5678)."
    return None


VALIDADORES = {
    "rut": validar_rut,
    "nombre": validar_nombre,
    "fecha_nacimiento": validar_fecha_nacimiento,
    "sexo": validar_sexo,
    "peso": validar_peso,
    "tipo_sangre": validar_tipo_sangre,
    "telefono": validar_telefono,
}


def validar_campo(campo, valor):
    """Valida un solo campo. Devuelve None si está bien, o el mensaje de error."""
    valor = str(valor or "").strip()
    if not valor:
        return "Campo obligatorio."
    return VALIDADORES[campo](valor)


def validar_donante(datos):
    """Valida todos los campos.

    Devuelve un diccionario {campo: mensaje de error}. Si está vacío, los
    datos son válidos. Así la interfaz puede mostrar el error en cada campo.
    """
    errores = {}
    for campo in CAMPOS_OBLIGATORIOS:
        error = validar_campo(campo, datos.get(campo))
        if error:
            errores[campo] = error
    return errores

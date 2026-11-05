"""Validación y formato del RUT chileno (módulo 11)."""

import re


def limpiar_rut(rut):
    """Quita puntos, guiones y espacios, y pasa la K a mayúscula."""
    return re.sub(r"[.\-\s]", "", str(rut)).upper()


def calcular_dv(cuerpo):
    """Calcula el dígito verificador (módulo 11) del cuerpo numérico del RUT."""
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_rut(rut):
    """Devuelve None si el RUT es válido, o un mensaje de error."""
    limpio = limpiar_rut(rut)
    if not re.fullmatch(r"\d{7,8}[\dK]", limpio):
        return "Formato de RUT inválido (ej: 12.345.678-5)."
    cuerpo, dv = limpio[:-1], limpio[-1]
    if calcular_dv(cuerpo) != dv:
        return "El dígito verificador del RUT es incorrecto."
    return None


def normalizar_rut(rut):
    """Deja el RUT como '12345678-5', que es como se guarda y se busca."""
    limpio = limpiar_rut(rut)
    return f"{limpio[:-1]}-{limpio[-1]}"

"""Menú de consola para registrar y buscar donantes."""

from donantes.servicio import DatosInvalidosError, DonanteDuplicadoError, ServicioDonantes
from donantes.validaciones import TIPOS_SANGRE, validar_campo

ETIQUETAS = {
    "rut": "RUT (ej: 12.345.678-5)",
    "nombre": "Nombre completo",
    "fecha_nacimiento": "Fecha de nacimiento (DD-MM-AAAA)",
    "sexo": "Sexo (F/M)",
    "peso": "Peso en kg",
    "tipo_sangre": "Tipo de sangre (" + ", ".join(TIPOS_SANGRE) + ")",
    "telefono": "Teléfono (ej: +56 9 1234 5678)",
}


def pedir_campo(campo):
    """Pide un dato y lo vuelve a pedir hasta que sea válido."""
    while True:
        valor = input(f"  {ETIQUETAS[campo]}: ")
        error = validar_campo(campo, valor)
        if error is None:
            return valor
        print(f"    ✘ {error}")


def registrar(servicio):
    print("\n--- Registrar donante ---")
    datos = {"rut": pedir_campo("rut")}

    # El RUT duplicado se revisa al tiro, antes de pedir el resto de los datos.
    if servicio.buscar_por_rut(datos["rut"]):
        print("\n✘ Ya existe un donante registrado con ese RUT.")
        return

    for campo in ETIQUETAS:
        if campo != "rut":
            datos[campo] = pedir_campo(campo)

    try:
        donante = servicio.registrar(datos)
        print(f"\n✔ Donante {donante['nombre']} ({donante['rut']}) registrado correctamente.")
    except DatosInvalidosError as e:
        print("\n✘ No se pudo registrar. Revise los siguientes campos:")
        for campo, mensaje in e.errores.items():
            print(f"   - {ETIQUETAS[campo]}: {mensaje}")
    except DonanteDuplicadoError as e:
        print(f"\n✘ {e}")


def buscar(servicio):
    print("\n--- Buscar donante ---")
    rut = input("  RUT: ")
    donante = servicio.buscar_por_rut(rut)
    if not donante:
        print("\nNo se encontró un donante con ese RUT.")
        return
    print()
    for campo, etiqueta in ETIQUETAS.items():
        print(f"  {etiqueta.split(' (')[0]}: {donante[campo]}")


def main():
    servicio = ServicioDonantes()
    opciones = {"1": registrar, "2": buscar}
    while True:
        print("\n=== DRACULATOR 3000 ===")
        print("1. Registrar donante")
        print("2. Buscar donante por RUT")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            break
        accion = opciones.get(opcion)
        if accion:
            accion(servicio)
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

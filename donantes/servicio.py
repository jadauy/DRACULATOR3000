"""Lógica de negocio: registrar y buscar donantes."""

from . import validaciones as v
from .repositorio import RepositorioDonantes
from .rut import normalizar_rut, validar_rut


class DonanteDuplicadoError(Exception):
    pass


class DatosInvalidosError(Exception):
    def __init__(self, errores):
        super().__init__("Datos inválidos")
        self.errores = errores  # {campo: mensaje}


class ServicioDonantes:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio or RepositorioDonantes()

    def registrar(self, datos):
        """Valida y guarda un donante. Lanza excepción si algo falla."""
        errores = v.validar_donante(datos)
        if errores:
            raise DatosInvalidosError(errores)

        donante = self._normalizar(datos)
        if self.repositorio.buscar_por_rut(donante["rut"]):
            raise DonanteDuplicadoError(f"El donante con RUT {donante['rut']} ya existe.")

        self.repositorio.guardar(donante)
        return donante

    def buscar_por_rut(self, rut):
        if validar_rut(rut):
            return None
        return self.repositorio.buscar_por_rut(normalizar_rut(rut))

    @staticmethod
    def _normalizar(datos):
        """Deja los datos en un formato uniforme antes de guardarlos."""
        return {
            "rut": normalizar_rut(datos["rut"]),
            "nombre": " ".join(str(datos["nombre"]).split()),
            "fecha_nacimiento": v.parsear_fecha(datos["fecha_nacimiento"]).strftime(v.FORMATO_FECHA),
            "sexo": datos["sexo"].strip().upper(),
            "peso": str(float(str(datos["peso"]).replace(",", "."))),
            "tipo_sangre": v.normalizar_tipo_sangre(datos["tipo_sangre"]),
            "telefono": v.limpiar_telefono(datos["telefono"]),
        }

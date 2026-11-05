import os
import tempfile
import unittest

from donantes.repositorio import RepositorioDonantes
from donantes.servicio import DatosInvalidosError, DonanteDuplicadoError, ServicioDonantes


def datos_validos(**cambios):
    datos = {
        "rut": "12.345.678-5",
        "nombre": "Ana Pérez",
        "fecha_nacimiento": "15-03-1990",
        "sexo": "F",
        "peso": "62",
        "tipo_sangre": "O+",
        "telefono": "+56 9 1234 5678",
    }
    datos.update(cambios)
    return datos


class TestServicioDonantes(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.carpeta.name, "donantes.txt")
        self.servicio = ServicioDonantes(RepositorioDonantes(self.ruta))

    def tearDown(self):
        self.carpeta.cleanup()

    def test_registro_exitoso_guarda_en_txt(self):
        donante = self.servicio.registrar(datos_validos())
        self.assertEqual(donante["rut"], "12345678-5")
        with open(self.ruta, encoding="utf-8") as f:
            self.assertIn("12345678-5;Ana Pérez", f.read())

    def test_rut_duplicado_se_rechaza(self):
        self.servicio.registrar(datos_validos())
        with self.assertRaises(DonanteDuplicadoError):
            # Mismo RUT escrito de otra forma
            self.servicio.registrar(datos_validos(rut="123456785", nombre="Otra Persona"))

    def test_rut_invalido_no_se_guarda(self):
        with self.assertRaises(DatosInvalidosError) as ctx:
            self.servicio.registrar(datos_validos(rut="12.345.678-9"))
        self.assertIn("rut", ctx.exception.errores)
        self.assertFalse(os.path.exists(self.ruta))

    def test_campos_faltantes_no_se_guarda(self):
        with self.assertRaises(DatosInvalidosError) as ctx:
            self.servicio.registrar(datos_validos(peso="", telefono=""))
        self.assertEqual(set(ctx.exception.errores), {"peso", "telefono"})
        self.assertFalse(os.path.exists(self.ruta))

    def test_buscar_por_rut_muestra_datos(self):
        self.servicio.registrar(datos_validos())
        encontrado = self.servicio.buscar_por_rut("12.345.678-5")
        self.assertEqual(encontrado["nombre"], "Ana Pérez")
        self.assertEqual(encontrado["tipo_sangre"], "O+")

    def test_buscar_rut_inexistente(self):
        self.assertIsNone(self.servicio.buscar_por_rut("11.111.111-1"))

    def test_datos_persisten_entre_instancias(self):
        self.servicio.registrar(datos_validos())
        otro = ServicioDonantes(RepositorioDonantes(self.ruta))
        self.assertIsNotNone(otro.buscar_por_rut("12345678-5"))


if __name__ == "__main__":
    unittest.main()

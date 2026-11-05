import unittest

from donantes import rut


class TestRut(unittest.TestCase):
    def test_ruts_validos_en_distintos_formatos(self):
        for r in ("12.345.678-5", "12345678-5", "123456785", "11.111.111-1", "10.000.013-k"):
            self.assertIsNone(rut.validar_rut(r), r)

    def test_digito_verificador_incorrecto(self):
        self.assertIn("verificador", rut.validar_rut("12.345.678-9"))

    def test_formato_invalido(self):
        for r in ("abc", "123", "12.345.678-Z"):
            self.assertIn("Formato", rut.validar_rut(r), r)

    def test_normalizar(self):
        self.assertEqual(rut.normalizar_rut("10.000.013-k"), "10000013-K")


if __name__ == "__main__":
    unittest.main()

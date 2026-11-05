import unittest
from datetime import date, timedelta

from donantes import validaciones as v


class TestTipoSangre(unittest.TestCase):
    def test_los_8_grupos_son_validos(self):
        for tipo in ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O−"):
            self.assertIsNone(v.validar_tipo_sangre(tipo), tipo)

    def test_otros_valores_se_rechazan(self):
        for tipo in ("C+", "A", "AB", "O+-"):
            self.assertIsNotNone(v.validar_tipo_sangre(tipo), tipo)


class TestPesoYFecha(unittest.TestCase):
    def test_peso_positivo(self):
        self.assertIsNone(v.validar_peso("70.5"))
        self.assertIsNone(v.validar_peso("70,5"))

    def test_peso_cero_negativo_o_texto(self):
        for peso in ("0", "-5", "setenta"):
            self.assertIsNotNone(v.validar_peso(peso), peso)

    def test_fecha_pasada_valida(self):
        self.assertIsNone(v.validar_fecha_nacimiento("15-03-1990"))

    def test_fecha_futura_rechazada(self):
        manana = (date.today() + timedelta(days=1)).strftime(v.FORMATO_FECHA)
        self.assertIn("futura", v.validar_fecha_nacimiento(manana))

    def test_fecha_mal_escrita(self):
        for fecha in ("1990-03-15", "31-02-1990", "hola"):
            self.assertIsNotNone(v.validar_fecha_nacimiento(fecha), fecha)


class TestOtrosCampos(unittest.TestCase):
    def test_telefono(self):
        for tel in ("+56 9 1234 5678", "912345678", "56912345678"):
            self.assertIsNone(v.validar_telefono(tel), tel)
        for tel in ("1234", "+56 2 1234 5678"):
            self.assertIsNotNone(v.validar_telefono(tel), tel)

    def test_sexo(self):
        self.assertIsNone(v.validar_sexo("f"))
        self.assertIsNotNone(v.validar_sexo("X"))


class TestCamposFaltantes(unittest.TestCase):
    def test_senala_todos_los_campos_faltantes(self):
        errores = v.validar_donante({"rut": "12.345.678-5", "nombre": "Ana Pérez"})
        self.assertEqual(
            set(errores),
            {"fecha_nacimiento", "sexo", "peso", "tipo_sangre", "telefono"},
        )
        self.assertTrue(all(m == "Campo obligatorio." for m in errores.values()))


if __name__ == "__main__":
    unittest.main()

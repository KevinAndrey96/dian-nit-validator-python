"""
Suite de pruebas unitarias para nit_validator.
"""

import unittest
from nit_validator import calcular_dv, validar_nit, formatear_nit, NITValidator
from verification import verificar_nit


class TestNITValidator(unittest.TestCase):

    def test_calcular_dv_empresas_colombianas(self):
        casos = [
            ("860007386", 1),  # Bancolombia S.A.
            ("899999068", 1),  # Ecopetrol S.A.
            ("890900050", 1),  # Grupo Nutresa S.A.
            ("890900608", 9),  # Almacenes Éxito S.A.
            ("800197268", 4),  # DIAN (Dirección de Impuestos y Aduanas Nacionales)
            ("800000008", 0),  # Residuo 0 -> DV 0
            ("800000001", 1),  # Residuo 1 -> DV 1
            (860007386, 1),    # Entrada como entero
            ("860.007.386", 1),# Entrada con puntos
        ]
        for nit, dv_esperado in casos:
            with self.subTest(nit=nit, dv_esperado=dv_esperado):
                self.assertEqual(calcular_dv(nit), dv_esperado)
                self.assertEqual(NITValidator.calcular_dv(nit), dv_esperado)

    def test_validar_nit_formatos(self):
        # NITs válidos con diferentes formatos
        self.assertTrue(validar_nit("860007386-1"))
        self.assertTrue(validar_nit("860.007.386-1"))
        self.assertTrue(validar_nit("860007386", 1))
        self.assertTrue(validar_nit("860007386", "1"))
        self.assertTrue(validar_nit(860007386, 1))

        # NITs inválidos
        self.assertFalse(validar_nit("860007386-2"))
        self.assertFalse(validar_nit("860007386", 9))
        self.assertFalse(validar_nit("860007386", "X"))

    def test_formatear_nit(self):
        self.assertEqual(formatear_nit(860007386), "860.007.386-1")
        self.assertEqual(formatear_nit("860007386", incluir_dv=False), "860.007.386")
        self.assertEqual(formatear_nit("860.007.386-1"), "860.007.386-1")

    def test_compatibilidad_historica(self):
        self.assertTrue(verificar_nit(860007386, 1))
        self.assertFalse(verificar_nit(860007386, 5))

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            calcular_dv("ABCDE")
        with self.assertRaises(ValueError):
            calcular_dv("")
        with self.assertRaises(ValueError):
            # Excede los 15 dígitos máximos soportados por la DIAN
            calcular_dv("123456789012345678")


if __name__ == '__main__':
    unittest.main()

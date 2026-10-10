import unittest
from red_empresarial import RedEmpresarial, RegistroRedes


class TestRedEmpresarial(unittest.TestCase):

    def setUp(self):
        self.registro = RegistroRedes()

        self.gerencia = RedEmpresarial(
            nombre="GERENCIA",
            cidr="10.10.0.0/24",
            vlan_id=10,
            gateway="10.10.0.1"
        )

        self.registro.agregar_red(self.gerencia)

    def test_buscar_red_por_vlan_existente(self):
        resultado = self.registro.buscar_red_por_vlan(10)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "GERENCIA")
        self.assertEqual(resultado.vlan_id, 10)

    def test_buscar_red_por_vlan_inexistente(self):
        resultado = self.registro.buscar_red_por_vlan(30)

        self.assertIsNone(resultado)

    def test_buscar_red_por_nombre_existente(self):
        resultado = self.registro.buscar_red_por_nombre("GERENCIA")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "GERENCIA")


    def test_buscar_red_por_nombre_inexistente(self):
         resultado = self.registro.buscar_red_por_nombre("SOPORTE")

         self.assertIsNone(resultado)

    def test_registrar_red_valida(self):
        desarrollo = RedEmpresarial(
            nombre="DESARROLLO",
            cidr="10.20.0.0/24",
            vlan_id=20,
            gateway="10.20.0.1"
        )

        self.registro.agregar_red(desarrollo)

        self.assertEqual(len(self.registro.redes), 2)
        
    def test_rechazar_vlan_duplicada(self):
        red = RedEmpresarial(
            nombre="VENTAS",
            cidr="10.30.0.0/24",
            vlan_id=10,
            gateway="10.30.0.1"
        )

        with self.assertRaisesRegex(ValueError, "VLAN"):
            self.registro.agregar_red(red)

    def test_rechazar_red_duplicada(self):
        red = RedEmpresarial(
            nombre="GERENCIA_COPIA",
            cidr="10.10.0.0/24",
            vlan_id=30,
            gateway="10.10.0.2"
        )

        with self.assertRaisesRegex(ValueError, "ya está registrada"):
            self.registro.agregar_red(red)

    def test_rechazar_subred_superpuesta(self):
        subred = RedEmpresarial(
            nombre="GERENCIA_SUBRED",
            cidr="10.10.0.0/25",
            vlan_id=30,
            gateway="10.10.0.2"
        )

        with self.assertRaisesRegex(ValueError, "superpone"):
            self.registro.agregar_red(subred)

    def test_rechazar_vlan_fuera_de_rango(self):
        with self.assertRaisesRegex(ValueError, "VLAN"):
            RedEmpresarial(
                nombre="RED_INVALIDA",
                cidr="10.40.0.0/24",
                vlan_id=5000,
                gateway="10.40.0.1"
            )

    def test_rechazar_gateway_fuera_de_red(self):
        with self.assertRaisesRegex(ValueError, "no pertenece"):
            RedEmpresarial(
                nombre="RED_INVALIDA",
                cidr="10.50.0.0/24",
                vlan_id=50,
                gateway="10.60.0.1"
            )


if __name__ == "__main__":
    unittest.main()
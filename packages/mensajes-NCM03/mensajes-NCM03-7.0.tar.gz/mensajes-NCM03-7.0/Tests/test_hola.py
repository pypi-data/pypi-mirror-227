import numpy as np
import unittest
from Mensajes.Hola.Saludos import generar_array


class Pruebas_Hola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))
        
        
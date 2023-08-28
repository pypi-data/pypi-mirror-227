
import numpy as np

def saludar ():
    print("Hola")


def generar_array(numeros):
    return np.arange(numeros)




class Saludo:
    def __init__(self):
        print("Hola te saludo desde saludo.__init()")


if __name__ == '__main__':
    print(generar_array(5))
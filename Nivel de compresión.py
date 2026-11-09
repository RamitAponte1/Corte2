
# Clase Estudiante
class Estudiante:

    # Constructor
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__notas = []

    # Propiedad para consultar el nombre
    @property
    def nombre(self):
        return self.__nombre

    # Propiedad para consultar las notas
    @property
    def notas(self):
        return self.__notas.copy()

    # Setter para agregar y validar notas
    @notas.setter
    def notas(self, nueva_nota):
        if not isinstance(nueva_nota, (int, float)) or isinstance(nueva_nota, bool):
            print("Advertencia: La nota debe ser un número.")
        elif 0 <= nueva_nota <= 5.0:
            self.__notas.append(nueva_nota)
            print("Nota agregada correctamente.")
        else:
            print("Advertencia: La nota debe estar entre 0 y 5.0.")

    # Método para calcular el promedio
    def calcular_promedio(self):
        if len(self.__notas) == 0:
            return 0.0

        return sum(self.__notas) / len(self.__notas)

    # Método para mostrar la información
    def mostrar_informacion(self):
        print("\n===== INFORMACIÓN DEL ESTUDIANTE =====")
        print("Nombre:", self.nombre)
        print("Notas:", self.notas)
        print("Promedio:", round(self.calcular_promedio(), 2))


# Crear un objeto estudiante
estudiante1 = Estudiante("Carlos")

# Agregar notas válidas
estudiante1.notas = 4.5
estudiante1.notas = 3.8
estudiante1.notas = 5.0
estudiante1.notas = 4.2

# Intentar agregar notas inválidas
estudiante1.notas = -1
estudiante1.notas = 6.0

# Mostrar información
estudiante1.mostrar_informacion()

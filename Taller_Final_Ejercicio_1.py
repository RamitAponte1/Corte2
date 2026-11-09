
class Producto:
    # Constructor
    def __init__(self, nombre, precio_inicial):
        self.__nombre = nombre
        self.__precios_historicos = []

        # Registrar el precio inicial usando el setter
        self.precio = precio_inicial

    # Propiedad para consultar el nombre
    @property
    def nombre(self):
        return self.__nombre

    # Propiedad para consultar el historial de precios
    @property
    def precios_historicos(self):
        return self.__precios_historicos.copy()

    # Getter del precio actual
    @property
    def precio(self):
        
        
        if self.__precios_historicos:
            return self.__precios_historicos[-1]
        return None

    # Setter para actualizar y validar el precio
    @precio.setter
    def precio(self, nuevo_precio):
        if not isinstance(nuevo_precio, (int, float)) or isinstance(nuevo_precio, bool):
            print("Advertencia: El precio debe ser un número.")
        elif 0 <= nuevo_precio <= 10000:
            self.__precios_historicos.append(nuevo_precio)
            print("Precio registrado correctamente.")
        else:
            print("Advertencia: El precio debe estar entre $0 y $10,000.")

    # Método para calcular el precio promedio
    @property
    def precio_promedio(self):
        if len(self.__precios_historicos) == 0:
            return 0

        return sum(self.__precios_historicos) / len(self.__precios_historicos)

    # Método para mostrar la información
    def mostrar_informacion(self):
        print("\n--- INFORMACIÓN DEL PRODUCTO ---")
        print("Nombre:", self.nombre)
        print("Precio actual: $", self.precio)
        print("Historial de precios:", self.precios_historicos)
        print("Precio promedio: $", round(self.precio_promedio, 2))


# Crear un objeto
producto1 = Producto("Computador", 2500)

# Registrar nuevos precios
producto1.precio = 3000
producto1.precio = 3500
producto1.precio = 4000

# Intentar registrar precios inválidos
producto1.precio = -500
producto1.precio = 15000

# Mostrar información
producto1.mostrar_informacion()

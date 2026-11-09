
# Clase base
class Envio:
    def __init__(self, peso_kg, distancia_km):
        self.peso_kg = peso_kg
        self.distancia_km = distancia_km

    def calcular_costo(self, monto_base):
        return monto_base


# Subclase EnvioEstandar
class EnvioEstandar(Envio):
    def calcular_costo(self, monto_base):
        return monto_base * 1.05


# Subclase EnvioExpress
class EnvioExpress(Envio):
    def calcular_costo(self, monto_base):
        return monto_base * 1.15


# Crear una lista mixta de envíos con sus montos base
envios = [
    (EnvioEstandar(5, 100), 100000),
    (EnvioExpress(10, 200), 150000),
    (EnvioEstandar(3, 50), 80000),
    (EnvioExpress(8, 150), 120000)
]


# Recorrer la lista y aplicar el polimorfismo
print("===== COTIZACIÓN DE ENVÍOS =====")

for envio, monto_base in envios:

    costo_final = envio.calcular_costo(monto_base)

    if isinstance(envio, EnvioEstandar):
        tipo = "Estándar"
    else:
        tipo = "Express"

    print("\nTipo de envío:", tipo)
    print("Peso:", envio.peso_kg, "kg")
    print("Distancia:", envio.distancia_km, "km")
    print("Monto base: $", monto_base)
    print("Costo final: $", round(costo_final, 2))

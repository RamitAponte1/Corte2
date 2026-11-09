
# Clase base
class TarjetaCredito:

    def calcular_cashback(self, monto):
        return 0.0


# Subclase TarjetaGold
class TarjetaGold(TarjetaCredito):

    def calcular_cashback(self, monto):
        return monto * 0.02


# Subclase TarjetaBlack
class TarjetaBlack(TarjetaCredito):

    def calcular_cashback(self, monto):
        return monto * 0.05


# Crear una lista mixta de tarjetas
tarjetas = [
    TarjetaGold(),
    TarjetaBlack(),
    TarjetaGold(),
    TarjetaBlack()
]

# Montos de las compras
montos = [100000, 200000, 150000, 300000]

# Recorrer la lista y aplicar el polimorfismo
print("===== SIMULADOR DE TARJETAS DE CRÉDITO =====")

for tarjeta, monto in zip(tarjetas, montos):

    cashback = tarjeta.calcular_cashback(monto)

    if isinstance(tarjeta, TarjetaGold):
        tipo = "Gold"
    else:
        tipo = "Black"

    print("\nTipo de tarjeta:", tipo)
    print("Monto de compra: $", monto)
    print("Cashback obtenido: $", round(cashback, 2))

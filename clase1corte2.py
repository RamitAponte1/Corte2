import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()

# Configurar el título de la ventana
ventana.setTitle = "Mi Ventana" # (Opcional, título de la barra superior)
ventana.title("Ventana de Presentación")

# Definir el tamaño de la ventana (ancho x alto)
ventana.geometry("800x400")

# Crear una etiqueta (Label) con el texto requerido
etiqueta = tk.Label(ventana, text="Ramit jesus Aponte Medina", font=("Arial", 14, "bold"))

# Colocar la etiqueta en el centro de la ventana con un margen (padding)
etiqueta.pack(expand=True)

# Iniciar el bucle principal de la ventana para que se mantenga abierta
ventana.mainloop()

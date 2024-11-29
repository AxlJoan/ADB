import tkinter as tk
from tkinter import messagebox
import subprocess

# Función que ejecuta el comando ADB en cada dispositivo
def open_link_on_devices():
    # Obtener el enlace del campo de texto
    link = entry_link.get()

    if not link:
        messagebox.showwarning("Entrada vacía", "Por favor ingresa un enlace.")
        return

    # Determinar la opción seleccionada
    selected_option = option_var.get()

    try:
        # Obtener la lista de dispositivos conectados
        devices_output = subprocess.check_output(["adb", "devices"]).decode("utf-8")
        devices = [line.split("\t")[0] for line in devices_output.splitlines() if "device" in line]

        if not devices:
            messagebox.showwarning("No se encontraron dispositivos", "No se encontraron dispositivos conectados.")
            return

        # Iterar sobre los dispositivos y abrir el enlace según la opción seleccionada
        for device in devices:
            if selected_option == "default":
                # Abrir con la aplicación predeterminada
                subprocess.run(["adb", "-s", device, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", link])
            elif selected_option == "chrome":
                # Abrir directamente en Google Chrome
                subprocess.run([
                    "adb", "-s", device, "shell", "am", "start", "-a", "android.intent.action.VIEW",
                    "-d", link, "-n", "com.android.chrome/com.google.android.apps.chrome.Main"
                ])

        messagebox.showinfo("Éxito", f"Enlace abierto en {len(devices)} dispositivos.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error de ADB", f"Hubo un problema ejecutando ADB: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Abrir Enlace en Dispositivos Android")
root.geometry("400x300")

# Crear y colocar los widgets
label = tk.Label(root, text="Ingresa el enlace:")
label.pack(pady=10)

entry_link = tk.Entry(root, width=50)
entry_link.pack(pady=10)

# Variable para almacenar la opción seleccionada
option_var = tk.StringVar(value="default")

# Botones de opción para seleccionar cómo abrir el enlace
radio_default = tk.Radiobutton(root, text="Abrir con la app predeterminada", variable=option_var, value="default")
radio_default.pack(anchor="w", padx=20)

radio_chrome = tk.Radiobutton(root, text="Abrir directamente en Chrome", variable=option_var, value="chrome")
radio_chrome.pack(anchor="w", padx=20)

# Botón para ejecutar el comando
button = tk.Button(root, text="Abrir Enlace", command=open_link_on_devices)
button.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()

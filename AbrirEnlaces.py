import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import threading
import time

# Función para abrir enlaces generales
def open_link_on_devices():
    link = entry_link.get()

    if not link:
        messagebox.showwarning("Entrada vacía", "Por favor ingresa un enlace.")
        return

    selected_option = option_var.get()

    try:
        devices_output = subprocess.check_output(["adb", "devices"]).decode("utf-8")
        devices = [line.split("\t")[0] for line in devices_output.splitlines() if "device" in line]

        if not devices:
            messagebox.showwarning("No se encontraron dispositivos", "No se encontraron dispositivos conectados.")
            return

        for device in devices:
            if selected_option == "default":
                subprocess.run(["adb", "-s", device, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", link])
            elif selected_option == "chrome":
                subprocess.run([
                    "adb", "-s", device, "shell", "am", "start", "-a", "android.intent.action.VIEW",
                    "-d", link, "-n", "com.android.chrome/com.google.android.apps.chrome.Main"
                ])

        messagebox.showinfo("Éxito", f"Enlace abierto en {len(devices)} dispositivos.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error de ADB", f"Hubo un problema ejecutando ADB: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# Función para abrir enlaces de YouTube y recargar cada 20 segundos
def open_video_on_devices():
    link = entry_link.get()

    if not link:
        messagebox.showwarning("Entrada vacía", "Por favor ingresa un enlace de YouTube.")
        return

    if not link.startswith("https://www.youtube.com/watch"):
        messagebox.showwarning("Enlace inválido", "Por favor ingresa un enlace válido de YouTube.")
        return

    try:
        devices_output = subprocess.check_output(["adb", "devices"]).decode("utf-8")
        devices = [line.split("\t")[0] for line in devices_output.splitlines() if "device" in line]

        if not devices:
            messagebox.showwarning("No se encontraron dispositivos", "No se encontraron dispositivos conectados.")
            return

        for device in devices:
            subprocess.run([
                "adb", "-s", device, "shell", "am", "start", "-a", "android.intent.action.VIEW",
                "-d", link, "-n", "com.android.chrome/com.google.android.apps.chrome.Main"
            ])
            start_page_refresh(device)

        messagebox.showinfo("Éxito", f"Video de YouTube abierto en {len(devices)} dispositivos.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error de ADB", f"Hubo un problema ejecutando ADB: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# Función para refrescar la página cada 20 segundos
def start_page_refresh(device):
    def refresh_page():
        while True:
            try:
                subprocess.run(["adb", "-s", device, "shell", "input", "keyevent", "KEYCODE_F5"])
                time.sleep(100)
            except Exception as e:
                print(f"Error al refrescar la página en el dispositivo {device}: {e}")

    refresh_thread = threading.Thread(target=refresh_page, daemon=True)
    refresh_thread.start()

# Crear la ventana principal
root = tk.Tk()
root.title("Abrir Enlace en Dispositivos Android")
root.geometry("500x700")
root.config(bg="#f0f0f0")

# Cargar imágenes de logos
logo_general_image = Image.open("logo.png").resize((150, 150), Image.Resampling.LANCZOS)
logo_general_tk = ImageTk.PhotoImage(logo_general_image)

logo_youtube_image = Image.open("youtube_logo.png").resize((150, 104), Image.Resampling.LANCZOS)
logo_youtube_tk = ImageTk.PhotoImage(logo_youtube_image)

# Crear frame principal 
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(padx=20, pady=20, expand=True, fill="both")

# Mostrar logos
logo_general_label = tk.Label(frame, image=logo_general_tk, bg="#ffffff")
logo_general_label.pack(pady=10)

# Título
title_label = tk.Label(frame, text="Abrir Enlace en Dispositivos Android", font=("Roboto", 16, "bold"), bg="#ffffff", fg="#269c0e")
title_label.pack(pady=10)

# Subtítulo
subtitle_label = tk.Label(frame, text="Ingresa el enlace y selecciona la opción", font=("Roboto", 12), bg="#ffffff", fg="#555555")
subtitle_label.pack(pady=5)

# Campo de texto para el enlace
entry_link = ttk.Entry(frame, width=50, font=("Roboto", 12), justify="center")
entry_link.pack(pady=15)

# Opciones de apertura para enlace general
option_var = tk.StringVar(value="default")

radio_default = ttk.Radiobutton(frame, text="Abrir con la app predeterminada", variable=option_var, value="default")
radio_default.pack(anchor="w", padx=10)

radio_chrome = ttk.Radiobutton(frame, text="Abrir directamente en Chrome", variable=option_var, value="chrome")
radio_chrome.pack(anchor="w", padx=10)

# Botón para abrir enlaces generales
button_general = ttk.Button(frame, text="Abrir Enlace", command=open_link_on_devices)
button_general.pack(pady=20)

# Logo de YouTube
logo_youtube_label = tk.Label(frame, image=logo_youtube_tk, bg="#ffffff")
logo_youtube_label.pack(pady=10)

# Botón para abrir videos de YouTube
button_youtube = ttk.Button(frame, text="Abrir Video de YouTube", command=open_video_on_devices)
button_youtube.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()

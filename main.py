import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import backend

def verify_connection():
    result = backend.isConnected()
    messagebox.showinfo("Network Connection", f"Network Connection: {result}")

def check_devices():
    if backend.isConnected():
        devices = backend.scanDevices()
        devices_info = "\n".join([f"IP: {device[0]}   MAC: {device[1]}   Brand: {device[2]}" for device in devices])
        messagebox.showinfo("Devices on Network", devices_info)
    else:
        messagebox.showwarning("Warning", "Network is not connected. Please check your connection.")

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Dragon Eye")

    # Configurar o estilo do tema escuro
    style = ThemedStyle(window)
    style.set_theme("equilux")

    btn_verify_connection = ttk.Button(window, text="Verify Network Connection", command=verify_connection)
    btn_verify_connection.pack(pady=10)

    btn_check_devices = ttk.Button(window, text="Check Devices on Network", command=check_devices)
    btn_check_devices.pack(pady=10)

    btn_exit = ttk.Button(window, text="Exit", command=window.destroy)
    btn_exit.pack(pady=10)

    window.mainloop()

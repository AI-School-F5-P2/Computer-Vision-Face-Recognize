# src/face_registration_interface.py
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import os

class FaceRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Caras")

        self.name_label = tk.Label(root, text="Nombre:")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.start_button = tk.Button(root, text="Iniciar Captura", command=self.start_capture)
        self.start_button.pack()

        self.capture = None
        self.image_counter = 0
        self.folder_path = None

        self.capture_button = tk.Button(root, text="Tomar Captura", command=self.capture_and_register)
        self.capture_button.pack()
        self.capture_button['state'] = 'disabled'  # Deshabilitar hasta que se inicie la captura

        self.message_label = Label(root, text="")
        self.message_label.pack()

        self.camera_label = Label(root)
        self.camera_label.pack()

    def start_capture(self):
        name = self.name_entry.get().strip()
        if name:
            # Obtener el nombre de la carpeta y el número actual de capturas
            self.folder_path = os.path.join('..', 'data', 'directorio_de_imagenes', name)
            os.makedirs(self.folder_path, exist_ok=True)

            # Buscar el último número de captura en la carpeta
            existing_files = os.listdir(self.folder_path)
            existing_numbers = [int(file.split('.')[0]) for file in existing_files if file.endswith('.jpg')]
            self.image_counter = max(existing_numbers, default=-1) + 1

            self.capture = cv2.VideoCapture(0)
            self.show_camera_preview()
            self.start_button['state'] = 'disabled'
            self.capture_button['state'] = 'normal'
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        else:
            print('Por favor, ingresa un nombre antes de iniciar la captura.')

    def show_camera_preview(self):
        ret, frame = self.capture.read()
        if ret:
            # Convertir el frame de OpenCV a formato de imagen
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)

            # Actualizar la etiqueta con la nueva imagen
            self.camera_label.img = img
            self.camera_label.config(image=img)

            self.root.after(10, self.show_camera_preview)
        else:
            print('Error al capturar imagen.')

    def on_closing(self):
        if self.capture is not None:
            self.capture.release()
            cv2.destroyAllWindows()

        self.root.destroy()

    def capture_and_register(self):
        ret, frame = self.capture.read()
        if ret:
            file_path = os.path.join(self.folder_path, f'{self.image_counter}.jpg')
            cv2.imwrite(file_path, frame)
            print(f'Imagen guardada en {file_path}')
            self.image_counter += 1

            # Mostrar mensaje de registro exitoso
            self.message_label.config(text="Registrado", fg="green")
            self.root.after(2000, self.clear_message)  # Limpiar el mensaje después de 2 segundos

    def clear_message(self):
        self.message_label.config(text="")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRegistrationApp(tk.Tk())
    app.main()

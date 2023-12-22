# src/face_registration_interface.py
import tkinter as tk
from tkinter import Label, Entry, Button, PhotoImage
from PIL import Image, ImageTk
import cv2
import os

class FaceRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Caras")
        self.root.geometry("400x300")  # Tamaño inicial de la ventana
        self.root.configure(bg="#1f1f1f")  # Color de fondo negro

        self.title_label = Label(root, text="Registro de Caras", font=("Helvetica", 16), fg="#61dafb", bg="#1f1f1f")
        self.title_label.pack(pady=10)

        self.name_label = Label(root, text="Nombre:", font=("Helvetica", 12), fg="#61dafb", bg="#1f1f1f")
        self.name_label.pack()

        self.name_entry = Entry(root, font=("Helvetica", 12), bg="#333333", fg="#ffffff")
        self.name_entry.pack(pady=10, side=tk.TOP)  # Alinear al centro con pady y side
        self.name_entry.bind("<FocusIn>", self.center_align_text)  # Llama a la función cuando el Entry obtiene el foco

        self.start_button = Button(root, text="Iniciar Captura", command=self.start_capture, font=("Helvetica", 12), bg="#61dafb", fg="#000000")
        self.start_button.pack(pady=10)

        self.capture = None
        self.image_counter = 0
        self.folder_path = None

        self.capture_button = Button(root, text="Tomar Captura", command=self.capture_and_register, font=("Helvetica", 12), bg="#61dafb", fg="#000000")
        self.capture_button.pack()
        self.capture_button['state'] = 'disabled'  # Deshabilitar hasta que se inicie la captura

        self.message_label = Label(root, text="", font=("Helvetica", 12), fg="green", bg="#1f1f1f")
        self.message_label.pack()

        self.camera_label = Label(root, bg="#1f1f1f")
        self.camera_label.pack()

    def center_align_text(self, event):
        # Mueve el cursor al centro del Entry
        current_text = self.name_entry.get()
        cursor_position = len(current_text) // 2
        self.name_entry.icursor(cursor_position)

    def start_capture(self):
        name = self.name_entry.get().strip()
        if name:
            self.folder_path = os.path.join('data', 'directorio_de_imagenes', name)
            os.makedirs(self.folder_path, exist_ok=True)

            existing_files = os.listdir(self.folder_path)
            existing_numbers = [int(file.split('.')[0]) for file in existing_files if file.endswith('.jpg')]
            self.image_counter = max(existing_numbers, default=-1) + 1

            self.capture = cv2.VideoCapture(0)
            self.show_camera_preview()
            self.start_button['state'] = 'disabled'
            self.capture_button['state'] = 'normal'
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        else:
            self.message_label.config(text='Por favor, ingresa un nombre antes de iniciar la captura.', fg='red')

    def show_camera_preview(self):
        ret, frame = self.capture.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)

            self.camera_label.img = img
            self.camera_label.config(image=img)

            # Ajustar automáticamente el tamaño de la ventana
            self.root.geometry(f"{frame.shape[1]}x{frame.shape[0] + 150}")

            # Centrar la ventana en la pantalla
            window_width = self.root.winfo_reqwidth()
            window_height = self.root.winfo_reqheight()
            position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
            position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
            self.root.geometry(f"+{position_right}+{position_down}")

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

            self.message_label.config(text='Registrado', fg='green')
            self.root.after(2000, self.clear_message)
        else:
            self.message_label.config(text='Error al capturar imagen.', fg='red')

    def clear_message(self):
        self.message_label.config(text='')

    def main(self):
        # Centrar la ventana en la pantalla
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f"+{position_right}+{position_down}")

        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRegistrationApp(tk.Tk())
    app.main()

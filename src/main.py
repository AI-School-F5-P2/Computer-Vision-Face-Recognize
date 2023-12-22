import cv2
import tkinter as tk
from tkinter import ttk
import subprocess
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import numpy as np

# Crear la variable global root
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")

# Cargar modelo de detección facial
detector = MTCNN()

# Cargar modelo de reconocimiento facial
model = load_model('models/modelo_reconocimiento.keras')

def preprocess(img):
    # Preprocesar la imagen para que coincida con el modelo de reconocimiento facial
    img = cv2.resize(img, (150, 150))  # Ajusta las dimensiones según las expectativas de tu modelo
    img = img.astype('float32')
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def reconocer_cara(cara):
    # Preprocesar la cara y realizar la clasificación
    cara = preprocess(cara)
    features = model.predict(cara)
    # Ajustar el umbral según tus necesidades
    umbral = 0.5

    # La salida del modelo es una probabilidad, aquí usamos un umbral para la clasificación binaria
    if features[0, 0] > umbral:
        return 'ACCESO PERMITIDO'
    else:
        return 'ACCESO DENEGADO'

def mostrar_resultados(imagen, resultados):
    for resultado in resultados:
        x, y, w, h = resultado['box']
        cara = imagen[y:y+h, x:x+w]
        resultado_reconocimiento = reconocer_cara(cara)
        color = (0, 255, 0)  # Verde por defecto para ACCESO PERMITIDO
        if resultado_reconocimiento == 'ACCESO DENEGADO':
            color = (0, 0, 255)  # Rojo para ACCESO DENEGADO

        # Mostrar resultados en la imagen
        cv2.rectangle(imagen, (x, y), (x+w, y+h), color, 2)
        cv2.putText(imagen, f'{resultado_reconocimiento}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('Reconocimiento Facial', imagen)
    cv2.waitKey(1)  # Cambiado de 0 a 1 para permitir la detección en tiempo real


# Función para detectar caras usando MTCNN
def detectar_caras(imagen):
    result = detector.detect_faces(imagen)
    return result

# Cambiar la función iniciar_deteccion para que llame a mostrar_resultados
def iniciar_deteccion():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        caras = detectar_caras(frame)
        mostrar_resultados(frame, caras)
        root.update_idletasks()
        root.update()

    cap.release()
    cv2.destroyAllWindows()

def abrir_interfaz_registro():
    # Ejecutar el script face_registration_interface.py
    subprocess.run(["python", "src/face_registration_interface.py"])

# Botones
inicio_button = ttk.Button(root, text="INICIO", command=iniciar_deteccion)
inicio_button.pack(pady=10)

registro_button = ttk.Button(root, text="REGISTRO", command=abrir_interfaz_registro)
registro_button.pack(pady=10)

# Inicia el bucle de la interfaz gráfica
root.mainloop()

import cv2
import tkinter as tk
from tkinter import ttk
import subprocess
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import numpy as np

# Cargar modelo de detección facial
detector = MTCNN()

# Cargar modelo de reconocimiento facial (FaceNet, por ejemplo)
# Asegúrate de que esta línea apunta al modelo correcto
model = load_model('models/modelo_reconocimiento.py')

def preprocess(img):
    # Preprocesar la imagen para que coincida con el modelo de reconocimiento facial
    img = cv2.resize(img, (150, 150))  # Ajusta las dimensiones según las expectativas de tu modelo
    img = img.astype('float32')
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def clasificar(features):
    # Función de clasificación basada en las características extraídas por el modelo
    # Ajusta esta función según las necesidades y el modelo que estás utilizando
    # Aquí simplemente devolvemos 'Desconocido' como ejemplo
    return 'Desconocido'

def calcular_confianza(resultados):
    # Función para calcular la confianza
    # Ajusta esta función según las necesidades y el modelo que estás utilizando
    # Aquí simplemente devolvemos un valor arbitrario del 95%
    return 0.95

def detectar_caras(imagen):
    # Utilizar MTCNN para detectar caras
    result = detector.detect_faces(imagen)
    return result

def reconocer_cara(cara):
    # Preprocesar la cara y realizar la clasificación
    # Asumiendo que el modelo devuelve un vector de características
    # y un nombre asociado
    # (Este código es un ejemplo y debe ajustarse según el modelo utilizado)
    cara = preprocess(cara)
    features = model.predict(cara)
    nombre = clasificar(features)
    return nombre

def mostrar_resultados(imagen, resultados):
    for resultado in resultados:
        x, y, w, h = resultado['box']
        cara = imagen[y:y+h, x:x+w]
        nombre = reconocer_cara(cara)
        porcentaje_confianza = calcular_confianza(resultados)  # Ajustar según el modelo utilizado

        # Mostrar resultados en la imagen
        cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(imagen, f'{nombre} - {porcentaje_confianza:.2%}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Reconocimiento Facial', imagen)
    cv2.waitKey(1)  # Cambiado de 0 a 1 para permitir la detección en tiempo real

def iniciar_deteccion():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        caras = detectar_caras(frame)
        mostrar_resultados(frame, caras)

    cap.release()
    cv2.destroyAllWindows()

def abrir_interfaz_registro():
    # Ejecutar el script face_registration_interface.py
    subprocess.run(["python", "src/face_registration_interface.py"])

# Interfaz gráfica
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")

# Botones
inicio_button = ttk.Button(root, text="INICIO", command=iniciar_deteccion)
inicio_button.pack(pady=10)

registro_button = ttk.Button(root, text="REGISTRO", command=abrir_interfaz_registro)
registro_button.pack(pady=10)

# Inicia el bucle de la interfaz gráfica
root.mainloop()

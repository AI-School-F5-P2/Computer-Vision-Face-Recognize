import cv2
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import numpy as np
import os

# Cargar modelo de detección facial
detector = MTCNN()

# Cargar modelo de reconocimiento facial
# Asegúrate de que esta línea apunta al modelo correcto (en este caso, 'model.py')
model = load_model('model.py')

def preprocess(img):
    # Preprocesar la imagen para que coincida con el modelo de reconocimiento facial
    img = cv2.resize(img, (160, 160))
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

def capturar_imagen():
    # Capturar imagen desde la cámara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

def cargar_imagenes_directorio(directorio):
    # Cargar imágenes desde un directorio y devolver una lista de rutas
    imagenes = []
    for filename in os.listdir(directorio):
        path = os.path.join(directorio, filename)
        imagenes.append(cv2.imread(path))
    return imagenes

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
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # Nivel Esencial
    imagen = capturar_imagen()
    caras = detectar_caras(imagen)
    mostrar_resultados(imagen, caras)

    # Nivel Medio
    imagenes_directorio = cargar_imagenes_directorio('directorio_de_imagenes/caras')
    for img in imagenes_directorio:
        caras = detectar_caras(img)
        mostrar_resultados(img, caras)

    # Nivel Avanzado
    # Implementar funciones adicionales para calcular porcentaje de seguridad,
    # reconocer un mayor número de empleados y realizar análisis empíricos.

if __name__ == "__main__":
    main()

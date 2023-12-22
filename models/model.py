import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Crear un modelo de reconocimiento facial
modelo = Sequential()
modelo.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Dropout(0.25))  # Capa Dropout para regularización
modelo.add(Conv2D(64, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Conv2D(128, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Conv2D(128, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Flatten())
modelo.add(Dense(512, activation='relu'))
modelo.add(Dropout(0.5))  # Capa Dropout para regularización
modelo.add(Dense(1, activation='sigmoid'))

# Cambios para clasificación binaria
modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Crear generadores de datos para entrenamiento con aumentación
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Directorio donde se encuentran las carpetas de cada usuario registrado
base_directory = 'data/directorio_de_imagenes/Rodrigo'

# Obtener la lista de nombres de usuarios registrados
usuarios_registrados = os.listdir(base_directory)

# Cambios para clasificación binaria
for usuario in usuarios_registrados:
    usuario_directory = os.path.join(base_directory, usuario)
    
    # Verificar que sea un directorio
    if os.path.isdir(usuario_directory):
        print(f'Entrenando con imágenes de {usuario}')
        
        train_generator = train_datagen.flow_from_directory(
            usuario_directory,
            target_size=(150, 150),
            batch_size=32,
            class_mode='binary'  # Cambiado a 'binary' para clasificación binaria
        )

        # Entrenar el modelo con las imágenes del usuario actual
        modelo.fit(train_generator, epochs=10, steps_per_epoch=len(train_generator))

# Guardar el modelo entrenado
modelo.save('models/modelo_reconocimiento.keras')

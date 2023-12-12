import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Crear un modelo simple de reconocimiento facial
modelo = Sequential()
modelo.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Conv2D(64, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Conv2D(128, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Conv2D(128, (3, 3), activation='relu'))
modelo.add(MaxPooling2D(2, 2))
modelo.add(Flatten())
modelo.add(Dense(512, activation='relu'))
modelo.add(Dense(1, activation='sigmoid'))

modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Crear generadores de datos para entrenamiento
train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'directorio_de_imagenes',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

# Entrenar el modelo
modelo.fit(train_generator, epochs=10, steps_per_epoch=len(train_generator))

# Guardar el modelo entrenado
modelo.save('modelo_reconocimiento.py')

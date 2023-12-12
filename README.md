# Sistema de Reconocimiento Facial para Control de Acceso - Proyecto de IA

Este proyecto tiene como objetivo implementar un sistema de reconocimiento facial para agilizar el control de acceso en la fiesta de la empresa. La solución propuesta utilizará machine learning y se ejecutará en un ordenador portátil, sin depender de servicios en la nube por razones de privacidad.

---

## Planteamiento

La empresa busca una solución que permita reconocer a los empleados mediante un sistema de reconocimiento facial utilizando machine learning. Antes de implementar la solución en producción, se realizará una prueba con los miembros del equipo. La metodología de desarrollo será el "Pair Programming", donde dos expertos trabajarán simultáneamente intercambiando roles cada hora.

---

## Metodología

Para llevar a cabo este proyecto, se utilizará la metodología de programación "Pair Programming". Dos personas trabajarán simultáneamente, una como Piloto (escribiendo código) y la otra como Copiloto (supervisando en tiempo real). Se intercambiarán los roles cada hora, y al final de cada sesión, se realizará un commit del trabajo desde la cuenta de GitHub del Piloto.

---

## Plazos

El jefe espera ver las propuestas de solución el día 21 de Diciembre.

---

## Condiciones de Entrega

**Para el día de la reunión (21 de Diciembre):**
- Un Speech con demostración de la solución en 10 minutos.

**Para el día siguiente a la reunión (22 de Diciembre):**
- Una presentación de código explicando la solución implementada y defendiendo por qué es la mejor dadas las condiciones.

**NOTA:** Se evaluará la calidad y claridad del código entregado.

---

## Niveles de Entrega

### Nivel Esencial:

- Modelo de ML/DL que detecte la posición de la cara y clasifique las imágenes.
- Captura manual de imágenes con la webcam para detección y clasificación.
- Resultados en menos de 2 segundos.
- Funciona en un ordenador portátil.

### Nivel Medio:

- Funcionamiento continuo desde un stream de video en tiempo real.
- Mostrar "ACCESO PERMITIDO" o "ACCESO DENEGADO" debajo de cada cara reconocida.
  
### Nivel Avanzado:

- Porcentaje de seguridad visible en la pantalla junto al nombre de la persona.
- Capacidad de detectar a un mayor número de empleados.
- Análisis del funcionamiento del algoritmo con datos empíricos.

### Nivel Experto:

- Funcionamiento con recursos limitados (microordenador tipo Raspberry Pi).
- Sistema de logging para almacenar imágenes clasificadas con fecha y hora.
- Creación de un dataset de test manualmente con IoU medio.
- Guardar imágenes de cada persona detectada para mejorar el entrenamiento futuro.
- Ampliación de funcionalidades con otros modelos de machine learning en el pipeline.

**Se solicita que todos los modelos añadidos al pipeline sean configurables para su uso o no.**

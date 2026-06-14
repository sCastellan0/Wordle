# 🔤 Wordle en Python

Este proyecto es una implementación del clásico **Wordle**, desarrollada en **Python**, que permite al usuario adivinar una palabra oculta en un número limitado de intentos. Incluye un archivo de palabras y un script principal que gestiona toda la lógica del juego.

---

## 🎮 ¿Cómo funciona?

El juego selecciona una palabra aleatoria del archivo `palabras_columna.txt`. El jugador debe adivinarla introduciendo palabras del mismo número de letras.

Después de cada intento, el programa indica:
* 🟩 **Letra correcta en la posición correcta** * 🟨 **Letra correcta en posición incorrecta** * ⬛ **Letra no presente en la palabra**

El objetivo es adivinar la palabra en el menor número de intentos posible.

---

## 📁 Estructura del proyecto

```text
Wordle/
│── palabras_columna.txt   # Lista de palabras válidas
└── woordle.py             # Lógica principal del juego
````
### ▶️ Cómo ejecutar el juego
1. Asegúrate de tener Python 3 instalado.

2. Ejecuta el script desde tu terminal: `python woordle.py`

## 🧠 Lógica del juego

El script gestiona el flujo de la partida de forma automática realizando las siguientes acciones:

1. **Carga de datos:** Lee y almacena todas las palabras disponibles desde el archivo `palabras_columna.txt`.
2. **Selección:** Escoge una palabra aleatoria del listado para que actúe como la palabra oculta de la partida.
3. **Entrada de usuario:** Solicita intentos de forma interactiva al jugador.
4. **Procesamiento:** Compara la palabra introducida letra por letra con la palabra secreta.
5. **Feedback visual:** Muestra en la terminal los colores correspondientes según el tipo de acierto (🟩, 🟨, ⬛).
6. **Condiciones de fin de partida:** El juego finaliza inmediatamente cuando:
   * El usuario acierta la palabra completa.
   * Se agotan todos los intentos disponibles.

import tkinter as tk
from tkinter import messagebox
import random

# Cargar palabras desde archivo
def cargar_palabras(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        return [linea.strip().upper() for linea in f if len(linea.strip()) == 5]

# Colores estilo Wordle
COLORES = {
    'verde':   '#6AAA64',
    'amarillo': '#C9B458',
    'gris':    '#3A3A3C',
    'vacío':   '#121213',
    'texto':   '#FFFFFF'
}

class WordleApp:
    def __init__(self, root, palabras):
        self.palabras = palabras
        self.secreta = random.choice(palabras)
        self.intento_actual = 0
        self.max_intentos = 6
        self.cuadros = []
        self.history = []
        self.root = root
        self.root.title("Wordle - Python")

        # palabra que se está escribiendo (sin Entry)
        self.buffer = ""

        # Fondo general
        self.root.configure(bg=COLORES['vacío'])

        # Contenedor vertical para tablero + teclado
        self.main_frame = tk.Frame(root, bg=COLORES['vacío'])
        self.main_frame.pack(expand=True, fill='both')

        # Cuadrícula 6x5
        self.frame_grid = tk.Frame(self.main_frame, bg=COLORES['vacío'])
        self.frame_grid.pack(pady=(20, 10))

        for fila in range(self.max_intentos):
            fila_cuadros = []
            for col in range(5):
                cuadro = tk.Label(
                    self.frame_grid,
                    text='',
                    width=2,
                    height=1,
                    font=('Helvetica Neue', 32, 'bold'),
                    bg="#3A3A3C",
                    fg=COLORES['texto'],
                    bd=2,
                    relief='solid'
                )
                cuadro.grid(row=fila, column=col, padx=4, pady=4)
                fila_cuadros.append(cuadro)
            self.cuadros.append(fila_cuadros)

        # ===== TECLADO TIPO WORDLE =====
        self.frame_teclado = tk.Frame(self.main_frame, bg=COLORES['vacío'])
        self.frame_teclado.pack(pady=(0, 20))

        # 10 columnas "virtuales" para todas las filas
        # Fila 1: QWERTYUIOP (10 teclas normales)
        fila1 = ["Q","W","E","R","T","Y","U","I","O","P"]
        fila2 = ["A","S","D","F","G","H","J","K","L","Ñ"]
        # Fila 3: ✓ ocupa 2 columnas, luego 6 letras, luego ⌫ 2 columnas (2+6+2 = 10)
        fila3 = ["✓","Z","X","C","V","B","N","M","⌫"]

        self.botones_teclas = {}

        # Fila 1
        for c, letra in enumerate(fila1):
            b = tk.Button(
                self.frame_teclado,
                text=letra,
                width=4,
                height=2,
                font=('Helvetica Neue', 11, 'bold'),
                bg="#565758",
                fg="white",
                bd=0,
                activebackground="#3A3A3C"
            )
            b.config(command=lambda l=letra: self.pulsar_tecla(l))
            b.grid(row=0, column=c, padx=4, pady=4)
            self.botones_teclas[letra] = b

        # Fila 2 (ligero desplazamiento centrando: empezamos en columna 0.5 -> simulamos
        # empezando en 0 pero añadiendo un poco más de padx a la izquierda)
        for c, letra in enumerate(fila2):
            extra_padx = 8 if c == 0 else 4
            b = tk.Button(
                self.frame_teclado,
                text=letra,
                width=4,
                height=2,
                font=('Helvetica Neue', 11, 'bold'),
                bg="#565758",
                fg="white",
                bd=0,
                activebackground="#3A3A3C"
            )
            b.config(command=lambda l=letra: self.pulsar_tecla(l))
            b.grid(row=1, column=c, padx=(extra_padx, 4), pady=4)
            self.botones_teclas[letra] = b

        # Fila 3 centrada: ✓ (col 0-1), Z–M (col 2-7), ⌫ (col 8-9)
        col = 0
        # ENTER grande
        self.b_enter = tk.Button(
            self.frame_teclado,
            text="✓",
            width=6,
            height=2,
            font=('Helvetica Neue', 11, 'bold'),
            bg="#565758",
            fg="white",
            bd=0,
            activebackground="#3A3A3C",
            command=self.intentar
        )
        self.b_enter.grid(row=2, column=col, columnspan=2, padx=4, pady=4, sticky="nsew")
        col += 2

        # Z X C V B N M (6 columnas)
        for letra in ["Z","X","C","V","B","N","M"]:
            b = tk.Button(
                self.frame_teclado,
                text=letra,
                width=4,
                height=2,
                font=('Helvetica Neue', 11, 'bold'),
                bg="#565758",
                fg="white",
                bd=0,
                activebackground="#3A3A3C"
            )
            b.config(command=lambda l=letra: self.pulsar_tecla(l))
            b.grid(row=2, column=col, padx=4, pady=4)
            self.botones_teclas[letra] = b
            col += 1

        # BORRAR grande (últimas 2 columnas)
        self.b_borrar = tk.Button(
            self.frame_teclado,
            text="⌫",
            width=6,
            height=2,
            font=('Helvetica Neue', 11, 'bold'),
            bg="#565758",
            fg="white",
            bd=0,
            activebackground="#3A3A3C",
            command=self.borrar_letra
        )
        self.b_borrar.grid(row=2, column=col, columnspan=2, padx=4, pady=4, sticky="nsew")

        # Atajos de teclado físico
        self.root.bind('<Return>', lambda e: self.intentar())
        self.root.bind('<BackSpace>', lambda e: self.borrar_letra())
        self.root.bind('<Key>', self.key_event)

    # ===== ENTRADA SIN ENTRY =====
    def pulsar_tecla(self, letra):
        if len(self.buffer) < 5:
            self.buffer += letra
            self.actualizar_fila_buffer()

    def borrar_letra(self):
        if self.buffer:
            self.buffer = self.buffer[:-1]
            self.actualizar_fila_buffer()

    def key_event(self, event):
        ch = event.char.upper()
        if 'A' <= ch <= 'Z' or ch == 'Ñ':
            self.pulsar_tecla(ch)

    def actualizar_fila_buffer(self):
        for i in range(5):
            letra = self.buffer[i] if i < len(self.buffer) else ''
            self.cuadros[self.intento_actual][i].config(text=letra, bg="#3A3A3C")

    # ===== PINTAR RESULTADOS =====
    def pintar_fila(self, palabra, pistas):
        for i, letra in enumerate(palabra):
            color = COLORES[pistas[i]]
            self.cuadros[self.intento_actual][i].config(text=letra, bg=color)

            btn = self.botones_teclas.get(letra)
            if btn:
                actual = btn.cget("bg")
                if (color == COLORES['verde'] or
                    (color == COLORES['amarillo'] and actual != COLORES['verde']) or
                    (color == COLORES['gris'] and actual not in (COLORES['verde'], COLORES['amarillo']))):
                    btn.config(bg=color)

    # ===== LÓGICA DEL JUEGO =====
    def analizar_palabra(self, intento):
        resultado = ['gris'] * 5
        secreta = list(self.secreta)
        intento_lista = list(intento)

        for i in range(5):
            if intento[i] == self.secreta[i]:
                resultado[i] = 'verde'
                secreta[i] = None
                intento_lista[i] = None

        for i in range(5):
            if intento_lista[i] is not None and intento_lista[i] in secreta:
                resultado[i] = 'amarillo'
                secreta[secreta.index(intento_lista[i])] = None

        return resultado

    def intentar(self):
        intento = self.buffer.upper().strip()
        if len(intento) != 5:
            return
        if intento not in self.palabras:
            messagebox.showerror("Error", "La palabra no está en el listado.")
            return

        pistas = self.analizar_palabra(intento)
        self.pintar_fila(intento, pistas)
        self.history.append((intento, pistas))
        self.buffer = ""

        if intento == self.secreta:
            messagebox.showinfo("¡Felicidades!", "Adivinaste la palabra secreta.")
            self.root.quit()
            return

        self.intento_actual += 1
        if self.intento_actual == self.max_intentos:
            messagebox.showinfo("Fin del juego", f"La palabra secreta era: {self.secreta}")
            self.root.quit()

if __name__ == "__main__":
    palabras = cargar_palabras('palabras_columna.txt')
    root = tk.Tk()
    root.geometry("500x800")
    root.minsize(500, 800)
    app = WordleApp(root, palabras)
    root.mainloop()

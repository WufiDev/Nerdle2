import tkinter as tk
from tkinter import messagebox
import random

class InterfazJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("Nerdle")
        self.root.geometry("400x300")
        self.root.configure(bg="green")

        self.label_nombre = tk.Label(root, text="Nombre del jugador:", bg="green", fg="white")
        self.label_nombre.pack(pady=5)

        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack(pady=5)

        self.label_dificultad = tk.Label(root, text="Seleccione una dificultad:", bg="green", fg="white")
        self.label_dificultad.pack(pady=5)

        self.combo_dificultad = tk.StringVar(root)
        self.combo_dificultad.set("Fácil")  # Valor predeterminado
        opciones_dificultad = ["Fácil", "Medio", "Difícil"]
        self.optionmenu_dificultad = tk.OptionMenu(root, self.combo_dificultad, *opciones_dificultad)
        self.optionmenu_dificultad.pack(pady=5)

        self.button_iniciar = tk.Button(root, text="Iniciar Juego", command=self.iniciar_juego)
        self.button_iniciar.pack(pady=10)

        self.button_estadisticas = tk.Button(root, text="Ver estadísticas", command=self.ver_estadisticas)
        self.button_estadisticas.pack(pady=10)

        self.button_salir = tk.Button(root, text="Salir", command=root.destroy)
        self.button_salir.pack(pady=10)

        self.puntaje = 0

    def iniciar_juego(self):
        nombre_jugador = self.entry_nombre.get()
        if not nombre_jugador:
            messagebox.showerror("Error", "Por favor, ingresa un nombre de jugador.")
            return

        dificultad = self.combo_dificultad.get()
        if not dificultad:
            messagebox.showerror("Error", "Por favor, selecciona una dificultad.")
            return

        self.juego = Juego(nombre_jugador, Dificultad(dificultad), self)
        self.juego.comenzar_partida()

    def ver_estadisticas(self):
        messagebox.showinfo("Estadísticas", f"Puntaje obtenido: {self.puntaje}")

    def actualizar_puntaje(self, puntos):
        self.puntaje += puntos

class Juego:
    def __init__(self, jugador, dificultad, interfaz):
        self.jugador = jugador
        self.dificultad = dificultad
        self.interfaz = interfaz

    def comenzar_partida(self):
        self.ecuaciones = self.dificultad.generar_ecuaciones()
        self.puntaje = 0
        self.indice_ecuacion = 0
        self.mostrar_ecuacion()

    def mostrar_ecuacion(self):
        if self.indice_ecuacion < len(self.ecuaciones):
            ecuacion = self.ecuaciones[self.indice_ecuacion]
            self.ventana_ecuacion = tk.Toplevel(self.interfaz.root)
            self.ventana_ecuacion.title("Ecuación")
            self.ventana_ecuacion.configure(bg="lightblue")

            self.label_ecuacion = tk.Label(self.ventana_ecuacion, text=ecuacion[0], bg="green", fg="white")
            self.label_ecuacion.pack(pady=5)

            self.entry_respuesta = tk.Entry(self.ventana_ecuacion)
            self.entry_respuesta.pack(pady=5)

            self.button_verificar = tk.Button(self.ventana_ecuacion, text="Verificar", command=self.verificar_respuesta)
            self.button_verificar.pack(pady=5)
        else:
            messagebox.showinfo("Fin del juego", f"¡Juego finalizado! Puntaje obtenido: {self.puntaje}")
            self.interfaz.actualizar_puntaje(self.puntaje)

    def verificar_respuesta(self):
        ecuacion = self.ecuaciones[self.indice_ecuacion]
        respuesta_correcta = ecuacion[4]
        respuesta_jugador = self.entry_respuesta.get()

        try:
            respuesta_jugador = int(respuesta_jugador)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una respuesta válida.")
            return

        diferencia = abs(respuesta_jugador - respuesta_correcta)

        if diferencia == 0:
            color = "green"
        elif diferencia <= 3:
            color = "yellow"
        else:
            color = "red"

        self.entry_respuesta.config(bg=color)

        if respuesta_jugador == respuesta_correcta:
            messagebox.showinfo("¡Correcto!", "¡Respuesta correcta!")
            self.puntaje += 1
        else:
            messagebox.showerror("Incorrecto", f"¡Respuesta incorrecta! La respuesta correcta era: {respuesta_correcta}")

        self.ventana_ecuacion.after(1000, self.cerrar_ventana_ecuacion)

    def cerrar_ventana_ecuacion(self):
        self.ventana_ecuacion.destroy()
        self.indice_ecuacion += 1
        self.mostrar_ecuacion()

class Dificultad:
    def __init__(self, nivel):
        self.nivel = nivel

    def generar_ecuaciones(self):
        ecuaciones = []

        if self.nivel == "Fácil":
            for _ in range(10):
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                operador = random.choice(["+", "-"])
                resultado = num1 + num2 if operador == "+" else num1 - num2
                ecuaciones.append((f"{num1} {operador} {num2} =", num1, operador, num2, resultado))

        elif self.nivel == "Medio":
            for _ in range(10):
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                resultado = num1 * num2
                ecuaciones.append((f"{num1} * {num2} =", num1, "*", num2, resultado))

        elif self.nivel == "Difícil":
            for _ in range(10):
                divisor = random.randint(1, 10)
                cociente = random.randint(1, 10)
                dividendo = divisor * cociente
                ecuaciones.append((f"{dividendo} / {divisor} =", dividendo, "/", divisor, cociente))

        return ecuaciones
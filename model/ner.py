import random 
import time

class Juego:
    def __init__(self, jugador, dificultad, ecuacion):
        self.jugador = jugador
        self.dificultad = dificultad
        self.ecuacion = ecuacion
        self.tiempo_inicio = None
        self.tiempo_fin = None 
    
    def registrar_jugador(self, nombre):
        self.jugador = Jugador(nombre)
        self.dificultad = Dificultad #Instancia de Dificultad 

    def mostrar_tiempo_record(self):
        if self.jugador.record_tiempo == float('inf'):
            print("¡Aún no tienes un tiempo récord!")
        else:
            print(f"Tu tiempo récord es: {self.jugador.record_tiempo:.2f} segundos.")

    def ver_estadisticas(self):
        if not self.jugador.tiene_estadisticas():
            print("¡Aún no tienes estadísticas!")
        else:
            nombre = self.jugador.nombre
            puntaje = self.jugador.puntaje
            posicion = self.jugador.posicion
            print(f"Estadísticas de {nombre}:")
            print(f"Puntaje: {puntaje}")
            print(f"Posición: {posicion}")

    def finalizar_juego(self, respuesta):
        if self.ecuacion.verificar_respuesta(respuesta):
            tiempo_fin = time.time()
            tiempo_transcurrido = tiempo_fin - self.tiempo_inicio
            self.jugador.establecer_tiempo_record(tiempo_transcurrido)
            return True, tiempo_transcurrido
        else: 
            self.intentos_restantes -= 1
            return False, self.intentos_restantes


class Jugador:
    def __init__(self, nombre, posicion, puntaje):
        self.nombre = nombre
        self.posicion = posicion
        self.puntaje = puntaje
    
    def seleccionar_dificultad(self, dificultad):
        self.dificultad = Dificultad(dificultad)

    def ingresar_respuesta(self, respuesta):
        partes = respuesta.split()
        
        if len(partes) != 5 or partes[3] != "=":
            raise ValueError("La respuesta debe tener el formato: 'num1 operador num2 = resultado' con espacios.")

        try:
            num1 = int(partes[0])
            operador = partes[1]
            num2 = int(partes[2])
            resultado = int(partes[4])
        except ValueError:
            raise ValueError("Formato de respuesta incorrecto. Asegúrese de ingresar números correctamente.")

        return (num1, operador, num2, resultado)

    def cambiar_dificultad(self, lista_dificultades, seleccion):
        return self.seleccionar_dificultad(lista_dificultades, seleccion)


class Dificultad:
    def __init__(self, dificultades):
        self.dificultades: dificultades["Facil","Medio","Dificil"]
    
    def generar_ecuaciones(self, nivel):
        ecuaciones = []

        if nivel == "Facil":
            for _ in range(10):
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                operador = random.choice(["+", "-"])
                resultado = num1 + num2 if operador == "+" else num1 - num2
                ecuaciones.append((f"{num1} {operador} {num2} = ?", num1, operador, num2, resultado))

        elif nivel == "Medio":
            for _ in range(10):
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                resultado = num1 * num2
                ecuaciones.append((f"{num1} * {num2} = ?", num1, "*", num2, resultado))

        elif nivel == "Dificil":
            for _ in range(10):
                divisor = random.randint(1, 10)
                cociente = random.randint(1, 10)
                dividendo = divisor * cociente
                ecuaciones.append((f"{dividendo} / {divisor} = ?", dividendo, "/", divisor, cociente))

        return ecuaciones
    
    def obtener_ecuacion_aleatoria(self):
        if not self.dificultades:
            raise ValueError("Primero debes seleccionar una dificultad")
        else:
            return random.choice(self.ecuaciones)

    def numero_de_intentos(self, nivel):
        return {"Facil": 3, "Medio": 5, "Dificil": 8}.get(nivel, 0)



class Ecuacion: 
    def __init__(self, ecuacion, respuesta):
        self.ecuacion = ecuacion
        self.respuesta = respuesta

    def verificar_respuesta(self, respuesta):
        num1, num2, resultado = respuesta
        return (num1 == self.num1 and
                num2 == self.num2 and 
                resultado == self.respuesta_correcta) 

    def evaluar_intento(self, respuesta):
        respuesta_partes = respuesta.split()
        if len(respuesta_partes) != 5 or respuesta_partes[1] != self.operador or respuesta_partes[3] != "=":
            return "Formato de respuesta incorrecto. Debe ser del tipo 'num1 operador num2 = resultado'"
        
        try: 
            num1_jugador = int(respuesta_partes[0])
            num2_jugador = int(respuesta_partes[2])
            resultado_jugador = int(respuesta_partes[4])
        except ValueError: 
            return "Formato de respuesta incorrecto. Asegúrese de ingresar números correctamente"
        
        retroalimentacion = []
        if num1_jugador == self.num1:
            retroalimentacion.append("num1: Verde")
        elif abs(num1_jugador - self.num1) <= 3:
            retroalimentacion.append("num1: Amarillo")
        else:
            retroalimentacion.append("num1: Rojo")
        
        if num2_jugador == self.num2:
            retroalimentacion.append("num2: Verde")
        elif abs(num2_jugador - self.num2) <= 3:
            retroalimentacion.append("num2: Amarillo")
        else:
            retroalimentacion.append("num2: Rojo")
        
        if resultado_jugador == self.respuesta_correcta:
            retroalimentacion.append("resultado: Verde")
        elif abs(resultado_jugador - self.respuesta_correcta) <= 3: 
            retroalimentacion.append("resultado: Amarillo")
        else:
            retroalimentacion.append("resultado: Rojo")
        
        return retroalimentacion

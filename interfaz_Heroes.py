import random, pygame, sys
from lista_Heroes import ListaHeroes
from lista_Turnos import ListaCircularTurnos

pygame.init()
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("⚔️ BATALLA DE HEROES ⚔️")

#LISTA HEROES
lista = ListaHeroes()
lista.agregar_heroe("Aatrox", 1, 50, 35, "Guerrero")
lista.agregar_heroe("Naafiri", 1, 50, 25, "Asesino")
lista.agregar_heroe("Varus", 1, 50, 20, "Mago")
lista.agregar_heroe("Rhaast", 1, 50, 30, "Guerrero")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 80, 80)
VERDE = (80, 255, 120)
AZUL = (100, 160, 255)
GRIS = (50, 50, 50)
AMARILLO = (255, 200, 50)
CAJA = (30, 30, 30)

fuente = pygame.font.SysFont("Segoe UI Emoji", 20)
fuente_titulo = pygame.font.SysFont("Segoe UI Emoji", 38)
fuente_mensaje = pygame.font.SysFont("Segoe UI Emoji", 18)

class Boton:
    def __init__(self, x, y, w, h, texto, color_fondo, color_texto):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def dibujar(self, pantalla):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(pantalla, self.color_fondo, self.rect, border_radius=10)
        if hover:
            pygame.draw.rect(pantalla, (200,200,200,30), self.rect, 2, border_radius=10)
        text_color = BLANCO if hover else self.color_texto
        texto_renderizado = fuente.render(self.texto, True, text_color)
        text_rect = texto_renderizado.get_rect(center=self.rect.center)
        pantalla.blit(texto_renderizado, text_rect.topleft)    

    def esta_clickeado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos)

mensajes = []

def mostrar_mensajes(texto):
    if len(mensajes) >= 8:
        mensajes.pop(0)
    mensajes.append(texto)

def agregar_y_mostrar_mensajes(nombre, nivel, vida, ataque, tipo):
    try:
        lista.agregar_heroe(nombre, nivel, vida, ataque, tipo)
        mostrar_mensajes(f"✨ Héroe {nombre} agregado.")
    except Exception as e:
        mostrar_mensajes(f"❌ Error al agregar héroe: {e}")

def eliminar_y_mostrar_mensajes(nombre):
    heroe_encontrado = lista.buscar_heroe(nombre)
    if not heroe_encontrado:
        mostrar_mensajes(f"❌ Héroe {nombre} no encontrado")
        return
    exito = lista.eliminar_heroe(nombre)
    if exito is None:
        verificacion = lista.buscar_heroe(nombre)
        if verificacion is None:
            mostrar_mensajes(f"💀 Héroe {nombre} eliminado")
        else:
            mostrar_mensajes(f"❌ No se pudo eliminar al héroe {nombre}")
    elif exito:
        mostrar_mensajes(f"💀 Héroe {nombre} eliminado")
    else:
        mostrar_mensajes(f"❌ Héroe {nombre} no encontrado o no eliminado.")

def mejorar_y_mostrar_mensajes(nombre, inc_vida, inc_ataque):
    heroe = lista.buscar_heroe(nombre)
    if heroe:
        lista.mejorar_heroe(nombre, inc_vida, inc_ataque)
        mostrar_mensajes(f"⚡ Héroe {nombre} mejorado: +{inc_vida} Vida, +{inc_ataque} Ataque.")
    else:
        mostrar_mensajes(f"❌ No se encontró al héroe {nombre}.")

boton_agregar = Boton(600, 100, 150, 40, "Agregar", VERDE, (0, 200, 0))
boton_eliminar = Boton(600, 150, 150, 40, "Eliminar", ROJO, (255, 100, 100))
boton_mejorar = Boton(600, 200, 150, 40, "Mejorar", AZUL, (100, 180, 255))
boton_batalla = Boton(600, 250, 150, 40, "Batalla", (250, 220, 70), (180, 180, 180))
boton_salir = Boton(600, 300, 150, 40, "Salir", GRIS, (180, 180, 180))


def iniciar_batalla(turno_actual=None):
    pantalla.fill(NEGRO)
    titulo = fuente_titulo.render("⚔️ Batalla De Héroes ⚔️", True, VERDE)
    pantalla.blit(titulo, (40, 20))
    
    y = 110
    actual = lista.cabeza
    idx = 0
    while actual:
        if actual.nombre == turno_actual:
            brillo = 150 + int(105 * (abs(pygame.time.get_ticks() % 1000 - 500) / 500))
            color = (100, brillo, 255)
        else:
            color = BLANCO
        vida_max = getattr(actual, "max_vida", actual.vida)
        exp = getattr(actual, "exp", 0)
        tipo_mostrar = getattr(actual, "tipo", "Guerrero")
        indicador = "✨" if actual.nombre == turno_actual else ""
        linea = f"{indicador} 🦸‍♂️ {actual.nombre} ({tipo_mostrar}) - Nv: {actual.nivel} - Vida: {actual.vida}/{vida_max} - Atq: {actual.ataque} - EXP: {exp}"
        vida_max = getattr(actual, "max_vida", actual.vida)
        vida_actual = max(0, actual.vida)
        proporcion = vida_actual / vida_max if vida_max > 0 else 0

        barra_x = 50
        barra_y = y + 25
        ancho_barra = 200
        alto_barra = 10

        if proporcion > 0.6:
            color_barra = VERDE
        elif proporcion > 0.3:
            color_barra = AMARILLO
        else:
            color_barra = ROJO

        pygame.draw.rect(pantalla, (60, 60, 60), (barra_x, barra_y, ancho_barra, alto_barra), border_radius=3)
        pygame.draw.rect(pantalla, color_barra, (barra_x, barra_y, int(ancho_barra * proporcion), alto_barra), border_radius=3)
        render = fuente.render(linea, True, color)
        pantalla.blit(render, (40, y + idx*44))
        idx += 1
        actual = actual.siguiente

    pygame.draw.rect(pantalla, CAJA, (680, 100, 200, 360), border_radius=12)
    for b in [boton_agregar, boton_eliminar, boton_mejorar, boton_batalla, boton_salir]:
        b.dibujar(pantalla)

    pygame.draw.rect(pantalla, (18, 18, 18), (30, 420, 820, 200), border_radius=10)
    pantalla.blit(fuente.render("📜 Registro de eventos:", True, VERDE), (40, 455))

    y_texto = 490
    for mensaje in mensajes:
        texto_renderizado = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_renderizado, (50, y_texto))
        y_texto += 20
    pygame.display.flip()


def dibujar_lista_heroes(turno_actual=None):
    pantalla.fill(NEGRO)

    titulo = fuente_titulo.render("🧙‍♂️ Héroes en la Arena", True, BLANCO)
    pantalla.blit(titulo, (50, 30))

    actual = lista.cabeza
    y = 120
    while actual:
        vida_max = getattr(actual, "max_vida", actual.vida)
        exp = getattr(actual, "exp", 0)
        tipo_mostrar = getattr(actual, "tipo", "Guerrero")
        indicador = "✨" if actual.nombre == turno_actual else ""
        texto = fuente.render(f"{indicador} 🦸‍♂️ {actual.nombre} ({tipo_mostrar}) - Nv: {actual.nivel} - Vida: {actual.vida}/{vida_max} - Atq: {actual.ataque} - EXP: {exp}", True, BLANCO)
        vida_max = getattr(actual, "max_vida", actual.vida)
        vida_actual = max(0, actual.vida)
        proporcion = vida_actual / vida_max if vida_max > 0 else 0

        barra_x = 50
        barra_y = y + 25
        ancho_barra = 200
        alto_barra = 10

        if proporcion > 0.6:
            color_barra = VERDE
        elif proporcion > 0.3:
            color_barra = AMARILLO
        else:
            color_barra = ROJO

        pygame.draw.rect(pantalla, (60, 60, 60), (barra_x, barra_y, ancho_barra, alto_barra), border_radius=3)
        pygame.draw.rect(pantalla, color_barra, (barra_x, barra_y, int(ancho_barra * proporcion), alto_barra), border_radius=3)
        pantalla.blit(texto, (50, y))
        y += 40
        actual = actual.siguiente

    for b in [boton_agregar, boton_eliminar, boton_mejorar, boton_batalla, boton_salir]:
        b.dibujar(pantalla)

    pygame.draw.rect(pantalla, (30, 30, 30), (30, 350, 740, 220), border_radius=10)
    pantalla.blit(fuente.render("📜 Registro de eventos:", True, VERDE), (40, 360))

    y_texto = 395
    for mensaje in mensajes:
        texto_renderizado = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_renderizado, (50, y_texto))
        y_texto += 20

    pygame.display.flip()

def pedir_texto(mensaje, max, espacio):
    texto = ""
    activo = True
    b = True
    lb = pygame.time.get_ticks()
    cancelado = False
    while activo:
        ahora = pygame.time.get_ticks()
        if ahora - lb > 500:
            b = not b
            lb = ahora
        
        pantalla.fill(NEGRO)
        render_mensaje = fuente.render(mensaje, True, BLANCO)
        mostrar_texto = texto + ("|" if b else "")  
        render_texto = fuente.render(texto, True, VERDE)
        pantalla.blit(render_mensaje, (50, 250))
        pantalla.blit(render_texto, (50, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                cancelado = True
                activo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    activo = False
                elif evento.key == pygame.K_ESCAPE:
                    texto = ""
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    c = evento.unicode
                    if c and len(texto) < max:
                        if espacio:
                            permitido = c.isprintable()
                        else:
                            permitido = c.isprintable() and not c.isspace()
                        if permitido:
                            texto += c
    return None if cancelado else texto.strip()

def simular_batalla(rondas=5, turno_delay_ms=1500):
    turnos = ListaCircularTurnos()
    actual = lista.cabeza
    contador = 0
    while actual:
        if actual.vida > 0:
            turnos.agregar_turno(actual.nombre)
            contador += 1
        actual = actual.siguiente

    if contador <= 1:
        mostrar_mensajes("⚠️ No hay suficientes héroes para combatir.")
        return

    mostrar_mensajes("🔥 Comienza la batalla!")
    pygame.event.pump()

    for ronda in range(1, rondas + 1):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mostrar_mensajes(f"🔁 Ronda {ronda} iniciada")
        jugadores_en_ronda = len(turnos.mostrar_turnos())
        for i in range(jugadores_en_ronda):
            nombre_turno = turnos.siguiente_turno()
            if nombre_turno is None:
                break

            dibujar_lista_heroes(turno_actual=nombre_turno)

            heroe = lista.buscar_heroe(nombre_turno)
            if not heroe or heroe.vida <= 0:
                if heroe and heroe.vida <= 0:
                    turnos.eliminar_turno(nombre_turno)
                mostrar_mensajes(f"❌ {nombre_turno} no disponible para turno.")
                pygame.event.pump()
                pygame.time.delay(150)
                continue

            accion = random.choice(["ataque", "curacion", "pasar"])
            valorAtaque = heroe.ataque
            valorCuracion = random.randint(5, 15)

            if accion == "curacion":
                heroe.vida += valorCuracion
                mostrar_mensajes(f"💚 {nombre_turno} se curó +{valorCuracion} puntos (vida: {heroe.vida})")
            elif accion == "ataque":
                objetivo = turnos.obtener_objetivo_aleatorio(nombre_turno, lista)
                if objetivo:
                    if random.random() < 0.10:
                        mostrar_mensajes(f"😎 {objetivo.nombre} esquivó el ataque de {nombre_turno}!")
                    else:
                        daño = valorAtaque
                        if random.random() < 0.15:
                            daño = int(daño * 2)
                            mostrar_mensajes(f"💥 ¡Golpe crítico de {nombre_turno}! Doble daño!")
                        if hasattr(heroe, "tipo") and hasattr(objetivo, "tipo"):
                            ventaja = {
                                "Guerrero": "Asesino",
                                "Asesino": "Mago",
                                "Mago": "Tanque",
                                "Tanque": "Guerrero"
                            }
                            if ventaja.get(heroe.tipo) == objetivo.tipo:
                                daño = int(daño*1.2)
                                mostrar_mensajes(f"💥 Ventaja de tipo: {heroe.tipo} hace más daño a {objetivo.tipo}!")
                            elif ventaja.get(objetivo.tipo) == heroe.tipo:
                                daño = int(daño*0.8)
                                mostrar_mensajes(f"🛡️ {objetivo.tipo} resiste el ataque de {heroe.tipo}!")
                        objetivo.vida -= daño
                        mostrar_mensajes(f"💥 {nombre_turno} atacó a {objetivo.nombre} (-{daño} vida, vida restante: {max(0, objetivo.vida)})")
                        if objetivo.vida <= 0:
                            mostrar_mensajes(f"☠️ {objetivo.nombre} ha caído en batalla!")
                            lista.eliminar_heroe(objetivo.nombre)
                            turnos.eliminar_turno(objetivo.nombre)
                else:
                    mostrar_mensajes(f"⚠️ {nombre_turno} no encontró objetivo")
            else:
                mostrar_mensajes(f"😐 {nombre_turno} pasó turno")

            dibujar_lista_heroes(turno_actual=nombre_turno)
            for i in range(3):
                pygame.event.pump()
                pygame.time.delay(int(turno_delay_ms/2))

            if not turnos.cabeza or len(turnos.mostrar_turnos()) <= 1:
                break

        if not turnos.cabeza or len(turnos.mostrar_turnos()) <= 1:
            break

    mostrar_mensajes("🏁 Fin de la batalla")
    actual = lista.cabeza
    ganador = None
    mayor_vida = -1
    while actual:
        if actual.vida > mayor_vida:
            mayor_vida = actual.vida
            ganador = actual.nombre
        actual = actual.siguiente

    if ganador:
        mostrar_mensajes(f"🏆 {ganador} es el héroe con mayor vida ({mayor_vida})")

        actual = lista.cabeza
        while actual:
            if actual.vida > 0:
                exp_ganada = random.randint(80, 100)
                subio = actual.experiencia(exp_ganada)
                mostrar_mensajes(f"✨ {actual.nombre} ganó {exp_ganada} EXP.")
                if subio:
                    mostrar_mensajes(f"🔥 {actual.nombre} subió a nivel {actual.nivel}!")
            actual = actual.siguiente
    else:
        mostrar_mensajes("💀 No quedó ningún héroe vivo")

    for i in range(6):
        dibujar_lista_heroes()
        pygame.event.pump()
        pygame.time.delay(400)

clock = pygame.time.Clock()
ejecutando = True
while ejecutando:
    dibujar_lista_heroes()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if boton_agregar.esta_clickeado(evento):
            nombre = (pedir_texto("Ingrese el nombre del héroe:", 24, True))
            if nombre is None or nombre == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            nivel_txt = (pedir_texto("Ingrese el nivel del héroe: (Valor númerico)",3,False))
            if nivel_txt is None or nivel_txt == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            vida_txt = (pedir_texto("Ingrese la vida del héroe: (Valor númerico)",5,False))
            if vida_txt is None or vida_txt == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            ataque_txt = (pedir_texto("Ingrese el ataque del héroe: (Valor númerico)",4,False))
            if ataque_txt is None or ataque_txt == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            tipo = (pedir_texto("Ingrese el tipo del héroe (Guerrero/Asesino/Mago/Tanque):", 8, False))
            if tipo is None or tipo == "":
                tipo_norm = "Guerrero"  # por defecto
            else:
                tipo_norm = tipo.strip().capitalize()
            
            tipos_validos = {"Guerrero", "Asesino", "Mago", "Tanque"}
            if tipo_norm not in tipos_validos:
                mostrar_mensajes(f"⚠️ Tipo '{tipo_norm}' no válido. Se asignará 'Guerrero' por defecto.")
                tipo_norm = "Guerrero"

            try:
                nivel = int(nivel_txt)
                vida = int(vida_txt)
                ataque = int(ataque_txt)
                agregar_y_mostrar_mensajes(nombre, nivel, vida, ataque, tipo_norm)
                mostrar_mensajes(f"✨ Héroe {nombre} agregado como {tipo_norm}.")
            except ValueError:
                mostrar_mensajes("❌ Error: nivel, vida y ataque deben ser números enteros")

        if boton_eliminar.esta_clickeado(evento):
            nombre = (pedir_texto("Ingrese el nombre del héroe a eliminar:", 24, True))
            if nombre is None or nombre == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            eliminar_y_mostrar_mensajes(nombre)
        
        if boton_mejorar.esta_clickeado(evento):
            nombre = (pedir_texto("Ingrese el nombre del héroe a mejorar:",24,True))
            if nombre is None or nombre == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            inc_vida_txt = (pedir_texto("Ingrese el incremento de vida: (Valor númerico)",5,False))
            if inc_vida_txt is None or inc_vida_txt == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue
            inc_ataque_txt = (pedir_texto("Ingrese el incremento de ataque: (Valor númerico)",4,False))
            if inc_ataque_txt is None or inc_ataque_txt == "":
                mostrar_mensajes("⚠️ Operacion Cancelada")
                continue

            try:
                inc_vida = int(inc_vida_txt)
                inc_ataque = int(inc_ataque_txt)
                mejorar_y_mostrar_mensajes(nombre, inc_vida, inc_ataque)
            except ValueError:
                mostrar_mensajes("❌ Error: vida y ataque deben ser números enteros")

        if boton_batalla.esta_clickeado(evento):
            simular_batalla()

        if boton_salir.esta_clickeado(evento):
            ejecutando = False
    clock.tick(30)
pygame.quit()
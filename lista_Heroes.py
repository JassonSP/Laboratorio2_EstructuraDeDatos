class NodoHeroe:
    def __init__(self, nombre, nivel, vida, ataque):
        self.nombre = nombre
        self.nivel = nivel
        self.vida = vida
        self.ataque = ataque
        self.siguiente = None

class ListaHeroes:
    def __init__(self):
        self.cabeza = None

    def agregar_heroe(self, nombre, nivel, vida, ataque):
        nuevo = NodoHeroe(nombre, nivel, vida, ataque)
        if self.cabeza is None:
            self.cabeza = nuevo
            print(f"🔥 Héroe {nombre} agregado como cabeza de la lista.")
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            print(f"✨ Héroe {nombre} agregado al final de la lista.")

    def buscar_heroe(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_heroe(self, nombre):
        if self.cabeza is None:
            print("⚠️ La lista está vacía, no hay héroes que eliminar.")
            return

        if self.cabeza.nombre == nombre:
            self.cabeza = self.cabeza.siguiente
            print(f"💀 Héroe {nombre} eliminado (era la cabeza).")
            return

        anterior = self.cabeza
        actual = self.cabeza.siguiente

        while actual:
            if actual.nombre == nombre:
                anterior.siguiente = actual.siguiente
                print(f"💥 Héroe {nombre} eliminado correctamente.")
                return
            anterior = actual
            actual = actual.siguiente

        print(f"❌ Héroe {nombre} no encontrado en la lista.")

    def mejorar_heroe(self, nombre, incremento_vida, incremento_ataque):
        heroe = self.buscar_heroe(nombre)
        if heroe:
            heroe.vida += incremento_vida
            heroe.ataque += incremento_ataque
            print(f"⚡ Héroe {nombre} mejorado: +{incremento_vida} Vida, +{incremento_ataque} Ataque.")
        else:
            print(f"❌ No se encontró al héroe {nombre}.")

    def mostrar_lista(self):
        if self.cabeza is None:
            print("🚫 No hay héroes en la lista.")
            return
        actual = self.cabeza
        print("\n📜 LISTA DE HÉROES:")
        while actual:
            print(f"🧙‍♂️ {actual.nombre} | Nivel {actual.nivel} | Vida: {actual.vida} | Ataque: {actual.ataque}")
            actual = actual.siguiente
        print()
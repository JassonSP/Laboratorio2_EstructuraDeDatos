import random

class NodoTurno:
    def __init__(self, nombre_heroe):
        self.nombre_heroe = nombre_heroe
        self.siguiente = None
    
class ListaCircularTurnos:
    def __init__(self):
        self.cabeza = None
        self.actual = None
    
    def agregar_turno(self, nombre_heroe):
        nuevo = NodoTurno(nombre_heroe)
        if not self.cabeza:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            self.actual = nuevo
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo
            nuevo.siguiente = self.cabeza

    def mostrar_turnos(self):
        if not self.cabeza:
            return []
        turnos = []
        temp = self.cabeza
        while True:
            turnos.append(temp.nombre_heroe)
            temp = temp.siguiente
            if temp == self.cabeza:
                break
        return turnos
    
    def eliminar_turno(self, nombre_heroe):
        if not self.cabeza:
            return False
        
        if self.cabeza.siguiente == self.cabeza and self.cabeza.nombre_heroe == nombre_heroe:
            self.cabeza = None
            self.actual = None
            return True
        
        if self.cabeza.nombre_heroe == nombre_heroe:
            tail = self.cabeza
            while tail.siguiente != self.cabeza:
                tail = tail.siguiente
            tail.siguiente = self.cabeza.siguiente
            if self.actual == self.cabeza:
                self.actual = self.cabeza.siguiente
            self.cabeza = self.cabeza.siguiente
            return True
        prev = self.cabeza
        curr = self.cabeza.siguiente
        while curr != self.cabeza:
            if curr.nombre_heroe == nombre_heroe:
                prev.siguiente = curr.siguiente
                if self.actual and self.actual.nombre_heroe == nombre_heroe:
                    self.actual = prev.siguiente
                return True
            prev = curr
            curr = curr.siguiente
        return False
    
    def siguiente_turno(self):
        if not self.actual:
            return None
        nombre = self.actual.nombre_heroe
        self.actual = self.actual.siguiente
        return nombre
    
    def obtener_objetivo_aleatorio(self, nombre_heroe, lista_heroes):
        vivos = []
        actual = lista_heroes.cabeza
        while actual:
            if actual.nombre != nombre_heroe and actual.vida > 0:
                vivos.append(actual)
            actual = actual.siguiente
        if vivos:
            return random.choice(vivos)
        return None
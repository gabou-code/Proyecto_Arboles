import os
import tkinter as tk
from tkinter import messagebox, filedialog

#logica del arbol

class Nodo:
    #clase para representar un nodo dentro del arbol binario
    def __init__(self, valor, es_pregunta = True):
        self.valor = valor
        self.es_pregunta = es_pregunta
        self.izquierda = None #rama para el si
        self.derecha = None #rama para el no

    def es_hoja(self):
        return not self.es_pregunta
    
class ArbolDecision:

    def __init__(self):
        self.raiz = self.crear_arbol_defecto()
        self.nodo_actual = self.raiz
    
    #funcion para crear un arbol por defecto al ejecutar el programa
    def crear_arbol_defecto(self):
        #crea un arbol basico por defecto si no se carga ningún archivo
        raiz = Nodo("¿Es un animal?", es_pregunta= True)
        raiz.izquierda = Nodo("perro", es_pregunta= False)
        raiz.derecho = Nodo("computadora", es_pregunta=False)
        return raiz
    
    #funcion para reiniciar la partida desde la raiz
    def reiniciar_partida(self):
        #regresa a la raíz del arbol
        self.nodo_actual = self.raiz

    #funcion para avanzar en el arbol
    def avanzar(self, respuesta_si):
        #avanza al hilo izquierdo (si) o derecho(no)

        #validacion de seguridad para evitar trabas
        if self.nodo_actual is None:
            return
        
        if respuesta_si:

            if self.nodo_actual.izquierda is not None:
                self.nodo_actual = self.nodo_actual.izquierda
        else:
            if self.nodo_actual.derecha is not None:
                self.nodo_actual = self.nodo_actual.derecha 

    #funcion para añadir pregunta y respuesta
    def aprender(self, respuesta_incorrecta, nueva_respuesta, nueva_pregunta, respuesta_para_nueva):
        #el nodo actual deja de ser hoja y se convierte en pregunta

        self.nodo_actual.valor = nueva_pregunta
        self.nodo_actual.es_pregunta = True

        nodo_nuevo = Nodo(nueva_respuesta, es_pregunta = False)
        nodo_viejo = Nodo(respuesta_incorrecta, es_pregunta= False)

        #asigna las ramas segun la respuesta que corresponde al nuevo elemento

        if respuesta_para_nueva:
            self.nodo_actual.izquierdo = nodo_nuevo
            self.nodo_actual.derecho = nodo_viejo
        else:
            self.nodo_actual.izquierdo = nodo_viejo
            self.nodo_actual.derecho = nodo_nuevo
        
    #Manejo de archivos

class ManejadorArchivos:
    #se encarga de manejar el arbol en archivos .txt

    def guardar(self,raiz, ruta_archivo):
        lineas = []
        self.preorden_a_lineas(raiz,lineas)
        with open(ruta_archivo, "w", encoding= "utf-8") as f:
            f.write("\n".join(lineas))

    def preorden_a_lineas(self,nodo,lineas):
        if nodo is None:
            return
        
        prefijo = "P:" if nodo.es_pregunta else "R:"
        lineas.append(f"{prefijo}{nodo.valor}")
        self._preorden_a_lineas(nodo.izquierdo, lineas)
        self._preorden_a_lineas(nodo.derecho, lineas)
    
    def cargar(self, ruta_archivo):
        """Lee el archivo de texto y reconstruye el árbol binario de decisión."""
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError("El archivo especificado no existe.")
            
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
            
        if not lineas:
            raise ValueError("El archivo está vacío.")
            
        iterador_lineas = iter(lineas)
        raiz = self._lineas_a_arbol(iterador_lineas)
        return raiz

    def _lineas_a_arbol(self, iterador):
        try:
            linea = next(iterador)
        except StopIteration:
            return None
            
        if not (linea.startswith("P:") or linea.startswith("R:")):
            raise ValueError("Formato de archivo incorrecto.")
            
        es_pregunta = linea.startswith("P:")
        valor = linea[2:]
        
        nodo = Nodo(valor, es_pregunta)
        if es_pregunta:
            nodo.izquierdo = self._lineas_a_arbol(iterador)
            nodo.derecho = self._lineas_a_arbol(iterador)
        return nodo
#revisar ultimos cambios


        

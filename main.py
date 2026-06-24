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
    
    def crear_arbol_defecto(self):
        #crea un arbol basico por defecto si no se carga ningún archivo
        raiz = Nodo("¿Es un animal?", es_pregunta= True)
        raiz.izquierda = Nodo("perro", es_pregunta= False)
        raiz.derecho = Nodo("computadora", es_pregunta=False)
        return raiz

        

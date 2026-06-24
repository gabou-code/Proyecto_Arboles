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

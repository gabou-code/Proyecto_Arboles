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


#interfaz grafica

class App:
    def __init__(self, root):
        self.root = root
        self.root.title = ("Adivina en qué estoy pensando")
        self.root.geometry = ("500x400")
        self.root.config(bg = "#d64343")

        #instancias base de logica y persistencia

        self.arbol = ArbolDecision()
        self.archivo_actual = "arbol_defecto.txt"
        #inicio los componentes visuales de una
        self.inicializar_components()
        self.mostrar_pantalla_inicial()

    def inicializar_components(self):
        
        # ---------------- Pantalla Inicial ----------------
        self.frame_inicio = tk.Frame(self.root, bg="#f0f0f0")
        
        lbl_titulo = tk.Label(self.frame_inicio, text="Adivina en qué estoy pensando", font=("Arial", 16, "bold"), bg="#f0f0f0")
        lbl_titulo.pack(pady=20)
        
        lbl_instrucciones = tk.Label(
            self.frame_inicio, 
            text="Piensa en un objeto o animal.\nEl sistema intentará adivinar mediante preguntas de Sí o No.",
            font=("Arial", 10), bg="#f0f0f0"
        )
        lbl_instrucciones.pack(pady=10)
        
        self.lbl_archivo_estado = tk.Label(self.frame_inicio, text=f"Archivo activo: {self.archivo_actual}", fg="green", bg="#f0f0f0")
        self.lbl_archivo_estado.pack(pady=5)
        
        btn_cargar = tk.Button(self.frame_inicio, text="Cargar Árbol desde Archivo", command=self.cargar_archivo, width=25)
        btn_cargar.pack(pady=5)
        
        btn_jugar = tk.Button(self.frame_inicio, text="Iniciar Partida", command=self.iniciar_partida, width=25, bg="#4CAF50", fg="white")
        btn_jugar.pack(pady=5)
        
        btn_salir = tk.Button(self.frame_inicio, text="Salir", command=self.root.quit, width=25)
        btn_salir.pack(pady=5)
        
        # ---------------- Pantalla de Juego ----------------
        self.frame_juego = tk.Frame(self.root, bg="#f0f0f0")
        
        self.lbl_pregunta = tk.Label(self.frame_juego, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=400)
        self.lbl_pregunta.pack(pady=40)
        
        self.frame_botones_juego = tk.Frame(self.frame_juego, bg="#f0f0f0")
        self.frame_botones_juego.pack(pady=20)
        
        self.btn_si = tk.Button(self.frame_botones_juego, text="SÍ", width=10, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.btn_si.pack(side=tk.LEFT, padx=20)
        
        self.btn_no = tk.Button(self.frame_botones_juego, text="NO", width=10, bg="#F44336", fg="white", font=("Arial", 12, "bold"))
        self.btn_no.pack(side=tk.RIGHT, padx=20)

    def mostrar_pantalla_inicial(self):
        self.frame_juego.pack_forget()
        self.frame_inicio.pack(fill=tk.BOTH, expand=True)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            try:
                # Se crea la instancia del manejador para usar su método normal
                manejador = ManejadorArchivos()
                raiz_cargada = manejador.cargar(ruta)
                
                self.arbol.raiz = raiz_cargada
                self.archivo_actual = ruta
                self.lbl_archivo_estado.config(text=f"Archivo activo: {os.path.basename(ruta)}")
                messagebox.showinfo("Éxito", "Árbol de decisión cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo.\nMotivo: {str(e)}\n\nSe continuará con el árbol actual.")


    def iniciar_partida(self):
        self.arbol.reiniciar_partida()
        self.frame_inicio.pack_forget()
        self.frame_juego.pack(fill=tk.BOTH, expand=True)
        self.actualizar_interfaz_juego()

    
    def actualizar_interfaz_juego(self):
        nodo = self.arbol.nodo_actual
        
        # Si por alguna razón el árbol quedó mal estructurado, regresa al menú
        if nodo is None:
            messagebox.showerror("Error", "Se llegó a un nodo vacío. Estructura de árbol inválida.")
            self.mostrar_pantalla_inicial()
            return
        
        if nodo.es_pregunta:
            # Si es pregunta, los botones avanzan en el árbol
            self.lbl_pregunta.config(text=nodo.valor)
            self.btn_si.config(command=lambda: self.procesar_respuesta(True))
            self.btn_no.config(command=lambda: self.procesar_respuesta(False))
        else:
            # SI ES HOJA: Los botones cambian de rol por completo (Victoria o Aprendizaje)
            # ¡Aquí ya NO deben llamar a avanzar()!
            self.lbl_pregunta.config(text=f"¿Estás pensando en un/a: {nodo.valor}?")
            self.btn_si.config(command=self.procesar_victoria)
            self.btn_no.config(command=self.abrir_formulario_aprendizaje)

    def procesar_respuesta(self, es_si):
        self.arbol.avanzar(es_si)
        self.actualizar_interfaz_juego()

    def procesar_victoria(self):
        messagebox.showinfo("¡Ganador!", "¡Excelente! He adivinado correctamente.")
        self.mostrar_pantalla_inicial()

    def abrir_formulario_aprendizaje(self):
        """Despliega una ventana emergente estructurada para capturar los nuevos nodos."""
        ventana_aprender = tk.Toplevel(self.root)
        ventana_aprender.title("Enseñar al sistema")
        ventana_aprender.geometry("400x320")
        ventana_aprender.grab_set()  
        
        # FIJAMOS EL VALOR DEL NODO INCORRECTO AQUÍ PARA EVITAR PROBLEMAS DE REFERENCIA EN LÓGICA DE TKINTER
        nodo_incorrecto_fijo = str(self.arbol.nodo_actual.valor)

        tk.Label(ventana_aprender, text="¡Me rindo! Ayúdame a aprender.", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(ventana_aprender, text="¿En qué elemento estabas pensando?").pack()
        txt_nuevo = tk.Entry(ventana_aprender, width=40)
        txt_nuevo.pack(pady=2)
        txt_nuevo.focus_set()
        
        tk.Label(ventana_aprender, text=f"Escribe una pregunta que diferencie tu elemento de '{nodo_incorrecto_fijo}':").pack()
        txt_pregunta = tk.Entry(ventana_aprender, width=40)
        txt_pregunta.pack(pady=2)
        
        tk.Label(ventana_aprender, text=f"Para tu elemento, ¿la respuesta a esa pregunta es Sí o No?").pack(pady=5)
        
        var_opcion = tk.StringVar(value="Si")
        tk.Radiobutton(ventana_aprender, text="Sí", variable=var_opcion, value="Si").pack()
        tk.Radiobutton(ventana_aprender, text="No", variable=var_opcion, value="No").pack()

    def abrir_formulario_aprendizaje(self):
        """Despliega una ventana emergente estructurada para capturar los nuevos nodos."""
        ventana_aprender = tk.Toplevel(self.root)
        ventana_aprender.title("Enseñar al sistema")
        ventana_aprender.geometry("400x320")
        ventana_aprender.grab_set()  
        
        # FIJAMOS EL VALOR DEL NODO INCORRECTO AQUÍ PARA EVITAR PROBLEMAS DE REFERENCIA EN LÓGICA DE TKINTER
        nodo_incorrecto_fijo = str(self.arbol.nodo_actual.valor)

        tk.Label(ventana_aprender, text="¡Me rindo! Ayúdame a aprender.", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(ventana_aprender, text="¿En qué elemento estabas pensando?").pack()
        txt_nuevo = tk.Entry(ventana_aprender, width=40)
        txt_nuevo.pack(pady=2)
        txt_nuevo.focus_set()
        
        tk.Label(ventana_aprender, text=f"Escribe una pregunta que diferencie tu elemento de '{nodo_incorrecto_fijo}':").pack()
        txt_pregunta = tk.Entry(ventana_aprender, width=40)
        txt_pregunta.pack(pady=2)
        
        tk.Label(ventana_aprender, text=f"Para tu elemento, ¿la respuesta a esa pregunta es Sí o No?").pack(pady=5)
        
        var_opcion = tk.StringVar(value="Si")
        tk.Radiobutton(ventana_aprender, text="Sí", variable=var_opcion, value="Si").pack()
        tk.Radiobutton(ventana_aprender, text="No", variable=var_opcion, value="No").pack()

        def guardar_conocimiento():
            nuevo_val = txt_nuevo.get().strip()
            preg_val = txt_pregunta.get().strip()
            
            if not nuevo_val or not preg_val:
                messagebox.showerror("Campos Vacíos", "Por favor, completa todos los campos de texto.", parent=ventana_aprender)
                return
                
            if not preg_val.startswith("¿") or not preg_val.endswith("?"):
                preg_val = f"¿{preg_val}?"

            es_si = (var_opcion.get() == "Si")
            
            # Pasamos explícitamente el valor congelado de la variable
            self.arbol.aprender(nodo_incorrecto_fijo, nuevo_val, preg_val, es_si)
            
            try:
                # Se crea la instancia del manejador para usar su método normal
                manejador = ManejadorArchivos()
                manejador.guardar(self.arbol.raiz, self.archivo_actual)
                
                messagebox.showinfo("Progreso Guardado", f"Árbol actualizado y guardado en '{os.path.basename(self.archivo_actual)}'.")
            except Exception as e:
                messagebox.showerror("Error al Guardar", f"El sistema aprendió pero no se pudo escribir el archivo: {str(e)}")

            ventana_aprender.destroy()
            self.mostrar_pantalla_inicial()

        tk.Button(ventana_aprender, text="Guardar Conocimiento", command=guardar_conocimiento, bg="#4CAF50", fg="white").pack(pady=15)

# =====================================================================
# EJECUCIÓN PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    if not os.path.exists("arbol_defecto.txt"):
        with open("arbol_defecto.txt", "w", encoding="utf-8") as archivo_base:
            archivo_base.write("P:¿Es un animal?\nR:perro\nR:computadora")
            
    root = tk.Tk()
    app = App(root)
    root.mainloop()



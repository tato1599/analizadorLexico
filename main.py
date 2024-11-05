import tkinter as tk
from tkinter import ttk
import lexico
from lexico import lexer  # Importa el lexer desde lexico.py


# Función para manejar el envío de datos
def enviar_datos():
    texto = entrada.get("1.0", tk.END).strip()  # Eliminar espacios en blanco

    for item in tabla.get_children():
        tabla.delete(item)

    entrada.tag_remove("palabraReservada", "1.0", tk.END)
    entrada.tag_remove("operador", "1.0", tk.END)
    entrada.tag_remove("numero", "1.0", tk.END)
    entrada.tag_remove("identificador", "1.0", tk.END)
    entrada.tag_remove("invalido", "1.0", tk.END)

    if not texto:
        return

    lexer.lineno = 1
    lexer.input(texto)

    for tok in lexer:
        tabla.insert("", "end", values=(tok.lexpos, tok.value, tok.type, tok.lineno, tok.lexpos))

    colorear_texto()


def colorear_texto(event=None):
    texto = entrada.get("1.0", tk.END)
    lexer.input(texto)

    entrada.tag_remove("palabraReservada", "1.0", tk.END)
    entrada.tag_remove("operador", "1.0", tk.END)
    entrada.tag_remove("numero", "1.0", tk.END)
    entrada.tag_remove("identificador", "1.0", tk.END)
    entrada.tag_remove("invalido", "1.0", tk.END)

    for tok in lexer:
        inicio = f"1.0 + {tok.lexpos} chars"
        fin = f"{inicio} + {len(str(tok.value))} chars"
        if tok.type in ["palabraReservadaFOR", "palabraReservadaINT"]:
            entrada.tag_add("palabraReservada", inicio, fin)
        elif tok.type in ["MAS", "MENOS", "MULTI", "DIVI", "IGUAL", "MAYOR", "MENOR", "MAYORIGUAL", "MENORIGUAL",
                          "EQUIVALENTE", "DIFERENTE"]:
            entrada.tag_add("operador", inicio, fin)
        elif tok.type == "NUM":
            entrada.tag_add("numero", inicio, fin)
        elif tok.type == "ID":
            entrada.tag_add("identificador", inicio, fin)
        elif tok.type == "INVALIDO":
            entrada.tag_add("invalido", inicio, fin)

    actualizar_lineas()


# Función para actualizar el conteo de líneas
def actualizar_lineas(event=None):
    lineas.config(state="normal")
    lineas.delete("1.0", tk.END)

    line_count = int(entrada.index("end-1c").split(".")[0])
    lines_content = "\n".join(str(i) for i in range(1, line_count + 1))
    lineas.insert("1.0", lines_content)

    lineas.config(state="disabled")

# Sincronizar el desplazamiento de líneas con el desplazamiento de entrada
def sync_line_numbers(event):
    # Sincroniza la vista de `lineas` con `entrada`
    lineas.yview_moveto(entrada.yview()[0])


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador Léxico")
ventana.geometry("1280x900")

# Botón de enviar
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_datos)
boton_enviar.pack(pady=10)

# Frame para entrada de texto y conteo de líneas con scroll
frame = tk.Frame(ventana)
frame.pack(pady=5, fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

# Widget de conteo de líneas
lineas = tk.Text(frame, width=4, height=20, bg="#333333", fg="white", font=("Courier", 14), state="disabled")
lineas.pack(side="left", fill="y")

# Configuración de entrada de texto
entrada = tk.Text(frame, wrap="word", width=200, height=20, bg="#c9c9c9", fg="black", insertbackground="white",
                  font=("Courier", 14), yscrollcommand=scrollbar.set)
entrada.tag_configure("palabraReservada", foreground="blue")
entrada.tag_configure("operador", foreground="red")
entrada.tag_configure("numero", foreground="purple")
entrada.tag_configure("identificador", foreground="black")
entrada.tag_configure("invalido", foreground="black", underline=True)
entrada.pack(side="left", fill="both", expand=True)

# Configurar scrollbar para entrada y sincronizar con líneas
scrollbar.config(command=entrada.yview)
entrada.bind("<<Scroll>>", sync_line_numbers)
entrada.bind("<KeyRelease>", lambda event: (colorear_texto(), actualizar_lineas()))


# Asignar eventos
entrada.bind("<KeyRelease>", lambda event: (colorear_texto(), actualizar_lineas()))

# Tabla para mostrar los resultados
columnas = ("columna", "lexema", "token", "linea", "posicion")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=50)

# Configurar encabezados
tabla.heading("columna", text="Columna")
tabla.heading("lexema", text="Lexema")
tabla.heading("token", text="Token")
tabla.heading("linea", text="Línea")
tabla.heading("posicion", text="Posición")

# Ajustar el tamaño de cada columna
tabla.column("columna", width=80)
tabla.column("lexema", width=150)
tabla.column("token", width=100)
tabla.column("linea", width=80)
tabla.column("posicion", width=80)

tabla.pack(pady=30, fill="x")

# Inicializar conteo de líneas al iniciar
actualizar_lineas()

ventana.mainloop()

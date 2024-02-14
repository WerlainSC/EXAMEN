import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText  
import ply.lex as lex

class Vocabulario(object):
    palabras_reservadas = {
        'for': 'FOR', 'do': 'DO', 'while': 'WHILE',
        'if': 'IF', 'else': 'ELSE', 'switch': 'SWITCH',
        'case': 'CASE', 'break': 'BREAK', 'return': 'RETURN',
        'static': 'STATIC', 'print': 'PRINT', 'int': 'INT',
        'float': 'FLOAT', 'void': 'VOID', 'public': 'PUBLIC',
        'private': 'PRIVATE',
        'area': 'Palabra_R', 'base': 'Palabra_R', 'altura': 'Palabra_R',
    }

    tokens = [
        'IDENTIFICADOR', 'NUMERO', 'CADENA',
        'OPERADOR', 'SIMBOLO', 'FIN',  
    ] + list(palabras_reservadas.values())

    t_OPERADOR = r'[\+\*-/=]'
    t_SIMBOLO = r'[\(\)\[\]\{\};,]'
    t_ignore = ' \t'

    def t_NUMERO(self, t):
        r'\d*\.\d+|\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        if t.value.is_integer():
            t.value = int(t.value)
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.palabras_reservadas.get(t.value.lower(), 'IDENTIFICADOR') 
        return t

    def t_CADENA(self, t):
        r'\".*?\"'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.build()
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

def analizar_codigo():
    codigo = entrada_codigo.get("1.0", "end-1c")
    vocabulario = Vocabulario()
    tokens = vocabulario.test(codigo)

    for i in result_tree.get_children():
        result_tree.delete(i)

    for tok in tokens:
        palabra_reservada = 'x' if tok.type in Vocabulario.palabras_reservadas.values() else ''
        identificador = 'x' if tok.type == 'IDENTIFICADOR' else ''
        operador = 'x' if tok.type == 'OPERADOR' else ''
        numero = 'x' if tok.type == 'NUMERO' else ''
        simbolo = 'x' if tok.type == 'SIMBOLO' else ''

        result_tree.insert("", 'end', values=(tok.value, palabra_reservada, identificador, operador, numero, simbolo, tok.lineno))

ventana = tk.Tk()
ventana.title("Analizador Léxico con Tkinter")

frame_izquierda = ttk.Frame(ventana)
frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

entrada_codigo = ScrolledText(frame_izquierda, width=40, height=10, wrap=tk.WORD)
entrada_codigo.pack(fill="both", expand=True)

boton_analizar = tk.Button(frame_izquierda, text="Analizar Código", command=analizar_codigo)
boton_analizar.pack(pady=5)

frame_derecha = ttk.Frame(ventana)
frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

result_tree = ttk.Treeview(frame_derecha, columns=("Token", "Palabra Reservada", "Identificador", "Operador", "Número", "Símbolo", "Línea"), show="headings")
result_tree.heading("Token", text="Token")
result_tree.heading("Palabra Reservada", text="Palabra Reservada")
result_tree.heading("Identificador", text="Identificador")
result_tree.heading("Operador", text="Operador")
result_tree.heading("Número", text="Número")
result_tree.heading("Símbolo", text="Símbolo")
result_tree.heading("Línea", text="Línea")

# Ajusta el ancho de cada columna
result_tree.column("Token", width=100)
result_tree.column("Palabra Reservada", width=100)
result_tree.column("Identificador", width=100)
result_tree.column("Operador", width=100)
result_tree.column("Número", width=100)
result_tree.column("Símbolo", width=100)
result_tree.column("Línea", width=100)

result_tree.pack(fill="both", expand=True)

ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(0, weight=1)

ventana.mainloop()
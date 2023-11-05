import tkinter as tk
from tkinter import ttk

def formatar_telefone(event):
    # Obtém o texto atual do campo de entrada
    texto = telefone_entry.get()
    
    # Remove todos os caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, texto))
    
    # Formata o número como (XXX) XXX-XXXX
    if len(numeros) >= 10:
        telefone_formatado = "({}) {}-{}".format(numeros[:2], numeros[2:7], numeros[7:])
    else:
        telefone_formatado = numeros

    # Atualiza o campo de entrada com o texto formatado
    telefone_entry.delete(0, tk.END)
    telefone_entry.insert(0, telefone_formatado)

# Cria a janela principal
janela = tk.Tk()
janela.title("Campo de Telefone com Máscara")

# Cria um campo de entrada
telefone_entry = ttk.Entry(janela)
telefone_entry.pack(padx=10, pady=10)

# Vincula a função de formatação ao evento de entrada
telefone_entry.bind("<KeyRelease>", formatar_telefone)

# Inicia a janela principal
janela.mainloop()

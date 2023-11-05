import tkinter as tk
from tkinter import Entry, Button, Label
import webview

# Função para exibir o mapa no WebView
def exibir_mapa():
    webview.create_window("Mapa do Brasil", "mapa.html", width=800, height=600)
    webview.start()

# Cria a janela principal
janela = tk.Tk()
janela.title("Mapa do Brasil")

# Cria campos de entrada para latitude e longitude
lat_label = Label(janela, text="Latitude:")
lat_label.pack()
lat_entry = Entry(janela)
lat_entry.pack()

lon_label = Label(janela, text="Longitude:")
lon_label.pack()
lon_entry = Entry(janela)
lon_entry.pack()

# Cria botão para exibir o mapa
exibir_botao = Button(janela, text="Exibir Mapa", command=exibir_mapa)
exibir_botao.pack()

# Inicia a janela principal
janela.mainloop()

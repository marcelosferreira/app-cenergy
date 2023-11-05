import tkinter as tk
from tkinter import Entry, Button, Label
import folium
import webbrowser  # Importe a biblioteca webbrowser

# Variáveis globais para armazenar as coordenadas
latitude = None
longitude = None

# Função para atualizar o mapa com as coordenadas inseridas
def atualizar_mapa():
    global latitude, longitude
    # Obtém as coordenadas da latitude e longitude dos campos de entrada
    latitude = float(lat_entry.get())
    longitude = float(lon_entry.get())

    # Cria um mapa Folium centrado nas coordenadas especificadas
    mapa = folium.Map(location=[latitude, longitude], zoom_start=6)

    # Adiciona um marcador no mapa nas coordenadas especificadas
    folium.Marker([latitude, longitude], tooltip="Localização").add_to(mapa)

    # Salva o mapa como um arquivo HTML temporário
    mapa.save('mapa.html')

    # Abre o arquivo mapa.html em um navegador
    abrir_mapa()

# Função para abrir o arquivo mapa.html em um navegador
def abrir_mapa():
    webbrowser.open('mapa.html')

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

# Cria botão para atualizar o mapa e abrir no navegador
atualizar_abrir_botao = Button(janela, text="Atualizar e Abrir Mapa", command=atualizar_mapa)
atualizar_abrir_botao.pack()

# Configura o WebView para exibir o mapa
import webview
webview.create_window("Mapa do Brasil", width=800, height=600)

# Inicia a janela principal
janela.mainloop()

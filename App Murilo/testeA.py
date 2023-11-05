import tkinter as tk
from tkinter import ttk

class FormularioAtraente:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Formulário de 3 Etapas")
        
        self.etapas = [
            "Especificação do esquema de certificação",
            "Especificação da demanda",
            "Especificação das fontes de geração de energia"
        ]
        self.etapa_atual = tk.StringVar(value=self.etapas[0])

        # Configurar menu lateral
        self.menu_lateral = ttk.Frame(self.janela)
        self.menu_lateral.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        for etapa in self.etapas:
            radio = tk.Radiobutton(self.menu_lateral, text=etapa, wraplength=200, justify="left", variable=self.etapa_atual, value=etapa, command=self.mostrar_etapa)
            radio.pack(side="top", anchor="w", padx=10, pady=5)

        # Configurar o conteúdo da etapa
        self.conteudo_etapa = ttk.Frame(self.janela)
        self.conteudo_etapa.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Botões de navegação
        self.botao_anterior = ttk.Button(self.conteudo_etapa, text="Anterior", command=self.etapa_anterior)
        self.botao_anterior.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.botao_proximo = ttk.Button(self.conteudo_etapa, text="Próximo", command=self.proxima_etapa)
        self.botao_proximo.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        # Configurar conteúdo das etapas
        self.conteudo_etapas = [self.criar_etapa1(), self.criar_etapa2(), self.criar_etapa3()]

        # Mostrar a primeira etapa por padrão
        self.mostrar_etapa()

    def criar_etapa1(self):
        etapa1 = ttk.Frame(self.conteudo_etapa)

        ttk.Label(etapa1, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = ttk.Entry(etapa1)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa1, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = ttk.Entry(etapa1)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa1, text="Senha:").grid(row=2, column=0, sticky="w")
        self.senha_entry = ttk.Entry(etapa1, show="*")
        self.senha_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        return etapa1

    def criar_etapa2(self):
        etapa2 = ttk.Frame(self.conteudo_etapa)

        ttk.Label(etapa2, text="Mensagem:").grid(row=0, column=0, sticky="w")
        self.mensagem_entry = ttk.Entry(etapa2)
        self.mensagem_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Comentário:").grid(row=1, column=0, sticky="w")
        self.comentario_entry = ttk.Entry(etapa2)
        self.comentario_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Caminho:").grid(row=2, column=0, sticky="w")
        self.caminho_entry = ttk.Entry(etapa2)
        self.caminho_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        return etapa2

    def criar_etapa3(self):
        etapa3 = ttk.Frame(self.conteudo_etapa)

        ttk.Label(etapa3, text="Nível de Satisfação:").grid(row=0, column=0, sticky="w")
        self.satisfacao_entry = ttk.Entry(etapa3)
        self.satisfacao_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa3, text="Nota do Atendimento:").grid(row=1, column=0, sticky="w")
        self.nota_entry = ttk.Entry(etapa3)
        self.nota_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(etapa3, text="Enviar", command=self.enviar_formulario).grid(row=2, column=0, columnspan=2, pady=20)

        return etapa3

    def mostrar_etapa(self):
        etapa_atual_index = self.etapas.index(self.etapa_atual.get())
        for etapa in self.conteudo_etapas:
            etapa.grid_remove()
        self.conteudo_etapas[etapa_atual_index].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.botao_anterior["state"] = "normal" if etapa_atual_index > 0 else "disabled"
        self.botao_proximo["state"] = "normal" if etapa_atual_index < len(self.etapas) - 1 else "disabled"

    def etapa_anterior(self):
        etapa_atual_index = self.etapas.index(self.etapa_atual.get())
        if etapa_atual_index > 0:
            self.etapa_atual.set(self.etapas[etapa_atual_index - 1])
            self.mostrar_etapa()

    def proxima_etapa(self):
        etapa_atual_index = self.etapas.index(self.etapa_atual.get())
        if etapa_atual_index < len(self.etapas) - 1:
            self.etapa_atual.set(self.etapas[etapa_atual_index + 1])
            self.mostrar_etapa()

    def enviar_formulario(self):
        i=0
        # Aqui você pode adicionar o código para enviar os dados do formulário para onde desejar
        # Por exemplo, você pode acessar os valores dos campos usando self.nome_entry.get(), self.email_entry.get(), etc.
        # E então, enviar esses dados para um servidor, banco de dados, ou onde quer que você precise.

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioAtraente(root)
    root.mainloop()
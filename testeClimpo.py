import json
import tkinter as tk
from tkinter import XView, ttk
from tkinter import font as tkfont
from tkinter import Canvas, Scrollbar
from tkinter import messagebox
from PIL import Image, ImageTk  # Importar a biblioteca PIL (Pillow) para trabalhar com imagens
from tkinter import Entry, Button, Label, filedialog
import masks
from validations import validate_latitude, CoordenadasInvalidasError
import folium

import webbrowser


# Retirar a bnd em branco subst para icone
# Retirar rest do 1, 2 e 5
# as correlações entre os campos na planilha na pasta
# complementar com duas colunas na etapa 3

# Variáveis globais para armazenar as coordenadas
latitude = None
longitude = None

class FormularioPassoAPasso:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("App")
        self.fonte = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.fonteB = tkfont.Font(family="Helvetica", size=10, weight="bold")

        self.etapas = [
            "1. Especificação do esquema de certificação",
            "2. Especificação da demanda",
            "3. Especificação das fontes de geração de energia",
            "4. Especificação da tecnologia de armazenamento",
            "5. Especificar parâmetros de projeto"
        ]
        self.etapa_atual = tk.StringVar(value=self.etapas[0])

        # Definição de estilos TTK
        style = ttk.Style()
        style.configure('TFrame', background="#EEE")
        style.configure('Estilo2.TFrame', background="teal")
        style.configure('TLabel', foreground="black")
        style.configure('Branco.TLabel', foreground="white")

        # Configurar menu lateral
        self.menu_lateral = ttk.Frame(self.janela, style='Estilo2.TFrame')
        self.menu_lateral.grid(row=0, column=0, padx=0, pady=0, sticky="n")
        ttk.Label(self.menu_lateral, text="Etapas:",font=self.fonte, style='Branco.TLabel', background='teal').pack(side="top", anchor="w", padx=10, pady=5)

        for etapa in self.etapas:
            #radio = ttk.Radiobutton(self.menu_lateral, text=etapa, variable=self.etapa_atual, value=etapa, command=self.mostrar_etapa)
            radio = tk.Radiobutton(self.menu_lateral, text=etapa, bg="teal", fg="white", selectcolor="black", wraplength=200, justify="left", variable=self.etapa_atual, value=etapa, command=self.mostrar_etapa)
            radio.pack(side="top", anchor="w", padx=10, pady=5)

        # Configurar o conteúdo da etapa
        self.conteudo_etapa = ttk.Frame(self.janela)
        self.conteudo_etapa.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")

        self.subframe_navegacao = ttk.Frame(self.menu_lateral, style='Estilo2.TFrame')
        self.subframe_navegacao.pack(side="right", fill="both")

        # Botões de navegação
        self.botao_anterior = ttk.Button(self.subframe_navegacao, text="Anterior", command=self.etapa_anterior)
        self.botao_anterior.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        #self.botao_anterior.pack(side="left", anchor="w", padx=10, pady=5)
        self.botao_proximo = ttk.Button(self.subframe_navegacao, text="Próximo", command=self.proxima_etapa)
        #self.botao_proximo.pack(side="right", anchor="w", padx=10, pady=5)
        self.botao_proximo.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        self.botao_enviar = ttk.Button(self.subframe_navegacao, text="Enviar", command=self.enviar_formulario)
        self.botao_enviar.grid(row=2, column=0, columnspan=3, padx=20, sticky="nsew")

        # Configurar conteúdo das etapas
        self.conteudo_etapas = [self.criar_etapa1(), self.criar_etapa2(), self.criar_etapa3(),  self.criar_etapa4(),  self.criar_etapa5()]

        # Mostrar a primeira etapa por padrão
        self.mostrar_etapa()

    def criar_etapa1(self):
        
        etapa1 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa1, text="Especificação do esquema de certificação",font=self.fonte).grid(row=0, column=0, columnspan=6, sticky="w")

        # Adicione uma barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(etapa1, orient="vertical")
        scrollbar_y.grid(row=1, column=1, sticky="ns")

        # Configure o widget Canvas para usar a barra de rolagem vertical
        self.canvas = tk.Canvas(etapa1, yscrollcommand=scrollbar_y.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        # Crie um quadro para conter o conteúdo real que será rolado
        conteudo = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=conteudo, anchor="nw")

        ttk.Label(conteudo, text="1. Tipo de Certificação:", font=self.fonteB).grid(row=1, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=1, column=3, pady=20)
        
        # Predefinições e interações entre menus e seleções
        self.certif_var = tk.StringVar()
        self.op_certfic_var = tk.StringVar()

        def on_certificacao_changed():
            selected_option = self.certif_var.get()
            if selected_option == "energia_fornecida":
                for widget in conteudo.winfo_children():
                    if isinstance(widget, tk.Radiobutton) and widget.cget("text") == "24 7 CFE (Carbon Free Energy)":
                        widget.config(state=tk.NORMAL)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "RED - Renewable Energy Directive":
                        widget.config(state=tk.DISABLED)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "Low Carbon Hydrogen Standart":
                        widget.config(state=tk.DISABLED)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "CHPS - Clean Hydrogen Production Standart":
                        widget.config(state=tk.DISABLED)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "Outro":
                        widget.config(state=tk.DISABLED)
                self.part_minima.config(state=tk.NORMAL)

            elif selected_option == "hidrgenio_produzido":
                for widget in conteudo.winfo_children():
                    if isinstance(widget, tk.Radiobutton) and widget.cget("text") == "24 7 CFE (Carbon Free Energy)":
                        widget.config(state=tk.DISABLED)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "RED - Renewable Energy Directive":
                        widget.config(state=tk.NORMAL)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "Low Carbon Hydrogen Standart":
                        widget.config(state=tk.NORMAL)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "CHPS - Clean Hydrogen Production Standart":
                        widget.config(state=tk.NORMAL)
                    elif isinstance(widget, tk.Radiobutton) and widget.cget("text") == "Outro":
                        widget.config(state=tk.NORMAL)
                self.part_minima.config(state=tk.DISABLED)
        
        def on_opcertificacao_changed():
            selected_option = self.op_certfic_var.get()
            if selected_option == "RED - Renewable Energy Directive":
                self.limite_intensidade.delete(0, tk.END)
                self.limite_intensidade.insert(0, "18")
                self.limite_particiapacao.delete(0, tk.END)
                self.limite_particiapacao.insert(0, "90")
                menu_balanco_energia.set("Horária")
                menu_limite_bidding_zone.set("SIN")
                self.limite_adicionalidade.delete(0, tk.END)
                self.limite_adicionalidade.insert(0, "3")
                self.limite_emissoes_cadeira_producao.delete(0, tk.END)
                self.limite_emissoes_cadeira_producao.insert(0, "28.2")
                menu_fronteira_analise.set("Até a entrega")
                self.imaterialidade.delete(0, tk.END)
                self.imaterialidade.insert(0, "N/A")
                #self.imaterialidade.config(state=tk.DISABLED)
                menu_criterio_fator_emissão_hidrogenio.set("Combustão + Upstream")
            elif selected_option == "Low Carbon Hydrogen Standart":
                self.limite_intensidade.delete(0, tk.END)
                self.limite_intensidade.insert(0, "N/A")
                self.limite_particiapacao.delete(0, tk.END)
                self.limite_particiapacao.insert(0, "0")
                menu_balanco_energia.set("A cada 30 min")
                menu_limite_bidding_zone.set("SIN")
                self.limite_adicionalidade.delete(0, tk.END)
                self.limite_adicionalidade.insert(0, "N/A")
                self.limite_emissoes_cadeira_producao.delete(0, tk.END)
                self.limite_emissoes_cadeira_producao.insert(0, "20")
                menu_fronteira_analise.set("Até a produção")
                self.imaterialidade.delete(0, tk.END)
                self.imaterialidade.insert(0, "0.2")
                #self.imaterialidade.config(state=tk.DISABLED)
                menu_criterio_fator_emissão_hidrogenio.set("Combustão + Upstream")
                
        tk.Radiobutton(conteudo, text="Certificação de Energia Fornecida", variable=self.certif_var, value="energia_fornecida", command=on_certificacao_changed).grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
        tk.Radiobutton(conteudo, text="Certificação de Hidrogênio Produzido", variable=self.certif_var, value="hidrgenio_produzido", command=on_certificacao_changed).grid(row=2, column=2, columnspan=2, sticky="w")

        ttk.Label(conteudo, text="2. Selecione uma opção de esquemas de certificação:", font=self.fonteB).grid(row=3, pady=20, column=0, columnspan=4, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=3, column=3, pady=20)

        self.certificacao_selecionadas = []
        certificacao_opcoes = ["24 7 CFE (Carbon Free Energy)", "RED - Renewable Energy Directive", "Low Carbon Hydrogen Standart", "CHPS - Clean Hydrogen Production Standart", "Outro"]
        for col, opcao in enumerate(certificacao_opcoes):
            certificacao_var = tk.BooleanVar(),
            self.certificacao_selecionadas.append((opcao, certificacao_var))

            imagem = Image.open(f"{opcao.lower().replace(' ', '_')}.png")
            largura_maxima = 50
            imagem.thumbnail((largura_maxima, largura_maxima))
            imagem = ImageTk.PhotoImage(imagem)

            imagem_label = tk.Label(conteudo, image=imagem)
            imagem_label.grid(row=4, column=col, padx=10, sticky="w")
            tk.Radiobutton(conteudo, text=opcao, justify="left", variable=self.op_certfic_var, value=opcao, wraplength=110, command=on_opcertificacao_changed).grid(row=5, column=col, padx=10, sticky="w")
            imagem_label.image = imagem
        

        ttk.Label(conteudo, text="3. Especificações dos critérios para uso da Energia da rede:", font=self.fonteB).grid(row=6, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=6, column=3, pady=20)
        ttk.Label(conteudo, wraplength=360, text="- No caso de Certificação de Energia Fornecida, qual a participação mínima de fontes de baixo carbono? (Em %)").grid(row=7, column=0, columnspan=6, padx=20, sticky="w")
        self.part_minima = ttk.Entry(conteudo)
        self.part_minima.grid(row=7, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, text="- No caso das Certificações do Hidrogênio, marque as opções de métricas apresentadas na tabela abaixo que compõe cada possível critério.").grid(row=8, column=0, columnspan=6, padx=20, pady=12, sticky="w")
        
        add_criterio_botao = ttk.Button(conteudo, text="Adicionar Critério")
        add_criterio_botao.grid(row=9, column=0, pady=20)
        tk.Label(conteudo, wraplength=110, justify="center", text="Intensidade de carbono no Grid").grid(row=9, column=1, padx=5, pady=20, sticky="w")
        tk.Label(conteudo, wraplength=110, justify="center", text="Participação mínima de renováveis no grid").grid(row=9, column=2, padx=5, pady=20, sticky="w")
        tk.Label(conteudo, wraplength=110, justify="center", text="Contratação de planta de baixo carbono com correlação temporal").grid(row=9, column=3, padx=5, pady=20, sticky="w")
        tk.Label(conteudo, wraplength=110, justify="center", text="Contratação de planta de baixo carbono com correlação espacial").grid(row=9, column=4, padx=5, pady=20, sticky="w")
        tk.Label(conteudo, wraplength=100, justify="center", text="Contratação de planta de baixo carbono com adicionalidade").grid(row=9, column=5, padx=25, pady=20, sticky="w")
        
        tk.Label(conteudo, wraplength=100, justify="center", text="Critério 1").grid(row=10, column=0, padx=20, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=10, column=1, padx=40, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=10, column=2, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=10, column=3, padx=50, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=10, column=4, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=10, column=5, padx=55, sticky="w")

        tk.Label(conteudo, wraplength=100, justify="center", text="Critério 2").grid(row=11, column=0, padx=20, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=11, column=1, padx=40, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=11, column=2, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=11, column=3, padx=50, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=11, column=4, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=11, column=5, padx=55, sticky="w")

        tk.Label(conteudo, wraplength=100, justify="center", text="Critério 3").grid(row=12, column=0, padx=20, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=12, column=1, padx=40, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=12, column=2, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=12, column=3, padx=50, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=12, column=4, padx=45, sticky="w")
        tk.Checkbutton(conteudo, justify="center").grid(row=12, column=5, padx=55, sticky="w")

        ttk.Label(conteudo, text="Especificações das Métricas selecionadas na tabela anterior:").grid(row=15, column=0, columnspan=6, padx=20, pady=14, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=15, column=3, pady=20)
        ttk.Label(conteudo, text="- Limite de Intensidade de Carbono do Grid (gCO2/MJ):").grid(row=16, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        self.limite_intensidade = ttk.Entry(conteudo)
        self.limite_intensidade.grid(row=16, column=3, padx=10, sticky="w")
        self.limite_intensidade.bind("<KeyRelease>", self.mask)
        ttk.Label(conteudo, wraplength=390, text="- Limite de Participação mínima de renováveis da energia da rede (em %):").grid(row=17, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        self.limite_particiapacao = ttk.Entry(conteudo)
        self.limite_particiapacao.grid(row=17, column=3, padx=10, sticky="w")
        self.limite_particiapacao.bind("<KeyRelease>", self.mask)
        ttk.Label(conteudo, wraplength=390, text="- Matching para balanço de energia:").grid(row=18, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        opcoes_balanco_energia = ["Mensal", "Semanal", "Horária", "A cada 30 min"]
        self.balanco_energia = tk.StringVar(conteudo)
        self.balanco_energia.set(opcoes_balanco_energia[0])
        menu_balanco_energia = ttk.Combobox(conteudo, textvariable=self.balanco_energia, values=opcoes_balanco_energia)
        menu_balanco_energia.grid(row=18, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=390, text="- Limite da Bidding Zone:").grid(row=19, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        opcoes_limite_bidding_zone = ["SIN", "Subsistema", "Distância (Informar valor)"]
        self.limite_bidding_zone = tk.StringVar(conteudo)
        self.limite_bidding_zone.set(opcoes_limite_bidding_zone[0])
        menu_limite_bidding_zone = ttk.Combobox(conteudo, textvariable=self.limite_bidding_zone, values=opcoes_limite_bidding_zone)
        menu_limite_bidding_zone.grid(row=19, column=3, padx=10, columnspan=3, sticky="w")
        self.limite_bidding_zone_distancia = ttk.Entry(conteudo)
        self.limite_bidding_zone_distancia.grid(row=19, column=4, columnspan=3, sticky="w")
        ttk.Label(conteudo, wraplength=390, text="- Limite para adicionalidade (em anos):").grid(row=20, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        self.limite_adicionalidade = ttk.Entry(conteudo)
        self.limite_adicionalidade.grid(row=20, column=3, padx=10, columnspan=3, sticky="w")
        self.limite_adicionalidade.bind("<KeyRelease>", self.mask)
        
        ttk.Label(conteudo, text="4. Especificações da contabilização das Emissões de CO2 do projeto:", font=self.fonteB).grid(row=21, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=21, column=3, pady=20)
        ttk.Label(conteudo, wraplength=360, text="- Limite de emissões da cadeia de produção (Em gCO2e/MJ de H2):").grid(row=22, column=0, columnspan=6, padx=20, sticky="w")
        self.limite_emissoes_cadeira_producao = ttk.Entry(conteudo)
        self.limite_emissoes_cadeira_producao.grid(row=22, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=390, text="- Fronteira de análise das emissões:").grid(row=23, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        opcoes_fronteira_analise = ["Até a produção", "Até a entrega"]
        self.fronteira_analise = tk.StringVar(conteudo)
        self.fronteira_analise.set(opcoes_fronteira_analise[0])
        menu_fronteira_analise = ttk.Combobox(conteudo, textvariable=self.fronteira_analise, values=opcoes_fronteira_analise)
        menu_fronteira_analise.grid(row=23, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=360, text="- Imaterialidade (Em gCO2e/MJ de H2):").grid(row=24, column=0, columnspan=6, padx=20, sticky="w")
        self.imaterialidade = ttk.Entry(conteudo)
        self.imaterialidade.grid(row=24, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=390, text="- Critério do fator de emissão do hidrogênio:").grid(row=25, column=0, columnspan=6, padx=20, pady=6, sticky="w")
        opcoes_criterio_fator_emissão_hidrogenio = ["Somente combustão", "Combustão + Upstream"]
        self.criterio_fator_emissão_hidrogenio = tk.StringVar(conteudo)
        self.criterio_fator_emissão_hidrogenio.set(opcoes_criterio_fator_emissão_hidrogenio[0])
        menu_criterio_fator_emissão_hidrogenio = ttk.Combobox(conteudo, textvariable=self.criterio_fator_emissão_hidrogenio, values=opcoes_criterio_fator_emissão_hidrogenio)
        menu_criterio_fator_emissão_hidrogenio.grid(row=25, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=390, text="- Período de validade da aprovação como grid fully renewable (Em anos):").grid(row=26, column=0, columnspan=6, padx=20, sticky="w")
        self.periodo_validade_aprovacao = ttk.Entry(conteudo)
        self.periodo_validade_aprovacao.grid(row=26, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, text="5. Especificações de padronização do H2:", font=self.fonteB).grid(row=27, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=27, column=3, pady=20)
        tk.Radiobutton(conteudo, wraplength=250, justify="left", text="Considerar padrão de pressão para H2. Informar valor ao lado (MPa): ", value="Opção 1").grid(row=28, column=0, columnspan=3, padx=10, sticky="w")
        self.padrao_pressao_hidrogenio = ttk.Entry(conteudo)
        self.padrao_pressao_hidrogenio.grid(row=28, column=2, padx=10, sticky="w")
        tk.Radiobutton(conteudo, justify="left", text="Considerar um padrão de 99,99% de pureza para o H2", value="Opção 2").grid(row=28, column=3, columnspan=3, sticky="w")
        
        ##VALORES DEFAULTS

        self.certif_var.set("hidrgenio_produzido")
        self.op_certfic_var.set("RED - Renewable Energy Directive")
        for widget in conteudo.winfo_children():
            if isinstance(widget, tk.Radiobutton) and widget.cget("text") == "24 7 CFE (Carbon Free Energy)":
                widget.config(state=tk.DISABLED)
        self.part_minima.config(state=tk.DISABLED)
        self.limite_intensidade.delete(0, tk.END)
        self.limite_intensidade.insert(0, "18")
        self.limite_particiapacao.delete(0, tk.END)
        self.limite_particiapacao.insert(0, "90")
        menu_balanco_energia.set("Horária")
        menu_limite_bidding_zone.set("SIN")
        self.limite_adicionalidade.delete(0, tk.END)
        self.limite_adicionalidade.insert(0, "3")
        self.limite_emissoes_cadeira_producao.delete(0, tk.END)
        self.limite_emissoes_cadeira_producao.insert(0, "28.2")
        menu_fronteira_analise.set("Até a entrega")
        self.imaterialidade.delete(0, tk.END)
        self.imaterialidade.insert(0, "N/A")
        menu_criterio_fator_emissão_hidrogenio.set("Combustão + Upstream")
          
        scrollbar_y.config(command=self.canvas.yview)
        
        # Configure o Canvas para rolar o conteúdo
        self.canvas.config(height=505, width=915)
        #conteudo.config(width=700)
        conteudo.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
       
        return etapa1
 

    ##
    ###
    # ETAPA 2
    ###
    ##
    def criar_etapa2(self):
        etapa2 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa2, text="Especificação da Produção de Hidrogênio",font=self.fonte).grid(row=0, column=0, columnspan=6, sticky="w")

        # Adicione uma barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(etapa2, orient="vertical")
        scrollbar_y.grid(row=1, column=1, sticky="ns")

        # Configure o widget Canvas para usar a barra de rolagem vertical
        self.canvas = tk.Canvas(etapa2, yscrollcommand=scrollbar_y.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        # Crie um quadro para conter o conteúdo real que será rolado
        conteudo = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=conteudo, anchor="nw")

        # Predefinições e interações entre menus e seleções
        tecnologia_var = tk.StringVar()
        def on_tecnologia_changed():
            selected_option = tecnologia_var.get()
            if selected_option == "pem":
                self.tamanho_eletrolisador.delete(0, tk.END)
                self.pressao_saida_eletrolisador.delete(0, tk.END)
                self.capex_eletrolisador.delete(0, tk.END)
                self.custos_om.delete(0, tk.END)
                self.vida_util_stack.delete(0, tk.END)
                self.custo_substituicao_stack.delete(0, tk.END)
                self.consumo_energetico_purificaco_h2.delete(0, tk.END)
                self.taxa_degradacao_eletrolisador.delete(0, tk.END)
                self.taxa_depreciacao_eletrolisador.delete(0, tk.END)
                self.tamanho_eletrolisador.insert(0, "1")
                self.pressao_saida_eletrolisador.insert(0, "3")
                self.capex_eletrolisador.insert(0, "1770")
                self.custos_om.insert(0, "3")
                self.vida_util_stack.insert(0, "7")
                self.custo_substituicao_stack.insert(0, "580")
                self.consumo_energetico_purificaco_h2.insert(0, "0.0013")
                self.taxa_degradacao_eletrolisador.insert(0, "0.9")
                self.taxa_depreciacao_eletrolisador.insert(0, "9")
            elif selected_option == "alk":
                self.tamanho_eletrolisador.delete(0, tk.END)
                self.pressao_saida_eletrolisador.delete(0, tk.END)
                self.capex_eletrolisador.delete(0, tk.END)
                self.custos_om.delete(0, tk.END)
                self.vida_util_stack.delete(0, tk.END)
                self.custo_substituicao_stack.delete(0, tk.END)
                self.consumo_energetico_purificaco_h2.delete(0, tk.END)
                self.taxa_degradacao_eletrolisador.delete(0, tk.END)
                self.taxa_depreciacao_eletrolisador.delete(0, tk.END)
                self.tamanho_eletrolisador.insert(0, "20")
                self.pressao_saida_eletrolisador.insert(0, "1.5")
                self.capex_eletrolisador.insert(0, "1400")
                self.custos_om.insert(0, "3")
                self.vida_util_stack.insert(0, "7")
                self.custo_substituicao_stack.insert(0, "345")
                self.consumo_energetico_purificaco_h2.insert(0, "0.0013")
                self.taxa_degradacao_eletrolisador.insert(0, "0.9")
                self.taxa_depreciacao_eletrolisador.insert(0, "9")

        ttk.Label(conteudo, text="1. Demanda:", font=self.fonteB).grid(row=1, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=1, column=3, pady=20)
        ttk.Label(conteudo, wraplength=320, text="Produção requerida de H2 (EM Kg):").grid(row=2, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.demandaH2 = ttk.Entry(conteudo)
        self.demandaH2.grid(row=2, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Periodicidade da demanda:").grid(row=3, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        opcoes_periodicidade_demanda = ["Diária", "Horária"]
        self.periodicidade_demanda = tk.StringVar(conteudo)
        self.periodicidade_demanda.set(opcoes_periodicidade_demanda[0])
        menu_periodicidade_demanda = ttk.Combobox(conteudo, textvariable=self.periodicidade_demanda, values=opcoes_periodicidade_demanda)
        menu_periodicidade_demanda.grid(row=3, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=240, text="Localizador do eletrolisador:").grid(row=4, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        ttk.Label(conteudo, text="- Latitude:").grid(row=5, column=1, sticky="w")
        ttk.Label(conteudo, text="- Longitude:").grid(row=6, column=1, sticky="w")

        self.latitude_entry = ttk.Entry(conteudo)
        self.latitude_entry.grid(row=5, column=3, padx=10, sticky="w")
        self.latitude_entry.bind("<KeyRelease>", self.mask)
        self.longitude_entry = ttk.Entry(conteudo)
        self.longitude_entry.grid(row=6, column=3, padx=10, sticky="w")
        atualizar_abrir_botao = ttk.Button(conteudo, text="Atualizar e Abrir Mapa", command=self.atualizar_e_abrir_mapa)
        atualizar_abrir_botao.grid(row=6, column=4, columnspan=2, pady=20)

        ttk.Label(conteudo, wraplength=320, text="Informar valor de Tust para consumo de energia da rede em horário de ponta ($/kW):").grid(row=7, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.valor_tust_ponta = ttk.Entry(conteudo)
        self.valor_tust_ponta.grid(row=7, column=3, padx=10, sticky="w")
        ttk.Label(conteudo, wraplength=320, text="Informar valor de Tust para consumo de energia da rede em horário fora da ponta ($/kW):").grid(row=8, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.valor_tust_fora_ponta = ttk.Entry(conteudo)
        self.valor_tust_fora_ponta.grid(row=8, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, text="2. Eletrolisador:", font=self.fonteB).grid(row=9, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=9, column=3, pady=20)
        
        ttk.Label(conteudo, wraplength=240, text="Tecnologia de eletrólise:").grid(row=10, column=0, pady=6, columnspan=2, padx=20, sticky="w")

        tk.Radiobutton(conteudo, text="PEM", variable=tecnologia_var, value="pem", command=on_tecnologia_changed).grid(row=10, column=3, columnspan=2, padx=10, sticky="w")
        tk.Radiobutton(conteudo, text="ALK", variable=tecnologia_var, value="alk", command=on_tecnologia_changed).grid(row=10, column=4, columnspan=2, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Tamanho comercial do eletrolisador (Em MW):").grid(row=11, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.tamanho_eletrolisador = ttk.Entry(conteudo)
        self.tamanho_eletrolisador.grid(row=11, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Informar pressão de saída do eletrolisador (Em MPa):").grid(row=12, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.pressao_saida_eletrolisador = ttk.Entry(conteudo)
        self.pressao_saida_eletrolisador.grid(row=12, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="CAPEX Eletrolisador (Em $/kW, CAPEX Total, incluindo equipamentos de purificação):").grid(row=13, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.capex_eletrolisador = ttk.Entry(conteudo)
        self.capex_eletrolisador.grid(row=13, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Custos de O&M do eletrolisador+purificador (% do CAPEX do eletrolisador/ano):").grid(row=14, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.custos_om = ttk.Entry(conteudo)
        self.custos_om.grid(row=14, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Vida útil do Stack (anos):").grid(row=15, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.vida_util_stack = ttk.Entry(conteudo)
        self.vida_util_stack.grid(row=15, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Custo de substituição do Stack ($/kW):").grid(row=16, column=0, columnspan=2, pady=6, padx=20, sticky="w")
        self.custo_substituicao_stack = ttk.Entry(conteudo)
        self.custo_substituicao_stack.grid(row=16, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Consumo energético para purificação do H2 (kWh/kgH2):").grid(row=17, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.consumo_energetico_purificaco_h2 = ttk.Entry(conteudo)
        self.consumo_energetico_purificaco_h2.grid(row=17, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Taxa de degradação do eletrolisador (% a.a):").grid(row=18, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.taxa_degradacao_eletrolisador = ttk.Entry(conteudo)
        self.taxa_degradacao_eletrolisador.grid(row=18, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Taxa de depreciação contábil do eletrolisador (% a.a):").grid(row=19, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.taxa_depreciacao_eletrolisador = ttk.Entry(conteudo)
        self.taxa_depreciacao_eletrolisador.grid(row=19, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, text="3. Compressor:", font=self.fonteB).grid(row=20, column=0, columnspan=5, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=20, column=3, pady=20)
        
        ttk.Label(conteudo, wraplength=320, text="CAPEX do compressor de referência ($):").grid(row=21, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.capex_compressor = ttk.Entry(conteudo)
        self.capex_compressor.grid(row=21, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Potência do compressor de referência (kW):").grid(row=22, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.potencia_compressor = ttk.Entry(conteudo)
        self.potencia_compressor.grid(row=22, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Fator de escala do compressor:").grid(row=23, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.fator_escala_compressor = ttk.Entry(conteudo)
        self.fator_escala_compressor.grid(row=23, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Custos deO&M do compressor (% do CAPEX do compressor/ano):").grid(row=24, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.custos_om_compressor = ttk.Entry(conteudo)
        self.custos_om_compressor.grid(row=24, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Vida útil do compressor (anos):").grid(row=25, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.vida_util_compressor = ttk.Entry(conteudo)
        self.vida_util_compressor.grid(row=25, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Custo de substituição do compressor (% do CAPEX do compressor):").grid(row=26, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.custo_substituicao_compressor = ttk.Entry(conteudo)
        self.custo_substituicao_compressor.grid(row=26, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Eficiência do compressor (%):").grid(row=27, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.eficiencia_compressor = ttk.Entry(conteudo)
        self.eficiencia_compressor.grid(row=27, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="Z - Fator de compressibilidade (admimensional):").grid(row=28, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.fator_compressibilidade = ttk.Entry(conteudo)
        self.fator_compressibilidade.grid(row=28, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="R - Constante de gases (kJ/(Kg*K):").grid(row=29, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.constante_gases = ttk.Entry(conteudo)
        self.constante_gases.grid(row=29, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="T - Temperatura de entrada (K):").grid(row=30, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.temperatura_entrada = ttk.Entry(conteudo)
        self.temperatura_entrada.grid(row=30, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="N - Número de estágios de compressão:").grid(row=31, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.numero_estagios_compressao = ttk.Entry(conteudo)
        self.numero_estagios_compressao.grid(row=31, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="ƞ - Eficiência isentrópica de compressão (%):").grid(row=32, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.eficiencia_compressao = ttk.Entry(conteudo)
        self.eficiencia_compressao.grid(row=32, column=3, padx=10, sticky="w")

        ttk.Label(conteudo, wraplength=320, text="ƙ - Razão entre os calores específicos (adimensional):").grid(row=33, column=0, columnspan=2, padx=20, pady=6, sticky="w")
        self.razao_calores = ttk.Entry(conteudo)
        self.razao_calores.grid(row=33, column=3, padx=10, sticky="w")

        #VALORES DEFAULS

        self.demandaH2.delete(0, tk.END)
        self.demandaH2.insert(0, "0")
        self.periodicidade_demanda.set("Diária")
        self.latitude_entry.delete(0, tk.END)
        self.latitude_entry.insert(0, "-22.890451")
        self.longitude_entry.delete(0, tk.END)
        self.longitude_entry.insert(0, "-43.188052")
        self.valor_tust_ponta.delete(0, tk.END)
        self.valor_tust_ponta.insert(0, "0")
        self.valor_tust_fora_ponta.delete(0, tk.END)
        self.valor_tust_fora_ponta.insert(0, "0")

        tecnologia_var.set("pem")
        self.tamanho_eletrolisador.delete(0, tk.END)
        self.pressao_saida_eletrolisador.delete(0, tk.END)
        self.capex_eletrolisador.delete(0, tk.END)
        self.custos_om.delete(0, tk.END)
        self.vida_util_stack.delete(0, tk.END)
        self.custo_substituicao_stack.delete(0, tk.END)
        self.consumo_energetico_purificaco_h2.delete(0, tk.END)
        self.taxa_degradacao_eletrolisador.delete(0, tk.END)
        self.taxa_depreciacao_eletrolisador.delete(0, tk.END)
        self.tamanho_eletrolisador.insert(0, "1")
        self.pressao_saida_eletrolisador.insert(0, "3")
        self.capex_eletrolisador.insert(0, "1770")
        self.custos_om.insert(0, "3")
        self.vida_util_stack.insert(0, "7")
        self.custo_substituicao_stack.insert(0, "580")
        self.consumo_energetico_purificaco_h2.insert(0, "0.0013")
        self.taxa_degradacao_eletrolisador.insert(0, "0.9")
        self.taxa_depreciacao_eletrolisador.insert(0, "9")

        self.capex_compressor.delete(0, tk.END)
        self.capex_compressor.insert(0, "4656000")
        self.potencia_compressor.delete(0, tk.END)
        self.potencia_compressor.insert(0, "4000")
        self.fator_escala_compressor.delete(0, tk.END)
        self.fator_escala_compressor.insert(0, "80%")
        self.custos_om_compressor.delete(0, tk.END)
        self.custos_om_compressor.insert(0, "3%")
        self.vida_util_compressor.delete(0, tk.END)
        self.vida_util_compressor.insert(0, "20")
        self.custo_substituicao_compressor.delete(0, tk.END)
        self.custo_substituicao_compressor.insert(0, "100%")
        self.eficiencia_compressor.delete(0, tk.END)
        self.eficiencia_compressor.insert(0, "95%")
        self.fator_compressibilidade.delete(0, tk.END)
        self.fator_compressibilidade.insert(0, "1.027")
        self.constante_gases.delete(0, tk.END)
        self.constante_gases.insert(0, "4.12")
        self.temperatura_entrada.delete(0, tk.END)
        self.temperatura_entrada.insert(0, "293")
        self.numero_estagios_compressao.delete(0, tk.END)
        self.numero_estagios_compressao.insert(0, "3")
        self.eficiencia_compressao.delete(0, tk.END)
        self.eficiencia_compressao.insert(0, "0.8")
        self.razao_calores.delete(0, tk.END)
        self.razao_calores.insert(0, "1.41")
        
        scrollbar_y.config(command=self.canvas.yview)
        
        # Configure o Canvas para rolar o conteúdo
        self.canvas.config(height=505, width=915)
        #conteudo.config(width=700)
        conteudo.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
       
        return etapa2



    ##
    ###
    # ETAPA 3
    ###
    ##
    def criar_etapa3(self):
        etapa3 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa3, text="Especificação das fontes de geração de energia",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")
        botao_restaurar = ttk.Button(etapa3, text="Restaurar")
        botao_restaurar.grid(row=0, column=1, pady=20)

        # Adicione uma barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(etapa3, orient="vertical")
        scrollbar_y.grid(row=0, rowspan=2, column=3, sticky="ns")

        # Adicione uma barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(etapa3, orient="horizontal")
        scrollbar_x.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Configure o widget Canvas para usar a barra de rolagem horizontal
        self.canvas = tk.Canvas(etapa3, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Crie um quadro para conter o conteúdo real que será rolado
        conteudo = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=conteudo, anchor="nw")

        
        # # Adicione uma barra de rolagem vertical
        # scrollbar_x = ttk.Scrollbar(etapa3, orient="horizontal", command=self.canvas.xview)
        # scrollbar_x.grid(row=2, column=0, columnspan=2, sticky="ew")

        # # Configure o widget Canvas para usar a barra de rolagem vertical
        # self.canvas = tk.Canvas(etapa3, xscrollcommand=scrollbar_x.set)
        # self.canvas.grid(row=1, column=0, sticky="nsew")

        # # Crie um quadro para conter o conteúdo real que será rolado
        # conteudo = ttk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=conteudo, anchor="nw")
                
        
        
        # # Crie um quadro para conter o conteúdo rolável
        # conteudo_frame = ttk.Frame(etapa3)
        # conteudo_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # # Adicione uma barra de rolagem horizontal
        # scrollbar_x = ttk.Scrollbar(etapa3, orient="horizontal", command=self.on_horizontal_scroll)
        # scrollbar_x.grid(row=2, column=0, columnspan=2, sticky="ew")

        # # Configure a tela de lona para usar a barra de rolagem horizontal
        # self.canvas = tk.Canvas(conteudo_frame, xscrollcommand=scrollbar_x.set)
        # self.canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # # Crie um quadro para conter o conteúdo real que será rolado
        # conteudo = ttk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=conteudo, anchor="nw")

        def abrir_janela_edicao(linha):
            def salvar_edicao():
                for col in range(21):
                    novo_valor = entry_vars[col].get()
                    tabela[linha][col] = novo_valor
                janela_edicao.destroy()
                atualizar_tabela()

            def atualizar_e_abrir_mapa():
                try:
                    latitude = float(entry_vars[3].get())
                    longitude = float(entry_vars[4].get())
                    mapa = folium.Map(location=[latitude, longitude], zoom_start=6)
                    folium.Marker([latitude, longitude], tooltip="Localização").add_to(mapa)
                    mapa.save('mapa.html')
                    webbrowser.open('mapa.html')
                except ValueError:
                    # Lidar com erros de entrada inválida (por exemplo, se as coordenadas não forem números)
                    pass

            def fazer_upload():
                arquivo_path = filedialog.askopenfilename()
                entry_vars[18].set(arquivo_path)

            def fazer_uploadB():
                arquivo_path = filedialog.askopenfilename()
                entry_vars[20].set(arquivo_path)

            janela_edicao = tk.Toplevel(conteudo)
            janela_edicao.title("Editar Linha {}".format(linha + 1))

            entry_vars = []
            titulos = ["Seleção de usinas para a simulação", "Nome da usina", "Fonte de energia", "Latitude", "Longitude", "Potência [MW]", "Capacidade do reservatório em caso de PCH [h]", "Aumentar fator de capacidade da geração eólica [sim/não]", "IP: Taxa de paradas programadas [%]", "IP: Taxa de paradas não programadas [%]", "Taxa de risco de curtailment [%]", "Taxa de degradação [%/ano]", "Taxa de depreciação contábil", "CAPEX [$]", "OPEX [$/Ano]", "Pagamento de TUSTg [$/kWh]", "Geração no mesmo local do consumo [sim/não]", "Idade da usina [anos]", "Previsão da geração [kWh/h]", "Estimar LCOE da usina ou deseja inserir projeção de preço/custo da usina?", "Custo/Preço de Energia [$/kWh]"]
            for col in range(21):
                ttk.Label(janela_edicao, text=titulos[col]).grid(row=col, column=0, padx=10, pady=5)
                entry_var = tk.StringVar()
                entry_var.set(tabela[linha][col])
                entry_vars.append(entry_var)
                if titulos[col]=="Seleção de usinas para a simulação":
                    ttk.Checkbutton(janela_edicao, variable=entry_var).grid(row=col, column=1, padx=10, pady=5)
                elif titulos[col]=="Fonte de energia":
                    opcoes_fronteira_analise = ["Eólica", "FV", "PCH"]
                    ttk.Combobox(janela_edicao, textvariable=entry_var, values=opcoes_fronteira_analise).grid(row=col, column=1, padx=10, pady=5)
                elif titulos[col]=="Latitude":
                    ttk.Entry(janela_edicao, textvariable=entry_var).grid(row=col, column=1, padx=10, pady=5)
                    #self.latitude_entry.bind("<KeyRelease>", self.formatar_coordenadas)
                elif titulos[col]=="Longitude":
                    ttk.Entry(janela_edicao, textvariable=entry_var).grid(row=col, column=1, padx=10, pady=5)
                elif titulos[col]=="Previsão da geração [kWh/h]":
                    tk.Button(janela_edicao, text="Upload", command=fazer_upload).grid(row=col, column=2, padx=10, pady=5)
                    tk.Label(janela_edicao, textvariable=entry_vars[18], text="").grid(row=col, column=1, padx=10, pady=5)
                elif titulos[col]=="Custo/Preço de Energia [$/kWh]":
                    tk.Button(janela_edicao, text="Upload", command=fazer_uploadB).grid(row=col, column=2, padx=10, pady=5)
                    tk.Label(janela_edicao, textvariable=entry_vars[20], text="").grid(row=col, column=1, padx=10, pady=5)
                else:
                    ttk.Entry(janela_edicao, textvariable=entry_var).grid(row=col, column=1, padx=10, pady=5)

            atualizar_abrir_botao = ttk.Button(janela_edicao, text="Atualizar e Abrir Mapa", command=atualizar_e_abrir_mapa)
            atualizar_abrir_botao.grid(row=4, column=2, columnspan=2)
            salvar_button = ttk.Button(janela_edicao, text="Salvar", command=salvar_edicao)
            salvar_button.grid(row=22, column=0, columnspan=2, pady=10)
        
        def atualizar_tabela():
            for linha in range(1,20):
                for coluna in range(21):
                    label_var[linha][coluna].set(tabela[linha][coluna])
            conteudo.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Crie uma tabela com 5 linhas e 6 colunas (5x6)
        tabela = [["" for _ in range(21)] for _ in range(21)]

        label_var = []

        # Adicione a primeira linha com títulos
        titulos = ["Seleção de usinas para a simulação", "Nome da usina", "Fonte de energia", "Latitude", "Longitude", "Potência [MW]", "Capacidade do reservatório em caso de PCH [h]", "Aumentar fator de capacidade da geração eólica [sim/não]", "IP: Taxa de paradas programadas [%]", "IP: Taxa de paradas não programadas [%]", "Taxa de risco de curtailment [%]", "Taxa de degradação [%/ano]", "Taxa de depreciação contábil", "CAPEX [$]", "OPEX [$/Ano]", "Pagamento de TUSTg [$/kWh]", "Geração no mesmo local do consumo [sim/não]", "Idade da usina [anos]", "Previsão da geração [kWh/h]", "Estimar LCOE da usina ou deseja inserir projeção de preço/custo da usina?", "Custo/Preço de Energia [$/kWh]"]
        label_var.append([tk.StringVar() for _ in range(21)])

        for coluna in range(21):
            label_var[0][coluna].set(titulos[coluna])
            tk.Label(conteudo, justify="left",wraplength=120,textvariable=label_var[0][coluna]).grid(row=0, column=coluna, padx=10, pady=5)
            
        for linha in range(1, 20):
            label_var.append([])
            for coluna in range(21):
                var = tk.StringVar()
                var.set(tabela[linha - 1][coluna])
                label_var[linha].append(var)
                tk.Label(conteudo, wraplength=120, textvariable=label_var[linha][coluna]).grid(row=linha, column=coluna, padx=10, pady=5)

            botao_editar = ttk.Button(conteudo, text="Editar", command=lambda linha=linha: abrir_janela_edicao(linha))
            botao_editar.grid(row=linha, column=22, padx=10, pady=5)

        # # Configure o Canvas para rolar o conteúdo
        # self.canvas.config(width=800)
        # #conteudo.config(width=700)
        # conteudo.update_idletasks()
        # self.canvas.config(scrollregion=self.canvas.bbox("all"))

        scrollbar_x.config(command=self.canvas.xview)
        scrollbar_y.config(command=self.canvas.yview)
        
        # Configure o Canvas para rolar o conteúdo
        self.canvas.config(height=450, width=920)
        #conteudo.config(width=700)
        conteudo.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
       
        return etapa3

    def on_horizontal_scroll(self, *args):
        self.canvas.xview(*args)

    
    def criar_etapa4(self):
        etapa4 = ttk.Frame(self.conteudo_etapa)

        # Predefinições e interações entre menus e seleções
        baterias_var = tk.StringVar()
        def on_op_baterias_changed():
            selected_option = baterias_var.get()
            if selected_option == "sim":
                print(selected_option)
            elif selected_option == "sim":
                print(selected_option)
        
        self.tecbaterias_var = tk.StringVar()
        def on_op_tec_baterias_changed():
            selected_option = self.tecbaterias_var.get()
            if selected_option == "litio":
                self.capex_bateria.delete(0, tk.END)
                self.capex_bateria.insert(0, "150")
                self.custos_om_bateria.delete(0, tk.END)
                self.custos_om_bateria.insert(0, "30")
                self.custos_substituicao_baterias.delete(0, tk.END)
                self.custos_substituicao_baterias.insert(0, "90%")
                self.capacidade_baterias.delete(0, tk.END)
                self.capacidade_baterias.insert(0, "1")
                self.capacidade_descarregamento.delete(0, tk.END)
                self.capacidade_descarregamento.insert(0, "1")
                self.capacidade_carregamento.delete(0, tk.END)
                self.capacidade_carregamento.insert(0, "1")
                self.eficiencia_carga_bateria.delete(0, tk.END)
                self.eficiencia_carga_bateria.insert(0, "90%")
                self.eficiencia_descarga_bateria.delete(0, tk.END)
                self.eficiencia_descarga_bateria.insert(0, "90%")
                self.ciclos.delete(0, tk.END)
                self.ciclos.insert(0, "2000")
                self.taxa_depreciacao_contabil_bateria.delete(0, tk.END)
                self.taxa_depreciacao_contabil_bateria.insert(0, "10%")
            elif selected_option == "chumbo_acido":
                print (selected_option)
            elif selected_option == "sodio":
                print (selected_option)
            elif selected_option == "outra":
                print (selected_option)

        ttk.Label(etapa4, text="Especificação da Tecnologia de armazenamento",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(etapa4, text="O projeto utiliza baterias?").grid(row=1, column=0, padx=20, pady=6, sticky="w")
        tk.Radiobutton(etapa4, text="Sim", variable=baterias_var, value="sim", command=on_op_baterias_changed).grid(row=1, column=1, columnspan=2, padx=10, sticky="w")
        tk.Radiobutton(etapa4, text="Não", variable=baterias_var, value="nao", command=on_op_baterias_changed).grid(row=1, column=2, columnspan=2, sticky="w")
        
        ttk.Label(etapa4, text="Selecionar tipo de tecnologia de baterias:").grid(row=3, column=0, padx=20, pady=6, sticky="w")
        tk.Radiobutton(etapa4, text="Lítio", variable=self.tecbaterias_var, value="litio", command=on_op_tec_baterias_changed).grid(row=3, column=1, padx=10, sticky="w")
        tk.Radiobutton(etapa4, text="Chumbo-Ácido", variable=self.tecbaterias_var, value="chumbo_acido", command=on_op_tec_baterias_changed).grid(row=3, column=2, sticky="w")
        tk.Radiobutton(etapa4, text="Sódio", variable=self.tecbaterias_var, value="sodio", command=on_op_tec_baterias_changed).grid(row=3, column=3, padx=10, sticky="w")
        tk.Radiobutton(etapa4, text="Outra", variable=self.tecbaterias_var, value="outra", command=on_op_tec_baterias_changed).grid(row=3, column=4, sticky="w")

        ttk.Label(etapa4, text="CAPEX bateria: ($/kW*ano)").grid(row=4, column=0, padx=20, pady=6, sticky="w")
        self.capex_bateria = ttk.Entry(etapa4)
        self.capex_bateria.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Custos de O&M bateria ($/(kW*ano)):").grid(row=5, column=0, padx=20, pady=6, sticky="w")
        self.custos_om_bateria = ttk.Entry(etapa4)
        self.custos_om_bateria.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Custos de substituição das baterias (% CAPEX bateria):").grid(row=6, column=0, padx=20, pady=6, sticky="w")
        self.custos_substituicao_baterias = ttk.Entry(etapa4)
        self.custos_substituicao_baterias.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Capacidade de referência das baterias (MWh):").grid(row=7, column=0, padx=20, pady=6, sticky="w")
        self.capacidade_baterias = ttk.Entry(etapa4)
        self.capacidade_baterias.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Capacidade de descarregamento (horas):").grid(row=8, column=0, padx=20, pady=6, sticky="w")
        self.capacidade_descarregamento = ttk.Entry(etapa4)
        self.capacidade_descarregamento.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Capacidade de carregamento (horas):").grid(row=9, column=0, padx=20, pady=6, sticky="w")
        self.capacidade_carregamento = ttk.Entry(etapa4)
        self.capacidade_carregamento.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Eficiência de carga da bateria (%):").grid(row=10, column=0, padx=20, pady=6, sticky="w")
        self.eficiencia_carga_bateria = ttk.Entry(etapa4)
        self.eficiencia_carga_bateria.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Eficiência de descarga da bateria (%):").grid(row=11, column=0, padx=20, pady=6, sticky="w")
        self.eficiencia_descarga_bateria = ttk.Entry(etapa4)
        self.eficiencia_descarga_bateria.grid(row=11, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Ciclos (ciclos):").grid(row=12, column=0, padx=20, pady=6, sticky="w")
        self.ciclos = ttk.Entry(etapa4)
        self.ciclos.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Taxa de depreciação contábil da bateria (%):").grid(row=13, column=0, padx=20, pady=6, sticky="w")
        self.taxa_depreciacao_contabil_bateria = ttk.Entry(etapa4)
        self.taxa_depreciacao_contabil_bateria.grid(row=13, column=1, padx=10, pady=5, sticky="w")

        baterias_var.set("nao")
        self.tecbaterias_var.set("litio")
        self.capex_bateria.delete(0, tk.END)
        self.capex_bateria.insert(0, "150")
        self.custos_om_bateria.delete(0, tk.END)
        self.custos_om_bateria.insert(0, "30")
        self.custos_substituicao_baterias.delete(0, tk.END)
        self.custos_substituicao_baterias.insert(0, "90%")
        self.capacidade_baterias.delete(0, tk.END)
        self.capacidade_baterias.insert(0, "1")
        self.capacidade_descarregamento.delete(0, tk.END)
        self.capacidade_descarregamento.insert(0, "1")
        self.capacidade_carregamento.delete(0, tk.END)
        self.capacidade_carregamento.insert(0, "1")
        self.eficiencia_carga_bateria.delete(0, tk.END)
        self.eficiencia_carga_bateria.insert(0, "90%")
        self.eficiencia_descarga_bateria.delete(0, tk.END)
        self.eficiencia_descarga_bateria.insert(0, "90%")
        self.ciclos.delete(0, tk.END)
        self.ciclos.insert(0, "2000")
        self.taxa_depreciacao_contabil_bateria.delete(0, tk.END)
        self.taxa_depreciacao_contabil_bateria.insert(0, "10%")

        return etapa4

    def criar_etapa5(self):
        
        etapa5 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa5, text="Especificação do esquema de certificação",font=self.fonte).grid(row=0, column=0, columnspan=6, sticky="w")

        # Adicione uma barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(etapa5, orient="vertical")
        scrollbar_y.grid(row=1, column=1, sticky="ns")

        # Configure o widget Canvas para usar a barra de rolagem vertical
        self.canvas = tk.Canvas(etapa5, yscrollcommand=scrollbar_y.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        # Crie um quadro para conter o conteúdo real que será rolado
        conteudo = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=conteudo, anchor="nw")

        ttk.Label(conteudo, text="1. Dados econômicos:", font=self.fonteB).grid(row=1, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=1, column=3, pady=20)
        ttk.Label(conteudo, text="     Horizonte de projeto (anos):").grid(row=2, column=0, sticky="w")
        self.horizonteprojeto = ttk.Entry(conteudo)
        self.horizonteprojeto.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Participação do capital próprio (%):").grid(row=3, column=0, sticky="w")
        self.partcaptaproprio = ttk.Entry(conteudo)
        self.partcaptaproprio.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Custo do capital próprio:").grid(row=4, column=0, sticky="w")
        self.custocapitalproprio = ttk.Entry(conteudo)
        self.custocapitalproprio.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Tipo de amortização:").grid(row=5, column=0, sticky="w")
        opcoes_tipoamortizacao = ["SAC", "Price", "Não Reembolsável"]
        self.tipoamortizacao_var = tk.StringVar(conteudo)
        self.tipoamortizacao_var.set(opcoes_tipoamortizacao[0])  # Define a opção padrão
        tipoamortizacao_menu = ttk.Combobox(conteudo, textvariable=self.tipoamortizacao_var, values=opcoes_tipoamortizacao)
        tipoamortizacao_menu.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Período de financiamento (anos):").grid(row=6, column=0, sticky="w")
        self.periodofuncionamento = ttk.Entry(conteudo)
        self.periodofuncionamento.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Taxa de juros real do financiamento (%):").grid(row=7, column=0, sticky="w")
        self.txjurosreal = ttk.Entry(conteudo)
        self.txjurosreal.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Período de carência (anos):").grid(row=8, column=0, sticky="w")
        self.periodocarencia = ttk.Entry(conteudo)
        self.periodocarencia.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Custos administrativos do projeto ($/ano):").grid(row=9, column=0, sticky="w")
        self.custosprojeto = ttk.Entry(conteudo)
        self.custosprojeto.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     PIS/Confins (%):").grid(row=10, column=0, sticky="w")
        self.pisconfins = ttk.Entry(conteudo)
        self.pisconfins.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     ICMS (%):").grid(row=11, column=0, sticky="w")
        self.icms = ttk.Entry(conteudo)
        self.icms.grid(row=11, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Imposto de Renda e Contribuição Social (%):").grid(row=12, column=0, sticky="w")
        self.impostorenda = ttk.Entry(conteudo)
        self.impostorenda.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="2. Oxigênio:", font=self.fonteB).grid(row=13, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=13, column=3, pady=20)

        ttk.Label(conteudo, text="     Considerar venda de oxigênio:").grid(row=14, column=0, sticky="w")
        opcoes_vendaoxigenio = ["Sim", "Não"]
        self.vendaoxigenio_var = tk.StringVar(conteudo)
        self.vendaoxigenio_var.set(opcoes_vendaoxigenio[0])  # Define a opção padrão
        vendaoxigenio_menu = ttk.Combobox(conteudo, textvariable=self.vendaoxigenio_var, values=opcoes_vendaoxigenio)
        vendaoxigenio_menu.grid(row=14, column=1, padx=10, pady=5, sticky="w") 

        ttk.Label(conteudo, text="     Taxa de produção de oxigênio (kg de O2 /kg de H2):").grid(row=15, column=0, sticky="w")
        self.taxaprodoxigenio = ttk.Entry(conteudo)
        self.taxaprodoxigenio.grid(row=15, column=1, padx=10, pady=5, sticky="w") 

        ttk.Label(conteudo, text="     Preço de venda de oxigênio ($/kg de O2):").grid(row=16, column=0, sticky="w")
        self.precovendaoxigenio = ttk.Entry(conteudo)
        self.precovendaoxigenio.grid(row=16, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Taxa de aumento anual do preço de venda do oxigênio (%):").grid(row=17, column=0, sticky="w")
        self.taxaaumentooxigenio = ttk.Entry(conteudo)
        self.taxaaumentooxigenio.grid(row=17, column=1, padx=10, pady=5, sticky="w") 

        ttk.Label(conteudo, text="3. Uso da Água:", font=self.fonteB).grid(row=18, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=18, column=3, pady=20)

        ttk.Label(conteudo, text="     Demanda de água para o eletrolisador (ultrapura) (kg/kgH2):").grid(row=19, column=0, sticky="w")
        self.demandaagua = ttk.Entry(conteudo)
        self.demandaagua.grid(row=19, column=1, padx=10, pady=5, sticky="w") 

        ttk.Label(conteudo, text="     Demanda de água de processo para o eletrolisador (kg/kgH2):").grid(row=20, column=0, sticky="w")
        self.demandaaguaeletro = ttk.Entry(conteudo)
        self.demandaaguaeletro.grid(row=20, column=1, padx=10, pady=5, sticky="w")      

        ttk.Label(conteudo, text="     Preço da água pura ($/kg de água):").grid(row=21, column=0, sticky="w")
        self.precoaguapura = ttk.Entry(conteudo)
        self.precoaguapura.grid(row=21, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Preço da água de processo ($/kg de água):").grid(row=22, column=0, sticky="w")
        self.precoaguaproc = ttk.Entry(conteudo)
        self.precoaguaproc.grid(row=22, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Preço de transporte da água, para levar água dessalinizada até a usina ($/(kgH2*100 km)):").grid(row=23, column=0, sticky="w")
        self.precotranspagua = ttk.Entry(conteudo)
        self.precotranspagua.grid(row=23, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Taxa de aumento anual dos custos relativos ao consumo de água (%):").grid(row=24, column=0, sticky="w")
        self.taxaaumentoanual = ttk.Entry(conteudo)
        self.taxaaumentoanual.grid(row=24, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="4. Mercado de carbono:", font=self.fonteB).grid(row=25, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=25, column=3, pady=20)

        ttk.Label(conteudo, text="     Precificação do carbono ($/gCO2 eq):").grid(row=26, column=0, sticky="w")
        self.precificacaocarbono = ttk.Entry(conteudo)
        self.precificacaocarbono.grid(row=26, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Aumento anual do preço do carbono (%):").grid(row=27, column=0, sticky="w")
        self.aumentoprecocarbono = ttk.Entry(conteudo)
        self.aumentoprecocarbono.grid(row=27, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Valor de referência para emissões da produção por reforma a vapor (gCO2e/MJ.de H2):").grid(row=28, column=0, sticky="w")
        self.valoremissoesprod = ttk.Entry(conteudo)
        self.valoremissoesprod.grid(row=28, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="5. Sistema de transmissão:", font=self.fonteB).grid(row=29, column=0, pady=20, sticky="w")
        botao_restaurar = ttk.Button(conteudo, text="Restaurar")
        botao_restaurar.grid(row=29, column=3, pady=20)

        ttk.Label(conteudo, text="     Preço de aquisição da energia da rede ($/kWh):").grid(row=30, column=0, sticky="w")
        self.precoaquisicaoenergia = ttk.Entry(conteudo)
        self.precoaquisicaoenergia.grid(row=30, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Informar se há possibilidade venda de excedente de energia para rede:").grid(row=31, column=0, sticky="w")
        opcoes_possibilidadevendaexcedente = ["Sim", "Não"]
        self.possibilidadevendaexcedente_var = tk.StringVar(conteudo)
        self.possibilidadevendaexcedente_var.set(opcoes_possibilidadevendaexcedente[1])  # Define a opção padrão
        possibilidadevendaexcedente_menu = ttk.Combobox(conteudo, textvariable=self.possibilidadevendaexcedente_var, values=opcoes_possibilidadevendaexcedente)
        possibilidadevendaexcedente_menu.grid(row=31, column=1, padx=10, pady=5, sticky="w") 

        ttk.Label(conteudo, text="     Informar preço de venda de excedente de energia para rede ($/kWh):").grid(row=32, column=0, sticky="w")
        self.precovendaenergia = ttk.Entry(conteudo)
        self.precovendaenergia.grid(row=32, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Informar custo relativo à construção de novas linhas de transmissão exclusivas para o projeto ($):").grid(row=33, column=0, sticky="w")
        self.custorelativonovaslinhas = ttk.Entry(conteudo)
        self.custorelativonovaslinhas.grid(row=33, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(conteudo, text="     Informar fator de emissão da rede (gCO2 eq/MJ):").grid(row=34, column=0, sticky="w")
        self.fatoremissaorede = ttk.Entry(conteudo)
        self.fatoremissaorede.grid(row=34, column=1, padx=10, pady=5, sticky="w")


        # self.telefone_entry = ttk.Entry(conteudo)
        # self.telefone_entry.grid(row=10, column=4, padx=10, pady=5, sticky="w")
        # self.telefone_entry.bind("<KeyRelease>", self.formatar_telefone)
        self.capex_bateria.delete(0, tk.END)
        self.capex_bateria.insert(0, "150")

        self.horizonteprojeto.delete(0, tk.END)
        self.horizonteprojeto.insert(0, "20")
        self.partcaptaproprio.delete(0, tk.END)
        self.partcaptaproprio.insert(0, "0")
        self.custocapitalproprio.delete(0, tk.END)
        self.custocapitalproprio.insert(0, "0")
        self.periodofuncionamento.delete(0, tk.END)
        self.periodofuncionamento.insert(0, "0")
        self.txjurosreal.delete(0, tk.END)
        self.txjurosreal.insert(0, "0")
        self.periodocarencia.delete(0, tk.END)
        self.periodocarencia.insert(0, "0")
        self.custosprojeto.delete(0, tk.END)
        self.custosprojeto.insert(0, "1000000")
        self.pisconfins.delete(0, tk.END)
        self.pisconfins.insert(0, "2.90%")
        self.icms.delete(0, tk.END)
        self.icms.insert(0, "18.00%")
        self.impostorenda.delete(0, tk.END)
        self.impostorenda.insert(0, "3.08%")
        self.taxaprodoxigenio.delete(0, tk.END)
        self.taxaprodoxigenio.insert(0, "8")
        self.precovendaoxigenio.delete(0, tk.END)
        self.precovendaoxigenio.insert(0, "3")
        self.taxaaumentooxigenio.delete(0, tk.END)
        self.taxaaumentooxigenio.insert(0, "0")
        self.demandaagua.delete(0, tk.END)
        self.demandaagua.insert(0, "9")
        self.demandaaguaeletro.delete(0, tk.END)
        self.demandaaguaeletro.insert(0, "18")
        self.precoaguapura.delete(0, tk.END)
        self.precoaguapura.insert(0, "0.00121")
        self.precoaguaproc.delete(0, tk.END)
        self.precoaguaproc.insert(0, "0.00116")
        self.precotranspagua.delete(0, tk.END)
        self.precotranspagua.insert(0, "0.06")
        self.taxaaumentoanual.delete(0, tk.END)
        self.taxaaumentoanual.insert(0, "0")
        self.precificacaocarbono.delete(0, tk.END)
        self.precificacaocarbono.insert(0, "0")
        self.aumentoprecocarbono.delete(0, tk.END)
        self.aumentoprecocarbono.insert(0, "0")
        self.valoremissoesprod.delete(0, tk.END)
        self.valoremissoesprod.insert(0, "94")
        self.precoaquisicaoenergia.delete(0, tk.END)
        self.precoaquisicaoenergia.insert(0, "0")
        self.precovendaenergia.delete(0, tk.END)
        self.precovendaenergia.insert(0, "0")
        self.custorelativonovaslinhas.delete(0, tk.END)
        self.custorelativonovaslinhas.insert(0, "0")
        self.fatoremissaorede.delete(0, tk.END)
        self.fatoremissaorede.insert(0, "1000")

        scrollbar_y.config(command=self.canvas.yview)
        
        # Configure o Canvas para rolar o conteúdo
        self.canvas.config(height=505, width=915)
        #conteudo.config(width=700)
        conteudo.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
       
        return etapa5

    # def criar_etapa5(self):
    #     etapa5 = ttk.Frame(self.conteudo_etapa)
    #     ttk.Label(etapa5, text="Especificar parâmetros de projeto",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

    #     ttk.Label(etapa5, text="Dados econômicos:").grid(row=1, column=0, sticky="w")
    #     ttk.Label(etapa5, text="     Horizonte de projeto:").grid(row=2, column=0, sticky="w")
    #     self.horizonteprojeto = ttk.Entry(etapa5)
    #     self.horizonteprojeto.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Percentual de valor de revenda do projeto:").grid(row=3, column=0, sticky="w")
    #     self.percentualrevenda = ttk.Entry(etapa5)
    #     self.percentualrevenda.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     CAPEX eletrolisador:").grid(row=4, column=0, sticky="w")
    #     self.capexeletrolisador = ttk.Entry(etapa5)
    #     self.capexeletrolisador.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Custos de O&M do eletrolisador:").grid(row=5, column=0, sticky="w")
    #     self.custoseletrolisador = ttk.Entry(etapa5)
    #     self.custoseletrolisador.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Vida útil do Stack:").grid(row=6, column=0, sticky="w")
    #     self.vidautilstack = ttk.Entry(etapa5)
    #     self.vidautilstack.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Custo de substituição do Stack:").grid(row=7, column=0, sticky="w")
    #     self.custosubstituicao = ttk.Entry(etapa5)
    #     self.custosubstituicao.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     CAPEX do compressor:").grid(row=8, column=0, sticky="w")
    #     self.capexcompressor = ttk.Entry(etapa5)
    #     self.capexcompressor.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Custo de O&M do compressor:").grid(row=9, column=0, sticky="w")
    #     self.custocompressor = ttk.Entry(etapa5)
    #     self.custocompressor.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="OXIGÊNIO:").grid(row=1, column=3, sticky="w")
    #     ttk.Label(etapa5, text="     Considerar venda de oxigênio:").grid(row=2, column=3, sticky="w")
    #     opcoes_vendaoxigenio = ["Sim", "Não"]
    #     self.vendaoxigenio_var = tk.StringVar(etapa5)
    #     self.vendaoxigenio_var.set(opcoes_vendaoxigenio[0])  # Define a opção padrão
    #     vendaoxigenio_menu = ttk.Combobox(etapa5, textvariable=self.vendaoxigenio_var, values=opcoes_vendaoxigenio)
    #     vendaoxigenio_menu.grid(row=2, column=4, padx=10, pady=5, sticky="w") 

    #     ttk.Label(etapa5, text="     Taxa de produção de oxigênio:").grid(row=3, column=3, sticky="w")
    #     self.taxaprodoxigenio = ttk.Entry(etapa5)
    #     self.taxaprodoxigenio.grid(row=3, column=4, padx=10, pady=5, sticky="w") 

    #     ttk.Label(etapa5, text="     Preço de venda de oxigênio:").grid(row=4, column=3, sticky="w")
    #     self.precovendaoxigenio = ttk.Entry(etapa5)
    #     self.precovendaoxigenio.grid(row=4, column=4, padx=10, pady=5, sticky="w")  

    #     ttk.Label(etapa5, text="USO DE AGUA:").grid(row=5, column=3, sticky="w")
    #     ttk.Label(etapa5, text="     Demanda de água para o eletrolisador (ultrapura):").grid(row=6, column=3, sticky="w")
    #     self.demandaagua = ttk.Entry(etapa5)
    #     self.demandaagua.grid(row=6, column=4, padx=10, pady=5, sticky="w") 

    #     ttk.Label(etapa5, text="     Demanda de água de processo para o eletrolisador:").grid(row=7, column=3, sticky="w")
    #     self.demandaaguaeletro = ttk.Entry(etapa5)
    #     self.demandaaguaeletro.grid(row=7, column=4, padx=10, pady=5, sticky="w")      

    #     ttk.Label(etapa5, text="     Preço da água pura:").grid(row=8, column=3, sticky="w")
    #     self.precoaguapura = ttk.Entry(etapa5)
    #     self.precoaguapura.grid(row=8, column=4, padx=10, pady=5, sticky="w")

    #     ttk.Label(etapa5, text="     Preço da água de processo:").grid(row=9, column=3, sticky="w")
    #     self.precoaguaproc = ttk.Entry(etapa5)
    #     self.precoaguaproc.grid(row=9, column=4, padx=10, pady=5, sticky="w")

    #     self.telefone_entry = ttk.Entry(etapa5)
    #     self.telefone_entry.grid(row=10, column=4, padx=10, pady=5, sticky="w")
    #     self.telefone_entry.bind("<KeyRelease>", self.formatar_telefone)

        
    #     return etapa5

    def mostrar_etapa(self):
        etapa_atual_index = self.etapas.index(self.etapa_atual.get())
        for etapa in self.conteudo_etapas:
            etapa.grid_remove()
        self.conteudo_etapas[etapa_atual_index].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.botao_anterior["state"] = "normal" if etapa_atual_index > 0 else "disabled"
        self.botao_proximo["state"] = "normal" if etapa_atual_index < len(self.etapas) - 1 else "disabled"
        self.botao_enviar["state"] = "disabled" if etapa_atual_index < len(self.etapas) - 1 else "normal"

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

    def atualizar_fronteira_menu(self, event):
        selecao_certificacao = self.certificacao_var.get()
        
        # Mapeie as seleções de certificação para as opções de fronteira correspondentes
        mapeamento_fronteira = {
            "H2Global": "Ponto de Uso",
            "CCEE": "Ponto de Produção",
            "Outros": "Inclui metano..."
        }
        
        # Obtenha a opção de fronteira correspondente com base na seleção de certificação
        opcao_fronteira = mapeamento_fronteira.get(selecao_certificacao, "")
        
        # Atualize o valor do fronteira_var e do fronteira_menu
        self.fronteira_var.set(opcao_fronteira)

    def formatar_telefone(self, event):
        # Obtém o texto atual do campo de entrada
        texto = self.telefone_entry.get()
        
        # Remove todos os caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Formata o número como (XXX) XXX-XXXX
        if len(numeros) >= 10:
            telefone_formatado = "({}) {}-{}".format(numeros[:2], numeros[2:7], numeros[7:])
        else:
            telefone_formatado = numeros

        # Atualiza o campo de entrada com o texto formatado
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, telefone_formatado)

    def formatar_coordenadas(self, event):
        # Obtém o texto atual do campo de entrada
        texto = self.latitude_entry.get()
        
        # Remove todos os caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, texto))
        
        # Formata o número como (XXX) XXX-XXXX
        if len(numeros) >= 10:
            lat_formatado = "({}) {}-{}".format(numeros[:2], numeros[2:7], numeros[7:])
        else:
            lat_formatado = numeros

        # Atualiza o campo de entrada com o texto formatado
        self.latitude_entry.delete(0, tk.END)
        self.latitude_entry.insert(0, lat_formatado)



    def mask(self, event):
        limite_intensidade = self.limite_intensidade.get()
        limite_intensidade_mask = masks.mask_numeral(limite_intensidade)
        self.limite_intensidade.delete(0, tk.END)
        self.limite_intensidade.insert(0, limite_intensidade_mask)

        limite_intensidade = self.limite_intensidade.get()
        limite_intensidade_mask = masks.mask_numeral(limite_intensidade)
        self.limite_intensidade.delete(0, tk.END)
        self.limite_intensidade.insert(0, limite_intensidade_mask)

        limite_particiapacao = self.limite_particiapacao.get()
        limite_particiapacao_mask = masks.mask_numeral(limite_particiapacao)
        self.limite_particiapacao.delete(0, tk.END)
        self.limite_particiapacao.insert(0, limite_particiapacao_mask)

        limite_adicionalidade = self.limite_adicionalidade.get()
        limite_adicionalidade_mask = masks.mask_numeral(limite_adicionalidade)
        self.limite_adicionalidade.delete(0, tk.END)
        self.limite_adicionalidade.insert(0, limite_adicionalidade_mask)

        periodo_validade_aprovacao_mask = masks.mask_numeral(self.periodo_validade_aprovacao.get())
        self.periodo_validade_aprovacao.delete(0, tk.END)
        self.periodo_validade_aprovacao.insert(0, periodo_validade_aprovacao_mask)

        latitude = self.latitude_entry.get()
        latitude_mask = masks.mask_coordenadas(latitude)
        self.latitude_entry.delete(0, tk.END)
        self.latitude_entry.insert(0, latitude_mask)



    def atualizar_e_abrir_mapa(self):
        global latitude, longitude

        try:
            # Obtém as coordenadas da latitude e longitude
            latitude = float(self.latitude_entry.get())
            longitude = float(self.longitude_entry.get())

            campo = "Erro em Especificação da Demanda"
            subcampo = "Campo Latitude"
            validate_latitude(latitude,subcampo)

            # Cria um mapa Folium centrado nas coordenadas especificadas
            mapa = folium.Map(location=[latitude, longitude], zoom_start=6)

            # Adiciona um marcador no mapa nas coordenadas especificadas
            folium.Marker([latitude, longitude], tooltip="Localização").add_to(mapa)

            # Salva o mapa como um arquivo HTML temporário
            mapa.save('mapa.html')

            # Abre o arquivo mapa.html em um navegador
            webbrowser.open('mapa.html')
        except CoordenadasInvalidasError as e:
            messagebox.showerror(campo, str(e))
        except ValueError:
            # Lidar com erros de entrada inválida (por exemplo, se as coordenadas não forem números)
            # Aqui você pode mostrar uma mensagem de erro para o usuário, se desejar.
            pass        
    
    def enviar_formulario(self):
        # Aqui você pode adicionar o código para enviar os dados do formulário para onde desejar
        # Por exemplo, você pode acessar os valores dos campos usando self.nome_entry.get(), self.email_entry.get(), etc.
        # E então, enviar esses dados para um servidor, banco de dados, ou onde quer que você precise.

        dados = {
            "tipo_certificacao": self.certif_var.get(), 
            "esquema_certificacao": self.op_certfic_var.get(), 
            "limite_intensidade_carbono": self.limite_intensidade.get(),
            "limite_participacao_minima": self.limite_particiapacao.get()
            }

        # Converte o dicionário para uma string JSON
        json_string = json.dumps(dados, indent=2)

        # Exibe a string JSON (você pode modificar isso para enviar os dados para algum lugar)
        print(json_string)


        # op_certfic_var.set("RED - Renewable Energy Directive")
        # for widget in conteudo.winfo_children():
        #     if isinstance(widget, tk.Radiobutton) and widget.cget("text") == "24 7 CFE (Carbon Free Energy)":
        #         widget.config(state=tk.DISABLED)
        # self.part_minima.config(state=tk.DISABLED)
        # self.limite_intensidade.delete(0, tk.END)
        # self.limite_intensidade.insert(0, "18")
        # self.limite_particiapacao.delete(0, tk.END)
        # self.limite_particiapacao.insert(0, "90")
        # menu_balanco_energia.set("Horária")
        # menu_limite_bidding_zone.set("SIN")
        # self.limite_adicionalidade.delete(0, tk.END)
        # self.limite_adicionalidade.insert(0, "3")
        # self.limite_emissoes_cadeira_producao.delete(0, tk.END)
        # self.limite_emissoes_cadeira_producao.insert(0, "28.2")
        # menu_fronteira_analise.set("Até a entrega")
        # self.imaterialidade.delete(0, tk.END)
        # self.imaterialidade.insert(0, "N/A")
        # menu_criterio_fator_emissão_hidrogenio.set("Combustão + Upstream")

    #def enviar_json():
        # # Obtém os valores das entryes
        # nome = entry_nome.get()
        # idade = entry_idade.get()

        # # Obtém o caminho do arquivo selecionado
        # arquivo_path = label_arquivo.cget("text")

        # # Cria um dicionário com as informações
        # dados = {"nome": nome, "idade": idade, "arquivo_path": arquivo_path}

        # # Converte o dicionário para uma string JSON
        # json_string = json.dumps(dados, indent=2)

        # # Exibe a string JSON (você pode modificar isso para enviar os dados para algum lugar)
        # print(json_string)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x550")  # Define o tamanho da janela
    root.configure(background="teal")
    app = FormularioPassoAPasso(root)
    root.mainloop()
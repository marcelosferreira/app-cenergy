import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk  # Importar a biblioteca PIL (Pillow) para trabalhar com imagens
from tkinter import Entry, Button, Label
import folium
import webbrowser

# Variáveis globais para armazenar as coordenadas
latitude = None
longitude = None

class FormularioPassoAPasso:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("App do Murilo")
        self.fonte = tkfont.Font(family="Helvetica", size=12)

        self.etapas = [
            "1. Especificação do esquema de certificação",
            "2. Especificação da demanda",
            "3. Especificação das fontes de geração de energia",
            "4. Especificação da tecnologia de armazenamento",
            "5. Especificar parâmetros de projeto"
        ]
        self.etapa_atual = tk.StringVar(value=self.etapas[0])

        # Configurar menu lateral
        self.menu_lateral = ttk.Frame(self.janela)
        self.menu_lateral.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        for etapa in self.etapas:
            #radio = ttk.Radiobutton(self.menu_lateral, text=etapa, variable=self.etapa_atual, value=etapa, command=self.mostrar_etapa)
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
        self.conteudo_etapas = [self.criar_etapa1(), self.criar_etapa2(), self.criar_etapa3(),  self.criar_etapa4(),  self.criar_etapa5()]

        # Mostrar a primeira etapa por padrão
        self.mostrar_etapa()

    def criar_etapa1(self):
        etapa1 = ttk.Frame(self.conteudo_etapa)
        etapa1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(etapa1, text="Especificação do esquema de certificação",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(etapa1, text="Selecione uma opção de esquemas de certificação:").grid(row=1, column=0, columnspan=4, sticky="w")

        self.certificacao_selecionadas = []  # Armazena as fontes selecionadas
        certificacao_opcoes = ["RED - Renewable Energy Directive", "Low Carbon Hydrogen Standart", "CHPS - Clean Hydrogen Production Standart", "Outro"]

        for col, opcao in enumerate(certificacao_opcoes):
            certificacao_var = tk.BooleanVar()
            ttk.Checkbutton(etapa1, variable=certificacao_var).grid(row=2, column=col, padx=10, pady=5, sticky="w")
            self.certificacao_selecionadas.append((opcao, certificacao_var))

            # Carregar a imagem
            imagem = Image.open(f"{opcao.lower().replace(' ', '_')}.png")
            # Redimensionar a imagem para uma largura máxima de 50 pixels
            largura_maxima = 50
            imagem.thumbnail((largura_maxima, largura_maxima))
            imagem = ImageTk.PhotoImage(imagem)

            # Exibir a imagem acima do texto
            imagem_label = tk.Label(etapa1, image=imagem)
            imagem_label.grid(row=3, column=col, padx=10, pady=5, sticky="w")

            # Exibir o texto da opção abaixo da imagem
            opcao_label = tk.Label(etapa1, text=opcao, justify="left", wraplength=120)
            opcao_label.grid(row=4, column=col, padx=10, pady=5, sticky="w")

            # Garantir que a imagem seja mantida na memória
            imagem_label.image = imagem

        ttk.Label(etapa1, text="Selecionar periodo de contabilização:").grid(row=5, column=0, sticky="w")
        opcoes_periodo = ["30 min", "horário", "diário", "semanal", "mensal"]
        self.periodo_var = tk.StringVar(etapa1)
        self.periodo_var.set(opcoes_periodo[0])  # Define a opção padrão
        periodo_menu = ttk.Combobox(etapa1, textvariable=self.periodo_var, values=opcoes_periodo)
        periodo_menu.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(etapa1, text="Selecionar uma opção de fronteira:").grid(row=6, column=0, sticky="w")
        opcoes_fronteira = ["Ponto de Uso", "Ponto de Produção", "Inclui metano..."]
        self.fronteira_var = tk.StringVar(etapa1)
        self.fronteira_var.set(opcoes_fronteira[0])  # Define a opção padrão
        fronteira_menu = ttk.Combobox(etapa1, textvariable=self.fronteira_var, values=opcoes_fronteira)
        fronteira_menu.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa1, text="Selecionar fontes de energia autorizadas:").grid(row=7, column=0, sticky="w")
        opcoes_fontes = ["Eólica", "Solar", "PCH", "UHE, Nuclear, UTE", "Rede Elétrica"]
        self.fontes_var = tk.StringVar(etapa1)
        self.fontes_var.set(opcoes_fontes[0])  # Define a opção padrão
        fontes_menu = ttk.Combobox(etapa1, textvariable=self.fontes_var, values=opcoes_fontes)
        fontes_menu.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        tk.Label(etapa1,wraplength=220, justify="left", text="Informar valor de meta de particiapação de renováveis: [valor entre 0 e 100]%").grid(row=9, column=0, sticky="w")
        self.metapar = ttk.Entry(etapa1)
        self.metapar.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # ttk.Label(etapa1, text="Selecione uma opção de esquemas de certificação:").grid(row=1, column=0, sticky="w")
        # opcoes_certificacao = ["H2Global", "CCEE", "Outros"]
        # self.certificacao_var = tk.StringVar(etapa1)
        # self.certificacao_var.set(opcoes_certificacao[0])  # Define a opção padrão
        # certificacao_menu = ttk.Combobox(etapa1, textvariable=self.certificacao_var, values=opcoes_certificacao)
        # certificacao_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        # certificacao_menu.bind("<<ComboboxSelected>>", self.atualizar_fronteira_menu)
        #certificacao_menu.config(state="disabled")

        # # Conjunto de checkboxes para seleção de fontes
        # ttk.Label(etapa1, text="Selecionar fontes de energia autorizadas:").grid(row=3, column=0, columnspan=2, sticky="w")
        # self.fontes_selecionadas = []  # Armazena as fontes selecionadas
        # fontes_opcoes = ["Eólica", "Solar", "Elétrica", "Outras"]

        # for row, opcao in enumerate(fontes_opcoes, start=3):
        #     fonte_var = tk.BooleanVar()
        #     checkbox = ttk.Checkbutton(etapa1, text=opcao, variable=fonte_var)
        #     checkbox.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        #     self.fontes_selecionadas.append((opcao, fonte_var))

        # ttk.Label(etapa1, text="Informar valor da meta de participação de renováveis:").grid(row=8, column=0, sticky="w")
        # self.vlMeta_entry = ttk.Entry(etapa1)
        # self.vlMeta_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        # ttk.Label(etapa1, text="Informar especificação da pressão do H2:").grid(row=9, column=0, sticky="w")
        # self.vlPressao_entry = ttk.Entry(etapa1)
        # self.vlPressao_entry.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # ttk.Label(etapa1, text="Informar especificação da pureza do H2:").grid(row=10, column=0, sticky="w")
        # self.vlPureza_entry = ttk.Entry(etapa1)
        # self.vlPureza_entry.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        # ttk.Label(etapa1, text="Selecionar periodo de contabilização:").grid(row=11, column=0, sticky="w")
        # opcoes_periodo = ["30 min", "horário", "diário", "semanal", "mensal"]
        # self.periodo_var = tk.StringVar(etapa1)
        # self.periodo_var.set(opcoes_periodo[0])  # Define a opção padrão
        # periodo_menu = ttk.Combobox(etapa1, textvariable=self.periodo_var, values=opcoes_periodo)
        # periodo_menu.grid(row=11, column=1, padx=10, pady=5, sticky="w")
        return etapa1


##
###
# ETAPA 2
###
##
    def criar_etapa2(self):
        etapa2 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa2, text="Especificação da Produção de Hidrogênio",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(etapa2, text="Demanda de H2:").grid(row=1, column=0, sticky="w")
        self.demandaH2 = ttk.Entry(etapa2)
        self.demandaH2.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Localizador do eletrolisador:").grid(row=2, column=0, sticky="w")

        ttk.Label(etapa2, text="     Latitude:").grid(row=3, column=0, sticky="w")
        self.latitude_entry = ttk.Entry(etapa2)
        self.latitude_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.latitude_entry.bind("<KeyRelease>", self.formatar_coordenadas)
        ttk.Label(etapa2, text="     Longitude:").grid(row=4, column=0, sticky="w")
        self.longitude_entry = ttk.Entry(etapa2)
        self.longitude_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        atualizar_abrir_botao = ttk.Button(etapa2, text="Atualizar e Abrir Mapa", command=self.atualizar_e_abrir_mapa)
        atualizar_abrir_botao.grid(row=4, column=2, columnspan=2, pady=20)

        ttk.Label(etapa2, text="Tecnologia de eletrólise:").grid(row=5, column=0, sticky="w")
        opcoes_tecnologia = ["PEM", "ALK", "Outra"]
        self.tecnologia_var = tk.StringVar(etapa2)
        self.tecnologia_var.set(opcoes_tecnologia[0])  # Define a opção padrão
        tecnologia_menu = ttk.Combobox(etapa2, textvariable=self.tecnologia_var, values=opcoes_tecnologia)
        tecnologia_menu.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Tamanho comercial do eletrolisador:").grid(row=6, column=0, sticky="w")
        self.tamanho = ttk.Entry(etapa2)
        self.tamanho.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Grau de pureza do H2 demandado:").grid(row=7, column=0, sticky="w")
        self.graupur = ttk.Entry(etapa2)
        self.graupur.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Nível de pressão de saída do eletrolisador:").grid(row=8, column=0, sticky="w")
        self.nivelpre = ttk.Entry(etapa2)
        self.nivelpre.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="Z - Fator de compressibilidade:").grid(row=9, column=0, sticky="w")
        self.fator = ttk.Entry(etapa2)
        self.fator.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="R - Constante dos gases:").grid(row=10, column=0, sticky="w")
        self.constante = ttk.Entry(etapa2)
        self.constante.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="T - Temperatura de entrada:").grid(row=11, column=0, sticky="w")
        self.temperatura = ttk.Entry(etapa2)
        self.temperatura.grid(row=11, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="N - Número de estágios de compressão:").grid(row=12, column=0, sticky="w")
        self.numestagios = ttk.Entry(etapa2)
        self.numestagios.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="ƞ - Eficiência isentrópica de compressão:").grid(row=13, column=0, sticky="w")
        self.eficienciaisent = ttk.Entry(etapa2)
        self.eficienciaisent.grid(row=13, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa2, text="ƙ - Razão entre os calores específicos:").grid(row=14, column=0, sticky="w")
        self.razaocalores = ttk.Entry(etapa2)
        self.razaocalores.grid(row=14, column=1, padx=10, pady=5, sticky="w")


        return etapa2

    def criar_etapa3(self):
        etapa3 = ttk.Frame(self.conteudo_etapa)

        # ttk.Label(etapa3, text="Nível de Satisfação:").grid(row=0, column=0, sticky="w")
        # self.satisfacao_entry = ttk.Entry(etapa3)
        # self.satisfacao_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # ttk.Label(etapa3, text="Nota do Atendimento:").grid(row=1, column=0, sticky="w")
        # self.nota_entry = ttk.Entry(etapa3)
        # self.nota_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # ttk.Button(etapa3, text="Enviar", command=self.enviar_formulario).grid(row=2, column=0, columnspan=2, pady=20)

        return etapa3

    def criar_etapa4(self):
        etapa4 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa4, text="Especificação da Tecnologia de armazenamento",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(etapa4, text="O projeto utiliza baterias?").grid(row=1, column=0, sticky="w")
        opcoes_baterias = ["Sim", "Não"]
        self.baterias_var = tk.StringVar(etapa4)
        self.baterias_var.set(opcoes_baterias[0])  # Define a opção padrão
        baterias_menu = ttk.Combobox(etapa4, textvariable=self.baterias_var, values=opcoes_baterias)
        baterias_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Limite para número de baterias?").grid(row=2, column=0, sticky="w")
        self.limitebat = ttk.Entry(etapa4)
        self.limitebat.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Selecionar tipo de tecnologia de baterias:").grid(row=3, column=0, sticky="w")
        opcoes_tecbaterias = ["Lítio", "Chumbo-Ácido", "Sódio", "Outra"]
        self.tecbaterias_var = tk.StringVar(etapa4)
        self.tecbaterias_var.set(opcoes_tecbaterias[0])  # Define a opção padrão
        tecbaterias_menu = ttk.Combobox(etapa4, textvariable=self.tecbaterias_var, values=opcoes_tecbaterias)
        tecbaterias_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="CAPEX bateria:").grid(row=4, column=0, sticky="w")
        self.capexbat = ttk.Entry(etapa4)
        self.capexbat.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Custos de O&M bateria:").grid(row=5, column=0, sticky="w")
        self.custosom = ttk.Entry(etapa4)
        self.custosom.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa4, text="Custos por desgaste de uso:").grid(row=6, column=0, sticky="w")
        self.custosdesg = ttk.Entry(etapa4)
        self.custosdesg.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        return etapa4

    def criar_etapa5(self):
        etapa5 = ttk.Frame(self.conteudo_etapa)
        ttk.Label(etapa5, text="Especificar parâmetros de projeto",font=self.fonte).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(etapa5, text="Dados econômicos:").grid(row=1, column=0, sticky="w")
        ttk.Label(etapa5, text="     Horizonte de projeto:").grid(row=2, column=0, sticky="w")
        self.horizonteprojeto = ttk.Entry(etapa5)
        self.horizonteprojeto.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Percentual de valor de revenda do projeto:").grid(row=3, column=0, sticky="w")
        self.percentualrevenda = ttk.Entry(etapa5)
        self.percentualrevenda.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     CAPEX eletrolisador:").grid(row=4, column=0, sticky="w")
        self.capexeletrolisador = ttk.Entry(etapa5)
        self.capexeletrolisador.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Custos de O&M do eletrolisador:").grid(row=5, column=0, sticky="w")
        self.custoseletrolisador = ttk.Entry(etapa5)
        self.custoseletrolisador.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Vida útil do Stack:").grid(row=6, column=0, sticky="w")
        self.vidautilstack = ttk.Entry(etapa5)
        self.vidautilstack.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Custo de substituição do Stack:").grid(row=7, column=0, sticky="w")
        self.custosubstituicao = ttk.Entry(etapa5)
        self.custosubstituicao.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     CAPEX do compressor:").grid(row=8, column=0, sticky="w")
        self.capexcompressor = ttk.Entry(etapa5)
        self.capexcompressor.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Custo de O&M do compressor:").grid(row=9, column=0, sticky="w")
        self.custocompressor = ttk.Entry(etapa5)
        self.custocompressor.grid(row=9, column=1, padx=10, pady=5, sticky="w")




        ttk.Label(etapa5, text="OXIGÊNIO:").grid(row=1, column=3, sticky="w")
        ttk.Label(etapa5, text="     Considerar venda de oxigênio:").grid(row=2, column=3, sticky="w")
        opcoes_vendaoxigenio = ["Sim", "Não"]
        self.vendaoxigenio_var = tk.StringVar(etapa5)
        self.vendaoxigenio_var.set(opcoes_vendaoxigenio[0])  # Define a opção padrão
        vendaoxigenio_menu = ttk.Combobox(etapa5, textvariable=self.vendaoxigenio_var, values=opcoes_vendaoxigenio)
        vendaoxigenio_menu.grid(row=2, column=4, padx=10, pady=5, sticky="w") 

        ttk.Label(etapa5, text="     Taxa de produção de oxigênio:").grid(row=3, column=3, sticky="w")
        self.taxaprodoxigenio = ttk.Entry(etapa5)
        self.taxaprodoxigenio.grid(row=3, column=4, padx=10, pady=5, sticky="w") 

        ttk.Label(etapa5, text="     Preço de venda de oxigênio:").grid(row=4, column=3, sticky="w")
        self.precovendaoxigenio = ttk.Entry(etapa5)
        self.precovendaoxigenio.grid(row=4, column=4, padx=10, pady=5, sticky="w")  

        ttk.Label(etapa5, text="USO DE AGUA:").grid(row=5, column=3, sticky="w")
        ttk.Label(etapa5, text="     Demanda de água para o eletrolisador (ultrapura):").grid(row=6, column=3, sticky="w")
        self.demandaagua = ttk.Entry(etapa5)
        self.demandaagua.grid(row=6, column=4, padx=10, pady=5, sticky="w") 

        ttk.Label(etapa5, text="     Demanda de água de processo para o eletrolisador:").grid(row=7, column=3, sticky="w")
        self.demandaaguaeletro = ttk.Entry(etapa5)
        self.demandaaguaeletro.grid(row=7, column=4, padx=10, pady=5, sticky="w")      

        ttk.Label(etapa5, text="     Preço da água pura:").grid(row=8, column=3, sticky="w")
        self.precoaguapura = ttk.Entry(etapa5)
        self.precoaguapura.grid(row=8, column=4, padx=10, pady=5, sticky="w")

        ttk.Label(etapa5, text="     Preço da água de processo:").grid(row=9, column=3, sticky="w")
        self.precoaguaproc = ttk.Entry(etapa5)
        self.precoaguaproc.grid(row=9, column=4, padx=10, pady=5, sticky="w")

        self.telefone_entry = ttk.Entry(etapa5)
        self.telefone_entry.grid(row=10, column=4, padx=10, pady=5, sticky="w")
        self.telefone_entry.bind("<KeyRelease>", self.formatar_telefone)

        
        return etapa5

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


    def atualizar_e_abrir_mapa(self):
        global latitude, longitude

        try:
            # Obtém as coordenadas da latitude e longitude
            latitude = float(self.latitude_entry.get())
            longitude = float(self.longitude_entry.get())

            # Cria um mapa Folium centrado nas coordenadas especificadas
            mapa = folium.Map(location=[latitude, longitude], zoom_start=6)

            # Adiciona um marcador no mapa nas coordenadas especificadas
            folium.Marker([latitude, longitude], tooltip="Localização").add_to(mapa)

            # Salva o mapa como um arquivo HTML temporário
            mapa.save('mapa.html')

            # Abre o arquivo mapa.html em um navegador
            webbrowser.open('mapa.html')
        except ValueError:
            # Lidar com erros de entrada inválida (por exemplo, se as coordenadas não forem números)
            # Aqui você pode mostrar uma mensagem de erro para o usuário, se desejar.
            pass

    def enviar_formulario(self):
        i=0
        # Aqui você pode adicionar o código para enviar os dados do formulário para onde desejar
        # Por exemplo, você pode acessar os valores dos campos usando self.nome_entry.get(), self.email_entry.get(), etc.
        # E então, enviar esses dados para um servidor, banco de dados, ou onde quer que você precise.

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x550")  # Define o tamanho da janela
    app = FormularioPassoAPasso(root)
    root.mainloop()
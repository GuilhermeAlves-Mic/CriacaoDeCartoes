import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import requests
import json
from tkcalendar import DateEntry
import traceback
import urllib.parse

# API e autenticação
api_key_add = "xi3ac1eue58j2ch0"
urlAPI = "https://b24-nfx6p2.bitrix24.com.br/rest/1/xi3ac1eue58j2ch0"
urlAPICheck = "https://b24-nfx6p2.bitrix24.com.br/rest/1/nc0by13eji6wfdkx"

def criar_fields(fields_dict):
    """
    Gera os campos no formato necessário para uma URL, com base em um dicionário.
    """
    fields = "&".join([f"FIELDS[{key}]={value}" for key, value in fields_dict.items()])
    return fields
    
class Aut_Cartao:
    def criarCartao(self):
        self.CentrodeCusto = self.CC.get()
        self.Fasee = str(self.Fase.get())  # Certifique-se de que é string
        self.especialidadeValor = self.especialidade.get()
        self.referencia = self.equipSoft.get()
        self.data_inicioo = self.data_inicio.get_date()
        self.data_fechamentoo = self.data_fechamento.get_date()
        self.prazoo = self.prazo.get_date()
        self.responsavell = self.responsavel.get()
        self.tempoEstimado_ = float(self.tempoEstimado.get()) if self.tempoEstimado.get() != '' else 0
        self.cartaopai = int(self.parent_id.get()) if self.parent_id.get() != '' else 0
        self.eixo_ = str(self.eixo.get())

        if self.colaborador:
            self.id_selecionado.set(self.colaborador["id"])

        if not isinstance(self.CentrodeCusto, str):
            messagebox.showerror("Erro", "Centro de Custo deve ser uma string.")
            return

        if not isinstance(self.Fasee, str):
            messagebox.showerror("Erro", "Fase deve ser uma string.")
            return

        if self.especialidadeValor == "Controle":
            self.especialidadeValor = "ESW002-Software_Controle-SP"
            self.entrega = "Software"
        else:
            self.entrega = self.especialidade.get()
            self.especialidadeValor = "ESW003-Software_Interface-SP"

        title = f"{self.CentrodeCusto}-FASE0{self.Fasee}-{self.especialidadeValor}-{self.entrega}-{self.referencia}"
        description = f"E%23{self.entrega} R%23{self.referencia}"
        print(f"O ID selecionado foi: {self.id_selecionado.get()}")

        if not self.task_vector:
            title = f"{self.CentrodeCusto}-FASE0{self.Fase}-{self.especialidadeValor}-{self.entrega}-{self.referencia}"
            description = f"E%23{self.entrega} R%23{self.referencia}"
            self.card_dict = {
                            "CREATED_BY": "1",
                            "TITLE": title,
                            "GROUP_ID": "2",
                            "DESCRIPTION": description,
                            "START_DATE_PLAN": self.data_inicio_,
                            "END_DATE_PLAN": self.data_fechamento_,
                            "DEADLINE": self.prazo_,
                            "RESPONSIBLE_ID": "1",
                            "CHECKLIST": self.checklist_items,
                            "ALLOW_TIME_TRACKING": "Y",
                            "TIME_ESTIMATE": self.tempoEstimado_ * 3600,
                            "PARENT_ID": self.cartaopai
            }
            self.task_vector = [self.card_dict]
    # Iterar sobre self.task_vector para criar as tarefas
        for task in self.task_vector:
            try:
                checklist_temp = task.pop("CHECKLIST", None)
                # Remove a chave CHECKLIST da requisição inicial
                print(f"Criando a tarefa: {task['TITLE']}")
                url_tarefa = f"{urlAPI}/task.item.add.json?{criar_fields(task)}"
                response = requests.get(url_tarefa)

                if response.status_code == 200:
                    try:
                        dadosTotal = response.json()
                        print(f"Resposta da API: {dadosTotal}")
                        result = dadosTotal.get("result", {})
                        if isinstance(result, int):
                            task_id_value = result
                            print(f"Tarefa criada com sucesso. ID da tarefa: {task_id_value}")

                            # Adicionar itens de checklist à tarefa criada
                            if checklist_temp is not None:  # Verifica se o checklist existe na tarefa
                                for item in checklist_temp:
                                    checklist_dict = {
                                        "taskId": task_id_value,  # O Bitrix espera "taskId" no corpo
                                        "fields": {  # Campos adicionais dentro de "fields"
                                            "TITLE": item
                                        }
                                    }
                                    url_checklist = f"{urlAPICheck}/task.checklistitem.add.json"
                                    response_checklist = requests.post(url_checklist, json=checklist_dict)

                                    if response_checklist.status_code == 200:
                                        dados_checklist = response_checklist.json()
                                        if "result" in dados_checklist:
                                            print(f"Checklist item '{item}' adicionado com sucesso para a tarefa ID {task_id_value}!")
                                        else:
                                            print(f"Erro ao adicionar checklist item '{item}': {dados_checklist}")
                                    else:
                                        print(f"Erro na API ao adicionar checklist. Status: {response_checklist.status_code}")
                                        print(checklist_dict)
                                        print(f"Resposta completa: {response_checklist.text}")
                        else:
                            print(f"Erro inesperado: resposta inválida ao criar a tarefa. Resposta: {dadosTotal}")
                    except ValueError:
                        print(f"Erro: resposta não é um JSON válido. Resposta: {response.text}")
                else:
                    print(f"Erro ao criar a tarefa. Status: {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Erro ao criar o cartão: {str(e)}")
                traceback.print_exc()

    
    def exibirListaCartoes(self):
            title = ""
            #print(title)
            self.CentrodeCusto = self.CC.get()
            self.AtualFase = str(self.Fase.get())  # Certifique-se de que é string
            self.especialidadeValor = self.especialidade.get()
            self.referencia = self.equipSoft.get()
            self.data_inicio_ = self.data_inicio.get_date()
            self.data_fechamento_ = self.data_fechamento.get_date()
            self.prazo_ = self.prazo.get_date()
            self.responsavel_ = self.responsavel.get()
            self.tempoEstimado_ = float(self.tempoEstimado.get()) if self.tempoEstimado.get() != '' else 0
            self.cartaopai = int(self.parent_id.get()) if self.parent_id.get() != '' else 0
            self.eixo_ = str(self.eixo.get())
            self.UF_ = self.UF.get()

            if self.colaborador:
                self.id_selecionado.set(self.colaborador["id"])

            if not isinstance(self.CentrodeCusto, str):
                messagebox.showerror("Erro", "Centro de Custo deve ser uma string.")
                return

            if not isinstance(self.AtualFase, str):
                messagebox.showerror("Erro", "Fase deve ser uma string.")
                return

            if self.especialidadeValor == "Controle":
                self.especialidadeValor = "ESW002-Software_Controle-SP"
                self.entrega = "Software"
            else:
                self.entrega = self.especialidade.get()
                self.especialidadeValor = "ESW003-Software_Interface-SP"

            description = f"E%23{self.entrega} R%23{self.referencia}"

            title = f"{self.CentrodeCusto}-FASE0{self.AtualFase}-{self.especialidadeValor}-{self.entrega}-{self.referencia}"

            self.card_titles.append(title)
            self.task_listbox.insert(tk.END, title)

            if self.entrega == "Software":
                self.checklist_items = ["#501 - Estudo Tecnico", "#102 - Especificação", "#103 - Manual", 
                                                   "#104 - Tabela de Variaveis / Roteiro de Testes",  
                                                   "#105 - Desenvolvimento", "#106 - Teste Funcional / Teste Unitario"]
            elif self.entrega == "IHM":
                self.checklist_items = ['#501 - Estudo Tecnico', '#202 - Manual', '#203 - Desenvolvimento', '#204 - Teste Funcional']
            elif self.entrega == "Supervisão":
                self.checklist_items = ["#501 - Estudo Tecnico", "#402 - Telas", "#403 - Drivers", "#404 - Bibliotecas", "#405 - Setup"]
            elif self.entrega == "G5":
                self.checklist_items = ["#501 - Estudo Tecnico", "#302 - Bibliotecas", "#303 - Modelos de Escrita", "#304 - Instancia", "#305 - Teste Funcional"]

            self.fulltask = {
                                "CREATED_BY": "1",
                                "TITLE": title,
                                "GROUP_ID": "2",
                                "DESCRIPTION": description,
                                "START_DATE_PLAN": self.data_inicio_,
                                "END_DATE_PLAN": self.data_fechamento_,
                                "DEADLINE": self.prazo_,
                                "RESPONSIBLE_ID": "1",
                                "CHECKLIST": self.checklist_items,
                                "ALLOW_TIME_TRACKING": "Y",
                                "TIME_ESTIMATE": self.tempoEstimado_ * 3600,
                                "PARENT_ID": self.cartaopai,
                                "TAGS": f"{self.eixo_}, {self.UF_}"
                            }

            self.checklist_vector.append(self.checklist_items.copy())
            self.task_vector.append(self.fulltask.copy())
            print(self.task_vector)
            print(self.checklist_vector)

    def tela(self):
        self.card_titles = []
        self.janela = ThemedTk(theme="winxpblue")
        self.janela.title("Criação de Cartões")
        self.janela.geometry("800x600")

        # Rótulo e Combobox para "Board"
        tk.Label(self.janela, text="Board: ", font="Arial 10 bold", padx=9).place(x=0, y=20)
        self.board = ttk.Combobox(self.janela, values=["Soft-SP-Atividades", "Soft-SP-Atividades EQX"], state="readonly")
        self.board.place(x=130, y=21)
        self.board.bind("<<ComboboxSelected>>", self.definirGroupID)

        self.janela.mainloop()

    def definirGroupID(self, event=None):
        board_value = self.board.get()
        if board_value == "Soft-SP-Atividades":
            self.groupid = "796"
        else:
            self.groupid = "812"
        self.telaContinuacao()

    def telaContinuacao(self):
        self.checklist_vector = []
        self.task_vector = []
        if self.groupid == '796':
            self.listEquip = ["C01", "C02", "C03", "C04", "C05", "MM", "TRAFO", "NB", "Gerador", "Relé de Proteção", "Relé Térmico",
                                "Medidor de Concessionária", "Medidor de Qualidade", "Chiller", "Termostato",
                                "HVAC", "SENSOR", "CLP", "IO REMOTO", "Hidrômetro", "Disjuntor", "ATS",
                                "Banco de Baterias", "Retificador"]
        else:
            self.listEquip = ["ARESET", "AHUMGR", "CLGMGR", "PUMPMGR", "RAS", "APRESET", "WTRSTGMGR",
                                "AHU", "CWBPV", "ACC", "CHRMMON", "COLOMAU", "COMPRESSOR", "CA", "CHWSTR",
                                "CHWBT", "CT", "CRAC", "CRAH", "D2SD", "DXUNIT", "FAN", "HDAC", "HX",
                                "HUM", "HUMUNITARY", "RMDMPR", "SUMP", "VLV2POS", "VLVMOD", "VFD", "VAV",
                                "VRF", "VRFOD", "ANALOGSENSOR", "GWM", "WHUMIDITY", "WTEMPERATURE",
                                "HAZGAS", "MISCALARMS", "METRICS", "WLPRESSURE", "WLHUMIDITY",
                                "WLTEMPERATURE", "WSTN", "FS", "LEAK", "VESDA", "ALHB", "RIO", "MECATS",
                                "PLCMON", "PLCNET", "REMIOMON", "VENDSWBUSDT", "GSB", "GRMU", "LVSB",
                                "MVSW", "MVTB", "MLTX", "PUSP", "RMU", "SUSP", "SUDB", "Utility Power",
                                "ZZRMU", "DPM", "LVDB", "LVCBM", "MVCB", "MVCBM", "PQM", "MVPLC", "MVUN",
                                "FBULK", "FDAY", "FFIL", "FPO", "GEN", "FC", "PV", "ATS", "MECHATS",
                                "DC Plant", "PDU", "STS", "UPS"]
        
        self.colaboradores = [
                                {"id": 498, "nome": "Guilherme Alves"},
                                {"id": 718, "nome": "Luckas Alexandre"},
                                {"id": 210, "nome": "Higor Lobo"},
                                {"id": 2670, "nome": "Diogo da Terra"},
                                {"id": 3026, "nome": "Felipe de Gouveia"},
                                {"id": 442, "nome": "Gabriel Lázaro"},
                                {"id": 652, "nome": "Lauren Machado"},
                                {"id": 1446, "nome": "Gustavo Martins"},
                                {"id": 398, "nome": "Evelyn Pereira"},
                                {"id": 196, "nome": "Kayque Rocha"},
                                {"id": 42, "nome": "Daniel Souza"},
                                {"id": 648, "nome": "Igor Vernasqui"}
                             ]
        self.id_selecionado = tk.IntVar(value=0)

        self.nomes_colaboradores = [self.colaborador["nome"] for self.colaborador in self.colaboradores]
        
        # Campos de entrada
        tk.Label(self.janela, text="Centro de Custo: ", font="Arial 10 bold", padx=9).place(x=0, y=60)
        self.CC = tk.Entry(self.janela, width=15, font="Arial 10")
        self.CC.place(x=130, y=61)

        tk.Label(self.janela, text="Eixo: ", font="Arial 10 bold", padx=9).place(x=268, y=60)
        self.eixo = (ttk.Combobox(self.janela, values=["A1", "A2", "CAG", "DC"], width=10, state="readonly"))
        self.eixo.place(x=360,y=63)

        tk.Label(self.janela, text="UF: ", font="Arial 10 bold", padx=9).place(x=465, y=60)
        self.UF = (ttk.Combobox(self.janela, values=["SP", "RJ"], width=10, state="readonly"))
        self.UF.place(x=510, y=62)

        # Campos para Fase, Especialidade, Equipamento/Software, e Data
        tk.Label(self.janela, text="Fase: ", font="Arial 10 bold", padx=9).place(x=0, y=100)
        self.Fase = tk.Entry(self.janela, width=15, font="Arial 10")
        self.Fase.place(x=130, y=101)

        tk.Label(self.janela, text="Especialidade: ", font="Arial 10 bold", padx=9).place(x=0, y=140)
        self.especialidade = ttk.Combobox(self.janela, values=["Controle", "IHM", "Supervisão", "G5"], state="readonly")
        self.especialidade.place(x=130, y=141)

        tk.Label(self.janela, text="Cartão Pai: ", font="Arial 10 bold", padx=9).place(x=268, y=138)
        self.parent_id = tk.Entry(self.janela,  width=15, font="Arial 10")
        self.parent_id.place(x=360, y=140)

        tk.Label(self.janela, text="Tempo estimado: ", font="Arial 10 bold", padx=9).place(x=0, y=180) 
        self.tempoEstimado = tk.Entry(self.janela, width=15, font="Arial 10")
        self.tempoEstimado.place(x=132, y=180)

        tk.Label(self.janela, text="Equipamento/Software: ", font="Arial 10 bold", padx=9).place(x=0, y=225)
        self.equipSoft = ttk.Combobox(self.janela, values=self.listEquip, width=35)
        self.equipSoft.place(x=165, y=228)
        tk.Label(self.janela, text="Data de inicio: ", font="Arial 10 bold", padx=9).place(x=0, y=267)

        self.data_inicio = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.data_inicio.place(x=120, y=270)

        tk.Label(self.janela, text="Data de término: ", font="Arial 10 bold", padx=9).place(x=248, y=266)
        self.data_fechamento = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.data_fechamento.place(x=380, y=269)

        tk.Label(self.janela, text="Prazo: ", font="Arial 10 bold", padx=9).place(x=525, y=266) 
        self.prazo = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.prazo.place(x=595, y=268)

        tk.Label(self.janela, text="Responsável:", font="Arial 10 bold",padx=9).place(x=0, y=305)
        self.responsavel = ttk.Combobox(self.janela, values=self.nomes_colaboradores, width=20)
        self.responsavel.place(x=120, y=306)

        # Botão para criar o cartão
        criar = ttk.Button(self.janela, text="Criar Cartão", command=self.criarCartao, width=20)
        criar.place(x=360, y=355)

        addLista = ttk.Button(self.janela, text="Adicionar a Lista", command=self.exibirListaCartoes, width=20)
        addLista.place(x=215, y=355)

        tk.Label(self.janela, text="Tarefas:", font="Arial 10 bold", wraplength=500, anchor="w", justify="left").place(x=325, y=400)
        self.task_listbox = tk.Listbox(self.janela, width=75, height=5, background="#F0F0F0", borderwidth=0) 
        self.task_listbox.place(x=195, y=430)

objeto = Aut_Cartao()
objeto.tela()

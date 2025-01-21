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
        self.Fase = str(self.Fase.get())  # Certifique-se de que é string
        self.especialidadeValor = self.especialidade.get()
        self.referencia = self.equipSoft.get()
        self.data_inicio = self.data_inicio.get_date()
        self.data_fechamento = self.data_fechamento.get_date()
        self.prazo = self.prazo.get_date()
        self.responsavel = self.responsavel.get()
        
        if self.colaborador:
            self.id_selecionado.set(self.colaborador["id"])

        if not isinstance(self.CentrodeCusto, str):
            messagebox.showerror("Erro", "Centro de Custo deve ser uma string.")
            return

        if not isinstance(self.Fase, str):
            messagebox.showerror("Erro", "Fase deve ser uma string.")
            return

        if self.especialidadeValor == "Controle":
            self.especialidadeValor = "ESW002-Software_Controle-SP"
            self.entrega = "Software"
        else:
            self.entrega = self.especialidade.get()
            self.especialidadeValor = "ESW003-Software_Interface-SP"

        title = f"{self.CentrodeCusto}-FASE0{self.Fase}-{self.especialidadeValor}-{self.entrega}-{self.referencia}"
        description = f"E%23{self.entrega} R%23{self.referencia}"
        print(f"O ID selecionado foi: {self.id_selecionado.get()}")

        self.card_dict = {
            "CREATED_BY": "1",
            "TITLE": title,
            "GROUP_ID": "2",
            "DESCRIPTION": description,
            "START_DATE_PLAN": self.data_inicio,
            "END_DATE_PLAN": self.data_fechamento,
            "DEADLINE": self.prazo,
            "RESPONSIBLE_ID": self.id_selecionado.get()
        }

        try:
            print("Criando a tarefa...")
            url_tarefa = f"{urlAPI}/task.item.add.json?{criar_fields(self.card_dict)}"
            response = requests.get(url_tarefa)

            if response.status_code == 200:
                try:
                    dadosTotal = response.json()
                    print(f"Resposta da API: {dadosTotal}")
                    result = dadosTotal.get("result", {})
                    if isinstance(result, int):
                        task_id_value = result
                        task_id_value = int(task_id_value)
                        print(f"Tarefa criada com sucesso. ID da tarefa: {task_id_value}")

                        # Itens do checklist a serem adicionados
                        if self.entrega == "Software":
                            checklist_items = ["#501 - Estudo Tecnico", "#102 - Especificação", "#103 - Manual" "#104 - Tabela de Variaveis / Roteiro de Testes",  
                                               "#105 - Desenvolvimento", "#106 - Teste Funcional / Teste Unitario"]
                        elif self.entrega == "IHM":
                            checklist_items = ['#501 - Estudo Tecnico', '#202 - Manual', '#203 - Desenvolvimento', '#204 - Teste Funcional']
                        elif self.entrega == "Supervisão":
                            checklist_items = ["#501 - Estudo Tecnico", "#402 - Telas", "#403 - Drivers", "#404 - Bibliotecas", "#405 - Setup"]
                        elif self.entrega == "G5":
                            checklist_items = ["#501 - Estudo Tecnico", "#302 - Bibliotecas", "#303 - Modelos de Escrita", "#304 - Instancia","#305 - Teste Funcional"]

                        # Loop para adicionar os itens do checklist
                        for item in checklist_items:
                            checklist_dict = {
                                "taskId": task_id_value,  # O Bitrix espera "taskId" no corpo
                                "fields": {         # Campos adicionais dentro de "fields"
                                    "TITLE": item
                                }
                            }

                            # Endpoint da API
                            url_checklist = f"{urlAPICheck}/task.checklistitem.add.json"

                            # Enviando como POST com JSON no corpo
                            response_checklist = requests.post(url_checklist, json=checklist_dict)

                            # Verificar a resposta
                            if response_checklist.status_code == 200:
                                dados_checklist = response_checklist.json()
                                if "result" in dados_checklist:
                                    print(f"Checklist item '{item}' adicionado com sucesso!")
                                else:
                                    print(f"Erro ao adicionar checklist item '{item}': {dados_checklist}")
                            else:
                                print(f"Erro na API ao adicionar checklist. Status: {response_checklist.status_code}")
                                print(f"Resposta completa: {response_checklist.text}")

                except ValueError:
                    print(f"Erro: resposta não é um JSON válido. Resposta: {response.text}")
            else:
                print(f"Erro ao criar a tarefa. Status: {response.status_code}")
        except Exception as e:
            print(f"Erro ao criar o cartão: {str(e)}")
            traceback.print_exc()

    def exibirListaCartoes(self):
        contagem =+1

        if contagem < 2:

            self.CentrodeCusto = self.CC.get()
            self.AtualFase = self.Fase.get()  # Certifique-se de que é string
            self.especialidadeValor = self.especialidade.get()
            self.referencia = self.equipSoft.get()


            if self.especialidadeValor == "Controle":
                self.entrega = "Software"
            else:
                self.entrega = self.especialidade.get()

            self.card_titles = f"{self.CentrodeCusto}-FASE0{self.AtualFase}-{self.especialidadeValor}-{self.entrega}-{self.referencia}"

            self.task_listbox.delete(0, tk.END)  # Limpar Listbox
            for title in self.card_titles:
                self.task_listbox.insert(tk.END, title)

            if self.card_titles:
                lista_cartoes = "\n".join(self.card_titles)
                messagebox.showinfo("Lista de Cartões", f"Títulos dos cartões criados:\n{lista_cartoes}")
            else:
                messagebox.showinfo("Lista de Cartões", "Nenhum cartão foi criado ainda.")

        else:
            print("Asteca")

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
        if self.groupid == '796':
            self.listEquip = ["C01", "C02", "C03", "C04", "C05"]
        else:
            self.listEquip = ["ARESET", "AHUMGR", "CLGMGR", "CTRMGR"]
        
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

        # Campos para Fase, Especialidade, Equipamento/Software, e Data
        tk.Label(self.janela, text="Fase: ", font="Arial 10 bold", padx=9).place(x=0, y=100)
        self.Fase = tk.Entry(self.janela, width=15, font="Arial 10")
        self.Fase.place(x=130, y=101)

        tk.Label(self.janela, text="Especialidade: ", font="Arial 10 bold", padx=9).place(x=0, y=140)
        self.especialidade = ttk.Combobox(self.janela, values=["Controle", "IHM", "Supervisão", "G5"], state="readonly")
        self.especialidade.place(x=130, y=141)

        tk.Label(self.janela, text="Equipamento/Software: ", font="Arial 10 bold", padx=9).place(x=0, y=180)
        self.equipSoft = ttk.Combobox(self.janela, values=self.listEquip, width=35)
        self.equipSoft.place(x=165, y=185)
        tk.Label(self.janela, text="Data de inicio: ", font="Arial 10 bold", padx=9).place(x=0, y=222)

        self.data_inicio = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.data_inicio.place(x=120, y=225)

        tk.Label(self.janela, text="Data de término: ", font="Arial 10 bold", padx=9).place(x=248, y=221)
        self.data_fechamento = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.data_fechamento.place(x=380, y=224)

        tk.Label(self.janela, text="Prazo: ", font="Arial 10 bold", padx=9).place(x=525, y=221) 
        self.prazo = DateEntry(self.janela, width=15, background='darkblue',
                   foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.prazo.place(x=595, y=223)

        tk.Label(self.janela, text="Responsável:", font="Arial 10 bold",padx=9).place(x=0, y=260)
        self.responsavel = ttk.Combobox(self.janela, values=self.nomes_colaboradores, width=20)
        self.responsavel.place(x=120, y=260)

        # Botão para criar o cartão
        criar = ttk.Button(self.janela, text="Criar Cartão", command=self.criarCartao, width=20)
        criar.place(x=650, y=410)

        exibir = ttk.Button(self.janela, text="Exibir Lista de Cartões", command=self.exibirListaCartoes, width=20)
        exibir.place(x=650, y=460)

        tk.Label(self.janela, text="Tarefas Criadas:", font="Arial 10 bold", wraplength=500, anchor="w", justify="left").place(x=400, y=20)
        self.task_listbox = tk.Listbox(self.janela, width=50, height=20) 
        self.task_listbox.place(x=400, y=50)

objeto = Aut_Cartao()
objeto.tela()

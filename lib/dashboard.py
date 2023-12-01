from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta, date
from datetime import datetime
from lib import crud as c  

class FinanceiroApp(Frame):
    def __init__(self, frame):
        super().__init__(frame)

        # Variáveis para armazenar dados
        
        self.taxas_sites = [dado[2] for dado in c.BANCOS["origem"].read()]
        
        self.receitas_aluguel = [(dado[2], dado[3], dado[5]) for dado in c.BANCOS["aluguel"].read()]
        
        self.lucros = [dado[2] - self.taxas_sites[dado[0]-1] * 0.01 * dado[2] for dado in self.receitas_aluguel]
        
        self.receitas_aluguel = [(dado[2], dado[3], dado[5]) for dado in c.BANCOS["aluguel"].read()]
        
        print(f"{self.receitas_aluguel} {self.lucros} {self.receitas_aluguel}")
        


        self.plotar_grafico_receitas()

    @staticmethod
    def get_days_between_dates(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
        delta = end_date - start_date
        days_in_between = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        result = [day.strftime("%Y%m%d") for day in days_in_between]
        return result

    def filtrar_por_data(self):
        data_inicial = self.data_inicial_var.get()
        data_final = self.data_final_var.get()

        # Converter datas para o formato datetime para comparação
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y")

        # Limpar as tabelas antes de aplicar o filtro
        self.tree_receitas.delete(*self.tree_receitas.get_children())

        # Adicionar transações filtradas de acordo com o intervalo de datas
        for transacao in self.receitas_aluguel:
            transacao_data = datetime.strptime(transacao[0], "%d/%m/%Y")
            if data_inicial <= transacao_data <= data_final:
                self.tree_receitas.insert('', 'end', values=transacao)

    def format_date(self, selected_date):
        parsed_date = datetime.strptime(str(selected_date), "%Y%m%d")
        return parsed_date.strftime("%d/%m/%y")

    def plotar_grafico_receitas(self):
        self.plotar_grafico(self.receitas_aluguel, 'Receitas de Aluguel por Data', 'green')

    def plotar_grafico(self, transacoes, titulo, cor):
        datas = [self.format_date(str(transacao[1])) for transacao in transacoes]
        valores = [float(self.lucros[index]) for index,transacao in enumerate(transacoes)]

        fig, ax = plt.subplots()
        ax.bar(datas, valores, color=cor)
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title(titulo)

        # Incorporar o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=12, padx=10, pady=10, sticky='nsew')

from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from datetime import datetime
from lib import crud as c  
from lib import date_formatting as df

class FinanceiroApp(Frame):
    """A class representing a financial application with graphical representation of rental revenues."""

    def __init__(self, frame):
        """
        Initialize the FinanceiroApp instance.

        Parameters:
        - frame: The Tkinter frame to which the FinanceiroApp belongs.
        """
        super().__init__(frame)
        
        self.atualizar_grafico()
        self.bind("<FocusIn>", self.atualizar_grafico)

    def atualizar_grafico(self, event=None):
        """
        Update the financial chart.

        Parameters:
        - event: The event that triggered the update (default is None).
        """
        self.taxas_sites = [dado[2] for dado in c.BANCOS["origem"].read()]
        
        self.receitas_aluguel = [(dado[2], dado[3], dado[5]) for dado in c.BANCOS["aluguel"].read()]
        
        self.lucros = [dado[2] - self.taxas_sites[dado[0]-1] * 0.01 * dado[2] for dado in self.receitas_aluguel]
             
        self.plotar_grafico_receitas()

    def filtrar_por_data(self):
        """Filter transactions based on date range."""
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

    def plotar_grafico_receitas(self, event=None):
        """Plot the rental revenues chart."""
        self.plotar_grafico(self.receitas_aluguel, 'Receitas de Aluguel por Data', 'green')

    def plotar_grafico(self, transacoes, titulo, cor):
        """
        Plot a bar chart for given transactions.

        Parameters:
        - transacoes: List of transactions to be plotted.
        - titulo: Title of the chart.
        - cor: Color of the bars in the chart.
        """
        datas = [df.unformat_date(str(transacao[1])) for transacao in transacoes]
        valores = [float(self.lucros[index]) for index, transacao in enumerate(transacoes)]

        fig, ax = plt.subplots()
        ax.bar(datas, valores, color=cor)
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title(titulo)

        # Incorporar o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=12, padx=10, pady=10, sticky='nsew')
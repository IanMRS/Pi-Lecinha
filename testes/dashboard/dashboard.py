import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class FinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Financeiro")

        # Variáveis para armazenar dados
        self.despesas = []
        self.receitas_aluguel = []

        # Variáveis para filtrar datas nos gráficos
        self.data_inicial_var = tk.StringVar()
        self.data_final_var = tk.StringVar()

        # Widgets
        self.label_data = tk.Label(root, text="Data:")
        self.entry_data = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')

        self.label_valor = tk.Label(root, text="Valor:")
        self.entry_valor = tk.Entry(root)

        self.label_tipo = tk.Label(root, text="Tipo:")
        self.tipo_var = tk.StringVar()
        self.tipo_combobox = ttk.Combobox(root, textvariable=self.tipo_var, values=["Receita", "Despesa"])
        self.tipo_combobox.set("Receita")

        self.button_adicionar = tk.Button(root, text="Adicionar Transação", command=self.adicionar_transacao)

        self.tree_receitas = ttk.Treeview(root, columns=('Data', 'Casa', 'Valor'), show='headings')
        self.tree_receitas.heading('Data', text='Data')
        self.tree_receitas.heading('Casa', text='Casa')
        self.tree_receitas.heading('Valor', text='Valor')
        self.tree_receitas_scroll = ttk.Scrollbar(root, orient='vertical', command=self.tree_receitas.yview)
        self.tree_receitas.configure(yscrollcommand=self.tree_receitas_scroll.set)

        self.tree_despesas = ttk.Treeview(root, columns=('Data', 'Tipo', 'Valor'), show='headings')
        self.tree_despesas.heading('Data', text='Data')
        self.tree_despesas.heading('Tipo', text='Tipo')
        self.tree_despesas.heading('Valor', text='Valor')
        self.tree_despesas_scroll = ttk.Scrollbar(root, orient='vertical', command=self.tree_despesas.yview)
        self.tree_despesas.configure(yscrollcommand=self.tree_despesas_scroll.set)

        self.button_filtrar = tk.Button(root, text="Filtrar por Data", command=self.filtrar_por_data)

        self.button_plot_receitas = tk.Button(root, text="Plotar Gráfico Receitas", command=self.plotar_grafico_receitas)
        self.button_plot_despesas = tk.Button(root, text="Plotar Gráfico Despesas", command=self.plotar_grafico_despesas)

        # Widgets para filtrar datas nos gráficos
        self.label_data_inicial = tk.Label(root, text="Data Inicial:")
        self.entry_data_inicial = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,
                                            textvariable=self.data_inicial_var, date_pattern='dd/mm/yyyy')

        self.label_data_final = tk.Label(root, text="Data Final:")
        self.entry_data_final = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,
                                          textvariable=self.data_final_var, date_pattern='dd/mm/yyyy')

        # Layout
        self.label_data.grid(row=0, column=0, padx=10, pady=5)
        self.entry_data.grid(row=0, column=1, padx=10, pady=5)

        self.label_valor.grid(row=1, column=0, padx=10, pady=5)
        self.entry_valor.grid(row=1, column=1, padx=10, pady=5)

        self.label_tipo.grid(row=2, column=0, padx=10, pady=5)
        self.tipo_combobox.grid(row=2, column=1, padx=10, pady=5)

        self.button_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

        self.tree_receitas.grid(row=4, column=0, columnspan=2, pady=10, rowspan=3, sticky='nsew')
        self.tree_receitas_scroll.grid(row=4, column=2, rowspan=3, sticky='ns')

        self.tree_despesas.grid(row=7, column=0, columnspan=2, pady=10, rowspan=3, sticky='nsew')
        self.tree_despesas_scroll.grid(row=7, column=2, rowspan=3, sticky='ns')

        self.button_filtrar.grid(row=10, column=0, columnspan=2, pady=10)

        self.button_plot_receitas.grid(row=4, column=3, rowspan=3, padx=10, pady=10, sticky='nsew')
        self.button_plot_despesas.grid(row=7, column=3, rowspan=3, padx=10, pady=10, sticky='nsew')

        self.label_data_inicial.grid(row=10, column=3, padx=10, pady=5)
        self.entry_data_inicial.grid(row=10, column=4, padx=10, pady=5)

        self.label_data_final.grid(row=11, column=3, padx=10, pady=5)
        self.entry_data_final.grid(row=11, column=4, padx=10, pady=5)

        # Configuração da grade para que as células se expandam com a janela
        for i in range(12):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)

    def adicionar_transacao(self):
        data = self.entry_data.get()
        tipo = self.tipo_var.get()
        valor = self.entry_valor.get()

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número.")
            return

        if data and tipo and valor:
            transacao = (data, tipo, valor)
            if tipo.lower() == 'receita':
                self.receitas_aluguel.append(transacao)
                self.tree_receitas.insert('', 'end', values=transacao)
            elif tipo.lower() == 'despesa':
                self.despesas.append(transacao)
                self.tree_despesas.insert('', 'end', values=transacao)

    def filtrar_por_data(self):
        data_inicial = self.data_inicial_var.get()
        data_final = self.data_final_var.get()

        # Converter datas para o formato datetime para comparação
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y")

        # Limpar as tabelas antes de aplicar o filtro
        self.tree_receitas.delete(*self.tree_receitas.get_children())
        self.tree_despesas.delete(*self.tree_despesas.get_children())

        # Adicionar transações filtradas de acordo com o intervalo de datas
        for transacao in self.receitas_aluguel:
            transacao_data = datetime.strptime(transacao[0], "%d/%m/%Y")
            if data_inicial <= transacao_data <= data_final:
                self.tree_receitas.insert('', 'end', values=transacao)

        for transacao in self.despesas:
            transacao_data = datetime.strptime(transacao[0], "%d/%m/%Y")
            if data_inicial <= transacao_data <= data_final:
                self.tree_despesas.insert('', 'end', values=transacao)

    def plotar_grafico_receitas(self):
        self.plotar_grafico(self.receitas_aluguel, 'Receitas de Aluguel por Data', 'green')

    def plotar_grafico_despesas(self):
        self.plotar_grafico(self.despesas, 'Despesas por Data', 'red')

    def plotar_grafico(self, transacoes, titulo, cor):
        datas = [transacao[0] for transacao in transacoes]
        valores = [float(transacao[2]) for transacao in transacoes]

        fig, ax = plt.subplots()
        ax.bar(datas, valores, color=cor)
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title(titulo)

        # Incorporar o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=12, padx=10, pady=10, sticky='nsew')

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceiroApp(root)
    root.mainloop()
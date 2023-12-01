from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from data import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Github\Tkinter-Designer\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
          return ASSETS_PATH / Path(path)

class AppFrame(Frame):
          def __init__(self, frame):
                    super().__init__(frame)

                    self.configure(bg = "#444444")


                    canvas = Canvas(
                    self,
                    bg = "#444444",
                    height = 550,
                    width = 1020,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge"
                    )

                    canvas.place(x = 0, y = 0)
                    image_image_1 = PhotoImage(
                    file=relative_to_assets("image_1.png"))
                    image_1 = canvas.create_image(
                    159.0,
                    75.0,
                    image=image_image_1
                    )

                    image_image_2 = PhotoImage(
                    file=relative_to_assets("image_2.png"))
                    image_2 = canvas.create_image(
                    159.0,
                    319.977783203125,
                    image=image_image_2
                    )

                    canvas.create_text(
                    44.0,
                    49.497772216796875,
                    anchor="nw",
                    text="Receitas de Aluguel",
                    fill="#000000",
                    font=("ArialRoundedMTBold", 16 * -1)
                    )

                    image_image_3 = PhotoImage(
                    file=relative_to_assets("image_3.png"))
                    image_3 = canvas.create_image(
                    31.0,
                    58.355560302734375,
                    image=image_image_3
                    )

                    image_image_4 = PhotoImage(
                    file=relative_to_assets("image_4.png"))
                    image_4 = canvas.create_image(
                    858.0,
                    73.0,
                    image=image_image_4
                    )

                    image_image_5 = PhotoImage(
                    file=relative_to_assets("image_5.png"))
                    image_5 = canvas.create_image(
                    858.0,
                    319.0,
                    image=image_image_5
                    )

                    canvas.create_text(
                    743.0,
                    49.0,
                    anchor="nw",
                    text="Despesas",
                    fill="#000000",
                    font=("ArialRoundedMTBold", 16 * -1)
                    )

                    image_image_6 = PhotoImage(
                    file=relative_to_assets("image_6.png"))
                    image_6 = canvas.create_image(
                    408.0,
                    73.0,
                    image=image_image_6
                    )

                    canvas.create_text(
                    356.652587890625,
                    49.0,
                    anchor="nw",
                    text="Casas Alugadas",
                    fill="#000000",
                    font=("ArialRoundedMTBold", 16 * -1)
                    )

                    image_image_7 = PhotoImage(
                    file=relative_to_assets("image_7.png"))
                    image_7 = canvas.create_image(
                    344.0,
                    59.0,
                    image=image_image_7
                    )

                    image_image_8 = PhotoImage(
                    file=relative_to_assets("image_8.png"))
                    image_8 = canvas.create_image(
                    1490.0,
                    2518.0,
                    image=image_image_8
                    )

                    image_image_9 = PhotoImage(
                    file=relative_to_assets("image_9.png"))
                    image_9 = canvas.create_image(
                    600.0,
                    73.0,
                    image=image_image_9
                    )

                    canvas.create_text(
                    539.0,
                    49.0,
                    anchor="nw",
                    text="Site mais vendido",
                    fill="#000000",
                    font=("ArialRoundedMTBold", 16 * -1)
                    )

                    image_image_10 = PhotoImage(
                    file=relative_to_assets("image_10.png"))
                    image_10 = canvas.create_image(
                    525.0,
                    60.0,
                    image=image_image_10
                    )

                    image_image_11 = PhotoImage(
                    file=relative_to_assets("image_11.png"))
                    image_11 = canvas.create_image(
                    509.0,
                    424.0,
                    image=image_image_11
                    )

                    image_image_12 = PhotoImage(
                    file=relative_to_assets("image_12.png"))
                    image_12 = canvas.create_image(
                    509.0,
                    214.0,
                    image=image_image_12
                    )

                    image_image_13 = PhotoImage(
                    file=relative_to_assets("image_13.png"))
                    image_13 = canvas.create_image(
                    727.0,
                    60.0,
                    image=image_image_13
                    )

                    revenue_data = pd.DataFrame(revenue)
                    revenue_data["date"] = pd.to_datetime(revenue_data["date"])

                    #grafico vertical
                    fig_1=Figure(figsize=(2.5, 2.2),facecolor="#D9D9D9")
                    ax_1 = fig_1.add_subplot()
                    ax_1.set_facecolor("#D9D9D9")
                    ax_1.fill_between(x=revenue_data["date"], y1=revenue_data["amount"], alpha=0.7)
                    ax_1.tick_params(labelsize=7, colors="black")
                    fig_1.autofmt_xdate()
                    ax_1.plot(revenue_data["date"], revenue_data["amount"], color="deepskyblue")
                    ax_1.grid(visible=True)

                    canvas = FigureCanvasTkAgg(figure=fig_1, master=self)
                    canvas.draw()
                    canvas.get_tk_widget().place(x=18, y=119)

                    #Criando um grafico circular

                    fig_2 = Figure(figsize=(2,1.8), facecolor="#D9D9D9")
                    ax_2= fig_2.add_subplot(projection="polar")
                    ax_2.set_facecolor("#D9D9D9")
                    ax_2.bar(x=sales["angles"], height=sales["revenue"], color=sales["colors"])
                    ax_2.set_frame_on(False)
                    ax_2.set_xticks([])
                    ax_2.tick_params(labelsize=2, color="white")
                    ax_2.grid(alpha=0.5)

                    for angle, label, rotation in zip(sales["angles"], sales["products"], sales["rotation"]):
                              ax_2.text(x=angle, y=max(sales["revenue"])+30, s=label, rotation=rotation,ha="center", va="center", color="black", fontsize=8)
                    
                    canvas=FigureCanvasTkAgg(figure=fig_2, master=self)
                    canvas.draw()
                    canvas.get_tk_widget().place(x=350, y=115)

                    #colunas horizontal
                    fig_3 = Figure(figsize=(2, 1.8), facecolor="#D9D9D9")
                    ax_3 = fig_3.add_subplot()

                    # Crie um gráfico de colunas horizontais
                    ax_3.barh(revenue_data["date"], revenue_data["amount"], color="deepskyblue", alpha=0.7)
                    ax_3.tick_params(labelsize=7, colors="black")
                    ax_3.invert_yaxis()  # Inverta o eixo y para que as datas sejam exibidas na ordem correta
                    fig_3.autofmt_xdate()
                    ax_3.grid(visible=True)

                    canvas = FigureCanvasTkAgg(figure=fig_3, master=self)
                    canvas.draw()
                    canvas.get_tk_widget().place(x=350, y=340)

                    table = ttk.Treeview(master=self, columns=table_columns, show="headings")

                    for collum in table_columns:
                              table.heading(column=collum, text=collum)
                              table.column(column=collum, width=70)
                    for row_data in table_data:
                              table.insert(parent="", index="end", values=row_data)
                    
                    style = ttk.Style()
                    style.theme_use("default")
                    style.configure("Treeview", background="#D9D9D9", fieldbackground="#D9D9D9", foreground="black")
                    style.configure("Treeview.Heading", background="#D9D9D9", fieldbackground="#D9D9D9", foreground="black")
                    style.map("Treeview", background=[("selected", "#C7C1C1")])

                    table.place(x=725, y=125, height=370, width=275)

if __name__ == "__main__":
          root = Tk()
          window = AppFrame(root)

          root.geometry("1020x550")
          root.configure(bg = "#444444")
          root.resizable(False, False)
          root.mainloop()

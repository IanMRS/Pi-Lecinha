from tkinter import *

root = Tk() # Cria uma instância da classe Tk(), que representa a janela principal da interface gráfica

class Application():
          def __init__(self): #função para abrir a janela
           self.root = root
           self.tela() #função tela, 
           self.frames_da_tela() #chamar a função frame da tela
           self.widgtes_frame1() #chamar os botões
           root.mainloop() #criar um loop para abrir a janela
          def tela(self): #função para configurar a tela
                    self.root.title("Cadastro de Clientes" ) #Texto da barra superior
                    self.root.configure(background='#444444')
                    self.root.geometry("800x600") #dimensões do começo da janela
                    self.root.resizable(True, True) #Tela responsiva
                    self.root.maxsize(width=1920, height=1800) #definir a largura e altura máximaSELF
                    self.root.minsize(width=600, height=500) #tamanho mínimo
          def frames_da_tela(self):
                    self.frame_1 = Frame(self.root, bd=4, bg= '#045D32', highlightbackground='#ffffff', highlightthickness=1 )
                    #3 formas de interação, os widgets. place, pack e grid
                    self.frame_1.place(relx= 0.02, rely=   0.02, relwidth= 0.96, relheight= 0.46)
                    
                    self.frame_2 = Frame(self.root, bd = 4,bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
                    self.frame_2.place(relx=0.02, rely=0.49, relwidth=0.96, relheight=0.46)
          def widgtes_frame1(self):
                    ###Botão Limpar
                    self.bt_limpar = Button(self.frame_1, text="Limpar")        
                    self.bt_limpar.place(relx=0.2, rely= 0.1, relwidth= 0.1, relheight=0.15)
                    
                    ###Botão buscar
                    self.bt_buscar = Button(self.frame_1, text="Buscar")
                    self.bt_buscar.place(relx=0.3, rely=0.1, relwidth= 0.1, relheight=0.15)
                    
                    ###Botão Novo
                    self.bt_novo = Button(self.frame_1, text="Novo")
                    self.bt_novo.place(relx=0.65, rely=0.1, relwidth= 0.1, relheight=0.15)
                    ###Botão Alterar
                    self.bt_alterar = Button(self.frame_1, text="Alterar")
                    self.bt_alterar.place(relx=0.75, rely=0.1, relwidth=0.1, relheight=0.15)
                    
                    ###Botão Apagar
                    self.bt_apagar = Button(self.frame_1, text="Apagar")
                    self.bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.15)
                    
                    ###Label e entrada dos códigos
                    self.lb_codigo = Label(self.frame_1, text="Código") ###Código de busca
                    self.lb_codigo.place(relx=0.05, rely= 0.05, relwidth=0.1, relheight=0.1)
                    
                    self.codigo_entry = Entry(self.frame_1)
                    self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.1)
                    
                    ###Label e entrada de nome
                    self.lb_nome = Label(self.frame_1, text="Nome")
                    self.lb_nome.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.1)
                    
                    self.nome_entry = Entry(self.frame_1)
                    self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.90, relheight=0.1)
                    
                    ###Label e entrada de telefone
                    self.lb_telefone = Label(self.frame_1, text="Telefone")
                    self.lb_telefone.place(relx=0.05, rely=0.6, relwidth= 0.1, relheight=0.1)
                    
                    self.telefone_entry = Entry(self.frame_1)
                    self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.1)
                    
                    
                    
Application() # Cria uma instância da classe Application, o que inicia a aplicação GUI
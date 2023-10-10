from tkinter import *

root = Tk() # Cria uma instância da classe Tk(), que representa a janela principal da interface gráfica

class Application():
          def __init__(self): #função para abrir a janela
           self.root = root
           self.tela() #função tela, 
           self.frames_da_tela() #chamar a função frame da tela
           root.mainloop() #criar um loop para abrir a janela
          def tela(self): #função para configurar a tela
                    self.root.title("Cadastro de Clientes" ) #Texto da barra superior
                    self.root.configure(background='#ffff5d')
                    self.root.geometry("700x500") #dimensões do começo da janela
                    self.root.resizable(True, True) #Tela responsiva
                    self.root.maxsize(width=900, height=700) #definir a largura e altura máximaSELF
                    self.root.minsize(width=400, height=300) #tamanho mínimo
          def frames_da_tela(self):
                    self.frame_1 = Frame(self.root)
                    #3 formas de interação, os widgets. place, pack e grid
                    self.frame_1.place(relx= 0.02, rely=   0.02, relwidth= 0.9, relheight= 0.5)
                    
Application() # Cria uma instância da classe Application, o que inicia a aplicação GUI
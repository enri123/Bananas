#Esto nos sirve para crear dististas ventanas
import tkinter as tk
from tkinter import  PhotoImage, Canvas
#Esto nos sirve para hacer click detras de nuestra ventana invisible
import ctypes
#Esto nos sirve para ver dode esta nuestro raton en la panalla
import pyautogui
#Esto es un random normal
import random

class Banana:
    #Si no nos indican donde esta la banana, por defecto va a ser en el 0,0
    def __init__(self, scene, x=0, y=0):
            self.scene = scene
            #Imagen default
            self.image = PhotoImage(file='assets/banana.png')
            #Tamaño de la imagen default
            self.image = self.image.subsample(16)
            #Imagen que se pone en el momento en que la imagen default y el cursor hacen contacto
            self.image_bomb = PhotoImage(file='assets/bomb.png')
            self.image_bomb = self.image_bomb.subsample(8)
            #Creamos la imagen
            self.imageRef = scene.canvas.create_image(x,y,image=self.image)
            #De default la imagen no ha explotado
            self.bomb_status = False

    def update(self):
        #Posicion del cursor
        x, y = pyautogui.position()
        #Posicion de las bananas
        ban_x, ban_y = self.scene.canvas.coords(self.imageRef)
        #Distancia entre las bananas y el cursor
        dist = (abs(x-ban_x)+abs(y-ban_y))
        #Conjunto de codigo que ocurre si el cursor entra en contacto con la imagen
        if self.bomb_status:
            #La banana que ha entrado en contacto con el cursor se desplaza aleatoriamente 30 pixeles del cursor (para que no entre en contato mas que una vez)
            self.scene.canvas.move(
                self.imageRef,
                random.choice((-30, 30)),
                random.choice((-30, 30))
            )
            self.scene.canvas.itemconfig(self.imageRef, image=self.image)
            if len(self.bananas) < 20:
                self.bananas = list()
                #Elije aleatoriamente entre los numeros desde el 1 hasta el 10, ambos inclusives y crea ese numero de bananas
                for _ in range(random.randint(1,10)):
                    self.scene.new_banana(
                        random.randint(0, self.scene.screen_width),
                        random.randint(0, self.scene.screen_height)
                        )
            #Hacemos que las explosiones vuelvan a ser bananas 
            self.bomb_status = False 
        #Si la distancia entre el cursor y la banana es de menos de 5 pixeles contamos que ya esta en contacto
        elif dist < 5:
            #Hacemos que las bananas pasen a ser explosiones
            self.scene.canvas.itemconfig(self.imageRef, image=self.image_bomb)
            self.bomb_status = True
        else: 
            #Elije aleatoriamente una de las opciones ofrecidas, en este caso se refiere a la velocidad de las bananas
            numero = random.choice((1,2,5))
            self.scene.canvas.move(
                self.imageRef,
                numero if x > ban_x else -numero,
                numero if y > ban_y else -numero
            )

class Scene:
    def __init__(self, window: tk.Tk):
        self.screen_width = window.winfo_screenwidth()       
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas(
            window,
            #Todo el ancho de la pantalla
            width=self.screen_width,
            #Todo el alto
            height=self.screen_height,
            #Si bordes
            highlightthickness=0,
            #Fondo blanco(Transparente)
            bg='white'
        )
        self.canvas.pack()
        self.bananas = list()

    def update(self):
        for banana in self.bananas:
            banana.update()

    def new_banana(self, x, y):
        #Ponemos un máximo de 20 bananas simultaneamentes
        if len(self.bananas) < 20:
            #Llamamos al constructor de la banana
            banana = Banana(self)
            self.canvas.move(banana.imageRef, x, y)
            self.bananas.append(banana)
        
class Game:
    def __init__(self):
        #Esto nos crea la ventana transparente
        self.window = self.create_window()
        #Esto hace que podamos hacer click detras de la ventana
        self.apply_click_through(self.window)
        self.scene = Scene(self.window)
        
    def update(self):
        self.scene.update()
        self.window.after(20, self.update)

    def create_window(self):

        window = tk.Tk()
        #Siempre encima de las démas
        window.wm_attributes("-topmost", True)
        #Siempre en pantalla completa
        window.attributes("-fullscreen", True)
        window.overrideredirect(True)
        #Transparencia
        window.attributes('-transparentcolor', 'white')
        window.config(bg='white')
        return window

    def apply_click_through(self, window):
        # Constantes API windows
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20

        # Obtener el identificador de ventana (HWND)
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        # Obtener los estilos actuales de la ventana
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        # Establecer nuevo estilo
        style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    
    def start(self):
        self.update()
        self.window.mainloop()

game = Game()
game.scene.new_banana(100,100)
game.start()
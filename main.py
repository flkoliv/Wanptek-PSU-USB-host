#!/usr/bin/python3

from tkinter import Tk, Button, Label
from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont
import pyglet
import customtkinter
from tkdial import Dial
from tkdial import Jogwheel
from tkdial import ImageKnob
from tkdial import Meter
from customtkinter import CTk, CTkImage, CTkLabel
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
import PIL

# On définit une classe qui dérive de la classe Tk (la classe de fenêtre).
class MyWindow(Tk):

    def __init__(self):
        # On appelle le constructeur parent
        super().__init__()

        pyglet.options['win32_gdi_font'] = True
        fontpath = Path(__file__).parent / 'digital-7.ttf'
        pyglet.font.add_file(str(fontpath))

        im = PIL.Image.open("./images/logo_resized.png")
        photo = PIL.ImageTk.PhotoImage(im)
        logo = Label(self, image=photo,background = "black",)
        logo.image = photo  # keep a reference!
        logo.grid(row=1, column=1, sticky='NW')

        slogan = Label(self, text="DC power supply \n  ", background="black", foreground="white",anchor='se', justify='left')
        slogan.grid(row=2, column="1",sticky='NW')

        # On injecte un premier label dans la fenêtre
        voltage = Label(self, background="black", text="24.00", font=tkfont.Font(family='digital-7', size=50), foreground="white")
        voltage.grid(row=3, column=1)
        voltageLabel = Label(self,  background="black", text="V",font=("Arial", 25), foreground="white")
        voltageLabel.grid(row=3, column=2)

        current = Label(self, background="black", text="2.000", font=tkfont.Font(family='digital-7', size=50), foreground="white")
        current.grid(row=4, column=1)
        currentLabel = Label(self,  background="black", text="A",font=("Arial", 25), foreground="white")
        currentLabel.grid(row=4, column=2)
        
        power = Label(self,  background="black", text="  OFF", font=tkfont.Font(family='digital-7', size=50), foreground="white")
        power.grid(row=5, column=1)
        powerLabel = Label(self,  background="black", text="W",font=("Arial", 25), foreground="white")
        powerLabel.grid(row=5, column=2)

        dialVoltage = Dial(self,end=32,radius=30, text_color='white',bg='black',text='V. ',scroll_steps=0.01, unit_length=2, unit_width=2 ) 
        dialVoltage.grid(row=3, column=3)
        dialCurrent = Dial(self,end=10.20,radius=30, text_color='white',bg='black',text='A. ',scroll_steps=0.01, unit_length=2, unit_width=2 ) 
        dialCurrent.grid(row=4, column=3)

        

        # Puis, on injecte un bouton dans la fenêtre. En cas de clic, il est
        # connecté au gestionnaire d'événements do_something.
        
        buttonPower = Button(self, text="Power", command=self.do_something)
        buttonPower.grid(row=6, column=1)
        
        buttonOut = Button(self, text="Out", command=self.do_something)
        buttonOut.grid(row=6, column=2)

        buttonOCP = Button(self, text="OCP", command=self.do_something)
        buttonOCP.grid(row=6, column=3)



        #self.iconbitmap("./images/favicon_resized.bmp",)
        self.iconphoto(False, tk.PhotoImage(file='./images/favicon.png'))
        # On dimensionne la fenêtre (300 pixels de large par 200 de haut).
        self.geometry("300x200")

        self.configure(background="#23272d")

        # On ajoute un titre à la fenêtre
        self.title("Wanptek PSU controller")

    # Le gestionnaire d'événement pour notre bouton.
    def do_something(self):
        print("Button clicked!")


# On crée notre fenêtre et on l'affiche
window = MyWindow()
window.mainloop()
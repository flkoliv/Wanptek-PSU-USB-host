import customtkinter
import tkinter
import PSUModel
import PSUView
import PSUController
import logging
import os

import ctypes

# Identifiant unique pour votre application (format: 'ma_compagnie.mon_app.version')
myappid = 'monentreprise.psu_controller.1.0' 
if os.name == 'nt':ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("PSU controller")
        self.configure(fg_color='#23272d')
        #self.wm_iconbitmap('./images/wanptek.ico')
        #self.iconphoto(True, tkinter.PhotoImage(file='./images/favicon.png'))
        ico = tkinter.PhotoImage(file="./images/favicon.png")
        self.iconphoto(True, ico)
        self._root().iconbitmap("./images/wanptek.ico")
        self.geometry("250x300")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # create a model
        self.model = PSUModel.PSUModel()

        # create a view and place it on the root window
        self.view = PSUView.PsuWindow(self)
        self.view.grid(row=0, column=0, padx=0, pady=0)

        # create a controller
        self.controller = PSUController.PSUController(self.model, self.view)

        # set the controller to view
        self.view.set_controller(self.controller)

    def close_window(self):
        self.view.close_graph_window()
        self.destroy()


FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app = App()
    app.mainloop()

import customtkinter
from PIL import Image
from tkdial import Dial
import time
import pygame


class LCDFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="black")
        customtkinter.FontManager.load_font("./ressources/digital-7.ttf")
        customtkinter.FontManager.load_font("./ressources/Sono-Regular.ttf")

        my_image = customtkinter.CTkImage(light_image=Image.open(
            'images/logo.png'), size=(100, 13))  # WidthxHeight
        self.logoLabel = customtkinter.CTkLabel(
            self, text="", image=my_image, height=13)
        self.logoLabel.grid(row=0, column=0, padx=10,
                            pady=(10, 0), sticky="SW")
        self.sloganLabel = customtkinter.CTkLabel(
            self, text="DC power supply", text_color="#737574",
            font=("Sono-Regular", 10), height=10)
        self.sloganLabel.grid(row=1, column=0, padx=10,
                              pady=(0, 0), sticky="NW")

        self.voltageLabel = customtkinter.CTkLabel(self,
                                                   text="00",
                                                   font=("digital-7", 40),
                                                   text_color="white",
                                                   height=5)
        self.voltageLabel.grid(row=2, column=0, padx=10,
                               pady=(10, 0), sticky="E")
        self.vLabel = customtkinter.CTkLabel(
            self, text="V", font=("Sono-Regular", 20), text_color="#737574")
        self.vLabel.grid(row=2, column=1, padx=10, pady=(10, 0))
        self.cvLabel = customtkinter.CTkLabel(self, text="C. V", font=(
            "Sono-Regular", 8), text_color="black", height=2)
        self.cvLabel.grid(row=3, column=1, padx=0, pady=(0, 0))

        self.currentLabel = customtkinter.CTkLabel(self,
                                                   text="00",
                                                   font=("digital-7", 40),
                                                   text_color="white", )
        self.currentLabel.grid(row=4, column=0, padx=10,
                               pady=(0, 0), sticky="E")
        self.ALabel = customtkinter.CTkLabel(
            self, text=" A", font=("Sono-Regular", 20), text_color="#737574")
        self.ALabel.grid(row=4, column=1, padx=10, pady=(5, 5))
        self.ccLabel = customtkinter.CTkLabel(self, text="C. C", font=(
            "Sono-Regular", 8), text_color="black", height=2)
        self.ccLabel.grid(row=5, column=1, padx=0, pady=(0, 0))

        self.powerLabel = customtkinter.CTkLabel(
            self, text=" OFF", font=("digital-7", 40), text_color="white")
        self.powerLabel.grid(row=6, column=0, padx=10, pady=(0, 0), sticky="E")
        self.WLabel = customtkinter.CTkLabel(
            self, text=" W", font=("Sono-Regular", 20), text_color="#737574")
        self.WLabel.grid(row=6, column=1, padx=10, pady=(5, 5))

        self.OCPLabel = customtkinter.CTkLabel(self, text="OCP", font=(
            "Sono-Regular", 8), text_color="black", height=2)
        self.OCPLabel.grid(row=7, column=0, padx=0, pady=(10, 0), sticky='E')
        self.OUTLabel = customtkinter.CTkLabel(self, text="OUT", font=(
            "Sono-Regular", 8), text_color="black", height=2,)
        self.OUTLabel.grid(row=7, column=1, padx=(
            10, 0), pady=(10, 0), sticky='W')


class KnobFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#23272d")
        self.voltageKnob = Dial(self,
                                bg="#23272d",
                                start=0,
                                end=0,
                                color_gradient=("grey", "white"),
                                scroll_steps=0.01,
                                text_color="white",
                                text="V ",
                                unit_width=3,
                                unit_length=5,
                                radius=25)
        self.voltageKnob.grid(row=0, column=0, padx=0, pady=10, columnspan=2)

        self.currentKnob = Dial(self,
                                bg="#23272d",
                                start=0,
                                end=0,
                                color_gradient=("grey", "white"),
                                scroll_steps=0.01,
                                text_color="white",
                                text="A ",
                                unit_width=3,
                                unit_length=5,
                                radius=25)
        self.currentKnob.grid(row=1, column=0, padx=0, pady=10, columnspan=2)

        self.ledRx = customtkinter.CTkCanvas(self,
                                             width=16,
                                             height=16,
                                             bg="#23272d",
                                             highlightthickness=0,
                                             bd=0)
        self.ledRxCircle = self.ledRx.create_aa_circle(
            8, 8, radius=5, fill="grey20")
        self.ledRx.grid(row=2, column=0, padx=0, pady=0, sticky='E')
        self.RxLabel = customtkinter.CTkLabel(self, text="State", font=(
            "Sono-Regular", 10), text_color="#737574", height=5)
        self.RxLabel.grid(row=2, column=1, padx=10, pady=(0, 0), sticky="W")


class ButtonsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="#23272d")
        self.buttonMenu = customtkinter.CTkButton(
            self, text="Menu", text_color="grey40",
            command=self.openSetupWindow, width=25, fg_color="grey10",
            hover_color="grey25")
        self.buttonMenu.grid(row=0, column=0, padx=2, pady=10)
        self.buttonGraph = customtkinter.CTkButton(
            self, text="Graph", text_color="grey40",
            command=self.openGraphWindow, width=25, fg_color="grey10",
            hover_color="grey25")
        self.buttonGraph.grid(row=0, column=1, padx=2, pady=10)
        self.buttonLock = customtkinter.CTkButton(
            self, text="Lock", text_color="grey40",
            command=self.pushButtonLock, width=25, fg_color="grey10",
            hover_color="grey25")
        self.buttonLock.grid(row=0, column=2, padx=2, pady=10)
        self.buttonOCP = customtkinter.CTkButton(
            self, text="OCP", text_color="grey40",
            command=self.pushButtonOCP, width=25, fg_color="grey10",
            hover_color="grey25")
        self.buttonOCP.grid(row=0, column=3, padx=2, pady=10)
        self.buttonOut = customtkinter.CTkButton(
            self, text="OUT", text_color="grey40",
            command=self.pushButtonOut, width=25, fg_color="grey10",
            hover_color="grey25")
        self.buttonOut.grid(row=0, column=4, padx=2, pady=10)

    def openSetupWindow(self):
        print("openSetupWindow")

    def openGraphWindow(self):
        print("openGraphWindow")

    def pushButtonLock(self):
        self.parent.controller.lock_button_pushed = True
        print("pushButtonLock")

    def pushButtonOCP(self):
        self.parent.controller.ocp_button_pushed = True
        print("pushButtonOCP")

    def pushButtonOut(self):
        self.parent.controller.out_button_pushed = True
        print("pushButtonOut")


class PsuWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.pair = False

        self.configure(fg_color='#23272d')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.LCD_frame = LCDFrame(self)
        self.LCD_frame.grid(row=0,
                            column=0,
                            padx=5,
                            pady=(10, 0),
                            sticky="nsw")

        self.knob_frame = KnobFrame(self)
        self.knob_frame.grid(row=0,
                             column=1,
                             padx=5,
                             pady=(10, 0),
                             sticky="nsw")

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.grid(row=1,
                                column=0,
                                columnspan=2,
                                padx=5,
                                pady=(10, 0))
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('./ressources/censor-beep.wav')

    def set_controller(self, controller):
        self.controller = controller

    def update_display(self,
                       out_on,
                       ocp_on,
                       keyboard_locked,
                       constant_current,
                       alarm,
                       real_voltage,
                       real_current,
                       set_voltage,
                       set_current,
                       max_voltage,
                       max_current):

        self.knob_frame.voltageKnob.configure(end=max_voltage)
        self.knob_frame.currentKnob.configure(end=max_current)
        if not keyboard_locked:
            self.knob_frame.voltageKnob.set(set_voltage)
            self.knob_frame.currentKnob.set(set_current)
            self.knob_frame.voltageKnob.configure(state='disabled',)
            self.knob_frame.currentKnob.configure(state='disabled',)
            self.buttons_frame.buttonLock.configure(text_color="grey40")
        else:
            self.knob_frame.voltageKnob.configure(state='normal',)
            self.knob_frame.currentKnob.configure(state='normal',)
            self.buttons_frame.buttonLock.configure(text_color="white")

        if not alarm:
            if ocp_on:
                self.buttons_frame.buttonOCP.configure(text_color="white")
                self.LCD_frame.OCPLabel.configure(text_color="red")
            else:
                self.buttons_frame.buttonOCP.configure(text_color="grey40")
                self.LCD_frame.OCPLabel.configure(text_color="black")
            if out_on:
                self.buttons_frame.buttonOut.configure(text_color="white")
                self.LCD_frame.OUTLabel.configure(text_color="green")
                self.LCD_frame.voltageLabel.configure(
                    text=('%05.2f' % real_voltage))
                self.LCD_frame.currentLabel.configure(
                    text=('%05.3f' % real_current))
                self.LCD_frame.powerLabel.configure(
                    text=('%05.1f' % (real_current * real_voltage)))
                if constant_current:
                    self.LCD_frame.ccLabel.configure(text_color="red")
                    self.LCD_frame.cvLabel.configure(text_color="black")
                else:
                    self.LCD_frame.ccLabel.configure(text_color="black")
                    self.LCD_frame.cvLabel.configure(text_color="green")
            else:
                self.buttons_frame.buttonOut.configure(text_color="grey40")
                self.LCD_frame.ccLabel.configure(text_color="black")
                self.LCD_frame.cvLabel.configure(text_color="black")
                self.LCD_frame.OUTLabel.configure(text_color="black")
                self.LCD_frame.voltageLabel.configure(
                    text=('%05.2f' % set_voltage))
                self.LCD_frame.currentLabel.configure(
                    text=('%05.3f' % set_current))
                self.LCD_frame.powerLabel.configure(
                    text="OFF")
        else:  # if there is an alarm
            self.LCD_frame.ccLabel.configure(text_color="black")
            self.LCD_frame.cvLabel.configure(text_color="black")
            self.LCD_frame.voltageLabel.configure(
                        text="----")
            self.LCD_frame.powerLabel.configure(
                        text="----")
            if self.pair:
                self.LCD_frame.currentLabel.configure(
                        text="OCP")
                self.sound.play()
                time.sleep(0.3)

            else:
                self.LCD_frame.currentLabel.configure(
                        text="")
                time.sleep(0.3)
            self.pair = not self.pair

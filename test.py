import customtkinter
import tkinter
import logging
from tkdial import Dial
from PIL import Image
from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
from pymodbus import FramerType
import crcmod
import pygame
import serial
import serial.tools.list_ports
from threading import Thread
import time
# from pickle import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# from scipy.interpolate import make_interp_spline


class LCDFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
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
            self, text="DC power supply", text_color="#737574", font=("Sono-Regular", 10), height=10)
        self.sloganLabel.grid(row=1, column=0, padx=10,
                              pady=(0, 0), sticky="NW")

        self.voltageLabel = customtkinter.CTkLabel(self, text=master.realVoltage, font=(
            "digital-7", 40), text_color="white", height=5)
        self.voltageLabel.grid(row=2, column=0, padx=10,
                               pady=(10, 0), sticky="E")
        self.vLabel = customtkinter.CTkLabel(
            self, text="V", font=("Sono-Regular", 20), text_color="#737574")
        self.vLabel.grid(row=2, column=1, padx=10, pady=(10, 0))
        self.cvLabel = customtkinter.CTkLabel(self, text="C. V", font=(
            "Sono-Regular", 8), text_color="black", height=2)
        self.cvLabel.grid(row=3, column=1, padx=0, pady=(0, 0))

        self.currentLabel = customtkinter.CTkLabel(
            self, text=master.realCurrent, font=("digital-7", 40), text_color="white", )
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


class knobFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#23272d")
        self.voltageKnob = Dial(self, bg="#23272d", start=0, end=self.master.maxVoltage, color_gradient=("grey", "white"), scroll_steps=0.01,
                                text_color="white", text="V ", unit_width=3, unit_length=5, radius=25)
        self.voltageKnob.grid(row=0, column=0, padx=0, pady=10, columnspan=2)

        self.currentKnob = Dial(self, bg="#23272d", start=0, end=self.master.maxCurrent, color_gradient=("grey", "white"), scroll_steps=0.01,
                                text_color="white", text="A ", unit_width=3, unit_length=5, radius=25)
        self.currentKnob.grid(row=1, column=0, padx=0, pady=10, columnspan=2)

        self.ledRx = customtkinter.CTkCanvas(
            self, width=16, height=16, bg="#23272d", highlightthickness=0, bd=0)
        self.ledRxCircle = self.ledRx.create_aa_circle(
            8, 8, radius=5, fill="grey20")
        self.ledRx.grid(row=2, column=0, padx=0, pady=0, sticky='E')
        self.RxLabel = customtkinter.CTkLabel(self, text="State", font=(
            "Sono-Regular", 10), text_color="#737574", height=5)
        self.RxLabel.grid(row=2, column=1, padx=10, pady=(0, 0), sticky="W")


class buttonsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="#23272d")
        self.buttonMenu = customtkinter.CTkButton(
            self, text="Menu", text_color="grey40", command=self.openSetupWindow, width=25, fg_color="grey10", hover_color="grey25")
        self.buttonMenu.grid(row=0, column=0, padx=2, pady=10)
        self.buttonGraph = customtkinter.CTkButton(
            self, text="Graph", text_color="grey40", command=self.openGraphWindow, width=25, fg_color="grey10", hover_color="grey25")
        self.buttonGraph.grid(row=0, column=1, padx=2, pady=10)
        self.buttonLock = customtkinter.CTkButton(
            self, text="Lock", text_color="grey40", command=self.pushButtonLock, width=25, fg_color="grey10", hover_color="grey25")
        self.buttonLock.grid(row=0, column=2, padx=2, pady=10)
        self.buttonOCP = customtkinter.CTkButton(
            self, text="OCP", text_color="grey40", command=self.pushButtonOCP, width=25, fg_color="grey10", hover_color="grey25")
        self.buttonOCP.grid(row=0, column=3, padx=2, pady=10)
        self.buttonOut = customtkinter.CTkButton(
            self, text="OUT", text_color="grey40", command=self.pushButtonOut, width=25, fg_color="grey10", hover_color="grey25")
        self.buttonOut.grid(row=0, column=4, padx=2, pady=10)
        self.graphs = {}

    def pushButtonOut(self):
        self.master.powerOutOn = not self.master.powerOutOn
        self.master.writeNewData()

    def pushButtonOCP(self):
        self.master.OCPOn = not self.master.OCPOn
        self.master.writeNewData()

    def pushButtonLock(self):
        self.master.keyboardLocked = not self.master.keyboardLocked
        self.master.writeNewData()

    def openSetupWindow(self):
        self.setup_window = ToplevelWindow(self.master)

    def openGraphWindow(self):
        plt.figure(num='Wanptek DC Power Supply')
        thismanager = plt.get_current_fig_manager()
        img = tkinter.PhotoImage(file='./images/favicon.png')
        thismanager.window.wm_iconbitmap('./images/favicon.png')
        fmt = ticker.FuncFormatter(
            lambda x, pos: time.strftime('%M:%S', time.gmtime(x)))

        ax1 = plt.subplot(3, 1, 1)
        ax1.plot(
            self.master.dataArray[:, 0], self.master.dataArray[:, 1], 'b', label='Voltage (V)')
        ax1.legend(loc="lower left")
        ax1.axhline(y=self.master.setVoltage)
        ax1.xaxis.set_major_formatter(fmt)

        ax2 = plt.subplot(3, 1, 2)
        ax2.plot(
            self.master.dataArray[:, 0], self.master.dataArray[:, 2], 'b', label='Current (A)')
        ax2.legend(loc='lower left')
        ax2.xaxis.set_major_formatter(fmt)

        ax3 = plt.subplot(3, 1, 3)
        ax3.plot(
            self.master.dataArray[:, 0], self.master.dataArray[:, 3], 'b', label='Power (W)')
        ax3.legend(loc='lower left')
        ax3.xaxis.set_major_formatter(fmt)

        plt.tight_layout()      # Sans cette ligne, il y a des chevauchements dans les étiquettes

        while not self.master.killed:
            ax1.clear()
            ax2.clear()
            ax3.clear()

            ax1.plot(
                self.master.dataArray[:, 0],
                self.master.dataArray[:, 1],
                'b',
                label='Voltage (V)')
            ax2.plot(
                self.master.dataArray[:, 0],
                self.master.dataArray[:, 2],
                'g',
                label='Current (A)')
            ax3.plot(
                self.master.dataArray[:, 0], self.master.dataArray[:, 3], 'r', label='Power (W)')
            ax1.grid()
            ax2.grid()
            ax3.grid()
            ax1.xaxis.set_major_formatter(fmt)
            ax2.xaxis.set_major_formatter(fmt)
            ax3.xaxis.set_major_formatter(fmt)
            ax1.set_ylabel("Voltage (V)")
            ax2.set_ylabel("Current (A)")
            ax3.set_ylabel("Power (W)")
            plt.xlabel("time")

            plt.tight_layout()
            plt.draw()
            plt.pause(1)
        plt.close()


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("275x180")
        self.title('Setup')
        self.focus()
        self.grab_set()
        serial_port = serial.tools.list_ports.comports()
        portList = []
        for port in serial_port:
            portList.append(port.device)
        deviceAddressList = []
        for i in range(32):
            deviceAddressList.append(str(i))

        self.optionmenuDeviceAddress = customtkinter.CTkOptionMenu(
            self, values=deviceAddressList)
        self.optionmenuDeviceAddress.set(self.master.deviceAddress)
        self.optionmenuDeviceAddress.grid(
            row=1, column=1, padx=2, pady=5, sticky='E')
        self.deviceAddressLabel = customtkinter.CTkLabel(
            self, text="Device Address ")
        self.deviceAddressLabel.grid(
            row=1, column=0, padx=10, pady=5, sticky='W')
        self.optionmenuSerialPortNumber = customtkinter.CTkOptionMenu(
            self, values=portList)
        self.optionmenuSerialPortNumber.set(self.master.serialPort)
        self.optionmenuSerialPortNumber.grid(
            row=2, column=1, padx=2, pady=5, sticky='E')
        self.SerialPortNumberLabel = customtkinter.CTkLabel(
            self, text="Serial Port ")
        self.SerialPortNumberLabel.grid(
            row=2, column=0, padx=10, pady=5, sticky='W')
        self.optionmenuBaudrate = customtkinter.CTkOptionMenu(
            self, values=['2400', '4800', '9600', '19200'])
        self.optionmenuBaudrate.set(self.master.baudrate)
        self.optionmenuBaudrate.grid(
            row=3, column=1, padx=2, pady=5, sticky='E')
        self.BaudrateLabel = customtkinter.CTkLabel(self, text="Baud rate ")
        self.BaudrateLabel.grid(row=3, column=0, padx=10, pady=5, sticky='W')
        self.saveButton = customtkinter.CTkButton(
            self, text="save", command=self.saveSetup)
        self.saveButton.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def saveSetup(self):
        print(self.master.serialPort)
        self.master.serialPort = self.optionmenuSerialPortNumber.get()
        print(self.master.serialPort)
        self.master.baudrate = int(self.optionmenuBaudrate.get())
        print(self.master.baudrate)
        self.master.deviceAddress = int(self.optionmenuDeviceAddress.get())
        print(self.master.deviceAddress)
        f = open("./param", "wb")
        pickle.dump(self.master.serialPort, f)
        pickle.dump(self.master.baudrate, f)
        pickle.dump(self.master.deviceAddress, f)
        f.close()
        self.master.client.close()
        self.master.connect()
        self.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.powerOutOn = False
        self.OCPOn = False
        self.keyboardLocked = False
        self.endian = "little"
        self.constantCurrent = False
        self.alarm = False
        self.realVoltage = 0
        self.realCurrent = 0
        self.setVoltage = 0
        self.setCurrent = 0
        self.maxVoltage = 10
        self.maxCurrent = 2
        self.pair = True
        self.pair2 = True
        self.pair3 = True
        self.serialPort = ""
        self.baudrate = 2400
        self.deviceAddress = 0x00
        self.killed = False
        self.timeOrigin = time.time()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.dataArray = np.empty([0, 4])

        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('./ressources/censor-beep.wav')

        self.title("PSU controller")
        self.configure(fg_color='#23272d')
        self.wm_iconbitmap('./images/favicon.ico')
        self.iconphoto(False, tkinter.PhotoImage(file='./images/favicon.ico'))
        self.geometry("250x300")
        self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.LCD_frame = LCDFrame(self)
        self.LCD_frame.grid(row=0,
                            column=0,
                            padx=5,
                            pady=(10, 0),
                            sticky="nsw")

        self.knob_frame = knobFrame(self)
        self.knob_frame.grid(row=0,
                             column=1,
                             padx=5,
                             pady=(10, 0),
                             sticky="nsw")
        self.buttons_frame = buttonsFrame(self)
        self.buttons_frame.grid(row=1,
                                column=0,
                                columnspan=2,
                                padx=5,
                                pady=(10, 0))

        try:
            f = open("./param", "rb")
            self.serialPort = pickle.load(f)
            self.baudrate = pickle.load(f)
            self.deviceAddress = pickle.load(f)
            f.close()
        except Exception:
            print('no setup file')

        self.connect()
        self._thread = Thread(target=self.refresh)
        self._thread.daemon = True
        self._thread.start()

    def close_window(self):
        print("close+++++++++++++++++++++")
        self.killed = True
        self.destroy()

    def connect(self):
        try:
            self.client = ModbusClient(
                port=self.serialPort,
                framer=FramerType.RTU,
                baudrate=self.baudrate,
                timeout=1,
                parity="N",)
            self.client.connect()
            self.client.read_holding_registers(
                address=0x00, count=8, slave=self.deviceAddress)

        except Exception:
            print('connection error')
            self.knob_frame.ledRx.itemconfig(
                self.knob_frame.ledRxCircle, fill='red')

    def readData(self):
        try:
            result = self.client.read_holding_registers(
                address=0x00, count=8, slave=self.deviceAddress).encode()
            statusBin = "{:08b}".format(int(result[1:2].hex(), 16))
            if statusBin[-1] == "1":
                self.powerOutOn = True
            else:
                self.powerOutOn = False
            if statusBin[-2] == "1":
                self.OCPOn = True
            else:
                self.OCPOn = False
            if statusBin[-4] == "1":
                self.endian = "big"
            else:
                self.endian = "little"
            if statusBin[-5] == "1":
                self.constantCurrent = True
            else:
                self.constantCurrent = False
            if statusBin[-6] == "1":
                self.alarm = True
            else:
                self.alarm = False

            decimalVoltage = 0.01
            decimalCurrent = 0.001
            voltageBin = "{:08b}".format(int(result[2:3].hex(), 16))
            currentBin = "{:08b}".format(int(result[3:4].hex(), 16))
            if voltageBin[0] == 1:
                decimalVoltage = 0.1
            if currentBin[0] == 1:
                decimalCurrent = 0.01

            self.realVoltage = round(int.from_bytes(
                result[5:7], self.endian)*decimalVoltage, 2)
            self.realCurrent = round(int.from_bytes(
                result[7:9], self.endian)*decimalCurrent, 3)

            self.maxVoltage = round(int.from_bytes(
                result[13:15], self.endian)*decimalVoltage, 2)
            self.maxCurrent = round(int.from_bytes(
                result[15:17], self.endian)*decimalCurrent, 3)

            if not (self.keyboardLocked):
                self.setVoltage = round(int.from_bytes(
                    result[9:11], self.endian)*decimalVoltage, 2)
                self.setCurrent = round(int.from_bytes(
                    result[11:13], self.endian)*decimalCurrent, 3)
            else:
                if self.setVoltage != self.knob_frame.voltageKnob.get():
                    self.setVoltage = self.knob_frame.voltageKnob.get()
                    self.writeData()

                if self.setCurrent != self.knob_frame.currentKnob.get():
                    self.setCurrent = self.knob_frame.currentKnob.get()
                    self.writeData()
        except Exception as inst:
            print(inst)
            self.knob_frame.ledRx.itemconfig(
                self.knob_frame.ledRxCircle, fill='red')

    def writeData(self):
        try:
            b = b'\x00\x10\x00\x00\x00\x03\x06'
            keyboardLocked = self.keyboardLocked
            OCPEnabled = self.OCPOn
            OutputOn = self.powerOutOn
            setVoltage = self.setVoltage
            setCurrent = self.setCurrent

            zero_one_string = "00000"
            if keyboardLocked:
                zero_one_string = zero_one_string+"1"
            else:
                zero_one_string = zero_one_string+"0"
            if OCPEnabled:
                zero_one_string = zero_one_string+"1"
            else:
                zero_one_string = zero_one_string+"0"
            if OutputOn:
                zero_one_string = zero_one_string+"1"
            else:
                zero_one_string = zero_one_string+"0"
            b = b + int(zero_one_string,
                        2).to_bytes((len(zero_one_string) + 7) // 8, 'little')
            b = b+b"\x00"
            setVoltage = int(setVoltage*100)
            b = b+setVoltage.to_bytes(2, 'little')
            setCurrent = int(setCurrent*1000)
            b = b+setCurrent.to_bytes(2, 'little')

            crc16 = crcmod.mkCrcFun(
                0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
            b = b+crc16(b).to_bytes(2, 'little')
            print(b)
            print("----------------------")
            print(self.client.send(b))
            print("----------------------")
        except Exception:
            print('write error')
            self.knob_frame.ledRx.itemconfig(
                self.knob_frame.ledRxCircle, fill='red')

    def refresh(self):
        while True:
            try:
                self.readData()
                if not (self.client.connected):
                    self.knob_frame.ledRx.itemconfig(
                        self.knob_frame.ledRxCircle, fill='red')
                    self.connect()
                    self.LCD_frame.currentLabel.configure(text_color="black")
                    self.LCD_frame.voltageLabel.configure(text_color="black")
                    self.LCD_frame.powerLabel.configure(text_color="black")
                else:
                    if self.alarm:  # if there is an alarm
                        self.LCD_frame.voltageLabel.configure(text="----")
                        self.LCD_frame.currentLabel.configure(text="OCP")
                        self.LCD_frame.powerLabel.configure(text="----")
                        self.LCD_frame.cvLabel.configure(text_color="black")
                        self.LCD_frame.ccLabel.configure(text_color="black")
                        if self.pair:
                            self.LCD_frame.currentLabel.configure(
                                text_color="White")
                            self.sound.play()
                            self.pair = False
                        else:
                            self.LCD_frame.currentLabel.configure(
                                text_color="Black")
                            self.pair = True
                        time.sleep(0.4)
                    else:  # if there is no alarm
                        self.LCD_frame.currentLabel.configure(
                            text_color="white")
                        self.LCD_frame.voltageLabel.configure(
                            text_color="white")
                        self.LCD_frame.powerLabel.configure(text_color="white")
                        if self.pair2:
                            self.knob_frame.ledRx.itemconfig(
                                self.knob_frame.ledRxCircle, fill='grey20')
                            self.pair2 = False
                        else:
                            self.knob_frame.ledRx.itemconfig(
                                self.knob_frame.ledRxCircle, fill='green')
                            self.pair2 = True

                        if self.powerOutOn:  # if out button pushed
                            self.LCD_frame.voltageLabel.configure(
                                text=('%05.2f' % self.realVoltage))
                            self.LCD_frame.currentLabel.configure(
                                text=('%05.3f' % self.realCurrent))
                            self.LCD_frame.powerLabel.configure(
                                text=('%05.1f' % (self.realCurrent
                                                  * self.realVoltage)))
                            self.buttons_frame.buttonOut.configure(
                                text_color='white')
                            self.LCD_frame.OUTLabel.configure(
                                text_color='green')
                            if self.constantCurrent:
                                self.LCD_frame.cvLabel.configure(
                                    text_color="black")
                                self.LCD_frame.ccLabel.configure(
                                    text_color="red")
                            else:
                                self.LCD_frame.cvLabel.configure(
                                    text_color="green")
                                self.LCD_frame.ccLabel.configure(
                                    text_color="black")
                        else:
                            self.LCD_frame.cvLabel.configure(
                                text_color="black")
                            self.LCD_frame.ccLabel.configure(
                                text_color="black")
                            self.LCD_frame.voltageLabel.configure(
                                text=('%05.2f' % self.setVoltage))
                            self.LCD_frame.currentLabel.configure(
                                text=('%05.3f' % self.setCurrent))
                            self.LCD_frame.powerLabel.configure(text="OFF")
                            self.buttons_frame.buttonOut.configure(
                                text_color='grey40')
                            self.LCD_frame.OUTLabel.configure(
                                text_color='black')

                        if self.keyboardLocked:
                            self.buttons_frame.buttonLock.configure(
                                text_color='white')
                            self.knob_frame.voltageKnob.configure(
                                state='normal',)
                            self.knob_frame.currentKnob.configure(
                                state='normal',)
                        else:
                            self.buttons_frame.buttonLock.configure(
                                text_color='grey40')
                            self.knob_frame.voltageKnob.configure(
                                state='disabled',)
                            self.knob_frame.currentKnob.configure(
                                state='disabled',)
                            self.knob_frame.voltageKnob.set(self.setVoltage)
                            self.knob_frame.currentKnob.set(self.setCurrent)

                        if self.OCPOn:
                            self.buttons_frame.buttonOCP.configure(
                                text_color='white')
                            self.LCD_frame.OCPLabel.configure(text_color='red')
                        else:
                            self.buttons_frame.buttonOCP.configure(
                                text_color='grey40')
                            self.LCD_frame.OCPLabel.configure(
                                text_color='black')

                        self.knob_frame.voltageKnob.configure(
                            end=self.maxVoltage,)
                        self.knob_frame.currentKnob.configure(
                            end=self.maxCurrent,)
            except Exception as inst:
                print(inst)

            if time.time()-self.timeOrigin > 600:
                self.dataArray = np.delete(self.dataArray, 0, 0)
            self.dataArray = np.append(self.dataArray, [[
                time.time()-self.timeOrigin,
                self.realVoltage,
                self.realCurrent,
                self.realVoltage*self.realCurrent]], axis=0)

    def writeNewData(self):
        self.writeData()

    def on_closing(self):
        self.killed = True
        print("+++++++++++++++++++++++++++++++++++")


FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

app = App()
app.mainloop()

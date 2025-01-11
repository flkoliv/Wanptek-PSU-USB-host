from pymodbus.client import ModbusSerialClient as ModbusClient
from threading import Thread
from pymodbus import FramerType
import crcmod


class PSUController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._thread = Thread(target=self.refresh)
        self._thread.daemon = True
        self.out_button_pushed = False
        self.ocp_button_pushed = False
        self.lock_button_pushed = False
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.client = ModbusClient(
                port=self.model.serialPort,
                framer=FramerType.RTU,
                baudrate=self.model.baudrate,
                timeout=1,
                parity="N",)
            self.client.connect()
            self.client.read_holding_registers(
                address=0x00, count=8, slave=self.model.deviceAddress)
            self.connected = True
            self._thread.start()
        except Exception as ex:
            print('connection error')
            print(ex)
            self.connected = False
            self.view.set_disabled()

    def refresh(self):
        while True:
            if self.connected:
                self.readData()
                self.view.update_display(
                    self.connected,
                    self.model.out_on,
                    self.model.ocp_on,
                    self.model.keyboard_locked,
                    self.model.constant_current,
                    self.model.alarm,
                    self.model.real_voltage,
                    self.model.real_current,
                    self.model.set_voltage,
                    self.model.set_current,
                    self.model.max_voltage,
                    self.model.max_current
                )
                if self.model.keyboard_locked:
                    if self.model.set_voltage !=\
                            self.view.knob_frame.voltageKnob.get():
                        self.model.set_voltage =\
                            self.view.knob_frame.voltageKnob.get()
                        self.writeData()
                    if self.model.set_current !=\
                            self.view.knob_frame.currentKnob.get():
                        self.model.set_current =\
                            self.view.knob_frame.currentKnob.get()
                        self.writeData()
                if self.out_button_pushed:
                    self.model.out_on = not self.model.out_on
                    self.writeData()
                    self.out_button_pushed = False
                if self.ocp_button_pushed:
                    self.model.ocp_on = not self.model.ocp_on
                    self.writeData()
                    self.ocp_button_pushed = False
                if self.lock_button_pushed:
                    self.model.keyboard_locked = not self.model.keyboard_locked
                    self.writeData()
                    self.lock_button_pushed = False

    def readData(self):
        try:
            result = self.client.read_holding_registers(
                address=0x00, count=8, slave=self.model.deviceAddress).encode()
            statusBin = "{:08b}".format(int(result[1:2].hex(), 16))
            if statusBin[-1] == "1":
                self.model.out_on = True
            else:
                self.model.out_on = False
            if statusBin[-2] == "1":
                self.model.ocp_on = True
            else:
                self.model.ocp_on = False
            if statusBin[-4] == "1":
                self.model.endian = "big"
            else:
                self.model.endian = "little"
            if statusBin[-5] == "1":
                self.model.constant_current = True
            else:
                self.model.constant_current = False
            if statusBin[-6] == "1":
                self.model.alarm = True
            else:
                self.model.alarm = False
            voltage_bin = "{:08b}".format(int(result[2:3].hex(), 16))
            current_bin = "{:08b}".format(int(result[3:4].hex(), 16))
            if voltage_bin[0] == 1:
                decimal_voltage = 0.1
            else:
                decimal_voltage = 0.01
            if current_bin[0] == 1:
                decimal_current = 0.01
            else:
                decimal_current = 0.001
            self.model.real_voltage = round(int.from_bytes(
                result[5:7], self.model.endian)*decimal_voltage, 2)
            self.model.real_current = round(int.from_bytes(
                result[7:9], self.model.endian)*decimal_current, 3)
            self.model.set_voltage = round(int.from_bytes(
                    result[9:11], self.model.endian)*decimal_voltage, 2)
            self.model.set_current = round(int.from_bytes(
                    result[11:13], self.model.endian)*decimal_current, 3)
            self.model.max_voltage = round(int.from_bytes(
                result[13:15], self.model.endian)*decimal_voltage, 2)
            self.model.max_current = round(int.from_bytes(
                result[15:17], self.model.endian)*decimal_current, 3)
            self.model.update_data_array()
            self.connected = True
        except Exception as inst:
            print(inst)
            self.connected = False

    def writeData(self):
        try:
            b = b'\x00\x10\x00\x00\x00\x03\x06'
            keyboardLocked = self.model.keyboard_locked
            print(keyboardLocked)
            OCPEnabled = self.model.ocp_on
            print(OCPEnabled)
            OutputOn = self.model.out_on
            print(OutputOn)
            setVoltage = self.model.set_voltage
            print(setVoltage)
            setCurrent = self.model.set_current
            print(setCurrent)

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
            self.client.send(b)
            self.client._wait_for_data()
        except Exception as ex:
            print(ex)

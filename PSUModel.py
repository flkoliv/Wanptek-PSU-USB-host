import pickle
import time
import numpy as np


class PSUModel:
    """Power supply model
    """
    def __init__(self):
        """initiate to default values, awaiting an update
        """
        self.out_on = False
        self.ocp_on = False
        self.keyboard_locked = False
        self.endian = "little"
        self.constant_current = False
        self.alarm = False
        self.real_voltage = 0
        self.real_current = 0
        self.set_voltage = 0
        self.set_current = 0
        self.max_voltage = 0
        self.max_current = 0
        self.data_array = np.empty([0, 4])
        self.time_origin = time.time()

        try:
            f = open("./param", "rb")
            self.serialPort = pickle.load(f)
            self.baudrate = pickle.load(f)
            self.deviceAddress = pickle.load(f)
            f.close()
        except Exception:
            print('no setup file')

    def update_data_array(self):
        """save last 10 minutes of voltage, current
           and power datas in a numpy array
        """
        if time.time()-self.time_origin > 600:
            self.data_array = np.delete(self.data_array, 0, 0)
        self.data_array = np.append(self.data_array, [[
            time.time()-self.time_origin,
            self.real_voltage,
            self.real_current,
            self.real_voltage*self.real_current]], axis=0)

    def update_values(self, output_on, ocp_on, keyboard_locked, endian,
                      constant_current, alarm_triggered, real_voltage,
                      real_current, set_voltage, set_current, max_voltage,
                      max_current):
        """update all variables with current values

        Args:
            output_on (bool): output on or off
            ocp_on (bool): OCP on or off
            keyboard_locked (bool): keyboard locked or not
            endian (str): "little" or "big"
            constant_current (bool): is CC light on or not
            alarm_triggered (bool): is alarm triggered or not
            real_voltage (float): real output voltage
            real_current (float): real output current
            set_voltage (float): requested voltage
            set_current (float): requested current
            max_voltage (float): maximum supported voltage
            max_current (float): maximum supported current
        """
        self.output_on = output_on
        self.ocp_on = ocp_on
        self.keyboard_locked = keyboard_locked
        self.endian = endian
        self.constant_current = constant_current
        self.alarm_triggered = alarm_triggered
        self.real_voltage = real_voltage
        self.real_current = real_current
        self.set_voltage = set_voltage
        self.set_current = set_current
        self.max_voltage = max_voltage
        self.max_current = max_current

    def is_output_on(self):
        """getter output ON

        Returns:
            bool: True if output ON, otherwise False
        """
        return self.out_on

    def is_ocp_on(self):
        """getter OCP On

        Returns:
            bool: True if OCP ON, otherwise False
        """
        return self.ocp_on

    def is_keyboard_locked(self):
        """getter keyboard locked

        Returns:
            bool: True if keyboard locked, otherwise False
        """
        return self.keyboard_locked

    def get_endian(self):
        """getter endian type for modbus com

        Returns:
            str: "little" or "big"
        """
        return self.endian

    def is_constant_current(self):
        """getter constant current

        Returns:
            bool: True if constant current, otherwise False
        """
        return self.constant_current

    def is_alarm_triggered(self):
        """getter alarm triggered

        Returns:
            bool: True if alarm triggered, otherwise False
        """
        return self.alarm_triggered

    def get_real_voltage(self):
        """getter real voltage

        Returns:
            float: output voltage
        """
        return self.real_voltage

    def get_real_current(self):
        """getter real current

        Returns:
            float: output current
        """
        return self.real_current

    def get_real_power(self):
        """getter real power

        Returns:
            float: output power (P=UI)
        """
        return (self.real_voltage * self.real_current)

    def get_set_voltage(self):
        """getter set voltage

        Returns:
            float: requested voltage
        """
        return self.set_voltage

    def get_set_current(self):
        """getter set current

        Returns:
            float: requested current
        """
        return self.set_current

    def get_max_voltage(self):
        """getter maximum voltage

        Returns:
            float: maximum supported voltage
        """
        return self.max_voltage

    def get_max_current(self):
        """getter maximum current

        Returns:
            float: maximum supported current
        """
        return self.max_current

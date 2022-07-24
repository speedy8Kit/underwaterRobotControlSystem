import numpy as np


class Limiter(object):

    def __init__(self, signal_gain_max: float, signal_max: float):
        self.signal_max = signal_max
        self.signal_gain_max = signal_gain_max
        self.value_previous = 0

    def limitationSignal(self, control_signal, time_step) -> float:
        if control_signal > self.signal_max:
            value = self.signal_max
        elif control_signal < -self.signal_max:
            value = -self.signal_max
        else:
            value = control_signal

        error = (value - self.value_previous)
        if np.abs(error) > self.signal_gain_max * time_step:
            if error > 0:
                value = self.value_previous + self.signal_gain_max * time_step
            else:
                value = self.value_previous - self.signal_gain_max * time_step

        self.value_previous = value
        return value


class PID_Regulator(object):

    def __init__(self, cof_p=1.0, cof_i=0.0, cof_d=0.0):
        self.cof_p = cof_p
        self.cof_i = cof_i
        self.cof_d = cof_d
        self.__sum_last_signal = 0
        self.__last_signal = 0

    def zeroing(self):
        self.__sum_last_signal = 0
        self.__last_signal = 0

    def regulate(self, signal: float, time_step: float) -> float:
        proportional_component = signal * self.cof_p

        delta_err = signal - self.__last_signal
        differential_component = (delta_err / time_step) * self.cof_d
        self.__sum_last_signal += self.cof_i * time_step * signal
        integral_component = self.__sum_last_signal
        control_signal = proportional_component + differential_component + integral_component
        self.__last_signal = control_signal

        # if self.limiter is not None:
        #     value = self.limiter.limitationSignal(control_signal, time_step)
        # else:
        #     value = control_signal

        return control_signal

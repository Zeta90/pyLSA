# from math import e
# from math import sqrt
import math
import array as arr
import numpy as np


class pyLSA:
    def __init__(self):
        #   Transfer Function
        self.sys_Wn = 0
        self.sys_Zeta = 0
        self.sys_K = 0

        #   SYSTEM CHECKS
        self.isValidTF = False

        #   TIME DELTA
        self.delta_t = 0

        #   SIMULATION PARAETERS
        self.sim_time = []
        self.sim_discretized_u_signal = []
        self.discretized_y_response = []
        self.step_input = []

    def TransferFunction_Standard(self, Wn, Zeta, K):
        if Wn <= 0 or K <= 0 or Zeta >= 1 or Zeta <= 0:
            return self.InvalidTF()
        else:
            self.sys_Wn = Wn
            self.sys_Zeta = Zeta
            self.sys_K = K
            self.isValidTF = True

    def TransferFunction_ByCoeffs(self, num, den):
        if len(den) != 3:
            return self.InvalidTF()
        elif den[0] != 0:
            S2_gain = den[0]
            sys_Wn = sqrt(den[2]) / S2_gain
            sys_Zeta = den[1] / (2 * sys_Wn * S2_gain)
            sys_K = num / (sys_Wn ^ 2 * S2_gain)
        else:
            return self.InvalidTF()
        isValidTF = True
        return self.InvalidTF()

    def SecondOrderStepResponse(self, u, t):
        damping = math.sqrt(1 - self.sys_Zeta ** 2)
        so_step_response = u - u * (
            (math.e ** (-self.sys_Zeta * self.sys_Wn * t))
            * (
                math.cos(self.sys_Wn * damping * t)
                + (self.sys_Zeta / damping) * math.sin(self.sys_Wn * damping * t)
            )
        )
        return so_step_response

    def LinearSimulation(self, inputs, time, delta_time):
        if isValidTF == True:
            if not (time[0] >= time[1]):
                self.sim_time = time
                self.sim_discretized_u_signal = inputs
                self.delta_t = delta_time
                self.InputConvolution()
            else:
                return 1
        else:
            return 1

    def LinearSimulationStepByStep(self, inputs, delta_time):
        u1 = 0
        u0 = 0
        u = 0

        #print("AAA -> " + str(inputs))
        #print("_AT -> " + str(delta_time))
        
        input_n = len(self.step_input)

        if (input_n == 2000):
            del self.step_input[0]

        self.step_input.append(inputs)

        input_n = len(self.step_input)

        step_output = 0

        for i in range(input_n):
            u1 = self.step_input[i]
            u = u1

            if i > 0:
                u0 = self.step_input[i - 1]
                if u1 != u0:
                    u = u1 - u0
                    delta_t_sbs = (input_n - i) * delta_time
                    step_output += self.SecondOrderStepResponse(u, delta_t_sbs)
                else:
                    step_output += 0
            else:
                delta_t_sbs = (input_n - i) * delta_time
                step_output += self.SecondOrderStepResponse(u, delta_t_sbs)
        return step_output

    def InputConvolution(self):
        simulation = sim_time[1] - sim_time[0]
        n_iterations = 100
        y0 = []
        y0_tmp = []

        for i in range(n_iterations):
            u = 0
            u1 = self.sim_discretized_u_signal[i]
            u = u1

            if i > 0:
                u0 = self.sim_discretized_u_signal[i - 1]
                if u1 != u0:
                    u = u1 - u0
                    for j in range(n_iterations):
                        if j > 1:
                            y0_tmp.append(0)
                        else:
                            t = (j - i) * self.delta_t
                            y0_tmp.append(self.SecondOrderStepResponse(u, t))
                else:
                    for j in range(i, n_iterations):
                        y0_tmp.append(0)
            else:
                for j in range(n_iterations):
                    t = (j - i) * self.delta_t
                    y0_tmp.append(self.SecondOrderStepResponse(u, t))

            y0.append(y0_tmp)
            y0_tmp.clear
        self.discretized_y_response = self.ColumnOutputReader(y0, n_iterations)

    def ColumnOutputReader(self, y0, n_iterations):
        y = arr.array()
        col_sum = 0
        for i in range(n_iterations):
            for j in range(n_iterations):
                col_sum += y0[i][j]
        y.append(col_sum)
        col_sum = 0
        return y

    def GetOutputResponse(self):
        return self.discretized_y_response()

    def InvalidTF(self):
        sys_Wn = 0
        sys_Zeta = 0
        sys_K = 0
        self.isValidTF = False
        return 0

    def PlotResponse(self):
        time_positions = len(self.discretized_y_response)

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(t, s1, t, s2)
        axs[0].set_xlim(0, 2)
        axs[0].set_xlabel("time")
        axs[0].set_ylabel("s1 and s2")
        axs[0].grid(True)

        cxy, f = axs[1].cohere(s1, s2, 256, 1.0 / dt)
        axs[1].set_yla
        bel("coherence")

        fig.tight_layout()
        plt.show()

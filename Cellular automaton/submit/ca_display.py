import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
from matplotlib import style
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from style_constants import *

matplotlib.use("TkAgg")
style.use("ggplot")

f = Figure(figsize=(4.4, 4.4), dpi=100)
f.patch.set_facecolor(BG_COLOR)
ax = f.add_subplot(111)


def animate(i):
    frame = CAFrame.ca_frame
    ca = frame.automaton

    if ca is not None:
        z = ca.automaton / 3

        ax.clear()
        c = ax.pcolormesh(z, cmap=CAFrame.color_map, vmin=0, vmax=1)

        if frame.run:
            if frame.steps_counter % 2:
                ca.move_all()

            else:
                ca.update_states()
            frame.steps_counter += 1
            frame.update_footer()


class CAFrame(tk.Frame):
    """
    Cellular Aurtomaton Frame class.
    Derives from tk.Frame and manages the automaton display.
    """

    color_map = ListedColormap([BG_COLOR, BLUE, RED])
    ca_frame = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        CAFrame.ca_frame = self

        self.params = dict()
        self.run = False
        self.automaton = None

        self.header = tk.StringVar()
        self.infected_s = tk.StringVar()
        self.steps_counter = 0
        self.generation_s = tk.StringVar()

        self.header.set("Error.\nValues must be set before entering this page.")
        self.infected_s.set("infected: 0 (0%)")
        self.generation_s.set("generation: 0")

        header_label = tk.Label(self, textvariable=self.header, font=SMALL_FONT, bg=BG_COLOR)
        header_label.pack(pady=10, padx=10)

        stats_frame = tk.Frame(self, bg=BG_COLOR)
        stats_frame.pack()

        buttons_frame = tk.Frame(self, bg=BG_COLOR)
        buttons_frame.pack()

        generation_label = tk.Label(stats_frame, textvariable=self.generation_s,
                                    font=SMALL_FONT, bg=BG_COLOR)
        infected_label = tk.Label(stats_frame, textvariable=self.infected_s,
                                  font=SMALL_FONT, bg=BG_COLOR)

        button1 = ttk.Button(buttons_frame, text="run", command=lambda: CAFrame.run_animation())
        button2 = ttk.Button(buttons_frame, text="step", command=lambda: self.step())
        button3 = ttk.Button(buttons_frame, text="stop", command=lambda: CAFrame.stop_animation())

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        generation_label.pack(side='left')
        infected_label.pack(side='left')

        button1.pack(side='left', pady=10)
        button2.pack(side='left', pady=10)
        button3.pack(side='left', pady=10)

    def _initialize(self):
        header_format = "nxm:{0}x{1}\t{2} creatures\tP={3}\tK={4}"
        self.header.set(header_format.format(int(self.params['n']), int(self.params['m']),
                                             int(self.params['num']), self.params['p'],
                                             int(self.params['k'])))
        self.update_footer()

    def step(self):
        if self.automaton:
            self.steps_counter += 2

            self.automaton.move_all()
            self.automaton.update_states()

            self.update_footer()

    def update_footer(self):
        if self.automaton:
            self.generation_s.set("generation: " + str(int(self.steps_counter / 2)) + ", ")
            infected = self.automaton.infected_count
            p = (infected / self.params["num"]) * 100
            self.infected_s.set("infected: " + str(infected) + "(" + str(round(p, 2)) + "%)")

    def add_automaton(self, a):
        self.automaton = a
        self._initialize()

    @staticmethod
    def run_animation():
        CAFrame.ca_frame.run = True

    @staticmethod
    def stop_animation():
        CAFrame.ca_frame.run = False


def submit(entries, controller):
    import cellular_automaton as ca
    params = dict()
    try:
        for key in entries:
            params[key] = float(entries[key].get())
        errors = ca.parameters_check(**params)
        if len(errors) > 0:
            errors_string = "\n".join(errors)
            messagebox.showerror("Error", "\tInvalid Parameters!\n" + errors_string)
            return
    except ValueError:
        messagebox.showerror("Error", "Parameters should only be integers or floats.")
        return

    # parameters are valid
    automaton = ca.CellularAutomaton(int(params['n']), int(params['m']),
                                     params['p'], int(params['k']))
    automaton.add_organisms(int(params['num']))

    CAFrame.ca_frame.params = params
    CAFrame.ca_frame.add_automaton(automaton)
    controller.show_frame(CAFrame)

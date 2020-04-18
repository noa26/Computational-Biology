import ca_display
import tkinter as tk
import matplotlib.animation as animation
from ca_display import CAFrame
from tkinter import ttk
from tkinter import messagebox
from style_constants import *


class CellularAutomatonApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("600x600")
        self.wm_title("Cellular Automaton")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = CAFrame(container, self)
        self.frames[CAFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.entries = dict()

        home_label = tk.Label(self, text="Home", font=LARGE_FONT, bg=BG_COLOR)
        home_label.pack(pady=20, padx=10)

        form_frame = tk.Frame(self, bg=BG_COLOR)
        form_frame.pack(pady=10)
        self.add_form(form_frame, self.entries)

        button3 = ttk.Button(self, text="submit", command=lambda: submit(self.entries, controller))
        button3.pack(pady=10)

    @staticmethod
    def add_form(container, entries: dict):

        label_params = {'column': 0, 'padx': 10, 'sticky': 'E'}
        entry_params = {'column': 1, 'sticky': 'N', 'columnspan': 3}

        dimensions_label = tk.Label(container, text="Dimensions (n x m): ", font=SMALL_FONT, bg=BG_COLOR)
        n_entry = ttk.Entry(container, width=10)
        n_entry.insert(0, "100")
        m_entry = ttk.Entry(container, width=10)
        m_entry.insert(0, "100")
        entries['n'] = n_entry
        entries['m'] = m_entry

        dimensions_label.grid(row=1, **label_params)
        n_entry.grid(row=1, column=1, sticky="N")
        tk.Label(container, text="x", font=SMALL_FONT, bg=BG_COLOR).grid(row=1, column=2)
        m_entry.grid(row=1, column=3, sticky="N")

        num_label = tk.Label(container, text="Number Of Organisms (N): ", font=SMALL_FONT, bg=BG_COLOR)
        num_entry = ttk.Entry(container, width=10)
        num_entry.insert(0, "200")
        entries['num'] = num_entry
        num_label.grid(row=2, **label_params)
        num_entry.grid(row=2, **entry_params)

        p_label = tk.Label(container, text="Contagion Probability (P): ", font=SMALL_FONT, bg=BG_COLOR)
        p_entry = ttk.Entry(container, width=10)
        p_entry.insert(0, "0.5")
        entries["p"] = p_entry
        p_label.grid(row=3, **label_params)
        p_entry.grid(row=3, **entry_params)

        k_label = tk.Label(container, text="Isolation Level (K): ", font=SMALL_FONT, bg=BG_COLOR)
        k_entry = ttk.Entry(container, width=10)
        k_entry.insert(0, "0")
        entries['k'] = k_entry
        k_label.grid(row=4, **label_params)
        k_entry.grid(row=4, **entry_params)


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


if __name__ == "__main__":
    app = CellularAutomatonApp()
    ani = animation.FuncAnimation(ca_display.f, ca_display.animate, interval=200)
    app.mainloop()

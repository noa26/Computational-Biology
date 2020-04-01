from tkinter import*


class Display:

    def __init__(self):
        self.window = Tk()
        self.size = '700x500'
        self.window.title('Computational Biology - Ex1')
        self.window.geometry(self.size)
        self.components = []

    def start_animation(self):
        """
        removes all prior components and starts the animation
        """
        pass

    def menu(self):
        """
        gets two inputs, M and N
        and a start button.
        """

        label = Label(self.window, text="menu bar")
        label.pack()
        self.components.append(label)
        self.window.mainloop()

    @staticmethod
    def remove_components(components):
        for component in components:
            component.destroy()


import time


d = Display()
d.menu()
time.sleep(5)
Display.remove_components(d.components)

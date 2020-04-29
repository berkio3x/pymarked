import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Separator
class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        #self.hi_there.pa(side="top")

        #self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=self.master.destroy)
        #self.quit.pack(side="bottom")
        ScrolledText(self).grid(row=1, column =0)
        Separator(self, orient='vertical').grid(row=0, column=1, sticky='ns')
        ScrolledText(self).grid(row=1, column =2)
    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()


import tkinter as tk
from tkinter.ttk import Separator


from tkinter.scrolledtext import ScrolledText

    


class ReactiveTextEntry(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
	
    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result	

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        entry = ReactiveTextEntry(self)
        entry.grid(row=1, column =0)
        entry.bind('<<TextModified>>', self.onModification)
        Separator(self, orient='vertical').grid(row=0, column=1, sticky='ns')
        self.preview = ScrolledText(self)
        self.preview.grid(row=1, column =2)

    def onModification(self, event):
        chars = event.widget.get("1.0", tk.END)
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, chars)


    
root = tk.Tk()
app = Application(master=root)
app.mainloop()


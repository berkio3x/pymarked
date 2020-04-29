import tkinter as tk
from tkinter.ttk import Separator
from enum import Enum

from tkinter.scrolledtext import ScrolledText

class TokenType(Enum):
    h1 = 0
    h2 = 1
    h3 = 2
    h4 = 3
    h5 = 4
    h6 = 5
    LI = 6
    bullet = 7  
    space = 8
    NEWLINE = 9

class Lex:
    def __init__(self, source):
        self.source = source 
        self.current_idx = 0
        self.token_start = 0
        self.token_end = 0 
        self.tokens = []

    def make_token(self, type, start_idx=None, end_idx =None):
        
        start_idx = start_idx or self.current_idx
        end_idx = end_idx or self.current_idx

        return {
                'type':type,
                'start_idx':start_idx,
                'end_idx':end_idx,
               }
    
    def is_end(self):
        return self.current_idx >= len(self.source)

    def emit_token(self, type):
        token = self.make_token(type, self.token_start, self.token_end) 
        self.tokens.append(token)

    def begin_token(self):
        self.token_start = self.current_idx
    
    def commit_token(self, type):
        self.token_end = self.current_idx
        self.emit_token(type)


    def peek(self):
        if not self.is_end():    
            return self.source[self.current_idx]
   
    def consume(self):
        if not self.is_end():
            self.current_idx += 1
            return self.source[self.current_idx]

    def tokenize(self):
        while self.current_idx < len(self.source) - 1:
            c = self.peek()
            if c == '\n':
                self.emit_token(TokenType.NEWLINE)
            if c == '*':
                self.consume()  
                self.begin_token()
                while(self.peek() and self.peek() != '\n'):
                    self.consume()
                self.commit_token(TokenType.LI)
            else: self.consume()
        return self.tokens        




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


def highlight( tokens, source):
   
    markdown = ''
    for t in tokens:
        if t['type'] == TokenType.LI:
            markdown += '•' + '' + source[t['start_idx']:t['end_idx']]
        if t['type'] == TokenType.NEWLINE:
            markdown += '\n'
    return markdown


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
        L = Lex(chars)        
        t = L.tokenize()
        highlighted = highlight(t,chars)
        self.preview.insert(tk.END, highlighted)


    
root = tk.Tk()
app = Application(master=root)
app.mainloop()


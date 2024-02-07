import customtkinter as tk

class Terminal:
    def __init__(self, tab):
        self.tab = tab
        self.textbox = tk.CTkTextbox(tab,state="disabled")
        self.textbox.pack(fill="both", expand=True)
        self.linesPrinted = 0
        
    def printGUI(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text)
        self.textbox.see("end")
        
        #delete first line if more than 100 lines are printed
        if self.linesPrinted > 100:
            self.textbox.delete("1.0", "2.0")
            self.linesPrinted -= 1
        
        
        self.linesPrinted += 1
        self.textbox.configure(state="disabled")
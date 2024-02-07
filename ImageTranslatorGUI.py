
import customtkinter
import Scripts
import os
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class MangaTranslatorGUI(Scripts.Tk):
    def __init__(self):
        super().__init__()
        self.title("MangaTranslator")
        appHeight = 1000
        appWidth = 800
        self.geometry(f"{appHeight}x{appWidth}")
        self.resizable(True, True)
        
        self.columnconfigure(0, weight=1,minsize=appWidth/2)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        
        #drag and drop section
        dragAndDropFrame = customtkinter.CTkFrame(self, border_width=0,corner_radius=0,fg_color="transparent")
        self.dragAndDrop = Scripts.DND(dragAndDropFrame,self.on_file_select)
        dragAndDropFrame.grid(row=0, column=0, sticky="nsew",rowspan=2)
        
        #Input Output Section
        inputOutputFrame = customtkinter.CTkFrame(self, width=appWidth/4, border_width=0,corner_radius=0, height=appHeight/6)
        inputOutputFrame.grid(row=0, column=1, sticky="nsew")
        
        self.InputOutput = Scripts.IO(inputOutputFrame,self.dragAndDrop,self.on_file_select)
        
        
        #OPTIONS SECTION
        optionsFrame = customtkinter.CTkFrame(self, border_width=0,corner_radius=0,width=appWidth/4)
        optionsFrame.grid(row=1, column=1, sticky="nsew")
        self.tabView = customtkinter.CTkTabview(optionsFrame)
        self.tabView.pack(fill="both", expand=True)
        self.tabView.add("General")
        self.tabView.add("Advanced")
        self.tabView.add("Misc")
        self.tabView.add("Terminal")
        
        self.generalSettings = Scripts.General(self.tabView.tab("General"))
        self.advancedSettings = Scripts.Advanced(self.tabView.tab("Advanced"))
        self.miscSettings = Scripts.Misc(self.tabView.tab("Misc"))
        self.terminal = Scripts.Terminal(self.tabView.tab("Terminal"))
        self.translator = Scripts.Translator(self.on_translation_complete, self.terminal)
    
    def on_close(self):
        print("Closing")
        self.InputOutput.save_settings()
        self.generalSettings.save_settings()
        #clear temp folder
        temp_path = self.dragAndDrop.temp_path
        for filename in os.listdir(temp_path):
            file_path = os.path.join(temp_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        self.destroy()
        
    def on_translation_complete(self, image):
        if image is not None:
            self.dragAndDrop.update_image(image)
        self.dragAndDrop.handle_next()
        
        
    def on_file_select(self, filename):
        translatorDirectory, outputFolder = self.InputOutput.get_intput_output()
        settings = self.generalSettings.get_settings()
        #settings.update(self.advancedSettings.get_settings())
        #settings.update(self.miscSettings.get_settings())
        settings.update({'dest': outputFolder})
        self.tabView.set("Terminal")
        self.translator.start_translate(filename, translatorDirectory, settings)

if __name__ == "__main__":
    root = MangaTranslatorGUI()
    root.protocol("WM_DELETE_WINDOW", root.on_close)
    root.mainloop()
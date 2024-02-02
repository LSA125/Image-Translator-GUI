import customtkinter
from customtkinter import filedialog
import os
import shelve
from PIL import Image
class IO:
    def __init__(self, inputOutputFrame,dnd,callback=lambda:None):
        self.dnd = dnd
        inputOutputFrame.columnconfigure((0,1), weight=1)
        inputOutputFrame.rowconfigure((0,1,2,3), weight=1)
        
        translatorButton = customtkinter.CTkButton(
            inputOutputFrame,
            text="Translator directory",
            command=self.get_translator_directory,
        )
        self.translatorEntry = customtkinter.CTkEntry(inputOutputFrame)
        outputButton = customtkinter.CTkButton(
            inputOutputFrame,
            text="Output Directory",
            command=self.get_output_directory
            
        )
        self.outputEntry = customtkinter.CTkEntry(inputOutputFrame)
        selectFileButton = customtkinter.CTkButton(
            inputOutputFrame,
            text="Select Image",
            command=self.get_file,
        )
        selectFolderButton = customtkinter.CTkButton(
            inputOutputFrame,
            text="Select Folder",
            command=self.get_image_folder,
        )
        translatorButton.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.translatorEntry.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        outputButton.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.outputEntry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        selectFileButton.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        selectFolderButton.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.callback = callback
        self.load_settings()
        
    def get_intput_output(self):
        return self.translatorEntry.get(), self.outputEntry.get()
        
    def get_translator_directory(self):
        filename = filedialog.askdirectory(title="Select a folder")
        self.translatorEntry.delete(0, customtkinter.END)
        self.translatorEntry.insert(0, filename)
    
    def get_output_directory(self):
        filename = filedialog.askdirectory(title="Select a folder")
        self.outputEntry.delete(0, customtkinter.END)
        self.outputEntry.insert(0, filename)

    def get_file(self):
        filetypes = [("Image Files", ".png .jpg .jpeg .bmp .webp"),("All Files", "*.*")]
        filename = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        self.dnd.update_image(filename)
        self.callback(filename)
        
    def get_image_folder(self):
        filename = filedialog.askdirectory(title="Select a folder")
        self.dropImagePath = filename
        first_image_file = self.get_first_image_in_folder(filename)
        if(first_image_file): 
            image = Image.open(first_image_file)
            self.dnd.update_image(image)
            self.callback(filename)
            image.close()

    def get_first_image_in_folder(self, folder):
        all_files_recursive = sum([[os.path.join(root, f) for f in files] for root, dirs, files in os.walk(folder)], [])
        def is_an_image(fpath): 
            return os.path.splitext(fpath)[-1] in ('.png','.jpg','.jpeg','.bmp','.webp')
        # Take the first matching result. Note: throws StopIteration if not found
        return next(filter(is_an_image, all_files_recursive))
    
    def save_settings(self):
        shelf = shelve.open('settings')
        shelf['translatorDirectory'] = self.translatorEntry.get()
        shelf['output'] = self.outputEntry.get()
        shelf.close()
        
    def load_settings(self):
        shelf = shelve.open('settings')
        if 'translatorDirectory' in shelf:
            print(shelf['translatorDirectory'])
            self.translatorEntry.insert(0, shelf['translatorDirectory'])
        else:
            self.translatorEntry.insert(0, '')
        if 'output' in shelf:
            self.outputEntry.insert(0, shelf['output'])
        else:
            self.outputEntry.insert(0, '')
            
        shelf.close()
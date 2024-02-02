import os
import customtkinter
from tkinterdnd2 import DND_FILES
from PIL import Image
class DND:
    def __init__(self,imageFrame, callback=lambda: None):
        #grab the image file from parent directory
        
        self.images_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Images")
        self.temp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Temp")
        self.imageFrame = imageFrame
        
        self.imageFrame.columnconfigure(0, weight=1)
        self.imageFrame.rowconfigure(0, weight=1)
        
        self.Image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(self.images_path, "image_icon_light.png")),
                                                                   light_image=Image.open(os.path.join(self.images_path, "image_icon_dark.png")),
                                                                   size=(200, 200))
        self.leftButton = customtkinter.CTkButton(self.imageFrame, text="<", command=self.cycleLeft)
        self.rightButton = customtkinter.CTkButton(self.imageFrame, text=">", command=self.cycleRight)
        self.trashButton = customtkinter.CTkButton(self.imageFrame, text="Delete Session", command=self.handle_next)
        self.saveButton = customtkinter.CTkButton(self.imageFrame, text="Save Session", command=self.handle_next)
        self.imageEntry = customtkinter.CTkLabel(
            self.imageFrame,
            fg_color="transparent", text="", image=self.Image,
        )
        self.imageEntry.grid(row=0, column=0, sticky="nsew") #columnspan=3, padx=10, pady=10)
        self.imageEntry.drop_target_register(DND_FILES)
        self.imageEntry.dnd_bind("<<Drop>>", self.drop)
        self.callback = callback
        
        self.toTranslate = []
    
    def handle_next(self):
        if len(self.toTranslate) > 0:
            print("directories to translate: " + str(len(self.toTranslate)))
            self.handle_drop(self.toTranslate.pop(0))
    
    def drop(self, event):
        data = event.data.split(" ")
        self.toTranslate.extend(data)
        self.handle_next()
    
    def cycleLeft(self):
        print("left")
        
    def cycleRight(self):
        print("right")
        
    def handle_drop(self, str):
        self.input = str.strip(r'{} ')
        print("handling drop: ", self.input)
        if(os.path.isdir(self.input)): 
            try:
                filename = self.get_first_image_in_folder(self.input)
                image = Image.open(filename)
                self.update_image(image)
                self.callback(self.input)
                image.close()
            except StopIteration:
                self.imageLabel.configure(text="No image found in folder")
        elif(os.path.isfile(self.input)):
            image = Image.open(self.input)
            
            #some drag and drop images delete themselves before they can be translated, idk why
            #get file name
            filename = os.path.basename(self.input)
            save_path = os.path.join(self.temp_path, filename)
            if os.path.exists(save_path):
                os.remove(save_path)
            image.save(save_path)
            self.callback(save_path)
            
    def update_image(self,image):
        width, height = image.size
        
        def scale(width, height, max_width, max_height):
            height *= max_width / width
            width = max_width
            if height > max_height:
                width *= max_height / height
                height = max_height
            return width, height
        
        width, height = scale(width, height, self.imageEntry.winfo_width(), self.imageEntry.winfo_height())
        newImage = customtkinter.CTkImage(
            image,
            size=(width, height)
        )
        self.imageEntry.configure(image=newImage)
        image.close()
    
    def get_first_image_in_folder(self, folder):
        all_files_recursive = sum([[os.path.join(root, f) for f in files] for root, dirs, files in os.walk(folder)], [])
        def is_an_image(fpath): 
            return os.path.splitext(fpath)[-1] in ('.png','.jpg','.jpeg','.bmp','.webp')
        # Take the first matching result. Note: throws StopIteration if not found
        return next(filter(is_an_image, all_files_recursive))

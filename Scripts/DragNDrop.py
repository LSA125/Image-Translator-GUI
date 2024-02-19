import os
import customtkinter
from tkinterdnd2 import DND_FILES
from PIL import Image
class DND:
    def __init__(self,imageFrame, callback=lambda: None, translator=None):
        #grab the image file from parent directory
        self.images_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Images")
        self.temp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Temp")
        self.imageFrame = imageFrame
        
        self.imageFrame.columnconfigure(1, weight=1)
        self.imageFrame.columnconfigure((0,2), weight=0)
        self.imageFrame.rowconfigure((0,2), weight=1)
        self.imageFrame.rowconfigure(1, weight=0)
        
        self.Image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(self.images_path, "image_icon_light.png")),
                                                                   light_image=Image.open(os.path.join(self.images_path, "image_icon_dark.png")),
                                                                   size=(200, 200))
        self.leftButton = customtkinter.CTkButton(self.imageFrame, text="<", command=self.cycle_left)
        self.rightButton = customtkinter.CTkButton(self.imageFrame, text=">", command=self.cycle_right)
        self.trashButton = customtkinter.CTkButton(self.imageFrame, text="Delete Session", command=self.handle_next)
        self.saveButton = customtkinter.CTkButton(self.imageFrame, text="Save Session", command=self.handle_next)
        self.imageEntry = customtkinter.CTkLabel(
            self.imageFrame,
            fg_color="transparent", text="", image=self.Image,
        )
        
        
        self.imageEntry.grid(row=0, column=0, sticky="nsew", columnspan=3,rowspan=3, padx=10, pady=10)
        self.imageEntry.drop_target_register(DND_FILES)
        self.imageEntry.dnd_bind("<<Drop>>", self.drop)
        
        self.leftButton.grid(row=1, column=0, sticky="nsew")
        self.rightButton.grid(row=1, column=2, sticky="nsew")
        
        self.callback = callback
        self.translator = translator
        self.toTranslate = []
        
        self.scrollingList = []
        self.currentscrollingImage = None
    
    def handle_next(self):
        if len(self.toTranslate) > 0 and self.translator is not None and not self.translator.translateRunning:
            print("directories to translate: " + str(len(self.toTranslate)))
            self.handle_drop(self.toTranslate.pop(0))
    
    def drop(self, event):
        data = event.data.split(" ")
        
        #images will sometimes delete themselves before they can be translated if dragged from browser
        #save image in tmp folder before then.
        if(len(data) == 1):
            file = data[0].strip("{} ")
            if os.path.isfile(file):
                image = Image.open(file)
                filename = os.path.basename(file)
                save_path = os.path.join(self.temp_path, filename)
                if os.path.exists(save_path):
                    os.remove(save_path)
                image.save(save_path)
                data = [save_path]
                image.close()
        
        self.toTranslate.extend(data)
        print("dropped: ", self.toTranslate)
        self.handle_next()
    
    def clear_scrolling_list(self):
        for img in self.scrollingList:
            img.close()
        self.scrollingList = []
        self.currentscrollingImage = None
    
    def cycle_left(self):
        if len(self.scrollingList) <= 1 or self.currentscrollingImage is None:
            return
        self.currentscrollingImage -= 1
        if self.currentscrollingImage < 0:
            self.currentscrollingImage = len(self.scrollingList) - 1
        self.update_image(self.scrollingList[self.currentscrollingImage])
        
    def cycle_right(self):
        if len(self.scrollingList) <= 1 or self.currentscrollingImage is None:
            return
        self.currentscrollingImage += 1
        if self.currentscrollingImage >= len(self.scrollingList):
            self.currentscrollingImage = 0
        self.update_image(self.scrollingList[self.currentscrollingImage])
    
    def add_to_scroll_list(self, image):
        self.scrollingList.append(image)
        
        #if its the first image, set it as the current image
        if self.currentscrollingImage is None:
            self.currentscrollingImage = 0
            self.update_image(image)
        #if user currently on the last image, switch to new image
        if len(self.scrollingList) == self.currentscrollingImage+2:
            self.cycle_right()
    
    def handle_drop(self, str):
        self.input = str.strip("{} ")
        print("handling drop: ", self.input)
        if(os.path.isdir(self.input)): 
            try:
                self.callback(self.input)
            except StopIteration:
                self.imageLabel.configure(text="No image found in folder")
        elif(os.path.isfile(self.input)):
            self.callback(self.input)
        else:
            print("Invalid file type")
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
    
    def get_first_image_in_folder(self, folder):
        all_files_recursive = sum([[os.path.join(root, f) for f in files] for root, dirs, files in os.walk(folder)], [])
        def is_an_image(fpath): 
            return os.path.splitext(fpath)[-1] in ('.png','.jpg','.jpeg','.bmp','.webp')
        # Take the first matching result. Note: throws StopIteration if not found
        return next(filter(is_an_image, all_files_recursive))

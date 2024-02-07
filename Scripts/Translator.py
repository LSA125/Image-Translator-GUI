import subprocess
import threading
import os
from PIL import Image
class Translator:
    def __init__(self,callback,terminal):
        self.callback = callback
        self.batchMode = False
        self.translateRunning = False
        self.terminal = terminal

    def start_translate(self, file, translatorDirectory, settings):
        if(self.translateRunning):
            return
        command = "python -m manga_translator "
        for key in settings:
            if settings[key] and (settings[key] != "none" or key == 'inpainter'):
                command += f"--{key} "
                if(settings[key] != True):
                    command += f"{settings[key]} "
        if(os.path.isdir(file)):
            command += "--mode batch "
            self.batchMode = True
        else:
            self.batchMode = False
        command += f"--input {file}"
        self.translateRunning = True
        print(command)
        threading.Thread(target=self.start_translate_blocking, args=(command, translatorDirectory,settings,file)).start()

    def start_translate_blocking(self, command, directory,settings,file):
        with subprocess.Popen(f"{command}", cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, text=True) as translator:
            if translator.stdout:
                while line := translator.stdout.readline():
                    self.terminal.printGUI(line)
                    translator.stdout.flush()
        self.translateRunning = False
        if not self.batchMode:
            image = Image.open(os.path.join(directory, "result", "final." + settings['format']))
            if settings['dest'] != "":
                image.save(os.path.join(settings['dest'], os.path.basename(file)))
            self.callback(image)
            image.close()
        else:
            self.callback(None)
        
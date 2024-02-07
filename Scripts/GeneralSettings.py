import customtkinter as tk
import shelve
VALID_LANGUAGES = {
    'Chinese (Simplified)': 'CHS',
    'Chinese (Traditional)': 'CHT',
    'Czech': 'CSY',
    'Dutch': 'NLD',
    'English': 'ENG',
    'French': 'FRA',
    'German': 'DEU',
    'Hungarian': 'HUN',
    'Italian': 'ITA',
    'Japanese': 'JPN',
    'Korean': 'KOR',
    'Polish': 'PLK',
    'Portuguese (Brazil)': 'PTB',
    'Romanian': 'ROM',
    'Russian': 'RUS',
    'Spanish': 'ESP',
    'Turkish': 'TRK',
    'Ukrainian': 'UKR',
    'Vietnamese': 'VIN',
    'Arabic': 'ARA',
}
VALID_LANGUAGES_INV = {
    'CHS': 'Chinese (Simplified)',
    'CHT': 'Chinese (Traditional)',
    'CSY': 'Czech',
    'NLD': 'Dutch',
    'ENG': 'English',
    'FRA': 'French',
    'DEU': 'German',
    'HUN': 'Hungarian',
    'ITA': 'Italian',
    'JPN': 'Japanese',
    'KOR': 'Korean',
    'PLK': 'Polish',
    'PTB': 'Portuguese (Brazil)',
    'ROM': 'Romanian',
    'RUS': 'Russian',
    'ESP': 'Spanish',
    'TRK': 'Turkish',
    'UKR': 'Ukrainian',
    'VIN': 'Vietnamese',
    'ARA': 'Arabic',
}
TRANSLATORS = ['google', 'youdao', 'baidu', 'deepl', 'papago', 
                'caiyun', 'gpt3', 'gpt3.5', 'gpt4', 'none', 'original', 'offline', 'nllb', 
                'nllb_big', 'sugoi', 'jparacrawl', 'jparacrawl_big', 'm2m100', 'm2m100_big']
OUTPUT_FORMATS = ['png','webp','jpg']
INPAINTERS = ['default','lama_mpe','sd','none','original'] 
UPSCALERS = ['waifu2x', 'esrgan', '4xultrasharp'] 
COLORIZERS = ['none','mc2']  
class General:
    def __init__(self, tab):
        tab.grid_columnconfigure((0,1), weight=1)
        tab.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.tab = tab

        # Label and Entry for 'target-lang'
        tk.CTkLabel(tab, text='Destination Language').grid(row=0, column=0, padx=5, pady=5)
        self.target_lang_var = tk.StringVar()
        tk.CTkComboBox(tab, values=list(VALID_LANGUAGES.keys()),variable=self.target_lang_var).grid(row=0, column=1, padx=5, pady=5)

        # Label and Entry for 'format'
        tk.CTkLabel(tab, text='Output Format').grid(row=1, column=0, padx=5, pady=5)
        self.format_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.format_var, values=OUTPUT_FORMATS).grid(row=1, column=1, padx=5, pady=5)
        
        # Label and Entry for 'inpainter'
        tk.CTkLabel(tab, text='Inpainter Model').grid(row=2, column=0, padx=5, pady=5)
        self.inpainter_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.inpainter_var, values=INPAINTERS).grid(row=2, column=1, padx=5, pady=5)

        # Label and Entry for 'upscaler'
        tk.CTkLabel(tab, text='Upscaler').grid(row=3, column=0, padx=5, pady=5)
        self.upscaler_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.upscaler_var, values=UPSCALERS).grid(row=3, column=1, padx=5, pady=5)

        # Label and Entry for 'upscale-ratio'
        tk.CTkLabel(tab, text='Upscale Ratio').grid(row=4, column=0, padx=5, pady=5)
        self.upscale_ratio_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.upscale_ratio_var, values=['1', '2', '3', '4', '8', '16', '32']).grid(row=4, column=1, padx=5, pady=5)

        # Label and Entry for 'colorizer'
        tk.CTkLabel(tab, text='Colorizer Model').grid(row=5, column=0, padx=5, pady=5)
        self.colorizer_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.colorizer_var, values=COLORIZERS).grid(row=5, column=1, padx=5, pady=5)
        
        tk.CTkLabel(tab, text='Translator').grid(row=6, column=0, padx=5, pady=5)
        self.translator_var = tk.StringVar()
        tk.CTkComboBox(tab, variable=self.translator_var, values=TRANSLATORS).grid(row=6, column=1, padx=5, pady=5)
        
        tk.CTkLabel(tab, text='Manga to Eng Optimization').grid(row=7, column=0, padx=5, pady=5)
        self.manga_var = tk.BooleanVar()
        tk.CTkCheckBox(tab, variable=self.manga_var,text='').grid(row=7, column=1, padx=5, pady=5)
        
        tk.CTkLabel(tab, text='Use Cuda').grid(row=8, column=0, padx=5, pady=5)
        self.cuda_var = tk.BooleanVar()
        tk.CTkCheckBox(tab, variable=self.cuda_var,text='').grid(row=8, column=1, padx=5, pady=5)
        self.load_settings()
        
    def get_settings(self):
        return {
            'target-lang': VALID_LANGUAGES[self.target_lang_var.get()],
            'format': self.format_var.get(),
            'inpainter': self.inpainter_var.get(),
            'upscaler': self.upscaler_var.get(),
            'upscale-ratio': self.upscale_ratio_var.get(),
            'colorizer': self.colorizer_var.get(),
            'translator': self.translator_var.get(),
            'manga2eng': self.manga_var.get(),
            'use-cuda': self.cuda_var.get()
        }
        
    def save_settings(self):
        shelf = shelve.open('settings')
        shelf['target-lang'] = VALID_LANGUAGES[self.target_lang_var.get()]
        shelf['format'] = self.format_var.get()
        shelf['inpainter'] = self.inpainter_var.get()
        shelf['upscaler'] = self.upscaler_var.get()
        shelf['upscale-ratio'] = self.upscale_ratio_var.get()
        shelf['colorizer'] = self.colorizer_var.get()
        shelf['translator'] = self.translator_var.get()
        shelf['manga'] = self.manga_var.get()
        shelf['use-cuda'] = self.cuda_var.get()
        shelf.close()
        
    def load_settings(self):
        shelf = shelve.open('settings')
        if(shelf):
            self.target_lang_var.set(VALID_LANGUAGES_INV[shelf['target-lang']])
            self.format_var.set(shelf['format'])
            self.inpainter_var.set(shelf['inpainter'])
            self.upscaler_var.set(shelf['upscaler'])
            self.upscale_ratio_var.set(shelf['upscale-ratio'])
            self.colorizer_var.set(shelf['colorizer'])
            self.translator_var.set(shelf['translator'])
            self.manga_var.set(shelf['manga'])
            self.cuda_var.set(shelf['use-cuda'])
        else:
            self.target_lang_var.set('English')
            self.format_var.set('jpg')
            self.inpainter_var.set('default')
            self.upscaler_var.set('waifu2x')
            self.upscale_ratio_var.set('1')
            self.colorizer_var.set('none')
            self.translator_var.set('google')
            self.manga_var.set(False)
            self.cuda_var.set(False)
        shelf.close()
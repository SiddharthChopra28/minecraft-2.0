import platform
import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import ctypes
import random
from pygame import mixer


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.virus_coords = [
            [(242, 261), (620, 261), (242, 296), (620, 296)],
            [(242, 309), (620, 309), (242, 338), (620, 338)],
            [(242, 353), (620, 353), (242, 386), (620, 386)],
            [(242, 421), (423, 421), (242, 454), (423, 454)],
            [(438, 420), (620, 420), (438, 450), (620, 450)],
            [(196, 420), (228, 420), (196, 453), (228, 453)],
            [(633, 421), (665, 421), (633, 454), (665, 454)]
        ]

        self.isWin = "windows" in platform.system().lower()

        self.protocol('WM_DELETE_WINDOW', lambda: self.false_close())

        self.windows = []

        self.setup()
        self.startup()
        
        

    def setup(self):

        self.screen_width, self.screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.width, self.height = 904, 500

        self.centerx, self.centery = int(
            self.screen_width/2 - self.width/2), int(self.screen_height/2.5 - self.height/2)

        self.geometry(
            f"{self.width}x{self.height}+{self.centerx}+{self.centery}")
        self.resizable(False, False)
        self.title("Minecraft 2.0")
        
        self.iconbitmap(r'resources/icon.ico')
        
        mixer.init()

        raw_img = Image.open(
            'resources/bg.png').resize((self.width, self.height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(raw_img)

    def homePage(self):
        if not self.isWin:
            l = tk.Label(self, text="This app works only for Windows :(")
            l.config(font=("Courier", 24))
            l.pack()
            self.after(60000, lambda: sys.exit())

        else:
            mixer.music.load('resources/intro.mp3')
            mixer.music.play(-1)

            self.background_label.destroy()
            self.background_image = ImageTk.PhotoImage(Image.open(
                'resources/mcbg.png').resize((self.width, self.height), Image.ANTIALIAS))
            self.background_label = tk.Label(self, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.background_label.bind("<Button-1>", self.handle_click)


    def startup(self):

        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.after(1500, self.homePage)

    def handle_click(self, event):
        for i in self.virus_coords:
            if event.x >= i[0][0] and event.x <= i[1][0] and event.y >= i[0][1] and event.y <= i[2][1]:
                self.initiate_virus()
                break

    def initiate_virus(self):
        mixer.music.stop()
        self.virus = Virus(self, 15)
        self.virus.change_bg()
        self.virus.play_song()
        for _ in range(self.virus.max_windows):
            randomX = random.randint(0, self.screen_width)
            randomY = random.randint(0, self.screen_height)

            self.windows.append(self.virus.spawn_new_window(f'600x300+{randomX}+{randomY}'))

    def false_close(self):
        try:
            for _ in range(15):
                randomX = random.randint(0, self.screen_width)
                randomY = random.randint(0, self.screen_height)

                self.windows.append(self.virus.spawn_new_window(f'600x300+{randomX}+{randomY}'))

        except:
            self.virus = Virus(self, 15)
            self.virus.change_bg()
            self.virus.play_song()

            for _ in range(15):
                randomX = random.randint(0, self.screen_width)
                randomY = random.randint(0, self.screen_height)

                self.windows.append(self.virus.spawn_new_window(f'600x300+{randomX}+{randomY}'))


    


class Virus:
    def __init__(self, root, maxWindows):
        isWin = "windows" in platform.system().lower()
        if not isWin:
            sys.exit()
        self.root = root
        self.winNames = ['HAHAHAHAHAHA!', 'VIRUS!!', 'THIS IS A TOTALLY REAL AND HARMFUL VIRUS',
                         'YOU HAVE BEEN HACKED', 'YOU ARE AN IDIOT!']
        self.imgLocations = ['resources/player.jpg', 'resources/creeper.png', 'resources/mobs.jpg']
        self.bgImg = 'resources/desktop.png'
        self.max_windows = maxWindows

    def spawn_new_window(self, geometry):
        return NewWindow(self, random.choice(self.winNames), random.choice(self.imgLocations), geometry, self.root)

    def change_bg(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), self.bgImg) , 0)

    def play_song(self):
            mixer.music.load('resources/song.mp3')
            mixer.music.play(-1)

        

class NewWindow(tk.Toplevel):
    
    def __init__(self, virus, windowName, imgLocation, geometry, root=None):
        super().__init__(master=root)
        
        self.title(windowName)
        self.geometry(geometry)
        self.resizable(False, False)
        self.iconbitmap(r'resources/icon.ico')
        self.background_image = ImageTk.PhotoImage(Image.open(imgLocation).resize((600, 300), Image.ANTIALIAS))
        
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        background_label.pack()
        
        self.protocol('WM_DELETE_WINDOW', lambda: self.false_close())
        
        self.virus = virus
        self.root = root

    def edit_geometry(self, geometry):
        self.geometry(geometry)
        
    def false_close(self):
        for _ in range(5):
            randomX = random.randint(0, self.root.screen_width)
            randomY = random.randint(0, self.root.screen_height)

            self.root.windows.append(self.virus.spawn_new_window(f"600x300+{randomX}+{randomY}"))

        self.destroy()

        
        
        



if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()


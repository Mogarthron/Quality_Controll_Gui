from tkinter import Tk, Label, Button
import tkinter.font as font
from models import DefectsModel


class MainView:
    def Btn(self, root, text, command, font, width=15, height=5):
        b = Button(
            root,
            text=text,
            justify="center",
            width=width,
            height=height,
            fg="white",
            bg="blue",
        )
        b["command"] = command
        b["font"] = font
        b.pack()


class SidePanelView:
    def __init__(self):
        mv = MainView()
        self.window = Tk()

        screen_width = int(200)
        screen_height = self.window.winfo_screenheight() - 100

        self.window.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
        self.window.resizable(0, 0)

        self.__myFont = font.Font(size=12)

        mv.Btn(
            self.window,
            "Okno Wad",
            self.__OpenDefectWindow,
            self.__myFont,
            width=20,
            height=5,
        )

        mv.Btn(
            self.window,
            "Zamknij",
            self.window.destroy,
            self.__myFont,
            width=20,
            height=5,
        )

    def __OpenDefectWindow(self):

        newWindow = DefectsView(Tk(), 5, 2)


class DefectsView:
    def __init__(self, master, workstation, shift):
        self.__workstation = workstation
        self.__shift = shift
        self.__d = DefectsModel()
        self.window = master

        self.window.title(f"KJ Stanowisko {str(workstation)}, Zmiana: {str(shift)}")

        screen_width = int(self.window.winfo_screenwidth() / 2)
        screen_height = self.window.winfo_screenheight() - 100

        self.window.geometry("{0}x{1}+200+0".format(screen_width, screen_height))
        self.window.resizable(0, 0)

        self.__myFont = font.Font(size=12)

        self.__SetLayout()

    def __btn(self, r, c, i):
        b = Button(
            self.window,
            text=i[1],
            wraplength=100,
            justify="center",
            width=15,
            height=5,
            fg="white",
            bg="blue",
        )
        b["font"] = self.__myFont
        b["command"] = lambda i=i: self.__d.SaveDefect(
            self.__workstation, self.__shift, i
        )
        b.grid(row=r, column=c, padx=1, pady=1)

    def __CloseWindow(self):
        self.window.destroy()

    def __SetLayout(self):
        q = Button(
            self.window,
            text="Zamknij",
            justify="center",
            width=10,
            height=2,
            fg="white",
            bg="blue",
            command=self.__CloseWindow,
        )
        q["font"] = self.__myFont
        q.grid(row=0, column=0, padx=1, pady=1)

        r = 1
        c = 0
        for x in self.__d.labels:

            l = Label(self.window, text=x)
            l.grid(row=r, column=c, padx=2)
            r += 1

            for i in self.__d.buttons_names:
                if i[0] == x:

                    if c >= 5:
                        r += 1
                        c = 0

                    self.__btn(r, c, i)
                    c += 1
            r += 1
            c = 0

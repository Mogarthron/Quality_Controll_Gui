from tkinter import Tk, Label, Button, StringVar
from tkinter.ttk import Combobox
import tkinter.font as font
from qualitycontrol_ktinker.models import DefectsModel, SidePanelModel


class MainView:
    def __init__(self, root):
        self.root = root
        self.myFont = font.Font(size=12)

    def Btn(self, root, text, command, font, width=15, height=5, _grid=None):
        b = Button(
            self.root,
            justify="center",
            fg="white",
            bg="blue",
        )
        b["text"] = text
        b["width"] = width
        b["height"] = height
        b["command"] = command
        # b["font"] = font
        b["font"] = self.myFont

        if type(_grid) == list:
            b.grid(row=_grid[0], column=_grid[1], padx=1, pady=1)
        else:
            b.pack()

    def BtnText(self, t):
        return t[0] + "\n" + "Forma: " + t[1] + "\n" + "Warsztat: " + t[2]

    def CloseWindowCommand(self):
        self.root.destroy()


class SidePanelView:
    def __init__(self):

        spm = SidePanelModel()
        self.window = Tk()
        mv = MainView(self.window)

        qc_list = spm.qc_list

        screen_width = int(200)
        screen_height = self.window.winfo_screenheight() - 100

        self.window.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
        self.window.resizable(0, 0)

        self.__myFont = font.Font(size=12)

        mv.Btn(
            self.window,
            mv.BtnText(qc_list[2]),
            lambda: self.__OpenDefectWindow(qc_list[2][0]),
            self.__myFont,
            width=20,
            height=5,
        )

        mv.Btn(
            self.window,
            mv.BtnText(qc_list[1]),
            lambda: self.__OpenDefectWindow(qc_list[1][0]),
            self.__myFont,
            width=20,
            height=5,
        )

        mv.Btn(
            self.window,
            "Zamknij",
            mv.CloseWindowCommand,
            self.__myFont,
            width=20,
            height=5,
        )

    def __OpenDefectWindow(self, card_no):

        newWindow = DefectsView(Tk(), 5, 2, card_no)


class DefectsView:
    def __init__(self, master, workstation, shift, number_of_work_card):

        self.__selectedValue = StringVar()
        self.__currentSelectedValue = ""
        self.__workstation = workstation
        self.__number_of_work_card = number_of_work_card
        self.__shift = shift
        self.__d = DefectsModel()
        self.window = master

        self.window.title(
            f"KJ Stanowisko {str(workstation)}, Karta Formowania: {str(number_of_work_card)}"
        )

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
            self.__workstation,
            self.__number_of_work_card,
            self.__shift,
            i,
            self.__currentSelectedValue,
        )
        b.grid(row=r, column=c, padx=1, pady=1)

    def __CloseWindow(self):
        self.window.destroy()

    def __OnSelectChanged(self, event):
        self.__currentSelectedValue = event.widget.get()

    def __SetLayout(self):
        mv = MainView(self.window)

        cb = Combobox(self.window, textvariable=self.__selectedValue)
        cb["values"] = self.__d.qcemp_list
        cb.current(0)
        cb.bind("<<ComboboxSelected>>", self.__OnSelectChanged)
        cb.grid(row=0, column=0, padx=1, pady=1)

        q = mv.Btn(
            self.window,
            "Zamknij",
            self.__CloseWindow,
            self.__myFont,
            height=2,
            width=10,
            _grid=[0, 1],
        )

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

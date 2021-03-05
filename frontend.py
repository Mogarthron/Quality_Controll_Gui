from tkinter import Tk, Label, Button
import tkinter.font as font
from backend import Defects

window = Tk()

__d = Defects()

workstation = 5
shift = 2

window.title(f'KJ Stanowisko {str(workstation)}, Zmiana: {str(shift)}')

screen_width = int(window.winfo_screenwidth() / 2)
screen_height = window.winfo_screenheight() - 100

window.geometry('{0}x{1}+0+0'.format(screen_width, screen_height))
window.resizable(0, 0)

myFont = font.Font(size=12)


def btn(r, c, i):
    b = Button(window, text=i[1], wraplength=100,
               justify='center', width=15, height=5, fg="white", bg="blue", command=lambda i=i: __d.SaveDefect(workstation, shift, i))
    b['font'] = myFont
    b.grid(row=r, column=c, padx=1, pady=1)


def SetLayout():

    r = 0
    c = 0
    for x in __d.labels:

        l = Label(window, text=x)
        l.grid(row=r, column=c, padx=2)
        r += 1

        for i in __d.buttons_names:
            if (i[0] == x):

                if (c >= 5):
                    r += 1
                    c = 0

                btn(r, c, i)
                c += 1
        r += 1
        c = 0


SetLayout()

window.mainloop()

from views import SidePanelView


class Controler:
    def __init__(self):

        view = SidePanelView()
        self.root = view.window

    def run(self):
        self.root.deiconify()
        self.root.mainloop()

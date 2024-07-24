from qualitycontrol_ktinker.views import SidePanelView


class MainControler:
    def __init__(self):

        view = SidePanelView()
        self.root = view.window

    def run(self):
        self.root.deiconify()
        self.root.mainloop()

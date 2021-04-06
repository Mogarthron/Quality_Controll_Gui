import os
import datetime


class DefectsModel:
    def __init__(self):

        self.def_path = "./Data/Defects"
        self.out_path = "./Output"

        self.labels = [x.replace(".csv", "") for x in os.listdir(self.def_path)]

        self.buttons_names = list()

        for d in os.listdir(self.def_path):
            f = open(os.path.join(self.def_path, d), "r", encoding="utf-8")
            for x in f:
                self.buttons_names.append([d.replace(".csv", ""), x.replace("\n", "")])

            f.close()

    def SaveDefect(self, workstation, shift, i):

        d = datetime.datetime.now()

        file_name = f'{d.strftime("%y%m%d")}_{str(shift)}_{str(workstation)}.csv'

        path = os.path.join(self.out_path, file_name)

        file_header = "Czas_Wpisu,Zmiana,Stan,Sort,Typ_Wady,Wada\n"

        o = f'{d.strftime("%Y-%m-%d %H:%M:%S")},{str(shift)},{str(workstation)},Sort_1,{i[0]},{i[1]}\n'

        if os.path.exists(path) == False:
            f = open(path, "w", encoding="utf-8")
            f.write(file_header)
            f.close()

        file = open(path, "a", encoding="utf-8")
        file.writelines(o)
        file.close()
        # print(o.replace('\n', ''))

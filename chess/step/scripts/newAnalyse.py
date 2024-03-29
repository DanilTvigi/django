# from subprocess import Popen, PIPE
import cv2
import numpy as np
from PIL import Image
import camera 
import search 
from analyse import Analyse
import copy
import statistics

class newAnalyse():
    def __init__(self, request):
        self.span = 10
        self.step_v = 50
        self.green = [
            'a1', 'b2', 'c1', 'd2', 'e1', 'f2', 'g1', 'h2',
            'a3', 'b4', 'c3', 'd4', 'e3', 'f4', 'g3', 'h4',
            'a5', 'b6', 'c5', 'd6', 'e5', 'f6', 'g5', 'h6',
            'a7', 'b8', 'c7', 'd8', 'e7', 'f8', 'g7', 'h8',
        ]
        self.blue = [
            'a2', 'b1', 'c2', 'd1', 'e2', 'f1', 'g2', 'h1',
            'a4', 'b3', 'c4', 'd3', 'e4', 'f3', 'g4', 'h3',
            'a6', 'b5', 'c6', 'd5', 'e6', 'f5', 'g6', 'h5',
            'a8', 'b7', 'c8', 'd7', 'e8', 'f7', 'g8', 'h7',
        ]


        self.kletki = request.kletki
        self.color = request.color

        self.img = Image.open('tmp.png')

        self.mean_empty_black = 0
        self.mean_empty_white = 0

        self.get_empty_cell()


    def walker(self, coordinates, size, step=8): # img_np, coodinates, size, step=5
        x = coordinates[0]
        y = coordinates[1]

        tmp_color = []

        zx = x + size
        zy = int(y / 5)
        global_step = int(size / step)
        print(f"global step | {global_step}")
        for dx in range(x, x+size, global_step):
            # -> x+
            r, g, b = self.img.getpixel((dx, y))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[y][dx] = (0,0,255)

            # -> x+
            r, g, b = self.img.getpixel((dx, y + size))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[y + size][dx] = (0,0,255)

            # /1
            r, g, b = self.img.getpixel((zx, zy))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[zy][zx] = (0,0,255)

            # /2
            r, g, b = self.img.getpixel((zx, zy*2))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[zy][zx] = (0,0,255)

            # /3
            r, g, b = self.img.getpixel((zx, zy*3))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[zy][zx] = (0,0,255)

            # /4
            r, g, b = self.img.getpixel((zx, zy*4))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[zy][zx] = (0,0,255)

            # /5
            r, g, b = self.img.getpixel((zx, zy*5))
            tmp_color.append(int((r + g + b) / 3))
            # self.img_np[zy][zx] = (0,0,255)


            zx -= global_step
            zy += global_step

        # cv2.imwrite('test.png', self.img_np)
        # print(tmp_color)
        return tmp_color

    # Получение среднего значения цвета для пустых ячеек белых и черных
    def get_mean_empty(self, empty_cells): #
        tmp = []
        for cell in empty_cells:
            color = self.walker(self.kletki[cell], int(self.step_v / 2) + 10, step=5)
            mean_color = statistics.mean(color)
            # print(f"{cell} = {color}")
            tmp.append(mean_color)
        
        return int(statistics.mean(tmp))

    def get_empty_cell(self):
        empty_green = []
        for cell in self.green:
            if self.color[cell] == 0: empty_green.append(cell)
        
        empty_blue = []
        for cell in self.blue:
            if self.color[cell] == 0: empty_blue.append(cell)
        
        self.mean_empty_black = self.get_mean_empty(empty_green)
        self.mean_empty_white = self.get_mean_empty(empty_blue)

        # print("mean_empty_black", self.mean_empty_black)
        # print("mean_empty_white", self.mean_empty_white)

    def check_color_figure(self):
        color_figure = copy.deepcopy(self.color)

        for key in color_figure.keys():
            if color_figure[key] == 0: # 0
                continue
            else:
                # print(f"OK -> {key}")
                z_colors = self.walker(self.kletki[key], self.step_v, step=int(self.step_v/2))
                tmp = []
                for w in z_colors:
                    if key in self.green:
                        if w > self.mean_empty_black + self.span:
                            tmp.append(w)
                        elif w < self.mean_empty_black - self.span:
                            tmp.append(w)
                    else:
                        if w > self.mean_empty_white + self.span:
                            tmp.append(w)
                        elif w < self.mean_empty_white - self.span:
                            tmp.append(w)
                
                if statistics.mean(tmp) > (self.mean_empty_black + self.mean_empty_white)/2:
                    color_figure[key] = "W"
                else:
                    color_figure[key] = "B"
        return color_figure
    
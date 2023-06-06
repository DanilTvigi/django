from django.http import HttpResponse
from subprocess import Popen, PIPE
import cv2
import numpy as np
from PIL import Image
import search
import camera
from analyse import Analyse
from step.models import Desk


def analyse(request):
    
    # temp = []
    # while len(temp) < 2:  

    #     img = camera.get_img("10.2.31.25","admin","Skills39!", True)
    #     tmp = bytes()
    #     for t in img:
    #         tmp += t
    #     nparr = np.frombuffer(tmp, np.uint8)
    #     img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #     cv2.imwrite('tmp.png', img_np)
    #     img_np = cv2.imread('tmp.png', 1)
    #     temp = search.search(img_np)


    # img_np = cv2.imread('4+2.png', 1)
    # temp = search.search(img_np)


    # QRs = Analyse.search_qr_code(temp)
    # cords_ancle = Analyse.cords_ancle_board(QRs)
    # img_np, kletki, color, past_pole = Analyse.search_cell(cords_ancle, img_np)
    # color = Analyse.color_pixel(img_np, kletki, color)

    # moves, step = Analyse.step(color, moves, past_pole) # moves массив прошлого хода
    # for key in kletki:
    #     cv2.putText(img_np, str(color[key]), kletki[key], cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1)
    #     cv2.imwrite('res22.png', img_np)
    
    print('ok')
    return HttpResponse('ok')
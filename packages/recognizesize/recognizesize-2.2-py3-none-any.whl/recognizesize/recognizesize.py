import matplotlib.pyplot as plt
import sys, os
import warnings

from .SizeRecognizer import *

warnings.filterwarnings("ignore", category=UserWarning) 


def recognize_size(path):
    size_recognizer = SizeRecognizer()
    image = Image.open(path)

    # image = size_recognozer.get_image_with_size(image)
    res_size = size_recognizer.get_image_with_size(image)
    # plt.imsave(result_path, image)
    print(res_size)


if __name__ == "__main__":
    # path = sys.argv[1]

    path = "/home/dggz/code/smart-mirror/size_recognizer/check_img/5.jpg"

    # photo_index = 4
    # path = f'/home/dggz/code/smart-mirror/size_recognizer/check_img/{photo_index}.jpg'
    # result_path = path.rsplit(os.sep, 1)[0] + '/result' + path.rsplit(os.sep, 1)[1]

    recognize_size(path)
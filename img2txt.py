import argparse
import cv2
import numpy as np
from skimage import io
import tempfile

tempfile.tempdir = "tmp"

# parameters
model_path = "model/model.json"  # or "model/model_light.json"
weight_path = "model/weight.hdf5"  # or "model/weight_light.json"
new_width = 0  # adjust the width of the image. the original width is used if new_width = 0.
input_shape = [64, 64, 1]


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input",
                        type=str,
                        default="data/input.jpg",
                        help="Path to input image")
    parser.add_argument("--output",
                        type=str,
                        default="data/output.txt",
                        help="Path to output text file")
    parser.add_argument("--mode",
                        type=str,
                        default="complex",
                        choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--num_cols",
                        type=int,
                        default=200,
                        help="number of character for output's width")
    args = parser.parse_args()
    return args


def main(input, mode, num_cols, scale):

    errors = " "

    if mode == "simple":
        CHAR_LIST = '@%#*+=-:. '
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    num_chars = len(CHAR_LIST)
    num_cols = num_cols
    image = io.imread(input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        errors = "Too many columns or rows. Using default setting."
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    # create and open the temporary file in text mode
    temp = tempfile.TemporaryFile(mode='w+t')

    # write to the file
    for i in range(num_rows):
        for j in range(num_cols):
            temp.writelines(CHAR_LIST[min(
                int(
                    np.mean(image[
                        int(i * cell_height):min(int((i + 1) *
                                                     cell_height), height),
                        int(j * cell_width):min(int((j + 1) *
                                                    cell_width), width)]) *
                    num_chars / 255), num_chars - 1)])
        temp.writelines("\n")

    # set the file pointer at the beginning of the file
    temp.seek(0)
    return temp.read(), errors

import sys
import PIL
from PIL import Image
import math
import matplotlib.pyplot as plt
from pathlib import Path

import numpy as np  
import argparse


parser = argparse.ArgumentParser(description=r'example: img_to_placepalette.py ugandaflag.png -a euclidean')

parser.add_argument("input", help="input image")
parser.add_argument('-a', '--diff', choices=["euclidean", "euclidean_modified", "redmean", "all"], default="all", action='store', dest='algo', help='Algorithm to use to calculate color difference from r/place palette')

args = parser.parse_args()


#r/place rgb palette
colors = {"red":(255,69,0), "orange":(255,168,0), "yellow":(255,214,53), "darkgreen":(0,163,104), 
          "green":(126,237,86), "darkblue":(36,90,164), "blue":(54,144,234), "lightblue": (81,233,244),
          "darkpurple":(129,30,159), "purple":(200,191,231), "pink":(255,153,170), "brown":(156,105,38),
          "black":(0,0,0), "darkgrey":(137,141,144), "grey":(212,215,217), "white":(255,255,255), "a":(190,0,57), 
          "b":(255,69,0), "c":(255,168,0), "d":(255,214,53), "e":(0,163,104), "f":(0,204,120), "g":(126,237,86), "h":(0,117,111),
          "v":(0,158,170), "l":(36,80,164), "fs":(54,144,234), "i":(81,233,244), "er":(73,58,193), "fv":(106,92,255), "ofa":(129,30,159),
          "sdf":(180,74,192), "psdf":(255,153,170), "psodf":(109,72,47), "cxf":(156,105,38), "cxf":(137,141,144), "xcvxcv":(212,215,217)}
colorvals = np.asarray(list(colors.values()))

#img = Image.open(r'D:\Projects\rplacepaletteconverter\NaMpixel.png')
img = Image.open(args.input)
if img.mode == "RGBA":
    img.load()
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])
    img = background
arr = np.asarray(img)


def euclidean(pixel1, pixel2):
    return np.linalg.norm(pixel1 - pixel2)

def euclidean_modified(pixel1, pixel2):
    dr = pixel1[0] - pixel2[0]
    dg = pixel1[1] - pixel2[1]
    db = pixel1[2] - pixel2[2]
    rhat = 0.5 * (pixel1[0] + pixel2[0])
    if rhat < 128:
        return 2*dr ** 2 + 4*dg**2 + 3*db**2
    else:
        return 3*dr**2 + 4*dg**2 + 2*db**2

def redmean(pixel1, pixel2):
    dr = pixel1[0] - pixel2[0]
    dg = pixel1[1] - pixel2[1]
    db = pixel1[2] - pixel2[2]
    rhat = 0.5 * (pixel1[0] + pixel2[0])
    return (2 + rhat/256) * dr ** 2 + 4 * dg**2 + (2 + (255- rhat)/256)*db**2


def calculate_best_color(pixel, colors, dist_function):
    best_color = colors[0]
    dist = dist_function(pixel, colors[0])
    for color in colors[1:]:
        new_dist = dist_function(pixel, color)
        if (new_dist < dist):
            dist = new_dist
            best_color = color
    return best_color

def convert_to_palette(arr, palette, distance_function):
    pixels = np.copy(arr)
    for row in range(len(pixels)):
        for column in range(len(pixels[row])):
            pixels[row][column] = calculate_best_color(pixels[row][column], palette, distance_function)
    return pixels


file_name = Path(args.input).stem

if args.algo == "euclidean" or args.algo == "all":
    arr1 = convert_to_palette(arr, colorvals, euclidean)
    im1 = PIL.Image.fromarray(np.uint8(arr1))
    im1.save(file_name + "_euclidean" + str(im1.width) + "x" + str(im1.height) + ".png")

if args.algo == "euclidean" or args.algo == "all":
    arr2 = convert_to_palette(arr, colorvals, euclidean_modified)
    im2 = PIL.Image.fromarray(np.uint8(arr2))
    im2.save(file_name + "_euclidean_mod" + str(im2.width) + "x" + str(im2.height) + ".png")

if args.algo == "euclidean" or args.algo == "all":
    arr3 = convert_to_palette(arr, colorvals, redmean)
    im3 = PIL.Image.fromarray(np.uint8(arr3))
    im3.save(file_name + "_redmean" + str(im3.width) + "x" + str(im3.height) + ".png")





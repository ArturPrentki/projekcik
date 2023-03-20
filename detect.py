
import numpy as np
import json
from pathlib import Path
from typing import Dict

import click
import cv2
from tqdm import tqdm



def detect(img_path: str) -> Dict[str, int]:
    """Object detection function, according to the project description, to implement.

    Parameters
    ----------
    img_path : str
        Path to processed image.

    Returns
    -------
    Dict[str, int]
        Dictionary with quantity of each object.
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # TODO: Implement detection method.
# for i in range(40):
#     if i < 10:
#
#         img1 = cv2.imread('data/0' + str(i) + '.jpg')
#     else:
#         img1 = cv2.imread('data/' + str(i) + '.jpg')


# jedno zdjecie w mniejszej rozdzielczosci, trzeba zmienic
    scale_percent_wys = 23
    scale_percent_szer = 31
    wys = int(img.shape[0] * scale_percent_wys / 100)
    szer = int(img.shape[1] * scale_percent_szer / 100)

    dim = (szer, wys)

    if (img.shape[0] > 1280 and img.shape[1] > 1280):
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    else:
        img = img
    kernel = np.ones((3, 3), np.uint8)

    # ustawianie granic dla  poszczegolnych barw
    dol_czerw = np.array([169, 35, 80])
    gora_czerw = np.array([180, 255, 255])

    dol_zolty = np.array([20, 100, 120])
    gora_zolty = np.array([30, 255, 255])

    dol_ziel = np.array([34, 110, 10])
    gora_ziel = np.array([89, 255, 255])

    dol_fiolet = np.array([65, 40, 0])
    gora_fiolet = np.array([175, 250, 160])



    # tworzenie i przypisywanie masek
    def maskfiltr(maska):
        maska = cv2.morphologyEx(maska, cv2.MORPH_OPEN, kernel, iterations=2)
        maska = cv2.morphologyEx(maska, cv2.MORPH_CLOSE, kernel, iterations=2)
        return maska

    img = cv2.medianBlur(img, 5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_czerw = cv2.inRange(hsv, dol_czerw, gora_czerw)
    mask_czerw = maskfiltr(mask_czerw)

    mask_zolty = cv2.inRange(hsv, dol_zolty, gora_zolty)
    mask_zolty = maskfiltr(mask_zolty)

    mask_ziel = cv2.inRange(hsv, dol_ziel, gora_ziel)
    mask_ziel = maskfiltr(mask_ziel)

    mask_fiolet = cv2.inRange(hsv, dol_fiolet, gora_fiolet)
    mask_fiolet = maskfiltr(mask_fiolet)



    wyn_czerw = cv2.bitwise_and(img, img, mask=mask_czerw)
    wyn_czerw2gray = cv2.cvtColor(wyn_czerw, cv2.COLOR_RGB2GRAY)

    wyn_ziel = cv2.bitwise_and(img, img, mask=mask_ziel)
    wyn_ziel2gray = cv2.cvtColor(wyn_ziel, cv2.COLOR_RGB2GRAY)

    wyn_zolty = cv2.bitwise_and(img, img, mask=mask_zolty)
    wyn_zolty2gray = cv2.cvtColor(wyn_zolty, cv2.COLOR_RGB2GRAY)

    wyn_fiolet = cv2.bitwise_and(img, img, mask=mask_fiolet)
    wyn_fiolet2gray = cv2.cvtColor(wyn_fiolet, cv2.COLOR_RGB2GRAY)

    #wykrywanie okregow na cukierkach

    circles_ziel = cv2.HoughCircles(wyn_ziel2gray, cv2.HOUGH_GRADIENT,
                                    1.5, 42, param1=100, param2=10, minRadius=5, maxRadius=20)
    circles_zolty = cv2.HoughCircles(wyn_zolty2gray, cv2.HOUGH_GRADIENT,
                                     1.5, 42, param1=100, param2=10, minRadius=5, maxRadius=20)
    circles_fiolet = cv2.HoughCircles(wyn_fiolet2gray, cv2.HOUGH_GRADIENT,
                                      1.5, 42, param1=100, param2=10, minRadius=5, maxRadius=20)
    circles_czerw = cv2.HoughCircles(wyn_czerw2gray, cv2.HOUGH_GRADIENT,
                                     1.5, 42, param1=100, param2=10, minRadius=5, maxRadius=20)

    if circles_czerw is None:
        red = 0

    else:
        red = circles_czerw.size / 3

    if circles_zolty is None:
        yellow = 0

    else:
        yellow = circles_zolty.size / 3

    if circles_ziel is None:
        green = 0


    else:

        green = circles_ziel.size / 3
    if circles_fiolet is None:

        purple = 0
    else:
        purple = circles_fiolet.size / 3

    red = red
    yellow = yellow
    green = green
    purple = purple

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory',
              type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path),
              required=True)
def main(data_path: Path, output_file_path: Path):
    img_list = data_path.glob('*.jpg')

    results = {}

    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)


if __name__ == '__main__':
    main()

    #
    #     if i < 10:
    #
    #         print('0' + str(i) + '.jpg: {')
    #         print('red:' + str(red))
    #         print('yellow:' + str(yellow))
    #         print('green:' + str(green))
    #         print('purple:' + str(purple))
    #         print('},')
    #
    #     else:
    #         print(str(i) + '.jpg: {')
    #         print('red:' + str(red))
    #         print('yellow:' + str(yellow))
    #         print('green:' + str(green))
    #         print('purple:' + str(purple))
    #         print('},')

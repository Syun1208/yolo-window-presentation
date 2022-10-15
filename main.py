from re import A
from weights.load_weights import weights
from tools.get_coordinate_yolo import detection
from tools.non_max_suppression import nms
from yolov5.hubconf import _create
import argparse
import numpy as np
import cv2
import tqdm
from tabulate import tabulate
from pathlib import Path
import os
import sys
import logging

FILE = Path(os.path.dirname(__file__)).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, help='initial weights path', default='weights\\best.pt')
    parser.add_argument('--cfg-detection', type=str, help='model configuration: yolov5, yolov7', default='yolov5')
    parser.add_argument('--img_path', type=str, help='Image path')
    parser.add_argument('--folder_path', type=str, help='Folder Image path')
    parser.add_argument('--folder_save_rotation', type=str,
                        default=str(ROOT / 'results/correct'),
                        required=False)
    parser.add_argument('--folder_save_detection', type=str,
                        default=str(ROOT / 'results/detect'),
                        required=False)
    parser.add_argument('--option', type=int, help='activate 1 to open camera or 0 to add image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    return parser.parse_args()

def predict(image, filename, args):
    # args = parse_arg()
    pretrainedModel = weights()
    coordinateBoundingBox = []
    classes = ['top-cmnd', 'back-cmnd', 'top-cccd', 'back-cccd', 'top-chip', 'back-chip', 'passport', 'rotate']
    # weightPath = 'weights\\best.pt'
    pretrainedYOLO = pretrainedModel.modelYOLOv5(args.weights)
    modelYOLO = detection(image)
    coordinate, score, name, image = modelYOLO.v5(pretrainedYOLO)
    coordinate, score = nms(coordinate, score, 0.4)
    if not os.path.exists(os.path.abspath(args.folder_save_detection)):
        os.makedirs(os.path.abspath(args.folder_save_detection))
    cv2.imwrite(os.path.join(os.path.abspath(args.folder_save_detection), filename), image)
    try:
        for i in tqdm.tqdm(range(len(name)), total=len(name)):
            coordinate[i] = np.array(coordinate[i])
            results = {"class_id": classes.index(name[i]), "class_name": name[i],
                    "bbox_coordinates": coordinate[i].tolist(),
                    "confidence_score": score[i]}
            coordinateBoundingBox.append(results)
        return coordinateBoundingBox, image
    except Exception as e:
        logging.error(e)
        text1 = ["NOTICE"]
        text2 = [["PLEASE TRY AGAIN !"], ["SUGGESTION: PUT YOUR IMAGE INCLUDING BACKGROUND"]]
        print(tabulate(text2, text1, tablefmt="pretty"))
        return {'status': 'try again'}, image

def main(args):
    pretrainedModel = weights()
    pretrainedYOLO = 0
    originalImage = cv2.imread(args.img_path)
    image = np.array(cv2.imread(args.img_path))
    coordinateCompute = []
    pretrainedYOLO = pretrainedModel.modelYOLOv5(args.weights)
    modelYOLO = detection(cv2.imread(args.img_path))
    coordinate, score, name, image = modelYOLO.v5(pretrainedYOLO)
    coordinate, score = nms(coordinate, score, 0.4)
    print('[INFO] NON MAX SUPPRESSION: ', coordinate)
    if not os.path.exists(os.path.abspath(args.folder_save_detection)):
        os.makedirs(os.path.abspath(args.folder_save_detection))
    cv2.imwrite(os.path.join(os.path.abspath(args.folder_save_detection), 'myresults.jpg'), image)
    # except Exception:
    #     text1 = ["NOTICE"]
    #     text2 = [["PLEASE TRY AGAIN !"], ["SUGGESTION: PUT YOUR IMAGE INCLUDING BACKGROUND"]]
    #     print(tabulate(text2, text1, tablefmt="pretty"))

if __name__ == '__main__':
    args = parse_arg()
    main(args)
    print(os.path.abspath(ROOT))

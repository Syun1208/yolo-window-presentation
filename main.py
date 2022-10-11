from weights.load_weights import weights
from utils.get_coordinate_yolo import detection
from utils.non_max_suppression import nms
import argparse
import numpy as np
import cv2
import tqdm
from tabulate import tabulate

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, help='initial weights path', default='weights/yolov7/best.onnx')
    parser.add_argument('--cfg-detection', type=str, help='model configuration: yolov5, yolov7', default='yolov5')
    parser.add_argument('--img_path', type=str, help='Image path')
    parser.add_argument('--folder_path', type=str, help='Folder mage path')
    parser.add_argument('--folder_save', type=str,
                        default='/home/long/Downloads/datasets/datasetsRotation/correctingImages', required=False)
    parser.add_argument('--option', type=int, help='activate 1 to open camera or 0 to add image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument("--coordinate", "--coords", help="comma seperated list of source points")
    return parser.parse_args()

def predict(image):
    pretrainedModel = weights()
    coordinateBoundingBox = []
    classes = ['top-cmnd', 'back-cmnd', 'top-cccd', 'back-cccd', 'top-chip', 'back-chip', 'passport', 'rotate']
    weightPath = 'weights/yolov5m/best.pt'
    pretrainedYOLO = pretrainedModel.modelYOLOv5(weightPath)
    modelYOLO = detection(cv2.imread(image))
    coordinate, score, name, image = modelYOLO.v5(pretrainedYOLO)
    coordinate, score = nms(coordinate, score, 0.4)
    try:
        for i in tqdm.tqdm(range(len(name)), total=len(name)):
            coordinate[i] = np.array(coordinate[i])
            results = {"class_id": classes.index(name[i]), "class_name": name[i],
                    "bbox_coordinates": coordinate[i].tolist(),
                    "confidence_score": score[i]}
            coordinateBoundingBox.append(results)
        return coordinateBoundingBox, image
    except Exception:
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
    cv2.imwrite('/home/long/Downloads/datasets/datasetsRotation/correctingImages/my1.jpg', image)
    try:
        pass
    except Exception:
        text1 = ["NOTICE"]
        text2 = [["PLEASE TRY AGAIN !"], ["SUGGESTION: PUT YOUR IMAGE INCLUDING BACKGROUND"]]
        print(tabulate(text2, text1, tablefmt="pretty"))

if __name__ == '__main__':
    args = parse_arg()
    main(args)

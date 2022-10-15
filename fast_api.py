import cv2
import io
import base64
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, APIRouter, File, Form, Body
import argparse
from typing import List, Union
from main import predict
import numpy as np
from pathlib import Path
import os
import sys
app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>"""
app = FastAPI(title="Chúa tể phát hiện cccd/cmnd", description=app_desc)
DETECTION_URL = '/id-card-yolo/detect/'
FILE = Path(os.path.dirname(__file__)).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, help='initial weights path', default='weights\\best.pt')
    parser.add_argument('--local_host', type=str, help='your local host connection', default='0.0.0.0')
    parser.add_argument('--folder_save_detection', type=str,
                        default=str(ROOT / 'results/detect'),
                        required=False)
    parser.add_argument('--port', type=int, help='your port connection', default=8000)
    return parser.parse_args()

# def base64str_to_PILImage(predictedImage):
#     base64_img_bytes = base64.b64encode(predictedImage).decode('utf-8')
#     base64bytes = base64.b64decode(base64_img_bytes)
#     bytesObj = io.BytesIO(base64bytes)
#     img = Image.open(bytesObj)
#     return img
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    img_data = base64.b64encode(buffer)
    return img_data
@app.post(DETECTION_URL)
async def detect(image: UploadFile = File(...)):
    args = parse_arg()
    if image.filename.split('.')[-1] in ("jpg", "jpeg", "png"):
        pass
    else:
        raise HTTPException(status_code=415, detail="Item not found")
    contents = await image.read()
    array = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(array, cv2.IMREAD_COLOR)
    coordinateBoundingBox, predictedImage = predict(img, image.filename, args)
    encoded_string = image_to_base64(predictedImage)
    return coordinateBoundingBox, {"encoded_image": encoded_string}
@app.get('/')
async def read():
    return {"message": 'chào mừng đến với bình nguyên vô tận'}

if __name__ == '__main__':
    args = parse_arg()
    app_str = 'fast_api:app'
    uvicorn.run(app_str, host=args.local_host, port=args.port, reload=True, workers=1)
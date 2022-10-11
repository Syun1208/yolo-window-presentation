import sys
sys.path.insert(0, '/home/long/Desktop/AdvancedTopicInCE/yolov5')
import torch
from yolov5.utils.downloads import attempt_download
from yolov5.utils.general import intersect_dicts
from yolov5.models.common import DetectMultiBackend

class weights:
    def __init__(self):
        self.cuda = True
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.cuda else ['CPUExecutionProvider']
        self.names = ['top-cmnd', 'back-cmnd', 'top-cccd', 'back-cccd', 'top-chip', 'back-chip', 'passport', 'rotate']
    def modelYOLOv5(self, path, classes=8):
        model = DetectMultiBackend(path, device=self.device, fuse=True)
        ckpt = torch.load(attempt_download(path), map_location=self.device)  # load
        csd = ckpt['model'].float().state_dict()  # checkpoint state_dict as FP32
        csd = intersect_dicts(csd, model.state_dict(), exclude=['anchors'])  # intersect
        model.load_state_dict(csd, strict=False)
        if len(ckpt['model'].names) == classes:
            model.names = ckpt['model'].names
        return model.to(self.device)
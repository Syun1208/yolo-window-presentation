import torch
import cv2

class detection:
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.imageSave = cv2.resize(image, (640, 640))
        # self.fileSave = os.path.splitext(image.split('/')[-1])
        # self.folderSave = os.path.join(list(image.split('/')).pop(-1))
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.names = ['top_left', 'top_right', 'bottom_right', 'bottom_left']

    def v5(self, modelDetection):
        listCoordinate = []
        self.image = cv2.resize(self.image, (640, 640))
        resultsDetection = modelDetection(self.image)
        # resultsDetection.show()
        print('\n', resultsDetection.pandas().xyxy[0])
        names = list(resultsDetection.pandas().xyxy[0]['name'])
        '''Calculate predicted bounding box'''
        for i in range(len(resultsDetection.xyxy[0])):
            x_min = int(resultsDetection.xyxy[0][i][0])
            # x_min = np.where(x_min < 0, 0, x_min)
            y_min = int(resultsDetection.xyxy[0][i][1])
            # y_min = np.where(y_min < 0, 0, y_min)
            x_max = int(resultsDetection.xyxy[0][i][2])
            # x_max = np.where(x_max > self.image.shape[1], 0, x_max)
            y_max = int(resultsDetection.xyxy[0][i][3])
            # y_max = np.where(y_max > self.image.shape[0], 0, y_max)
            cv2.rectangle(self.imageSave, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)
            cv2.putText(self.imageSave, names[i], (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        [225, 255, 255], thickness=3)
            listCoordinate.append([x_min, y_min, x_max, y_max, names[i]])
        return listCoordinate, list(resultsDetection.pandas().xyxy[0].confidence[:]), names, self.imageSave
import requests
import argparse
import json


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_host', type=str, help='your local host connection', default='0.0.0.0')
    parser.add_argument('--port', type=str, help='your port connection', default='8000')
    # parser.add_argument('--option', type=str, help='option (yes) to show encoded image, else not show',
    #                     default='no')
    parser.add_argument('--image', type=str, help='image path', default='/home/long/Downloads/long.jpg')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arg()
    url = 'http://' + args.local_host + ':' + args.port + '/id-card-yolo/detect/'
    # with open(args.image, "rb") as image_file:
    #     data = base64.b64encode(image_file.read()).decode('utf-8')
    option = input('Do you want to show encoded image[Y/N]: ')
    file = {'image': open(args.image, 'rb')}
    data = {'option': option}
    response = requests.post(url=url, files=file, params=data)
    with open('/home/long/Desktop/base64.json', 'w') as fileSave:
        json.dump(response.json(), fileSave, indent=4)
    # fileSave.write(json_object)
    # response = requests.post(
    #     url='http://10.40.2.223:8000/yolo-id-card/request/',
    #     data=str(data)
    # )
    # image_name = os.path.basename(args.image)
    # response = requests.post(
    #     url='http://10.40.2.223:8000/id-card-yolo/detect/',
    #     data={
    #         "image": data,
    #         "image_name": image_name
    #     }
    # )
    #
    # # Print output
    print(requests.status_codes, response.json())

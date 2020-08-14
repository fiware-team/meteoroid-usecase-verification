import io
import json
import tempfile
import threading

import requests

import cv2
from flask import Flask, request


app = Flask(__name__)


@app.route('/image', methods=['POST'])
def update():
    body = request.json
    update_image(body['url'])
    return ""


def image_read_from_url(url):
    res = requests.get(url)
    img = None
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


def update_image(url):
    img = image_read_from_url(url)
    cv2.imshow("Loaded image", img)
    return


if __name__ == '__main__':
    init_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': '5000'})
    init_thread.start()

    url = 'http://192.168.28.10:30007/images/image1.jpeg'
    img = image_read_from_url(url)
    cv2.namedWindow("Loaded image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Loaded image", 500, 500)
    cv2.imshow("Loaded image", img)
    if cv2.waitKey() & 0xff == 27: quit()

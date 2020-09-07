import io
import json
import tempfile
import threading

import requests

import cv2
from flask import Flask, request


app = Flask(__name__)


@app.route('/image', methods=['POST'])
def update_image():
    body = request.json
    img = image_read_from_url(body['url'])
    cv2.imshow("Loaded image", img)
    return {'status': 'success'}


def image_read_from_url(url):
    res = requests.get(url)
    img = None
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


if __name__ == '__main__':
    init_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': '5000'})
    init_thread.start()

    url = 'https://prtimes.jp/data/corp/18705/tmp-e7e85f4f14675d37ecb0f9a80369cb4c-847d679de842d94ad6f9b6b165580419.jpg'
    img = image_read_from_url(url)
    cv2.namedWindow("Loaded image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Loaded image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Loaded image", img)
    if cv2.waitKey() & 0xff == 27: quit()

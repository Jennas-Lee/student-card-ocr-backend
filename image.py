import base64
import os
from cv2 import cv2
import numpy as np
# import matplotlib.pyplot as plt
import requests


class Image:
    def __init__(self, websocket, image_data):
        self.websocket = websocket
        self.image_data = image_data
        self.image_byte_data = None

    async def main(self):
        await self.websocket.send('{"progress": 50, "message": "사진 전송 성공"}')
        await self.websocket.send('{"progress": 60, "message": "이미지 전처리중"}')
        self.base64ToCv2()
        await self.websocket.send('{"progress": 70, "message": "OCR 처리중"}')
        self.ocr()
        await self.websocket.send('{"progress": 80, "message": "OCR 처리 완료"}')
        await self.websocket.send('{"progress": 90, "message": "OCR 검증 중"}')
        #   sagemaker를 통한 모델 검증
        await self.websocket.send('{"progress": 100, "message": "OCR 검증 완료"}')

    def base64ToCv2(self):
        decoded_data = base64.b64decode(self.image_data)
        np_arr = np.fromstring(decoded_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
        cv2_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        x = cv2_img.shape[0]
        y = int(cv2_img.shape[0] / 1.58 / 2)
        y_middle = int(cv2_img.shape[1] / 2)

        resize_img = cv2_img[0:x, y_middle - y:y_middle + y].copy()
        resize_img = cv2.rotate(resize_img, cv2.ROTATE_90_CLOCKWISE)
        resize_img = cv2.resize(resize_img, None, fx=1024.0 / x, fy=1024.0 / x)

        ocr_img = cv2.imencode(".jpg", resize_img)[1]

        self.image_byte_data = ocr_img.tobytes()

        # plt.figure()
        # plt.imshow(resize_img)
        # plt.show()

        print("DONE")

    def ocr(self):
        API_URL = "https://dapi.kakao.com/v2/vision/text/ocr"
        appkey = os.environ.get('KAKAO_AK')

        headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

        ocr_data = requests.post(API_URL, headers=headers, files={"image": self.image_byte_data}).json()

        print(ocr_data)

import json

from sys import argv
from math import *
import cv2, os
import numpy as np
from urllib import request as urlRequest
# import pyzbar.pyzbar as pyzbar

import boto3
s3 = boto3.client('s3')
# bucket=os.getenv("AWS_S3_BUCKET")
bucket='snn-a360-storage' #os.getenv("AWS_S3_BUCKET")

# 解析图片中的条形码和二维码
def detectBarcode(image):
    import pyzbar.pyzbar as pyzbar
    # 识别图中的码，加入到集合中
    result = []
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    texts = pyzbar.decode(gray)
    for text in texts:
        tt = text.data.decode("utf-8")
        result.append(tt)
    #旋转45度
    image = rotate_bound_white_bg(image, 45)
    texts = pyzbar.decode(image)
    for text in texts:
        tt = text.data.decode("utf-8")
        result.append(tt)
    # 旋转90度
    image = rotate_bound_white_bg(image, 45)
    
    texts = pyzbar.decode(image)
    for text in texts:
        tt = text.data.decode("utf-8")
        result.append(tt)

    #去重
    resultForReturn = []
    resultForReturn = list(set(result))
    return resultForReturn


# 旋转angle角度，缺失背景白色（255, 255, 255）填充
def rotate_bound_white_bg(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    # -angle位置参数为角度参数负值表示顺时针旋转; 1.0位置参数scale是调整尺寸比例（图像缩放参数），建议0.75
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    # borderValue 缺失背景填充色彩，此处为白色，可自定义
    return cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))
    # borderValue 缺省，默认是黑色（0, 0 , 0）
    # return cv2.warpAffine(image, M, (nW, nH))


def lambda_handler(event, context):
    os.environ['PATH'] = os.environ['PATH'] + ":/opt/lib/x86_64-linux-gnu/"
    os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ":/opt/lib/x86_64-linux-gnu/"
    print("PATH:>",os.environ)

    print("event", event)
    print("context", context)
    #request_data = event['queryStringParameters']
    #imgurl = request_data['imgURL']
    response = s3.get_object(
        Bucket=bucket,
        Key="image/2023-03-08/tmp_9a049da155b010e00bd959f8514d02aeeeded6a1ea09d96f.jpg",
    )
    image = np.asarray(bytearray(response['Body'].read()), dtype="uint8")
    result = detectBarcode(image)
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

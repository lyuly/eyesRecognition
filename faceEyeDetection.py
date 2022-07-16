import numpy as np
import cv2
import os
import sys
from PIL import Image

def captureImg():
    cap = cv2.VideoCapture(0)
    cap.set(3,600)
    cap.set(4,480)
    img = cap.read()
    cv2.show('video', img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
    cap.release()
    cv2.destroyAllWindows()

def isSupporttedImgExt(imgName):

    portion = os.path.splitext(imgName)
    if portion[1] == '.jpg':
        return '.jpg'
    elif portion[1] == '.JPG':
        return '.JPG'
    elif portion[1] == '.JPEG':
        return '.JPEG'
    elif portion[1] == '.png':
        return '.png'
    elif portion[1] == '.PNG':
        return '.PNG'
    else:
        return False

# 裁剪图片
def cutImg(thisDir, imgName, id, x, y, w, h):

    imgPath = os.path.join(thisDir, imgName)
    if os.path.exists(imgPath) != True:
        print('cutImg:没有找到要被裁剪文件.')
        return
    ext = isSupporttedImgExt(imgName)
    name = imgName.replace(ext, '_'+str(id)+ext)
    # 裁切后的目录名称，它在thisDir下面
    cropImgDirName = 'crops'
    cropImgDir = os.path.join(thisDir, cropImgDirName)
    cropedImgName = os.path.join(cropImgDir, name)
    # 存在同名的文件，目前的策略是返回，不再生成
    if os.path.exists(cropedImgName) == True:
        return
    if os.path.exists(cropImgDir) != True:
        os.mkdir(cropImgDir)
    elif os.path.isdir(cropImgDir) != True:
        os.mkdir(cropImgDir)
    
    # 打开特定图片，裁切后保存
    Image.open(imgPath).crop((x, y, (x+w), (y+h))).save(cropedImgName)

def main(args):
    # 获取用户从命令行输入的参数
    imgName = args[0]
    if isSupporttedImgExt(imgName) == False:
        print('不支持这种文件！')
        return 0
    thisDir = os.getcwd()
    imgPath = os.path.join(thisDir, imgName)
    if os.path.exists(imgPath) != True:
        print('main:没找到要探测的文件.')
        return

    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
    
    # cap = cv2.VideoCapture(0)
    # cap.set(3,640) # set Width
    # cap.set(4,480) # set Height

    while True:
        # ret, img = cap.read()
        # img = cv2.flip(img, 1)
        img = cv2.imread(imgPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,      
            minSize=(30, 30)
        )
        # print("找到{0}张人脸！".format(len(faces)))

        # detectedId = 0   
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eyeCascade.detectMultiScale(
                roi_gray,
                scaleFactor= 1.1,
                minNeighbors=5,
                minSize=(6, 6),
                )
            print("找到{0}只眼睛！".format(len(eyes)))
                     
            detectedId = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                print("x={0},y={1},dx={2},dy={3}".format(ex, ey, ew, eh))
            # print("x={0},y={1},dx={2},dy={3}".format(x, y, w, h))
                detectedId = detectedId + 1
            # cv2.imwrite()
                cutImg(thisDir, imgName, detectedId, ex, ey, ew, eh)

            # cv2.imshow('video', img)
        if len(args) > 1:
            cv2.imshow("Face Detect: {0}".format(len(faces)), img)
            c = cv2.waitKey(0)
            if 'ESC' == chr(c & 255):
                cv2.destroyAllWindows()
        else:
            cv2.destroyAllWindows()

        # k = cv2.waitKey(30) & 0xff
        # if k == 27: # press 'ESC' to quit
            # break

    # cap.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv[1:])
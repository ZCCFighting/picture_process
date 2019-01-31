import cv2 as cv 
import numpy 
import math 
import re
import exifread
import gdal
import numpy as np
import skimage.io

def latitude_and_longitude_convert_to_decimal_system(*arg):
    """
    经纬度转为小数, 作者尝试适用于iphone6、ipad2以上的拍照的照片，
    :param arg:
    :return: 十进制小数
    """
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)

def find_GPS_image(pic_path):
    GPS={}
    date=''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('GPS GPSLatitudeRef', tag):
                GPS['GPSLatitudeRef'] = str(value)
            elif re.match('GPS GPSLongitudeRef', tag):
                GPS['GPSLongitudeRef'] = str(value)
            elif re.match('GPS GPSAltitudeRef', tag):
                GPS['GPSAltitudeRef'] = str(value)
            elif re.match('GPS GPSLatitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSLongitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
            elif re.match('.*Date.*', tag):
                date = str(value)
    return {'GPS_information': GPS, 'date_information': date}
def imageread(pic_path):
    GPS={}
    date=''
    f=open(pic_path,'rb')
    imagetext=exifread.process_file(f)
    #for key in imagetext:
        #print(key,":",imagetext[key])
    print('************************\n************************')
    for q in imagetext:
        if q=="GPS GPSLatitude":
            print("GPS经度=",imagetext[q],imagetext['GPS GPSLatitudeRef'])
        elif q=="GPS GPSLongitude":
            print("GPS纬度=",imagetext[q],imagetext['GPS GPSLongitudeRef'])
            print(type(imagetext[q]))
        elif q=="GPS GPSAltitude":
            print("GPS高度=",imagetext[q])           
        elif q=='Image DateTime':
            print("拍摄时间=",imagetext[q])
def get_pic_size(pic_path):
    img=cv.imread(pic_path)
    sp=img.shape
    Pheignt=sp[0]
    Pwidth=sp[1]
    return{'Pheight':Pheignt,'Pwidth':Pwidth}
def get_video_size(video_path):
    cap = cv.VideoCapture(video_path)
    width=int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv.CAP_PROP_FPS)
    while(True):
        ret,frame=cap.read()
        font=cv.FONT_HERSHEY_SIMPLEX
        str1='video_height:'+str(height)+'   '+'video_width:'+str(width)+'   '+'video_fps:'+str(fps)
        cv.putText(frame,str1,(10,30),font,0.5,(255,255,255),1)
        cv.imshow('video',frame)
        k=cv.waitKey(5)&0xFF
        if k==27:
            cv.destroyAllWindows()
            break 
    cap.release()
    cv.destroyAllWindows()
    #return {'video_height':height,'video_width':width,'video_fps':fps}




show=get_video_size(0)
#imageread('test.JPG')
print(show)
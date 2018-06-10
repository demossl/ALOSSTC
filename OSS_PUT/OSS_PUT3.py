#-*- coding:utf-8: -*-
Auther = "Demons"
Blog = "https://www.lsowl.xyz"
data = "2018.6.10"
version = "V2.0 Beta"

"""
    所依赖的第三方库说明：
        win32con 和 win32clipboard ：安装了pywin32即可使用
        PIL ：图像处理库
        oss2 ：阿里云官方 OSS SDK
        第三方HTTP库请求和crcmod   oss2所依赖的第三方库（Windows上面可能安装不上C扩展模式，但并影响使用）
    安装：
        pip install pywin32
        PIL在Windows上面安装有点问题，所以直接下载exe安装
        pip install oss2     会默认安装所依赖的第三方库
"""
import win32con
import win32clipboard as w
from PIL import ImageGrab
from PIL import Image
import os,time,sys,random
import oss2
import shutil

sys.path.append(os.path.dirname(__file__))

class OSS_Intelligent_Upload(object):
    def __init__(self,acc_id,acc_secret,bucket_name,endpoint):
        self.acc_id = acc_id
        self.acc_secret = acc_secret
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    #将返回的图片地址复制到粘贴板
    def setText(self,aString):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT,aString)  #win32con.CF_TEXT在Python2里面可以全部写入，py3里面貌似只能写入首个字符
        w.CloseClipboard()

    #从粘贴板获取图片，并保存到本地，文件名为时间戳
    def ImageSave(self):
        im = ImageGrab.grabclipboard()      #从粘贴板获取内容
        if isinstance(im,Image.Image):      #判断是不是图片
            name = str(time.time()) + ".png"
            print ("[+] 生成本地图片路径:" + name)
            if not os.path.exists("image"):
                os.mkdir("image")
            path = ("image/" + name)
            im.save(path)
            print ("[+] 图片准备上传！")
            self.upload(path,name)

    def upload(self,file_name,name):
        bucket = oss2.Bucket(oss2.Auth(self.acc_id,self.acc_secret),self.endpoint,self.bucket_name)
        data = bucket.put_object_from_file(key='Blog/'+ name,filename='image/'+ name, headers=None, progress_callback=None)
        str = "https://demos-qq.oss-cn-beijing.aliyuncs.com/Blog/" + name  #由于官方的SDK不提供获取文件访问地址的接口，所以采用这种固有的模式连接
        msk =  r'![]({})'.format(str)                                      #将字符串格式化成makedown插入图片的语法
        self.setText(msk)
        print ("[+] 上传成功，已将地址复制到粘贴板")
        print ("[+] 正在监听...")
        shutil.rmtree('image')

def main():
    # 从外部吸取config.conf内容
    try:
        infoDict = {}
        with open("config.conf","r") as file:
            ApiInfo = file.readlines()
            for info in ApiInfo:
                try:
                    if info != "\n" and info != "":
                        tmp = info.split("=")
                        infoDict[tmp[0].strip()] = tmp[1].strip()
                except Exception as e:
                    print ("[-] 请按照要求配置config.conf")
                    sys.exit()
    except Exception as e:
        print ("[-] 请在config.conf中配置阿里云 API信息")
        sys.exit()

    # 配置API信息
    acc_id = infoDict["acc_id"]
    acc_secret = infoDict["acc_secret"]
    endpoint = infoDict["endpoint"]
    bucket_name = infoDict["bucket_name"]
    oss = OSS_Intelligent_Upload(acc_id,acc_secret,bucket_name,endpoint)
    print("""
                                     _    _     ___  ____ ____ _____ ____
                                    / \  | |   / _ \/ ___/ ___|_   _/ ___|
                                   / _ \ | |  | | | \___ \___ \ | || |
                                  / ___ \| |__| |_| |___) |__) || || |___
                                 /_/   \_\_____\___/|____/____/ |_| \____|

                                                           Author : Demons
                                                       Version : V2.0 Beta
                                              Blog : https://www.lsowl.xyz
    """)
    print ("[+] 正在监听...")
    while True:
        oss.ImageSave()
        time.sleep(random.random())

if __name__ == '__main__':
    main()

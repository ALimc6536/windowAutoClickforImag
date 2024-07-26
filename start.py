
import cv2
import numpy as np
import pyautogui
import cv2
import win32con
import win32gui
import time
import json




imgzuofan=cv2.imread('.\\src\\zuofan.jpg')
imgtysl=cv2.imread('.\\src\\tianyuanshala.jpg')
imgkspr=cv2.imread('.\\src\\kaishipengren.jpg')
imgcz=cv2.imread('.\\src\\chanzi.jpg')
imgnf=cv2.imread('.\\src\\nafan.jpg')

data=json.load(open('info.json','r',encoding='utf-8'))
appWindowW=data['windowSize'][0]
appWindowH=data['windowSize'][1]


# 获取窗口截图
def getScreenshotAsHwnd(hwnd):
    '''获取窗口截图'''
    # 最小化 (-32000, -32000, 237, 39)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return cv2.cvtColor(
        np.asarray(
            pyautogui.screenshot(region=(
                left, top, right - left, bottom - top
            ))
        ),
        cv2.COLOR_RGB2BGR
    )
# 点击窗口
def clickWindow(hwnd, x, y):
    win32gui.SetForegroundWindow(hwnd)
    mousex, mousey = pyautogui.position()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    pyautogui.moveTo(left+x, top+y)
    pyautogui.click()
    pyautogui.moveTo(mousex, mousey)
# 图片分析
def getTemplateImageInImage(templateImage,image,
        threshold=0.8,
        type_='rectangle+avgpos',
        rectangleColor=(255, 0, 0)
    ):
    '''
    type:

        rectangle返回画框的图片

        avgpos返回平均坐标

        rectangle+avgpos返回画框的图片和平均坐标

    '''
    try:
        res = cv2.matchTemplate(image, templateImage, cv2.TM_CCOEFF_NORMED)
    except:
        return None, None
    else:
        h, w = templateImage.shape[:2]
        if type_=='rectangle':
            while (val:=cv2.minMaxLoc(res))[1]>=threshold:
                res[val[3][1]][val[3][0]]=0
                br=(val[3][0]+w,val[3][1]+h)
                cv2.rectangle(image, val[3], br, rectangleColor, 5)
            return image, None
        elif type_=='avgpos':
            avgs=[]
            while (val:=cv2.minMaxLoc(res))[1]>=threshold:
                res[val[3][1]][val[3][0]]=0
                avg=((
                    int(val[3][0]*2+w)/2,
                    int(val[3][1]*2+h)/2
                ))
                avgs.append(avg)
            return None, avgs
        elif type_=='rectangle+avgpos':
            avgs=[]
            while (val:=cv2.minMaxLoc(res))[1]>=threshold:
                res[val[3][1]][val[3][0]]=0
                br=(val[3][0]+w,val[3][1]+h)
                avg=((int(val[3][0]+br[0])/2, int(val[3][1]+br[1])/2))
                avgs.append(avg)
                cv2.rectangle(image, val[3], br, rectangleColor, 5)
            return image,avgs
# 调整窗口大小
def adjustWindow(hwnd, width, height):
    win32gui.SetWindowPos(hwnd,
        win32con.HWND_TOPMOST,
        0, 0, width, height,
        win32con.SWP_SHOWWINDOW+win32con.SWP_NOMOVE)

# while 1:
#     cv2.waitKey(25)
#     cv2.imshow('window', getScreenshotAsHwnd(win32gui.FindWindow(data['winClass'], data['winName'])))

   
print('按k键启动/暂停程序')
run=False
appHwnd=None
steps:list=list(data['steps'])
item=[None]
appHwnd = win32gui.FindWindow(data['winClass'], data['winName'])
if appHwnd:
    adjustWindow(appHwnd, appWindowW, appWindowH)
    #前置窗口
    win32gui.SetForegroundWindow(appHwnd)
while 1:
    appHwnd = win32gui.FindWindow(data['winClass'], data['winName'])
    if not appHwnd:
        print("找不到窗口，类：", data['winClass'], "标题：", data['winName'])
        time.sleep(1)
        continue
    appScreenshot=getScreenshotAsHwnd(appHwnd)
    if run:
        #前置窗口
        # win32gui.SetForegroundWindow(appHwnd)
        if not steps:
            print('一次循环完成')
            steps=list(data['steps'])
        if len(item)==1:
            if item[0]:print(item[0],' 进行完成')
            item=steps.pop(0)
        
        if item[1]=='number':
            assert type(item[2])==int, item[2]+'要求为int类型'
            assert type(item[3])==str, item[3]+'要求为str类型'
            rectangle, avgpos=getTemplateImageInImage(
                cv2.imread('.\\src\\'+item[3]),
                appScreenshot
            )
            if not avgpos:
                print('未找匹配内容', item[3])
            else:
                if appWindowW>0 and appWindowH>0:
                    adjustWindow(appHwnd, appWindowW, appWindowH)
                clickWindow(appHwnd, avgpos[0][0], avgpos[0][1])
                item[2]-=1
                if item[2]<=0:item=[item[0]]
        elif item[1]=='waitFor':
            rectangle, avgpos=getTemplateImageInImage(
                cv2.imread('.\\src\\'+item[2]),
                appScreenshot
            )
            if avgpos:
                print('由于', item[2] ,'出现，结束', item[0],'执行')
                item=[item[0]]
            else:
                print('由于', item[2] ,'未出现，检查', item[3],'出现')
                rectangle, avgpos=getTemplateImageInImage(
                    cv2.imread('.\\src\\'+item[3]),
                    appScreenshot
                )
                if avgpos:
                    if appWindowW>0 and appWindowH>0:
                        adjustWindow(appHwnd, appWindowW, appWindowH)
                    clickWindow(appHwnd, avgpos[0][0], avgpos[0][1])
                    if len(item)>=5:
                        time.sleep(item[4])
                else:
                    print('等待', item[3],'出现以点击')
        elif item[1]=='sleep':
            print('根据', item[0],'等待', item[2],'秒')
            time.sleep(item[2])
            item=[item[0]]
        else:
            print('未知的指示：', item[1])
    else:
        ...

    if cv2.waitKey(30) & 0xFF == ord('r'):
        run=False
        steps=data['steps']
        item=[None]
        print('程序已停止')
        print('步骤已重置')
    if cv2.waitKey(30) & 0xFF == ord('k'):
        run= not run
        if run:
            print('程序已启动')
        else:
            print('程序已停止')
    if cv2.waitKey(30) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    cv2.imshow('window', appScreenshot)



quit(0)

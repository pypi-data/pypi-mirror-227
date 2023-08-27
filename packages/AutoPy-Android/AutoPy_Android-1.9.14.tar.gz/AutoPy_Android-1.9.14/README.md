
# 1. AutoPy文档

## 1.2. 目录
autoauto- [1. AutoPy文档](#1-autopy文档)auto    - [1.1. 目录](#11-目录)auto    - [1.2. 简介](#12-简介)auto    - [1.3. 捐赠AutoPy](#13-捐赠autopy)auto    - [1.4. 安装](#14-安装)auto    - [1.5. APK下载地址](#15-apk下载地址)auto    - [1.6. AutoPy](#16-autopy)auto    - [1.7. AutoPy Lite（推荐使用，快，稳，准，狠）](#17-autopy-lite推荐使用快稳准狠)auto    - [1.8. 端口号](#18-端口号)auto        - [1.8.1. AutoPy Lite ：8020](#181-autopy-lite-8020)auto        - [1.8.2. AutoPy ：33445](#182-autopy-33445)auto    - [1.9. 快速开始](#19-快速开始)auto    - [1.10. 准备](#110-准备)auto                - [1.10.0.0.1. 安装模块](#110001-安装模块)auto                - [1.10.0.0.2. 开启无障碍辅助权限](#110002-开启无障碍辅助权限)auto                - [1.10.0.0.3. 显示指针位置](#110003-显示指针位置)auto    - [1.11. 测试](#111-测试)auto    - [1.12. 导入](#112-导入)auto    - [1.13. 使用](#113-使用)auto        - [1.13.1. AutoPy.tap(X,Y)](#1131-autopytapxy)auto        - [1.13.2. AutoPy.swipe(x1,y1,x2,y2,t)](#1132-autopyswipex1y1x2y2t)auto        - [1.13.3. AutoPy.gesturer([x1,y1,x2,y2,...,t])](#1133-autopygesturerx1y1x2y2t)auto                    - [1.13.3.0.3.1. .](#1133031-)auto        - [1.13.4. AutoPy.capturer()](#1134-autopycapturer)auto        - [1.13.5. AutoPy.StartServer()](#1135-autopystartserver)auto        - [1.13.6. AutoPy.HOME()](#1136-autopyhome)auto        - [1.13.7. AutoPy.RECENTS()](#1137-autopyrecents)auto        - [1.13.8. AutoPy.BACK()](#1138-autopyback)auto        - [1.13.9. AutoPy.openapp()](#1139-autopyopenapp)auto        - [1.13.10. AutoPy.getID()](#11310-autopygetid)auto        - [1.13.11. AutoPy.getText()](#11311-autopygettext)auto        - [1.13.12. AutoPy.getView()](#11312-autopygetview)auto        - [1.13.13. AutoPy.Locker()](#11313-autopylocker)auto        - [1.13.14. 悬浮窗和Toast功能](#11314-悬浮窗和toast功能)auto        - [1.13.15. AutoPy.floatWindowOpenApi()](#11315-autopyfloatwindowopenapi)auto    - [1.14. 录制教学功能](#114-录制教学功能)auto    - [1.15. 最后所有方法实现代码](#115-最后所有方法实现代码)auto                - [1.15.0.0.4. 更多功能持续开发中......](#115004-更多功能持续开发中)auto                - [1.15.0.0.5. QQ群:540717901](#115005-qq群540717901)autoauto

## 1.3. 简介
> ``AutoPy``是为python开发者提供的一个安卓插件,主要功能为了实现使用python在安卓端完成一些操作,例如点击,滑动,返回，吐司。。。
## 1.4. 捐赠AutoPy
我们利用有限的业余时间设计了 AutoPy，虽然它并不那么美好，但正努力前行。

如果你喜欢我们的作品，可以捐赠来支持我们。


![avatar](https://img2020.cnblogs.com/blog/1150532/202101/1150532-20210108180802579-1522943811.png)

**所有的捐赠都将用来：提升AutoPy的功能以及开发的积极性。**

**联系方式：
QQ：1019157263
QQ群：1019924151,540717901**


<!-- 支付宝: 18381801393

PayPal: wiar1824@gmail.com -->

## 1.5. 安装
```shell
pip install AutoPy-Android -i https://pypi.python.org/simple
```
## 1.6. APK下载地址
## 1.7. AutoPy（因设计缺陷已停止更新，推荐使用AutoPy Lite）
    https://www.coolapk.com/apk/260916
## 1.8. AutoPy Lite（全新优化引擎，无设计缺陷，推荐使用，快，稳，准，狠）
    https://www.coolapk.com/apk/276714
    #如酷安链接被ban，请加群获取
    QQ群：1019924151
## 1.9. 端口号
### 1.9.1. AutoPy Lite ：8020
### 1.9.2. AutoPy ：33445
## 1.10. 快速开始
下面演示了AutoPy Lite的一个使用例子,该示例实现了在android上画圆.
其中 a,b 表示圆心坐标, r 表示半径.
本示例中 使用了 AutoPy 中的悬浮窗接口方法 `AutoPy.floatWindowOpenApi()` 和 手势方法 `AutoPy.gesturer()`.
这两个方法将在后续的文档中介绍.
```python
import AutoPy_Android as AutoPy

AutoPy.server_url="http://127.0.0.1:8020/?code="
#同一局域网下的安卓设备地址,wifi就可以
# AutoPy端口为33445
# AutoPy Lite端口为8020

a=535
b=1696
r=100

li=[]

for x in range(a-r,a+r):
    y=int((((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)
    

for x in range(a+r,a-r,-1):
    y=int(-1*(((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)

li.append(4000)#执行速度
AutoPy.gesturer(li)

# 接下来是悬浮窗UI
Butt=AutoPy.FloatButton("b1")#按钮控件
Butt.View["Y"]="1000"
Butt.delete()
Butt.show()

A=AutoPy.FloatWindow("a1")
A.View["Y"]="800"
A.delete()
A.show()

info_O = Butt.getinfo()
N=0
while True:
    info_N = Butt.getinfo()
    print(info_N,end="\r")
    if info_N != info_O:
        print("已点击")
        AutoPy.gesturer(li)
        N+=1
        A.View["text"]=f"已点击{N}下"
        A.modify()
    info_O=info_N

```

## 2022年3月28日更新
`1.通知亮屏`\
`2.编辑框输入文本`
## 1.通知接口
为了在无root环境下实现亮屏，该接口可用来对手机亮屏，设置通知来时亮屏即可
```python
#接口格式：http://127.0.0.1:8020/?code=Notice,[标题],[内容]
```
# 2.编辑框输入文本
实现输入功能
该功能有两个接口配合实现，
首先获取可以输入的控件，
再选择第几个进行设置
接口如下：
```
获取可以输入的控件信息：
http://127.0.0.1:8020/?code=getEditView

设置第0个控件内容
http://127.0.0.1:8020/?code=setEditView,0,设置的内容
返回修改成功
```

## 1.11. 准备
> 安装`AutoPy Lite.apk`,点击`安装模块`,开启`无障碍权限`,开启`开发者选项`中`显示指针位置`


##### 1.11.0.0.1. 安装模块
点击安装模块后会在`/sdcard/qpython`目录下写入 `AutoPy.py` 文件.
在`AutoPy.py` 文件中包含AutoPy中的所有方法,用户可以自行修改该文件,进行自定义操作.

用户可以将 `AutoPy.py` 文件移动到 用户自己的项目中去导入..

在本文的最后会给出AutoPy.py的方法实现代码.



##### 1.11.0.0.2. 开启无障碍辅助权限

AutoPy依赖android的无障碍辅助权限进行自动化操作.

Android 的辅助模式（Accessibility）功能非常的强大。基本上被获取到授权之后，可以监听手机上的任何事件，例如：屏幕点击、窗口的变化、以及模拟点击、模拟系统按键等等。

无障碍功能实现 点击 滑动 手势 等全局操作.

##### 1.11.0.0.3. 显示指针位置
PS:AutoPy不依赖此项功能,这项功能打开才能 "看到" 点击效果

1. 打开Android手机`“设置”`APP，点击`“关于手机”`。
2. 在`版本号`上连续点击5次，打开“开发者选项”。也有些手机在`“关于手机”`里找不到`“版本号”`条目，那么也可以点击其他类似的条目，比如`“软件版本”`。
3. 在“设置”APP里找到“开发者选项”，打开它。
4. 打开“指针位置”，这个时候可以在手机顶部看到以下一行说明：`P:0/0  X:0/0  Y:0/0  Xv:0:0  Yv:0:0  Prs:0:0  Size:0:0`。其中的X/Y冒号后面的值就是绝对坐标，这行表示坐标原点(0,0)，也就是手机左上角。这个时候在屏幕上点击某个位置，就可以看到该位置的坐标；如果在屏幕上划动，也可以看到划动的轨迹。
5. 比如用手指按在“某按钮”上，如下图所示，界面上显示一横一竖两条线，中间有个交叉的点，手机顶部有一行说明：`P:1/1  X:458  Y:647  Xv:0:0  Yv:0:0  Prs:0.25  Size:0.2`。这说明这个点的X坐标是458.6，Y坐标是647.7。
6. 有了坐标值，就可以利用它来做一些简单的自动化。比如利用命令`AutoPy.tap(458,647)`点击坐标(458，647)，从而自动打开“某按钮”。


## 1.12. 测试
> 完成准备工作后,点测试按钮,测试相应功能,若功能正常,请继续后面操作,若功能无响应,则检查准备工作

点击 AutoPy的`高级`按钮可以打开AutoPy的测试界面,
如果你`确保`你已经`打开了无障碍,显示指针位置` 等各种权限.那么你点击测试按钮时会看到相应的效果.
每一个测试按钮都有对应的相关的python方法接口,可以使用python 灵活的对方法编程.


## 1.13. 导入
> 完成上述操作后,模块路径`/sdcard/qpython/AutoPy.py` 进入目录导入模块
```shell
$ cd /sdcard/qpython  #进入目录
$ python  #启动python
$
```
```python
>>> import AutoPy_Android as AutoPy#导入模块
>>>
```
## 1.14. 使用
### 1.14.1. AutoPy.tap(X,Y)
> 点击指定位置

|参数|类型|说明|
|:-:|:-:|:-:|
|X|`int`| 点击位置x坐标 |
|Y|`int`| 点击位置y坐标 |



>
**示例:**
某 `铁匠铺游戏` 制作材料等均需要用手进行快速点击,所谓能者多得.勤劳致富.
**例: 刷`500`铁** 
该功能用 AutoPy 编程实现即用:

```python
import AutoPy_Android as AutoPy#导入模块

number=500
#点击次数
coordinate={
    #按钮坐标位置
    "x":400,
    "y":400,
}
for i in range(number):
    AutoPy.tap(coordinate["x"],coordinate["y"]) 
    #点击(400,400)位置
```
上述代码轻松实现刷铁工作的自动化,并且AutoPy的响应速度十分的快.

### 1.14.2. AutoPy.swipe(x1,y1,x2,y2,t)
> 滑动操作

|参数|类型|说明|
|:-:|:-:|:-:|
|x1|`int`| 起始位置x坐标 |
|y1|`int`| 起始位置y坐标|
|x2|`int`| 结束位置x坐标 |
|y2|`int`| 结束位置y坐标 |
|t|`int`| 执行时间(默认为8000毫秒) |



**示例:**
某 `画板` 工具上用手画直线十分的难画直,并且长度无法精确控制.

**例: 画边长为`500`的正方形** 
画一个正方形需要它的边长`定型尺寸`以外,我们还需要它的`定位尺寸` 也就是我们把 `边长500 `的正方形放在哪个位置.
以右下角`角点`定位为例.
因为要画4条边的正方形,所有需要调用4次`AutoPy.swipe()`方法.

该功能用 AutoPy 编程实现即用:

```python
import AutoPy_Android as AutoPy#导入模块

Corner_point={
    #右下角角点坐标,可以方便的修改坐标位置
    "x":100,
    "y":100,
}

lenth=500

AutoPy.swipe(Corner_point["x"],Corner_point["y"],Corner_point["x"]+lenth,Corner_point["y"])
#画第一条边
AutoPy.swipe(Corner_point["x"]+lenth,Corner_point["y"],Corner_point["x"]+lenth,Corner_point["y"]+lenth)
#画第二条边
AutoPy.swipe(Corner_point["x"]+lenth,Corner_point["y"]+lenth,Corner_point["x"],Corner_point["y"]+lenth)
#画第三条边
AutoPy.swipe(Corner_point["x"],Corner_point["y"]+lenth,Corner_point["x"]+lenth,Corner_point["y"])
#画第四条边

```

### 1.14.3. AutoPy.gesturer([x1,y1,x2,y2,...,t])
> 连续滑动操作

###### 1.14.3.0.3.1. .
 **注意:AutoPy.gesturer方法只有一个list(列表)参数**
**AutoPy.gesturer只能传入一个列表**

其中`list列表`数据格式如下
|参数|类型|说明|
|:-:|:-:|:-:|
|x1|`int`|起始位置x坐标|
|y1|`int`|起始位置y坐标|
|x2|`int`|结束位置x坐标|
|y2|`int`|结束位置y坐标|
|...|`int`|...|
|t [必须]|`int`|起始位置到结束位置持续时间|



**示例:**
上一个方法介绍了怎样画一个正方形,有些小伙伴就要问了,那怎么样画一个曲线呢,连续光滑的曲线.于是便有了`AutoPy.gesturer()`方法,可以传入多个坐标,实现画出连续光滑的曲线.可以制作迷宫,连连看,等游戏的自动化解题.
**例: 画`r100`圆** 
上面说到r100是圆的`定型尺寸`,所以还需要圆的`定位尺寸`,即圆放在哪个位置.

该功能用 AutoPy 编程实现即用:


```python
import AutoPy_Android as AutoPy
a=535
b=1696
r=100

li=[]

for x in range(a-r,a+r):
    y=int((((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)
    

for x in range(a+r,a-r,-1):
    y=int(-1*(((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)

li.append(4000)#执行速度

AutoPy.gesturer(li)

```

其中a,b是圆心坐标,r是半径.

### 1.14.4. AutoPy.capturer()

**新版Lite 请授权后访问http://127.0.0.1:8020/code=cupter, 获取屏幕截图**+

在autoPy lite 软件界面下方有三个按钮，点击其中的开启录屏按钮，系统会提示开启录屏。
开启成功后，访问http://127.0.0.1:8020/code=cupter即可看到当前屏幕图像。
使用requests等网络库下载即可。




> 三指下滑截图,没有三指截图功能机型无效

三指截图功能是3个异步的手势同时滑动模拟出了3条路径
截图后的文件会储存到手机自带的截图文件夹里面,例`/sdcard/截图文件夹/`.需要自行获取路径+文件名来配合使用.


**示例:**
如我们需要自动录制3帧的视频,则需要调用3次截图功能,最后用图片来合成视频.
**例: 每10秒 截`1帧`图** 


该功能用 AutoPy 编程实现即用:



```python

import AutoPy_Android as AutoPy#导入模块
import time

#**例: 每10秒 截`1帧`图** 
num=3
for i in range(num):
    AutoPy.capturer()#三指下滑实现截图
    time.sleep(10)

```



### 1.14.5. AutoPy.StartServer()#旧版AutoPy接口（新版Lite已弃用）
> 截图服务

**新版Lite 请授权后访问http://127.0.0.1:8020/code=cupter, 获取屏幕截图**

在上面我们介绍到截图的图片会放到手机自带的文件夹里面去,对于我们去取这个图片就会造成极大的不便.
本方法实现的主要功能是监控手机的截图文件夹,如有新截图会自动返回并且将新图片放到用户自定义的位置去,方便用户使用截图进行分析.


**示例:**
以小米手机为例,将监控的截图文件夹的新文件,自动监控并自动转移至我们工程目录下.
小米手机的截图目录:`/sdcard/DCIM/Screenshots/`
工程目录:`/sdcard/qpython/`

**例: 监控截图到工程目录下** 

该功能需要改写 AutoPy.py的`AutoPy.StartServer()`方法
编程实现即用:

```python

import AutoPy_Android as AutoPy#导入模块

def StartServer(_Screenshots_='/sdcard/DCIM/Screenshots/',_newdir_='/sdcard/qpython/'):
     _thread.start_new_thread(ListenServer, (_Screenshots_,_newdir_) )

StartServer()

```
如上便能自动监控截图并且自动返回到项目目录中.

### 1.14.6. AutoPy.HOME()
> 主页键

主页键就是返回桌面.
```python
import AutoPy_Android as AutoPy#导入模块
AutoPy.HOME()#模拟主页键
```

### 1.14.7. AutoPy.RECENTS()
> 多任务键

```python
import AutoPy_Android as AutoPy#导入模块
AutoPy.RECENTS()#模拟多任务键
```

### 1.14.8. AutoPy.BACK()
> 返回键

```python
import AutoPy_Android as AutoPy#导入模块
AutoPy.BACK()#模拟返回键
```

### 1.14.9. AutoPy.openapp() 新版Lite 更加可靠
> 打开第三方app

**例: 打开QQ界面** 

```python
import AutoPy_Android as AutoPy#导入模块open

pkg_name="com.tencent.mobileqq"#QQ的包名
cls_name="com.tencent.mobileqq.activity.SplashActivity"#界面的类名
#这两个参数可以用工具"当前界面.apk"找到

AutoPy.openapp(pkg_name,cls_name)

```



### 1.14.10. AutoPy.getID()
> ID点击按钮

**例: 通过控件ID点击按钮** 

```python
import AutoPy_Android as AutoPy#导入模块

ID="button1"#可通过"当前界面"app获取

AutoPy.getID(ID)

```

### 1.14.11. AutoPy.getText()
> 文本点击按钮

**例: 通过文本点击按钮** 

```python
import AutoPy_Android as AutoPy#导入模块open


AutoPy.getText("按钮")

```


### 1.14.12. AutoPy.getView()
> 获取当前界面控件树

**例: 通过爬取控件文本信息** 

```python
import AutoPy_Android as AutoPy#导入模块open


AutoPy.getView()

```



### 1.14.13. AutoPy.Locker()
> 锁屏

**例: 完成工作后自动锁屏** 

```python
import AutoPy_Android as AutoPy#导入模块
def job():
    print("这是一个需要执行5个小时的工作....")

job()
print("工作结束.")
AutoPy.Locker()#锁屏

```


### 1.14.14. 悬浮窗和Toast功能
用法如下
下面为测试程序

```python
import AutoPy_Android as AutoPy
AutoPy.server_url='http://192.168.31.93:8020/?code='
A=AutoPy.FloatWindow("a1")#创建一个悬浮窗，通过指定不同id可以创建多个悬浮窗
A.delete()#删除悬浮窗(清屏)
A.makeToast("开始运行AutoPy测试程序")#弹出一条Toast
time.sleep(1)
A.show()#显示悬浮窗
for i in range(20):
    A.View["text"]=f"测试{i}"#修改View属性
    A.View["size"]=str(int(A.View["size"])+1)#修改View属性
    A.View["X"]=str(int(A.View["X"])+10)#修改View属性
    A.View["Y"]=str(int(A.View["Y"])+10)#修改View属性
    A.modify()#修改生效
    # time.sleep(0.5)
A.View["text"]=f"两秒关掉"#修改View属性
A.modify()#修改生效

time.sleep(2)
A.delete()#删除悬浮窗(清屏)
A.makeToast("已关掉，已结束")#弹出一条Toast

```
test2.py 按钮与文本互动
```python
import AutoPy_Android as AutoPy
import time,json

AutoPy.server_url='http://192.168.31.93:8020/?code='
Butt=AutoPy.FloatButton("b1")#按钮控件
Butt.View["Y"]="1000"
Butt.delete()
Butt.show()

A=AutoPy.FloatWindow("a1")
A.View["Y"]="800"
A.delete()
A.show()

info_O = Butt.getinfo()
N=0
while True:
    info_N = Butt.getinfo()
    print(info_N,end="\r")
    if info_N != info_O:
        print("已点击")
        N+=1
        A.View["text"]=f"已点击{N}下"
        A.modify()
    info_O=info_N
```
test3.py imgView的基本用法
imgView 接收一个base64编码的图片用于展示

```python

import AutoPy_Android as AutoPy
import time,json,base64
import json,base64


def img_to_base64(path):
    image_path = path

    image= open(image_path, 'rb').read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return image_base64

if __name__ == "__main__":
    img_list=[
        r'C:\Users\Administrator\Desktop\都市蓝领 .png',
        r'C:\Users\Administrator\Desktop\小镇中老年.png',
        r'C:\Users\Administrator\Desktop\旅游.png',
    ]
    base64_data=img_to_base64(img_list[0])

    AutoPy.server_url='http://192.168.31.93:8020/?code='
    imgView=AutoPy.FloatImgView("xx")#设置ID
    imgView.View["X"]="0"#设置位置
    imgView.View["Y"]="100"#设置位置
    imgView.View["Width"]="1000"#设置大小
    imgView.View["Height"]="1000"#设置大小
    imgView.setImg(base64_data)
    ret=imgView.show()
    print(ret)
    for x in range(10):
        for i in img_list:
            base64_data=img_to_base64(i)
            imgView.setImg(base64_data)
            ret=imgView.modify()
            print(ret)
    print(imgView.getinfo())
    imgView.delete()

```
test4.py
```python
import AutoPy_Android as AutoPy
AutoPy.server_url='http://192.168.31.93:8020/?code='
Butt=AutoPy.FloatButton("b1")#按钮控件
Butt.delete()
Butt.show()
print(Butt.getinfo())
edittext= AutoPy.FloatEditText("ED1")#编辑框控件
edittext.View["Y"]="1000"
edittext.delete()
edittext.show()
A=AutoPy.FloatWindow("a1")
A.delete()
A.makeToast("开始运行AutoPy测试程序")
time.sleep(1)
A.show()
for i in range(20):
    A.View["text"]=f"测试{i}"
    A.View["size"]=str(int(A.View["size"])+1)
    A.View["X"]=str(int(A.View["X"])+10)
    A.View["Y"]=str(int(A.View["Y"])+10)
    A.modify()
    # time.sleep(0.5)
A.View["text"]=f"两秒关掉"
A.modify()

time.sleep(2)
A.delete()
A.makeToast("已关掉，已结束")
print(Butt.getinfo())#获取按钮点击状态
print(edittext.getinfo())#获取编辑框状态
Butt.delete()
edittext.delete()


```
其中View的参数有：
```python



{
	"id":"new",
	"type":"textview",
	"color":[255,255,255],
	"text":"测试文本",
	"Width":"100",
	"Height":"100",
	"X":"100",
	"Y":"100",
	"operation":"newly",
	"info":"备用"
}
#新增悬浮窗
#指定唯一ID新增.指定operation为newly



{
	"id":"new",
	"operation":"delete",
	"info":"备用"
}

#删除悬浮窗
#指定ID删除.指定operation为delete


{
	"id":"new",
	"type":"textview",
	"color":[255,255,255,255],
	"text":"测试文本",
	"Width":"100",
	"Height":"100",
	"X":"100",
	"Y":"100",
	"operation":"modify",
	"info":"备用"
}
#修改悬浮窗
#指定ID修改.指定operation为modify
#执行完modify()后立刻生效


{
	"id":"newx",
	"type":"Toast",
	"color":[255,255,255,255],
	"text":"测试文本",
	"Width":"100",
	"Height":"100",
	"X":"100",
	"Y":"100",
	"operation":"modify",
	"info":"备用"
}

#弹出一条 Toast
#必填参数type："Toast"，"text":"测试文本",其他非必填

```




## 1.14.15. 多指手势接口
```python
http://127.0.0.1:8020/?code=S,428-1295-339-1295-339-1044-361-1044-361-1266-428-1266-428-1295-|458-1053-458-1049-459-1044-462-1039-465-1035-469-1033-471-1033-474-1033-477-1035-481-1039-484-1044-485-1049-485-1053-485-1057-484-1062-481-1067-477-1071-474-1073-471-1073-468-1073-465-1071-462-1067-459-1062-458-1057-458-1053-|461-1295-461-1116-482-1116-482-1295-461-1295-|587-1293-584-1296-580-1298-575-1299-569-1299-553-1299-541-1292-537-1272-537-1246-537-1142-516-1142-516-1116-537-1116-537-1073-558-1063-558-1116-587-1116-587-1142-558-1142-558-1240-558-1249-559-1257-562-1265-566-1271-570-1273-575-1273-578-1273-582-1272-585-1270-587-1267-587-1293-|720-1214-637-1214-637-1228-640-1242-647-1258-657-1269-666-1273-675-1273-685-1273-694-1271-703-1264-712-1254-712-1282-704-1291-695-1297-683-1299-670-1299-657-1299-644-1293-629-1275-619-1251-615-1228-615-1206-615-1186-619-1164-631-1139-646-1119-659-1112-670-1112-682-1112-694-1117-707-1134-717-1156-720-1177-720-1198-720-1214-|699-1188-699-1176-697-1164-691-1151-684-1141-677-1137-670-1137-664-1137-657-1141-648-1151-641-1165-638-1177-637-1188-699-1188-|


更多手势实例：如下
```
           //好用！
            "S,315-1293-331-1297-344-1300-353-1299-358-1295-361-1289-361-1281-361-1150-310-1150-300-1153-291-1140-361-1140-361-1117-361-1094-361-1074-360-1055-373-1067-400-1000-330-1000-315-1005-305-990-400-990-410-973-431-1003-424-1005-416-1011-404-1026-393-1043-384-1057-378-1070-386-1077-377-1088-377-1140-413-1140-428-1118-449-1150-377-1150-377-1288-377-1305-374-1319-365-1330-352-1338-352-1328-348-1319-334-1310-315-1301-315-1293-|190-1331-187-1326-209-1306-228-1284-240-1260-250-1235-235-1225-222-1216-213-1211-205-1208-213-1174-219-1138-225-1099-230-1058-208-1058-197-1062-188-1048-231-1048-235-1017-238-988-240-967-241-950-265-968-257-978-254-992-252-1008-249-1027-247-1048-279-1048-287-1033-303-1055-294-1065-289-1117-284-1163-276-1198-268-1228-280-1236-291-1244-299-1254-304-1265-304-1277-302-1287-300-1290-299-1290-297-1290-294-1289-292-1285-289-1280-283-1270-277-1260-270-1252-262-1245-251-1270-236-1293-215-1313-190-1331-|220-1205-226-1207-233-1210-243-1215-254-1220-262-1190-269-1155-275-1109-280-1058-245-1058-239-1099-232-1138-226-1172-220-1205-|625-1085-625-1173-700-1173-700-1085-625-1085-|655-1288-670-1290-683-1291-692-1291-698-1287-700-1279-700-1268-700-1183-625-1183-625-1236-626-1279-626-1300-627-1310-610-1321-610-1274-611-1233-611-1205-611-1183-538-1183-534-1227-526-1268-510-1303-491-1335-488-1331-498-1306-508-1273-516-1226-522-1163-524-1080-524-1006-524-972-523-957-540-973-699-973-707-955-724-975-715-988-715-1280-716-1301-713-1318-704-1327-691-1333-690-1319-685-1307-672-1301-655-1296-655-1288-|540-983-540-1075-611-1075-611-983-540-983-|625-983-625-1075-700-1075-700-983-625-983-|540-1085-539-1120-539-1148-538-1164-538-1173-611-1173-611-1085-540-1085-|872-1226-875-1230-878-1236-879-1248-877-1261-871-1270-865-1275-862-1276-860-1276-858-1276-855-1275-849-1271-843-1262-841-1249-842-1235-847-1226-853-1221-857-1220-860-1220-863-1220-865-1221-869-1223-872-1226-|875-1027-875-1036-873-1062-869-1121-864-1178-860-1196-856-1178-851-1121-847-1059-845-1026-846-1010-851-1002-856-998-859-997-861-997-863-997-866-998-871-1003-875-1010-876-1019-875-1027-|",
            //AutoPy
            "S,284-1277-260-1277-243-1208-173-1208-157-1277-133-1277-197-1025-220-1025-284-1277-|237-1180-211-1075-211-1073-210-1069-209-1064-209-1057-208-1057-207-1063-207-1068-206-1072-205-1075-180-1180-237-1180-|416-1277-394-1277-394-1249-394-1249-388-1265-380-1277-369-1281-357-1281-336-1281-320-1272-314-1243-314-1205-314-1097-335-1097-335-1200-335-1228-339-1248-349-1255-363-1255-370-1255-378-1251-386-1240-392-1225-394-1213-394-1201-394-1097-416-1097-416-1277-|522-1275-518-1278-514-1280-509-1281-503-1281-487-1281-475-1274-471-1254-471-1227-471-1124-450-1124-450-1097-471-1097-471-1054-492-1044-492-1097-522-1097-522-1124-492-1124-492-1222-492-1231-493-1239-496-1247-500-1253-505-1255-509-1255-513-1255-516-1254-519-1252-522-1249-522-1275-|550-1189-550-1167-554-1144-566-1119-582-1100-597-1093-611-1093-625-1093-639-1099-653-1118-665-1142-669-1165-669-1186-669-1208-665-1230-652-1255-637-1275-622-1281-608-1281-595-1281-581-1275-566-1256-554-1232-550-1210-550-1189-|571-1188-571-1204-574-1220-582-1237-592-1250-601-1255-610-1255-619-1255-628-1251-638-1237-645-1220-647-1204-647-1187-647-1171-645-1154-638-1137-628-1124-619-1119-610-1119-601-1119-592-1124-582-1138-574-1156-571-1172-571-1188-|734-1183-734-1277-712-1277-712-1025-760-1025-773-1025-787-1030-802-1045-813-1064-817-1083-817-1101-817-1120-813-1139-799-1161-783-1178-769-1184-756-1183-734-1183-|734-1054-734-1154-754-1154-764-1154-774-1151-784-1141-792-1128-794-1115-794-1103-794-1078-789-1060-775-1054-756-1054-734-1054-|954-1097-899-1304-892-1333-882-1355-870-1362-856-1362-852-1362-849-1361-846-1360-843-1359-843-1331-846-1333-849-1334-852-1335-855-1335-862-1335-868-1332-873-1322-876-1309-886-1277-838-1097-862-1097-893-1232-896-1247-896-1247-897-1245-897-1242-898-1237-899-1233-932-1097-954-1097-|65-915-65-1420-1010-1420-1010-915-|",
            //Lite
            "S,428-1295-339-1295-339-1044-361-1044-361-1266-428-1266-428-1295-|458-1053-458-1049-459-1044-462-1039-465-1035-469-1033-471-1033-474-1033-477-1035-481-1039-484-1044-485-1049-485-1053-485-1057-484-1062-481-1067-477-1071-474-1073-471-1073-468-1073-465-1071-462-1067-459-1062-458-1057-458-1053-|461-1295-461-1116-482-1116-482-1295-461-1295-|587-1293-584-1296-580-1298-575-1299-569-1299-553-1299-541-1292-537-1272-537-1246-537-1142-516-1142-516-1116-537-1116-537-1073-558-1063-558-1116-587-1116-587-1142-558-1142-558-1240-558-1249-559-1257-562-1265-566-1271-570-1273-575-1273-578-1273-582-1272-585-1270-587-1267-587-1293-|720-1214-637-1214-637-1228-640-1242-647-1258-657-1269-666-1273-675-1273-685-1273-694-1271-703-1264-712-1254-712-1282-704-1291-695-1297-683-1299-670-1299-657-1299-644-1293-629-1275-619-1251-615-1228-615-1206-615-1186-619-1164-631-1139-646-1119-659-1112-670-1112-682-1112-694-1117-707-1134-717-1156-720-1177-720-1198-720-1214-|699-1188-699-1176-697-1164-691-1151-684-1141-677-1137-670-1137-664-1137-657-1141-648-1151-641-1165-638-1177-637-1188-699-1188-|",
            //稳
            "S,480-1192-619-1192-619-1155-486-1155-486-1126-619-1126-619-1090-486-1090-486-1063-482-1069-479-1063-475-1058-470-1053-465-1047-482-1025-497-1001-508-974-519-945-541-951-538-960-534-969-531-977-527-986-612-986-612-1014-606-1026-601-1037-595-1049-589-1060-640-1060-640-1237-619-1237-619-1221-480-1221-480-1192-|369-1246-383-1218-395-1186-405-1148-413-1105-375-1105-375-1075-415-1075-415-1007-407-1008-398-1009-389-1010-380-1011-380-1004-379-997-378-988-376-980-400-978-423-975-447-971-471-966-475-998-466-999-456-1001-446-1002-436-1004-436-1075-472-1075-472-1105-436-1105-436-1157-448-1143-456-1155-464-1168-472-1181-479-1194-462-1215-456-1202-449-1189-443-1178-436-1167-436-1372-415-1372-415-1181-408-1211-400-1238-390-1261-379-1282-377-1273-375-1264-372-1255-369-1246-|504-1246-525-1246-525-1308-525-1320-528-1329-535-1332-544-1332-571-1332-580-1332-588-1330-591-1321-593-1311-594-1302-595-1293-596-1282-597-1271-602-1274-607-1277-613-1280-619-1284-617-1295-616-1305-614-1315-612-1324-609-1343-603-1357-592-1362-578-1362-540-1362-522-1362-508-1355-504-1336-504-1309-504-1246-|586-1014-514-1014-508-1027-501-1039-495-1050-488-1060-564-1060-570-1048-576-1036-581-1025-586-1014-|473-1246-492-1256-487-1279-482-1301-476-1322-469-1343-465-1339-460-1335-455-1332-449-1329-456-1311-463-1291-468-1269-473-1246-|617-1259-636-1247-644-1270-651-1291-657-1309-662-1324-642-1339-637-1321-632-1303-625-1282-617-1259-|536-1239-552-1222-560-1237-568-1251-575-1265-582-1278-564-1297-558-1282-551-1267-544-1253-536-1239-|",
            //E=MC^2
            "S,272-1364-175-1364-175-1093-268-1093-268-1124-198-1124-198-1211-263-1211-263-1242-198-1242-198-1333-272-1333-272-1364-|442-1224-324-1224-324-1198-442-1198-442-1224-|442-1305-324-1305-324-1278-442-1278-442-1305-|688-1364-665-1364-665-1253-665-1237-664-1222-659-1208-652-1198-645-1194-637-1194-631-1194-624-1199-616-1212-609-1228-607-1242-607-1254-607-1364-584-1364-584-1249-584-1222-581-1201-570-1194-556-1194-549-1194-542-1199-534-1211-528-1227-526-1241-526-1254-526-1364-503-1364-503-1171-526-1171-526-1201-526-1201-533-1184-541-1170-553-1166-566-1166-573-1166-580-1169-589-1177-597-1187-601-1196-603-1205-610-1186-619-1171-631-1166-646-1166-667-1166-683-1176-688-1205-688-1245-688-1364-|827-1355-819-1361-811-1366-801-1368-791-1368-777-1368-762-1361-746-1341-733-1316-729-1293-729-1272-729-1248-734-1223-747-1195-765-1173-781-1166-796-1166-805-1166-813-1167-820-1171-827-1175-827-1209-820-1202-813-1196-805-1194-796-1194-787-1194-776-1199-765-1215-755-1234-752-1252-752-1269-752-1285-755-1303-764-1321-775-1335-785-1340-795-1340-803-1340-812-1338-819-1332-827-1323-827-1355-|908-1057-908-1050-906-1042-902-1033-895-1027-890-1025-884-1025-880-1025-875-1026-868-1031-861-1036-857-1042-853-1048-853-1024-856-1020-861-1015-867-1010-875-1006-881-1005-886-1005-894-1005-903-1008-913-1018-921-1032-924-1044-924-1055-924-1066-922-1078-917-1092-911-1105-903-1115-896-1123-888-1131-880-1139-874-1146-870-1153-867-1160-865-1166-865-1171-865-1176-928-1176-928-1197-848-1197-848-1187-848-1179-849-1170-851-1160-855-1148-861-1137-868-1127-875-1119-882-1112-890-1104-897-1095-903-1084-907-1073-908-1065-908-1057-|",


```


测试上面的接口，可以看到多指手势在屏幕上画出lite字样


```
#### 上面接口解析如下
```
接口为：服务器接口+code=[手势路径]

如：http://127.0.0.1:8020/?code=[手势路径]
```
#### 手势路径格式解析如下
```
S,路径1|路径2|路径3|路径4|
其中路径格式解析如下
x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-


如：3条手势路径实例如下：

格式：
S,路径1|路径2|路径3|路径4|
路径：
x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-
组合后：

S,x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-|x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-|x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-|x1-y1-x2-y2-x3-y3-x4-y4-x5-y5-|

这样即为三条路径的接口原数据

更多手指手势，同理可推导出




```






### 1.14.15. AutoPy.floatWindowOpenApi()
> 悬浮窗接口

该功能是AutoPy的高级用法,一般用于阻塞当前程序,等待按钮按下后再运行.
一般用作按钮的按钮的点击事件触发.
如上面的程序都是执行后马上运行,不会等待用户到达指定场景后再运行,该功能就可以解决上面的问题,将等带用户点击开启悬浮窗后才会执行,即可达到交互的控制.

**例: 用户点击后进行画圆操作** 
使用`AutoPy.floatWindowOpenApi()`和`AutoPy.floatWindowClose()`方法进行控制.
AutoPy目前提供了两个按钮的接口服务.可供处理两个按钮的点击事件.
如下用了一个开启按钮事件:


```python
import AutoPy_Android as AutoPy
a=535
b=1696
r=100

li=[]

for x in range(a-r,a+r):
    y=int((((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)
    

for x in range(a+r,a-r,-1):
    y=int(-1*(((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)

li.append(4000)#执行速度

while True:
    if AutoPy.floatWindowOpenApi():
       AutoPy.floatWindowClose()
       AutoPy.gesturer(li)


```
**关闭按钮写法与开启按钮类似**
如下:

```python
import AutoPy_Android as AutoPy
a=535
b=1696
r=100

li=[]

for x in range(a-r,a+r):
    y=int((((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)
    

for x in range(a+r,a-r,-1):
    y=int(-1*(((r**2)-(x-a)**2)**(1/2))+b)
    li.append(x)
    li.append(y)

li.append(4000)#执行速度

while True:
    if AutoPy.floatWindowCloseApi():
       AutoPy.floatWindowClose()
       AutoPy.gesturer(li)


```


## 1.15. 录制教学功能
点击录制教学,按住文字可以拖动,当拖动到适当位置的时候,选择执行点击或拖动功能,AutoPy会自动记录下当前的坐标,并且会自动点击当前选定的位置,会生成一个悬浮窗标记当前位置,可以很方便的实现坐标记录和python代码生成.

AutoPy可以自动生成python代码.
生成一段代码如下:
**示例:**
```python
import AutoPy_Android as AutoPy,time

dy=80 #y坐标偏移调整
dx=0 #x坐标偏移调整
t=1000 #毫秒数转秒数

"""
此脚本由 AutoPy自动生成，
位置坐标和时间延迟可能不准确，
请手动微调！
"""
    
AutoPy.tap(324+dx,1692+dy)
time.sleep(1)
AutoPy.tap(559+dx,1680+dy)
time.sleep(750/t)
AutoPy.tap(343+dx,1600+dy)
time.sleep(1363/t)
AutoPy.tap(600+dx,1731+dy)
time.sleep(708/t)
AutoPy.tap(696+dx,1669+dy)
time.sleep(1100/t)
AutoPy.tap(241+dx,1835+dy)
time.sleep(959/t)
AutoPy.tap(557+dx,1845+dy)
time.sleep(904/t)
AutoPy.tap(685+dx,1804+dy)
time.sleep(821/t)
AutoPy.tap(781+dx,1676+dy)
time.sleep(779/t)
AutoPy.tap(855+dx,1555+dy)
time.sleep(930/t)
AutoPy.tap(455+dx,1949+dy)
time.sleep(2147/t)
AutoPy.swipe(681+dx,1844+dy,396+dx,1784+dy,2683)
time.sleep(396/t)
AutoPy.tap(396+dx,1784+dy)
time.sleep(2216/t)
AutoPy.tap(640+dx,1796+dy)
time.sleep(2672/t)
AutoPy.swipe(281+dx,1853+dy,571+dx,1864+dy,1326)
time.sleep(571/t)
AutoPy.swipe(145+dx,1692+dy,145+dx,1692+dy,754)
time.sleep(145/t)
AutoPy.tap(120+dx,1941+dy)
time.sleep(8120/t)
AutoPy.tap(105+dx,1770+dy)
time.sleep(1463/t)
AutoPy.tap(699+dx,1871+dy)
time.sleep(3436/t)
```
以上代码由AutoPy自动生成.


## 1.16. 最后所有方法实现代码

```python
# -*- coding: utf-8 -*-

import sys
import time
import os,_thread

if sys.version[0] == 2:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

server_url = 'http://127.0.0.1:33445?code='

def dian(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def tuo(x1,y1,x2,y2,t=1000):
    f=urlopen(server_url+'1,'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(t))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]滑动执行成功')
    time.sleep(0.0023*t)

def swipe(x1,y1,x2,y2,t=1000):
    f=urlopen(server_url+'1,'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(t))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]滑动执行成功')
    time.sleep(0.0023*t)

def tap(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def click(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def capturer():
    f=urlopen(server_url+'2,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]截屏执行成功')
    
def ListenServer(_Screenshots_='/sdcard/DCIM/Screenshots/',_newdir_='/sdcard/qpython/'):#暂时无用
    _Screenshots_=_Screenshots_
    _newdir_=_newdir_
    t=os.listdir(_Screenshots_)
    while (True):
      nt=os.listdir(_Screenshots_)
      li=list(set(nt)-set(t))
      if(len(li)!=0):
         t=os.listdir(_Screenshots_)
         print('监控到截图',li)#监控到截图
         os.system('mv '+_Screenshots_+li[0]+' '+_newdir_+'AutoPy_Screenshots.jpg')



def StartServer(_Screenshots_='/sdcard/DCIM/Screenshots/',_newdir_='/sdcard/qpython/'):
     _thread.start_new_thread(ListenServer, (_Screenshots_,_newdir_) )


def gesturer(li):
    li=li
    f=urlopen(server_url+'3,'+','.join(map(str,li)))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]手势执行成功')
    
def HOME():
    f=urlopen(server_url+'HOME,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]主页键执行成功')

def BACK():
    f=urlopen(server_url+'BACK,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]返回键执行成功')
    
def RECENTS():
    f=urlopen(server_url+'RECENTS,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]菜单键执行成功')


    
def Locker():
    f=urlopen(server_url+'Lock,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]锁屏执行成功')

def floatWindowOpenApi():
    f=open('/sdcard/AutoFloatWindow.info','r+').read()
    if f=='1':
        return True
    #o=open('/sdcard/AutoFloatWindow.info',1w+').close()


def floatWindowCloseApi():
    f=open('/sdcard/AutoFloatWindow.info','r+').read()
    if f=='0':
        return True

def floatWindowClose():
    o=open('/sdcard/AutoFloatWindow.info','w+').close()
def systemCapturer():
    f=urlopen(server_url+'capturer,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]返回键执行成功')
    
    
#作者:sunny开始学坏

```

##### 1.16.0.0.4. 更多功能持续开发中......
##### 1.16.0.0.5. QQ群:540717901